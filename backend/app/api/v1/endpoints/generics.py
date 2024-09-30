from fastapi import APIRouter, Depends, HTTPException
from app.services.generics_service import GenericsService
from app.models.generics import GenericResponse
from typing import List

router = APIRouter()

@router.get("/generics", response_model=List[GenericResponse])
async def get_generics(generics_service: GenericsService = Depends()):
    return await generics_service.get_generics()