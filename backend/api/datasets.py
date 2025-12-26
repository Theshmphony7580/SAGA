from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from backend.database.utils import get_dataset_metadata, delete_dataset

router = APIRouter(tags=["datasets"])


@router.get("/datasets/{dataset_id}")#(, response_model=List[Dict[str, Any]])
def get_datasets(dataset_id: str):
    """
    GET /v1/datasets/{dataset_id}
    Returns all datasets from the registry
    """
    dataset = get_dataset_metadata(dataset_id)
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {
        "dataset_id": dataset["id"],
        "filename": dataset["filename"],
        "upload_date": dataset["upload_date"],
        "table_name": dataset["table_name"],
        "is_cleaned": dataset.get("is_cleaned"),
        "source_dataset_id": dataset.get("source_dataset_id"),
    }
    
@router.delete("/datasets/{dataset_id}")
def delete_datasets(dataset_id: str):
    """
    DELETE /v1/datasets/{dataset_id}
    Deletes a dataset from the registry
    """
    success = delete_dataset(dataset_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found or could not be deleted")
    
    return {
        "status": "success",
        "dataset_id": dataset_id
    }