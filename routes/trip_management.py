from fastapi import APIRouter, HTTPException
from database import trips_collection
from schemas import TripSchema
from bson import ObjectId

router = APIRouter(prefix="/trip", tags=["Trip Management"])

# Create a trip
@router.post("/create_trip")
async def create_trip(trip: TripSchema):
    new_trip = {"name": trip.name, "description": trip.description, "location": trip.location}
    result = trips_collection.insert_one(new_trip)
    
    return {"message": "Trip created successfully", "trip_id": str(result.inserted_id)}

# Get all trips
@router.get("/trips/")
async def get_trips():
    trips = list(trips_collection.find({}, {"_id": 0}))  # Exclude _id for simplicity
    return {"trips": trips}

# Get trip by ID
@router.get("/trip/{trip_id}")
async def get_trip(trip_id: str):
    trip = trips_collection.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip["_id"] = str(trip["_id"])
    return trip

# Delete trip by ID
@router.delete("/trip/{trip_id}")
async def delete_trip(trip_id: str):
    result = trips_collection.delete_one({"_id": ObjectId(trip_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return {"message": "Trip deleted successfully"}
