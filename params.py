import os

OPENAI_API_KEY = os.environ["OPENAPI_KEY"]
MONGODB_CONN_STRING = (
    "mongodb+srv://fkadmin:" + os.environ["MONGODB_PASSWORD"] + "@prd.hixjx.mongodb.net/"
)
