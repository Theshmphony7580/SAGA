from fastapi import APIRouter, HTTPException
from backend.database.utils import get_columns_for_dataset

router = APIRouter(tags=["columns"])

@router.get("/columns")
def list_columns(dataset_id: str):
    try:
        return {
            "dataset_id": dataset_id,
            "columns": get_columns_for_dataset(dataset_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

