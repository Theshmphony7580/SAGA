from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List
from backend.ml.insights_engine import generate_insights
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["insights"])


class InsightsRequest(BaseModel):
    path: str


class InsightItem(BaseModel):
    title: str
    description: str
    score: float


class InsightsResponse(BaseModel):
    insights: List[InsightItem]


@router.post("/insights/auto", response_model=InsightsResponse)
async def insights_auto(req: InsightsRequest) -> InsightsResponse:
    try:
        items = generate_insights(req.path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return InsightsResponse(insights=[InsightItem(**i) for i in items])


