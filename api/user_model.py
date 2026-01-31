# User model for MongoDB
from .mongodb import get_database
from bson import ObjectId
from datetime import datetime
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production-!@#$%^&*()')

def get_users_collection():
    """Get users collection"""
    db = get_database()
    return db['users']

class User:
    """User model for MongoDB"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def create(username, email, password, is_admin=False):
        """Create a new user"""
        collection = get_users_collection()
        
        # Check if user already exists
        if collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            return None, 'Username or email already exists'
        
        user_data = {
            'username': username,
            'email': email,
            'password': User.hash_password(password),
            'is_admin': is_admin,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = collection.insert_one(user_data)
        return str(result.inserted_id), None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user and return user data"""
        collection = get_users_collection()
        user = collection.find_one({'$or': [{'username': username}, {'email': username}]})
        
        if not user:
            return None, 'Invalid credentials'
        
        if not User.verify_password(password, user['password']):
            return None, 'Invalid credentials'
        
        return User._to_dict(user), None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        collection = get_users_collection()
        try:
            user = collection.find_one({'_id': ObjectId(user_id)})
            if user:
                return User._to_dict(user)
            return None
        except:
            return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        collection = get_users_collection()
        user = collection.find_one({'username': username})
        if user:
            return User._to_dict(user)
        return None
    
    @staticmethod
    def generate_token(user_data):
        """Generate JWT token"""
        payload = {
            'user_id': user_data['_id'],
            'username': user_data['username'],
            'is_admin': user_data.get('is_admin', False)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # JWT 2.x returns string, but ensure it's a string
        if isinstance(token, bytes):
            return token.decode('utf-8')
        return token
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = User.get_by_id(payload['user_id'])
            return user, None
        except jwt.ExpiredSignatureError:
            return None, 'Token expired'
        except jwt.InvalidTokenError:
            return None, 'Invalid token'
    
    @staticmethod
    def get_all():
        """Get all users"""
        collection = get_users_collection()
        users = collection.find()
        return [User._to_dict(user) for user in users]
    
    @staticmethod
    def update_admin_status(user_id, is_admin):
        """Update user admin status"""
        collection = get_users_collection()
        try:
            result = collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'is_admin': is_admin, 'updated_at': datetime.now()}}
            )
            return result.modified_count > 0, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete(user_id):
        """Delete user"""
        collection = get_users_collection()
        try:
            result = collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def _to_dict(user):
        """Convert MongoDB document to dictionary"""
        return {
            '_id': str(user['_id']),
            'id': str(user['_id']),
            'username': user.get('username', ''),
            'email': user.get('email', ''),
            'is_admin': user.get('is_admin', False),
        }
