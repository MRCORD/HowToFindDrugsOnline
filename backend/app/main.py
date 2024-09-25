import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the main FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",  # Enable Swagger UI for the main app
    redoc_url="/redoc"  # Enable ReDoc for the main app
)

# Create a sub-application for /api routes
api_app = FastAPI(
    title=f"{settings.PROJECT_NAME} - API",
    version=settings.PROJECT_VERSION,
    docs_url="/docs",  # Swagger UI for the API app
    redoc_url="/redoc"  # ReDoc for the API app
)

# Configure CORS
logger.info(f"Allowed CORS origins: {settings.ALLOWED_ORIGINS}")

# Apply CORS middleware to both the main app and the api_app
for application in [app, api_app]:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include router in the api_app
api_app.include_router(api_router, prefix="/v1")

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

# Startup event to log when the application starts
@app.on_event("startup")
async def startup_event():
    logger.info("Application has started")
    logger.info(f"Main app routes: {[route.path for route in app.routes]}")
    logger.info(f"API routes: {[route.path for route in api_app.routes]}")

# Shutdown event to log when the application stops
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down")