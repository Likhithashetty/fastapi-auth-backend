from fastapi import APIRouter, HTTPException, Depends
from database import users_collection
from schemas import UserSchema, UserLoginSchema
from bson import ObjectId
import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Hash password
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Register User
@router.post("/register")
async def register(user: UserSchema):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = hash_password(user.password)
    new_user = {"email": user.email, "name": user.name, "password": hashed_password}
    users_collection.insert_one(new_user)
    
    return {"message": "User registered successfully"}

# Login User
@router.post("/login")
async def login(user: UserLoginSchema):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}
