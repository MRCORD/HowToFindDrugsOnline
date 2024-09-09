import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from . import views

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the main FastAPI application
app = FastAPI(docs_url=None, redoc_url=None)

# Create a sub-application for /api routes
api_app = FastAPI(docs_url='/docs', redoc_url='/redoc')

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://buscatupepa.com,http://frontend_react_service:3000").split(",")
origins = [origin.strip() for origin in origins if origin.strip()]

logger.info(f"Allowed CORS origins: {origins}")

# Apply CORS middleware to both the main app and the api_app
for application in [app, api_app]:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include router in the api_app
api_app.include_router(views.router)

# Mount the api_app under /api
app.mount("/api", api_app)

# Define a route to retrieve logs
@api_app.get("/logs")
async def get_logs():
    try:
        with open("app.log", "r") as log_file:
            logs = log_file.readlines()
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving logs")

# Root route for the main app
@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Please use /api for all endpoints."}

# Catch-all route for the main app to redirect non-/api requests
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    return JSONResponse(
        status_code=404,
        content={"message": f"Endpoint /{path_name} not found. Please use /api for all endpoints."}
    )

# Startup event to log when the application starts
@app.on_event("startup")
async def startup_event():
    logger.info("Application has started")
    logger.info(f"API routes: {[route.path for route in api_app.routes]}")

# Shutdown event to log when the application stops
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down")