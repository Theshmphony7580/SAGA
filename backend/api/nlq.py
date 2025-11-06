from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from backend.ml.nlq_engine import run_nlq
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

router = APIRouter(tags=["nlq"])


class NLQRequest(BaseModel):
    path: str
    question: str


class NLQResponse(BaseModel):
    code: str
    result_summary: Optional[str]
    figure_json: Optional[Dict[str, Any]]


@router.post("/nlq/run", response_model=NLQResponse)
async def nlq_run(req: NLQRequest) -> NLQResponse:
    try:
        code, result_summary, figure_json = run_nlq(req.path, req.question)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return NLQResponse(code=code, result_summary=result_summary, figure_json=figure_json)


