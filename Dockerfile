# === File: Dockerfile ===

# --- Stage 1: Base Image ---
FROM python:3.10-slim

# --- Stage 2: Set Working Directory ---
WORKDIR /app

# --- Stage 3: Install Dependencies (Cached Layer) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy Application Code ---
COPY . .

# --- Stage 5: Expose Port ---
EXPOSE 8000

# --- Stage 6: Run Command ---
# Define the *default* command to run when the container starts.
# We use uvicorn to run the 'app' object from the 'main.py' file.
#
# IMPORTANT:
# We use "--host 0.0.0.0" (NOT "127.0.0.1").
# "0.0.0.0" means "listen on all available network interfaces".
# "127.0.0.1" means "ONLY listen to traffic from *inside* the container".
# We *must* use 0.0.0.0 so Docker can forward traffic from
# our host machine (our laptop) *into* the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]