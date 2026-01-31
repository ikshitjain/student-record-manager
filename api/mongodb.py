from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

_client = None

def get_mongo_client():
    global _client
    if _client is None:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI check failed")
        
        _client = MongoClient(mongo_uri)
        _client.admin.command('ping')
    return _client

def get_database():
    client = get_mongo_client()
    db_name = os.getenv('MONGO_DB_NAME', 'student_records')
    return client[db_name]

def get_students_collection():
    return get_database()['students']
