# === File: pipeline.py ===

# To fetch data from the internet and put it in database.

import requests
import time
import datetime
from sqlalchemy.orm import Session

import database
from database import SessionLocal, Weather, create_db_and_tables

# --- (E) EXTRACT: API Configuration ---
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CITY_NAME = "Brno" 
CITY_LATITUDE = 49.19
CITY_LONGITUDE = 16.61

def fetch_and_store_weather():
    """
    This is the core ETL function.
    It fetches data, transforms it, and loads it into the database.
    """
    print(f"[{datetime.datetime.now()}] Starting ETL run...")

    try:
        # --- (E) EXTRACT ---
        params = {
            "latitude": CITY_LATITUDE,
            "longitude": CITY_LONGITUDE,
            "current": "temperature_2m,relative_humidity_2m", 
            "timezone": "auto"
        }

        print(f"Fetching data from Open-Meteo for {CITY_NAME}...")
        response = requests.get(OPEN_METEO_URL, params=params)

        response.raise_for_status()

        data = response.json()


        # --- (T) TRANSFORM ---
        current_data = data['current']

        timestamp = datetime.datetime.fromisoformat(current_data['time'])
        temp = current_data['temperature_2m']
        humidity = current_data['relative_humidity_2m']

        print(f"Data received: Temp={temp}°C, Humidity={humidity}%, Time={timestamp}")

        # --- (L) LOAD ---
        print("Loading data into database...")
        with SessionLocal() as db:
            weather_entry = Weather(
                city=CITY_NAME,
                timestamp=timestamp,
                temperature=temp,
                humidity=humidity
            )
            
            db.add(weather_entry) 
            db.commit()           
        
        print(f"Data stored successfully for {timestamp}.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except KeyError as e:
        print(f"Error parsing API response. Missing key: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    print("Pipeline worker starting... Verifying database tables.")
    create_db_and_tables()
    print("Database tables verified.")
    
    print("Starting infinite ETL loop (runs every 1 hour).")
    while True:
        fetch_and_store_weather() # Run the ETL job
        
        # Sleep for 1 hour (3600 seconds)
        print(f"Sleeping for 1 hour (3600 seconds)...")
        time.sleep(3600)