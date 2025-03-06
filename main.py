from fastapi import FastAPI
from routes.auth import router as auth_router  # ✅ Correct path for auth.py
from routes.trip_routes import router as trip_router  # ✅ Correct path for trip_routes.py
from routes.leader_auth import router as leader_auth_router  # ✅ Correct path for leader_auth.py

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Trip Management API is running!"}

# ✅ Include routers
app.include_router(auth_router)
app.include_router(trip_router)
app.include_router(leader_auth_router)  # ✅ Use correct router variable
