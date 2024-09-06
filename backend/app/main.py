import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import views

app = FastAPI(docs_url='/')

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router without dependencies
app.include_router(views.router)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a route to retrieve logs
@app.get("/logger")
async def get_logs():
    try:
        # Open the log file and read its content
        with open("app.log", "r") as log_file:
            logs = log_file.readlines()
        # Return logs as response
        return {"logs": logs}
    except Exception as e:
        # If an error occurs, raise an HTTPException with status code 500
        raise HTTPException(status_code=500, detail=str(e))
