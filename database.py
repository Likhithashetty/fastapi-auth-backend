from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")  # Load from .env file

client = MongoClient(MONGO_URL)
db = client["fastapi_auth_db"]
users_collection = db["users"]
