from pydantic import BaseModel
from typing import List, Dict, Optional

class TripSchema(BaseModel):
    id: Optional[str]  # ✅ MongoDB _id is optional (FastAPI auto-generates it)
    name: str
    description: str
    location: str
    itinerary: List[Dict[str, str]]  # [{"day": "1", "activity": "Sightseeing"}]
    schedule: Dict[str, str]  # {"start_date": "2025-06-10", "end_date": "2025-06-15"}
    transportation: Dict[str, str]  # {"mode": "Bus", "details": "Luxury AC Bus"}
    price: int  # Price field added

    class Config:
        orm_mode = True
