from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.profiling import generate_profile
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["profile"])


class ProfileRequest(BaseModel):
    path: str


class ProfileResponse(BaseModel):
    summary: Dict[str, Any]


@router.post("/profile", response_model=ProfileResponse)
async def profile_dataset(req: ProfileRequest) -> ProfileResponse:
    try:
        summary = generate_profile(req.path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ProfileResponse(summary=summary)


