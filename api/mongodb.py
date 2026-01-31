from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

_client = None

def get_mongo_client():
    """Get MongoDB client connection (singleton)"""
    global _client
    if _client is None:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        
        _client = MongoClient(mongo_uri)
        # Test connection
        _client.admin.command('ping')
    return _client

def get_database():
    """Get MongoDB database"""
    client = get_mongo_client()
    # Extract database name from URI or use default
    db_name = os.getenv('MONGO_DB_NAME', 'student_records')
    return client[db_name]

def get_students_collection():
    """Get students collection"""
    db = get_database()
    return db['students']
