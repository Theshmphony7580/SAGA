from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from backend.database.utils import (
    get_dataset_metadata,
    read_dataframe_from_db,
    load_dataframe_to_db,
    insert_dataset_metadata
)

from backend.ml.cleaning import clean_dataframe

router = APIRouter(tags=["clean"])

class CleanResponse(BaseModel):
    original_dataset_id: str
    cleaned_dataset_id: str
    report: Dict[str, Any]


@router.post("/clean/{dataset_id}", response_model=CleanResponse)
async def clean(dataset_id: str) -> CleanResponse:
    """
    Cleans a specified dataset and creates a new, cleaned version in the database.
    """
    
    original_metadata = get_dataset_metadata(dataset_id)
    
    if not original_metadata:
        raise HTTPException(status_code=404, detail="Original dataset not found")
    original_table = original_metadata["table_name"]
    try :
        df = read_dataframe_from_db(original_table)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read original dataset: {str(e)}")
    
    cleaned_df, report = clean_dataframe(df)
    cleaned_dataset_id = str(uuid.uuid4())
    cleaned_table_name = f"dataset_{cleaned_dataset_id.replace('-', '_')}"
    
    try : 
        load_dataframe_to_db(cleaned_df, cleaned_table_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load cleaned dataset: {str(e)}")

    insert_dataset_metadata(
        dataset_id=cleaned_dataset_id,
        filename=original_metadata["filename"],
        table_name=cleaned_table_name,
        is_cleaned=True,
        source_dataset_id=dataset_id
    )

    return CleanResponse(
        original_dataset_id=dataset_id,
        cleaned_dataset_id=cleaned_dataset_id,
        report=report
    )
