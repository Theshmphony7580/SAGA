from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.ml.nlq_engine import run_nlq
import traceback

router = APIRouter(tags=["nlq"])


class NLQRequest(BaseModel):
    dataset_id: str
    question: str


class NLQResponse(BaseModel):
    dataset_id: str
    table: str
    sql: str
    columns: List[str]
    rows: List[Any]
    row_count: int



@router.post("/nlq/run", response_model=NLQResponse)
async def nlq_run(req: NLQRequest):
    try:
        return NLQResponse(**run_nlq(req.dataset_id, req.question))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as e:
        print("nlq_run error:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=repr(e))


