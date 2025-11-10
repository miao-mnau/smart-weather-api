import uvicorn
from fastapi import FastAPI

import model
import database

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

# --- API Endpoints (Routes) ---




# --- (For Local Development) ---
if __name__ == "__main__":
    print("Starting server in [Development Mode], visit http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)