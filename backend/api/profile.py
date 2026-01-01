from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.ml.profiling import generate_profile 
from backend.database.utils import get_dataset_metadata, read_dataframe_from_db 

router = APIRouter(tags=["profile"])


# class ProfileResponse(BaseModel):
#     dataset_id: str
#     profiling: Dict[str, Any]


@router.get("/profile")     
async def profile_dataset(dataset_id: str):
    
    
    try:
        return generate_profile(dataset_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # metadata = get_dataset_metadata(dataset_id)
    # if not metadata:
    #     raise HTTPException(status_code=404, detail="Dataset not found")
    # table_name = metadata["table_name"]
    # try:
    #     df = read_dataframe_from_db(table_name)

    # except FileNotFoundError as e:
    #     raise HTTPException(status_code=404, detail=str(e))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    # profiling = basic_profile(dataset_id)
    # return ProfileResponse(
    #     dataset_id=dataset_id,
    #     profiling=profiling
    # )
