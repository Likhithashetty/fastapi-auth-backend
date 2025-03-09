from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from routes.auth import router as auth_router  
from routes.trip_management import router as trip_router  
from routes.leader_auth import router as leader_auth_router  

app = FastAPI()

# ✅ Include routers (No duplicates)
app.include_router(auth_router)
app.include_router(leader_auth_router)
app.include_router(trip_router)  # trip_router already has prefix="/trip"

# ✅ MongoDB Connection
client = MongoClient("mongodb://localhost:27017")
db = client["trip_management"]
users_collection = db["users"]
applications_collection = db["applications"]
trips_collection = db["trips"]

@app.get("/")
def home():
    return {"message": "FastAPI Trip Management API is running!"}

# ✅ Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    area: str
    role: str  # 'admin', 'mandali', 'individual'

class MandaliApplication(BaseModel):
    leader_id: str
    trip_id: str
    group_members: list[str]

class IndividualApplication(BaseModel):
    user_id: str
    trip_id: str

# ✅ 1️⃣ Admin Adding Users Area-wise
@app.post("/admin/add-user", tags=["Admin Management"])
def add_user(user: UserCreate):
    if user.role not in ["admin", "mandali", "individual"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    new_user = users_collection.insert_one(user.dict())
    return {"message": "User added successfully", "user_id": str(new_user.inserted_id)}

# ✅ 2️⃣ Mandali (Group) Applying for a Trip
@app.post("/trip/apply-mandali", tags=["Trip Management"])
def apply_mandali(application: MandaliApplication):
    leader = users_collection.find_one({"_id": ObjectId(application.leader_id), "role": "mandali"})
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    new_application = applications_collection.insert_one(application.dict())
    return {"message": "Mandali application submitted", "application_id": str(new_application.inserted_id)}

# ✅ 3️⃣ Individual Applying for a Trip
@app.post("/trip/apply-individual", tags=["Trip Management"])
def apply_individual(application: IndividualApplication):
    user = users_collection.find_one({"_id": ObjectId(application.user_id), "role": "individual"})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_application = applications_collection.insert_one(application.dict())
    return {"message": "Individual application submitted", "application_id": str(new_application.inserted_id)}
