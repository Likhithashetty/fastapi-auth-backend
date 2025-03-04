from pymongo import MongoClient
from database import db  # Import the database connection

# User collection
users_collection = db["users"]
