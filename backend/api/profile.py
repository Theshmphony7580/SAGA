from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.profiling import generate_profile
from backend.utils.file_utils import get_dataset_path
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["profile"])


class ProfileResponse(BaseModel):
    dataset_id: str
    profiling: Dict[str, Any]


@router.get("/profile", response_model=ProfileResponse)
async def profile_dataset(dataset_id: str) -> ProfileResponse:
    dataset_path = get_dataset_path(dataset_id)
    if not dataset_path:
        raise HTTPException(status_code=404, detail="Dataset not found")
    try:
        summary = generate_profile(dataset_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ProfileResponse(
        dataset_id=dataset_id,
        profiling=summary
    )
