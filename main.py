import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Hello from Railway!",
        "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "local")
    }

@app.get("/health")
def health_check():
    return {"healthy": True}
