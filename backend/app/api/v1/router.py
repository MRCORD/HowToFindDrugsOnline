from app.api.v1.endpoints import drugs, generics, mongo, catalog
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
api_router.include_router(generics.router, prefix="/generics", tags=["generics"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])