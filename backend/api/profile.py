from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.profiling import generate_profile

router = APIRouter(tags=["profile"])


class ProfileResponse(BaseModel):
    dataset_id: str
    profiling: Dict[str, Any]


@router.get("/profile", response_model=ProfileResponse)
async def profile_dataset(dataset_id: str) -> ProfileResponse:
    try:
        summary = generate_profile(dataset_id)
        return ProfileResponse(
            dataset_id=dataset_id,
            profiling=summary
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
