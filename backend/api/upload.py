from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from backend.utils.file_utils import save_dataset, get_extension
from backend.utils.security import sanitize_text
from backend.config import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES
from backend.database.file_manager import FileIngestionManager

router = APIRouter(tags=["upload"])


class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    message: str
    rows: int
    columns: int
    schema_context: str


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)) -> UploadResponse:
    """
    Handles dataset upload. Validates the file, then delegates all processing
    to FileIngestionManager for robust parsing, caching, and schema extraction.
    """
    filename = sanitize_text(file.filename)

    # --- Validation ---
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported")

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid content type: {file.content_type}")

    # Save the file temporarily to disk
    saved_file_info = await save_dataset(file)
    stored_path = saved_file_info["file_path"]

    # File size check
    if os.path.getsize(stored_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
        os.remove(stored_path)
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE_MB} MB)")

    try:
        # --- Delegate to FileIngestionManager ---
        result = FileIngestionManager.ingest(stored_path, filename)

        return UploadResponse(
            dataset_id=result["dataset_id"],
            filename=filename,
            message="File uploaded and processed successfully.",
            rows=result["rows"],
            columns=result["columns"],
            schema_context=result["schema_context"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(stored_path):
            os.remove(stored_path)
