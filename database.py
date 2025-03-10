from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")  # Default to localhost if not in .env
client = MongoClient(MONGO_URL)
db = client["trip_management"]  # Database name

# ✅ Define collections
users_collection = db["users"]  
trips_collection = db["trips"]  
leaders_collection = db["leaders"]  # Add this if needed for leaders
applications_collection = db["applications"]  # ✅ Add this line for storing applications
