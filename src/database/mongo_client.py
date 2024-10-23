import os
import time
import pymongo

from functools import wraps
from pymongo.errors import AutoReconnect

# Global variable to store the connection
mongo_client = None

def retry_connection(max_attempts=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except AutoReconnect:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_connection()
def get_mongo_client():
    MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')
    
    global mongo_client
    if mongo_client is None or not mongo_client.is_primary:
        mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
    return mongo_client

def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()
        mongo_client = None
