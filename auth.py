from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import db
from bson.objectid import ObjectId
from jose import JWTError, jwt
import datetime

# Router setup
router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Schema for User Registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to create JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 📌 Route: User Registration
@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = db["users"].find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Password Validation: At least 8 characters, 1 letter, 1 number
    if len(user.password) < 8 or not any(char.isalpha() for char in user.password) or not any(char.isdigit() for char in user.password):
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long, contain at least one letter and one number.")

    hashed_password = hash_password(user.password)

    # Save user to database
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }

    inserted_user = db["users"].insert_one(new_user)
    return {"message": "User registered successfully", "user_id": str(inserted_user.inserted_id)}


# 📌 Route: User Login
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"email": form_data.username})

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate JWT Token
    access_token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
