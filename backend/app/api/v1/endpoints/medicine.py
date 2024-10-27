from fastapi import APIRouter, HTTPException
from app.models.medicine import *
from app.services.medicine_service import MedicineService
from app.tasks.scrapers.medicine_scraper import RateLimitException, ForbiddenException
from app.core.database import db

router = APIRouter()

@router.post("/raw", response_model=MedicineSearchResponse)
def search_medicines_raw(request: MedicineSearchRequest):
    """Raw medicine search endpoint that directly queries the DIGEMID API"""
    try:
        medicine_service = MedicineService(db)
        result = medicine_service.search_medicines(
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

@router.post("/process-document")
def process_document(request: ProcessDocumentRequest):
    """Process a single searchterms document by ID and return transformed data"""
    try:
        medicine_service = MedicineService(db)
        result = medicine_service.process_document(
            document_id=request.document_id,
            region_data=request.region_data.dict(),
            limit=request.limit
        )
        return {
            "message": "Document processing completed",
            "stats": {
                "total_concentrations": result["total_concentrations"],
                "processed": result["processed"],
                "success": result["success"],
                "failed": result["failed"]
            },
            "data": result["transformed_data"]
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/process-document-store")
def process_and_store_document(request: ProcessDocumentRequest):
    """Process a document and store results in MongoDB"""
    try:
        medicine_service = MedicineService(db)
        result = medicine_service.store_processed_data(
            document_id=request.document_id,
            region_data=request.region_data.dict(),
            limit=request.limit
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing and storing: {str(e)}")
    
@router.post("/process-all")
def process_all_documents(request: ProcessAllRequest):
    """Process all searchterms documents with persistence"""
    try:
        medicine_service = MedicineService(db)
        result = medicine_service.process_all_documents(
            region_data=request.region_data.dict(),
            run_id=request.run_id,
            batch_size=request.batch_size
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing documents: {str(e)}"
        )

@router.get("/processing-run/{run_id}")
def get_processing_run(run_id: str):
    """Get details of a processing run"""
    try:
        medicine_service = MedicineService(db)
        run = medicine_service.get_processing_run(run_id)
        if not run:
            raise HTTPException(
                status_code=404,
                detail=f"Processing run {run_id} not found"
            )
        return run
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting processing run: {str(e)}"
        )
        
@router.post("/retry-failed")
def retry_failed_documents(request: RetryFailedRequest):
    """Retry processing failed documents from a previous run"""
    try:
        medicine_service = MedicineService(db)
        result = medicine_service.retry_failed_documents(
            original_run_id=request.run_id,
            region_data=request.region_data.dict() if request.region_data else None,
            batch_size=request.batch_size or 100
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrying failed documents: {str(e)}"
        )