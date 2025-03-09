from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from schemas import TripSchema
from database import trips_collection
from bson import ObjectId

router = APIRouter(prefix="/trip", tags=["Trip Management"])

# ✅ Define Response Model for Swagger UI
class ItineraryItem(BaseModel):
    day: str
    activity: str

class Schedule(BaseModel):
    start_date: str
    end_date: str

class Transportation(BaseModel):
    mode: str
    details: str

class TripResponse(BaseModel):
    id: str  # _id converted to string
    name: str
    description: str
    location: str
    itinerary: list[ItineraryItem]
    schedule: Schedule
    transportation: Transportation

# ✅ Create a trip
@router.post("/create_trip", response_model=dict)
async def create_trip(trip: TripResponse):
    new_trip = {
        "name": trip.name,
        "description": trip.description,
        "location": trip.location,
        "itinerary": [dict(item) for item in trip.itinerary],  
        "schedule": dict(trip.schedule),
        "transportation": dict(trip.transportation)
    }
    result = trips_collection.insert_one(new_trip)
    return {"message": "Trip created successfully", "trip_id": str(result.inserted_id)}

# ✅ Get all trips (Fixed for Swagger UI)
@router.get("/trips/", response_model=list[TripSchema])
async def get_trips():
    try:
        trips = list(trips_collection.find({}))  # Fetch all trips from MongoDB

        if not trips:
            return []  # ✅ Return empty list if no trips exist

        # ✅ Convert MongoDB _id to string and rename it to "id"
        for trip in trips:
            trip["id"] = str(trip.pop("_id"))  # Convert ObjectId to string

        return trips  # ✅ Return the updated trip list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # ✅ Return detailed error

# ✅ Get trip by ID
@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: str):
    trip = trips_collection.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip["_id"] = str(trip["_id"])
    return trip

# ✅ Delete trip by ID
@router.delete("/{trip_id}", response_model=dict)
async def delete_trip(trip_id: str):
    result = trips_collection.delete_one({"_id": ObjectId(trip_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"message": "Trip deleted successfully"}
