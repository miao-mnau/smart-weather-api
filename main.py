import uvicorn
from fastapi import FastAPI

import model
import database

from database import SessionLocal, Weather
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

# --- Startup Tasks ---

print("API Server is  starting up...")

# 1. Create database tables
database.create_db_and_tables()
print("Database tables verified/created.")

# 2. Train/Load the model
print("Executing startup model training...")
model.train_model()
print("Startup model training complete.")

# --- Create FastAPI "app" instance ---
app = FastAPI(
    title="Smart Weather API",
    description="A FastAPI project to extract, store, and predict weather data.",
    version="1.0.0"
)

# ---Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# --- API Endpoints (Routes) ---
@app.get("/api/v1/history")
def get_weather_history(db: Session = Depends(get_db)):
    """
    Fetches the most recent weather data entries from the database.
    """
    history = db.query(Weather).order_by(Weather.timestamp.desc()).limit(100).all()
    return history

@app.get("/api/v1/predict")
def get_weather_prediction(future_time: datetime):
    """
    Predicts the weather for a given future datetime.
    The time must be provided as an ISO format query parameter.
    Example: /api/v1/predict?future_time=2025-12-31T23:59:59
    """

    prediction = model.predict_weather(future_datetime=future_time)

    if prediction is None:
    
        return {
            "error": "Model is not trained or model file (model.pkl) not found."
        }
    return {
        "predicted_temperature": prediction,
        "future_time": future_time
    }

# --- (For Local Development) ---
if __name__ == "__main__":
    print("Starting server in [Development Mode], visit http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)