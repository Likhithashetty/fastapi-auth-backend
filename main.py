from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["fastapi_auth"]
users_collection = db["users"]

app = FastAPI()

# Pydantic model for user registration
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

# User Registration Route
@app.post("/auth/register")
def register(user: RegisterUser):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Insert new user into MongoDB
    user_data = user.dict()
    result = users_collection.insert_one(user_data)
    
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# User Login Route
@app.post("/auth/login")
def login(user: LoginRequest):
    # Find user in MongoDB
    db_user = users_collection.find_one({"username": user.username})

    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful!"}

