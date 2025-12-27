from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
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


@router.post("/insights/{dataset_id}", response_model=InsightsResponse)
async def insights_auto(dataset_id: str):
    try:
        # insights = generate_insights(dataset_id)
        return generate_insights(dataset_id)

        # return InsightsResponse(
        #     dataset_id=dataset_id,
        #     insights=insights
        # )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
