from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from schemas import UserCreate, UserLogin
from passlib.context import CryptContext
import asyncio

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function for hashing passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Helper function for verifying passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@auth_router.post("/register")
async def register_user(user: UserCreate):
    # Check if user exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Insert user into DB
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    await users_collection.insert_one(user_data)
    
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login_user(user: UserLogin):
    # Find user in DB
    stored_user = await users_collection.find_one({"email": user.email})
    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"message": "Login successful"}
