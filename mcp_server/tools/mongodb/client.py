import os
from pymongo import MongoClient
from pymongo.database import Database


def get_db() -> Database:
    uri = os.environ.get("MONGODB_URI")
    db_name = os.environ.get("MONGODB_DATABASE")
    if not uri:
        raise RuntimeError("MONGODB_URI environment variable is required.")
    if not db_name:
        raise RuntimeError("MONGODB_DATABASE environment variable is required.")
    client = MongoClient(uri)
    return client[db_name]
