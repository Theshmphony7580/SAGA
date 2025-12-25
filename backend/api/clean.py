from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.cleaning import clean_dataset

router = APIRouter(tags=["clean"])

class CleanResponse(BaseModel):
    original_dataset_id: str
    cleaned_dataset_id: str
    rows_before: int
    rows_after: int
    cleaning_log: Dict[str, Any]

@router.post("/clean/{dataset_id}", response_model=CleanResponse)
async def clean(dataset_id: str) -> CleanResponse:
    """
    Cleans a specified dataset and creates a new, cleaned version in the database.
    """
    try:
        result = clean_dataset(dataset_id)
        return CleanResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during cleaning: {e}")
