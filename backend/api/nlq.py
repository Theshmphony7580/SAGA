from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.ml.nlq_engine import run_nlq

router = APIRouter(tags=["nlq"])


class NLQRequest(BaseModel):
    question: str


class NLQResponse(BaseModel):
    dataset_id: str
    code: str
    result_summary: Optional[str]
    result_table: Optional[List[Dict[str, Any]]]



@router.post("/nlq/{dataset_id}", response_model=NLQResponse)
async def nlq_run(dataset_id: str, req: NLQRequest) -> NLQResponse:
    """
    Executes a natural language query against the specified dataset.
    It automatically uses the best available version of the dataset (cleaned, if available).
    """
    try:
        code, result_summary, result_table = run_nlq(dataset_id, req.question)
        return NLQResponse(
            dataset_id=dataset_id, 
            code=code, 
            result_summary=result_summary, 
            result_table=result_table
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during NLQ processing: {e}")



