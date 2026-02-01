"""
Script to create an admin user in MongoDB
Run: python create_admin.py
"""
import os
from dotenv import load_dotenv
from api.user_model import User

load_dotenv()

def create_admin():
    print("Creating admin user...")
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    user_id, error = User.create(username, email, password, is_admin=True)
    if error:
        print(f"Error: {error}")
    else:
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"User ID: {user_id}")

if __name__ == '__main__':
    create_admin()
