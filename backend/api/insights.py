from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from backend.ml.insights_engine import generate_insights
from backend.utils.file_utils import get_dataset_path
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

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
    if not get_dataset_path(dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        result = generate_insights(dataset_id)
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insight generation error: {str(e)}")
    
    return InsightsResponse(**result)


# class InsightsRequest(BaseModel):
#     path: str


# class InsightItem(BaseModel):
#     title: str
#     description: str
#     score: float
