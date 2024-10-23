import os

from src.database.mongo_client import get_mongo_client

def insert_one_doc(collection_name, document):
    MONGODB_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME")
    
    client = get_mongo_client()
    db = client[MONGODB_DATABASE_NAME]
 
    result = db[collection_name].insert_one({**document})    
    if not result:
        raise Exception(f"Failed to insert one document to {collection_name}")
    
    return document

def find_one_doc(collection_name, query, projection={"_id": 0}):
    MONGODB_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME")
    
    client = get_mongo_client()
    db = client[MONGODB_DATABASE_NAME]
    
    return db[collection_name].find_one(query, projection)