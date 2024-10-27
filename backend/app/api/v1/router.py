from app.api.v1.endpoints import drugs, generics, mongo, catalog, searchterm, medicine, pharmacies
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
api_router.include_router(generics.router, prefix="/generics", tags=["generics"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(searchterm.router, prefix="/searchterm", tags=["searchterm"])
api_router.include_router(medicine.router, prefix="/medicine", tags=["medicine"])
api_router.include_router(pharmacies.router, prefix="/pharmacies", tags=["pharmacies"])