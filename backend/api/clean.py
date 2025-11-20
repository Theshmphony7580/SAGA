from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.cleaning import clean_dataset
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError
from backend.utils.file_utils import get_dataset_path

router = APIRouter(tags=["clean"])


class CleanRequest(BaseModel):
    path: str


class CleanResponse(BaseModel):
    dataset_id: str
    cleaned_path: str
    row_after_cleaning: int
    cleaning_logs: Dict[str, Any]


@router.post("/clean/{dataset_id}", response_model=CleanResponse)
async def clean(dataset_id: str) -> CleanResponse:

    if not get_dataset_path(dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    

    try:
        result = clean_dataset(dataset_id)
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return CleanResponse(
        dataset_id=dataset_id,
        cleaned_path=result["cleaned_path"],
        row_after_cleaning=result["rows_after_cleaning"],
        cleaning_logs=result["cleaning_log"]
    )


