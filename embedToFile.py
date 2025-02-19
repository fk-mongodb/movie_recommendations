import argparse
from openai import OpenAI
import params
import json

# Encode our question
client = OpenAI(api_key=params.OPENAI_API_KEY)

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


def encode(topic):
    response = client.embeddings.create(model="text-embedding-ada-002", input=topic)
    embedding = response.data[0].embedding
    return embedding


def getRecommendations(topic, output_file=None):
    embedding = encode(topic)
    # Save embedding to file if output path provided
    if output_file:
        with open(output_file, "w") as outfile:
            json.dump(embedding, outfile)

    return embedding


results = getRecommendations(topic, output_file="Destination")
