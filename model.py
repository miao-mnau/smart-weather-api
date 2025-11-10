# === File: model.py ===

import pandas as pd
import joblib
import os 
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- 1. Import database setup ---
from database import SessionLocal, Weather, engine

# --- 2. Define Model Path ---
MODEL_PATH = "model.pkl"

# --- 3. Action 1: Training Function ---

def train_model():
    """
    Fetches all data from the database, trains a simple linear regression
    model, and saves it to a file (model.pkl).
    """
    print("Connecting to database...")

    with SessionLocal() as db:
        try:
            query = db.query(Weather).statement
            df = pd.read_sql(query, con=engine)

        except Exception as e:
            print(f"Error reading from database: {e}")
            return
        
        if df.empty:
            print("Database is empty. No data to train on. Skipping training.")
            return
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp_numeric'] = df['timestamp'].astype('int64') // 10**9

        X = df[['timestamp_numeric']]      # Needs to be a 2D-array for sklearn
        y = df['temperature']

        # Need at least 2 data points to train a line
        if len(X) < 2:
            print("Not enough data to train (need at least 2 records). Skipping.")
            return
        
        print(f"Training model on {len(X)} data points...")

        model = LinearRegression()
        model.fit(X, y)

        print(f"Training complete. Saving model to {MODEL_PATH}")
        joblib.dump(model, MODEL_PATH)
        print("Model saved.")

# --- 4. Action 2: Prediction Function ---
def predict_weather(future_datetime: datetime) -> float | None:
    """
    Loads the saved model and uses it to predict the temperature
    for a given future datetime object.
    """

    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}. Run training first.")
        return None
    
    model = joblib.load(MODEL_PATH)

    if future_datetime.tzinfo is None:
        future_datetime = future_datetime.replace(tzinfo=timezone.utc)

    future_timestamp_numeric = future_datetime.timestamp()

    X_future = [[future_timestamp_numeric]]

    prediction = model.predict(X_future)

    predicted_temp = prediction[0]

    print(f"Prediction for {future_datetime}: {predicted_temp:.2f}°C")
    return predicted_temp
    
# --- 5. Main execution block ---
if __name__ == "__main__":
    train_model()

