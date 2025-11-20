from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.ml.nlq_engine import run_nlq
from backend.utils.file_utils import get_dataset_path
from pandas.errors import ParserError
from backend.utils.data_utils import CSVValidationError

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

    if not get_dataset_path(dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        code, result_summary, result_table = run_nlq(dataset_id, req.question)
    except CSVValidationError as e:
        raise HTTPException(status_code=400, detail=f"CSV validation failed: {str(e)}")
    except ParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NLQ processing error: {str(e)}")
    return NLQResponse(dataset_id=dataset_id, code=code, result_summary=result_summary, result_table=result_table)


