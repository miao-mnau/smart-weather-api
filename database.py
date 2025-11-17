 # === File: database.py ===

import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel

# --- 1. Database URL configuration ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_weather.db")

# --- 2. SQLAlchemy Engine Setup ---
engine_args = {"connect_args":{"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, **engine_args)

# --- 3. Session Configuration ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 4. Base Class for Models
class Base(DeclarativeBase):
    pass

# --- 5. Define the Weather Model (Our Table) ---
class Weather(Base):
    __tablename__ = "weather_data"

    # Define the columns (fields)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=lambda:datetime.now(timezone.utc))
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<Weather(city='{self.city}', temp={self.temperature})>")
    
# --- 6. Create Tables Function ---
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# Pydantic Model
class WeatherRead(BaseModel):
    """
    This Pydantic model defines the "public" shape of our Weather data.
    It ensures we *only* return the fields we want clients to see.
    """

    # We list *only* the fields that are safe to show the public.
    city: str
    timestamp: datetime.datetime
    temperature: float
    humidity: float

    # This special config tells Pydantic to be "compatible"
    # with our SQLAlchemy database models.
    class Config:
        orm_mode = True 
        # (Note: In Pydantic v2, this might be 'from_attributes = True')

# ---Main execution block ---
if __name__ == "__main__":
    print("creating database tables (if they don't exist)...")
    create_db_and_tables()
    print("Database tables check complete.")