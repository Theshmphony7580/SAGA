from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import os

from backend.utils.file_utils import save_dataset, get_extension
from backend.utils.data_utils import read_dataframe_auto
from backend.database.utils import load_dataframe_to_db, insert_dataset_metadata
from backend.utils.security import sanitize_text
from backend.config import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES

router = APIRouter(tags=["upload"])

class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    message: str
    
@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)) -> UploadResponse:
    """
    Handles dataset upload, saving it to the database.
    """
    filename = sanitize_text(file.filename)
    
    # Basic validation
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported")
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid content type: {file.content_type}")

    # Save the file temporarily to read it
    saved_file_info = await save_dataset(file)
    stored_path = saved_file_info["file_path"]

    # File size check
    if os.path.getsize(stored_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
        os.remove(stored_path)
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE_MB} MB)")

    try:
        # Read data into DataFrame
        df = read_dataframe_auto(stored_path)

        # Generate a unique ID and table name for the dataset
        dataset_id = str(uuid.uuid4())
        table_name = f"dataset_{dataset_id.replace('-', '_')}"

        # Load DataFrame into the database
        load_dataframe_to_db(df, table_name)

        # Record metadata
        insert_dataset_metadata(dataset_id=dataset_id, filename=filename, table_name=table_name)
        
        return UploadResponse(
            dataset_id=dataset_id,
            filename=filename,
            message="File uploaded and processed successfully.",
        )
    except Exception as e:
        # If anything goes wrong, delete the temp file
        os.remove(stored_path)
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    finally:
        # Optionally, delete the original file after processing to save space
        if os.path.exists(stored_path):
             os.remove(stored_path)


