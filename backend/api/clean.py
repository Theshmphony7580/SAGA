from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.cleaning import clean_dataset
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["clean"])


class CleanRequest(BaseModel):
    path: str


class CleanResponse(BaseModel):
    cleaned_path: str
    report: Dict[str, Any]


@router.post("/clean", response_model=CleanResponse)
async def clean(req: CleanRequest) -> CleanResponse:
    try:
        cleaned_path, report = clean_dataset(req.path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CleanResponse(cleaned_path=cleaned_path, report=report)


