from pydantic import BaseModel
from typing import List, Dict, Optional

class TripSchema(BaseModel):
    id: Optional[str] = None  # Allows an optional ID
    name: str
    description: str
    location: str
    itinerary: List[Dict[str, str]]  # Example: [{"day": "1", "activity": "Sightseeing"}]
    schedule: Dict[str, str]  # Example: {"start_date": "2025-06-10", "end_date": "2025-06-15"}
    transportation: Dict[str, str]  # Example: {"mode": "flight", "details": "Flight XYZ123"}

    class Config:
        form_attributes = True  # Enables conversion from DB objects
