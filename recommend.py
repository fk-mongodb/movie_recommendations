from openai import OpenAI
import params
from pymongo import MongoClient
import json
import argparse


# Process arguments
parser = argparse.ArgumentParser(description="Movie Search")
parser.add_argument(
    "-t", "--question", help="What type of movie are you in the mood for?"
)
args = parser.parse_args()

if args.question is None:
    # Some topics to try...
    topic = "A group of unlikely heroes that must band together to save the world from an impending alien invasion."
    topic = "a magical realm and a battle against dark forces to protect it."
    topic = "A dystopian future, a lone hero rebeling against a tyrannical government."
    topic = "A comedy about a mismatched pair of strangers."
    topic = "A poisoned man fights to find the antidote."
else:
    topic = args.question


# Encode our question
client = OpenAI(api_key=params.OPENAI_API_KEY)
def encode(topic):
    response = client.embeddings.create(model="text-embedding-ada-002", input=topic)
    return response.data[0].embedding


# Establish connection to MongoDB
def searchMongoDB(embedding):
    mongo_client = MongoClient(params.MONGODB_CONN_STRING)
    result_collection = mongo_client["sample_mflix"]["embedded_movies"]

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": embedding,
                "path": "plot_embedding",
                "limit": 5,  # number of nearest neighbors to return
                "numCandidates": 50,  # number of HNSW entry points to explore
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "plot": 1,
                "rating": "$imdb.rating",
                "score": {"$meta": "searchScore"},
            }
        },
        {"$limit": 5},
    ]

    return result_collection.aggregate(pipeline)


def getRecommendations(topic):
    embedding = encode(topic)
    search_results_cursor = searchMongoDB(embedding)
    documents = list(search_results_cursor)
    json_data = json.dumps(documents, default=str, indent=2)
    return json_data


results = getRecommendations(topic)

print(results)


