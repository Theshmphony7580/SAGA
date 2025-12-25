from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from backend.ml.insights_engine import generate_insights

router = APIRouter(tags=["insights"])

class InsightsResponse(BaseModel):
    dataset_id: str
    num_rows: int
    num_columns: int
    numeric_summary: Dict[str, Any]
    correlations: Dict[str, Any]
    category_insights: Dict[str, Any]
    extremes: Dict[str, Any]

@router.get("/insights/{dataset_id}", response_model=InsightsResponse)
async def insights_auto(dataset_id: str) -> InsightsResponse:
    """
    Generates and returns a set of automated insights for the specified dataset.
    It will automatically use the latest cleaned version of the dataset if available.
    """
    try:
        result = generate_insights(dataset_id)
        return InsightsResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during insight generation: {e}")
