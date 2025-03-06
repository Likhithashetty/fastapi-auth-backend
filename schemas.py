from pydantic import BaseModel
from typing import Optional

# User Schema
class UserSchema(BaseModel):
    email: str
    name: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

# Trip Schema
class TripSchema(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
