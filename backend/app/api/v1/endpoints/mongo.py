from fastapi import APIRouter, Depends, HTTPException
from app.services.mongo_service import MongoService
from app.models.mongo import MongoQuery, ResponseModel

router = APIRouter()

@router.post("/consult", response_model=ResponseModel, tags=["MongoDB", "Production"])
async def consult_mongo(request: MongoQuery, mongo_service: MongoService = Depends()):
    try:
        result = await mongo_service.consult_mongo(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MongoDB query: {str(e)}")