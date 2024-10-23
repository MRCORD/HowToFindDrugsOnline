from fastapi import APIRouter, HTTPException
from app.models.medicine import MedicineSearchRequest, MedicineSearchResponse
from app.tasks.scrapers.medicine_scraper import scraper, RateLimitException, ForbiddenException

router = APIRouter()

@router.post("/raw", response_model=MedicineSearchResponse)
async def search_medicines_raw(request: MedicineSearchRequest):
    """
    Raw medicine search endpoint that directly queries the DIGEMID API
    """
    try:
        result = scraper.search_medicines(
            request.product_data.dict(),
            request.region_data.dict(),
            request.exact_search
        )
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No results found or service unavailable"
            )
        
        return MedicineSearchResponse(
            data=result.get('data', []),
            totalFilas=result.get('totalFilas', 0),
            message=result.get('message')
        )
        
    except RateLimitException:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
        
    except ForbiddenException:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )