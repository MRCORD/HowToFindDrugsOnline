from fastapi import APIRouter, Depends, HTTPException
from app.services.pharmacy_service import PharmacyService
from app.models.pharmacy import PharmacySearchRequest, PharmacyResponse
from app.api.dependencies import get_pharmacy_service

router = APIRouter()

@router.post("/raw", response_model=PharmacyResponse)
def get_raw_pharmacies(
    request: PharmacySearchRequest,
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    data = pharmacy_service.get_raw_pharmacies(request)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch pharmacy data")
    return data