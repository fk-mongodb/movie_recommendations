import os
import openai
import params
from pymongo import MongoClient
import json
import argparse

# Process arguments
parser = argparse.ArgumentParser(description='Movie Search')
parser.add_argument('-t', '--question', help="What type of movie are you in the mood for?")
args = parser.parse_args()

if args.question is None:
    # Some topics to try...
    topic = "A group of unlikely heroes that must band together to save the world from an impending alien invasion."
    topic = "a magical realm and a battle against dark forces to protect it."
    topic = "A dystopian future, a lone hero rebeling against a tyrannical government."
    topic = "A comedy about a mismatched pair of strangers."
    topic = "A poisened man fights to find the antidote."
else:
    topic = args.question

# Encode our question
openai.api_key = params.OPENAI_API_KEY
response = openai.Embedding.create(
  model="text-embedding-ada-002",
  input=topic
)

embedding = response.data[0].embedding

# Establish connection to MongoDB
mongo_client = MongoClient(params.MONGODB_CONN_STRING)
result_collection = mongo_client["sample_mflix"]["embedded_movies"]

pipeline = [
    {
        "$search": {
            "knnBeta": {
                "vector": embedding,
                "path": "plot_embedding",
                "k": 5
            }
        }
    },
    {
    "$project": {
      "_id": 0,
      "title": 1,
      "plot": 1,
      "rating":"$imdb.rating",
      "score": { '$meta': "searchScore" }
    }
  },
    {
        "$limit": 5
    },

]

results = result_collection.aggregate(pipeline)

for result in results:
    print(json.dumps(result, indent=4), "\n")
