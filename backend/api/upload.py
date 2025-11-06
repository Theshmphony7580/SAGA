from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.utils.file_utils import save_temp_file, sniff_delimiter
from backend.utils.security import sanitize_text
from backend.config import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES
import os


router = APIRouter(tags=["upload"])


class UploadResponse(BaseModel):
    filename: str
    stored_path: str
    delimiter: Optional[str]
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)) -> UploadResponse:
    filename = sanitize_text(file.filename)
    ext = filename.lower().rsplit(".", 1)
    ext = "." + ext[1] if len(ext) == 2 else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .csv and .xlsx files are supported")

    # Some clients send application/octet-stream; allow if extension is valid
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid content type")

    # size check (read first then enforce)
    stored_path = await save_temp_file(file)
    try:
        size_mb = (os.path.getsize(stored_path) / (1024 * 1024))
    except Exception:
        size_mb = 0
    if size_mb > MAX_FILE_SIZE_MB:
        try:
            os.remove(stored_path)
        except Exception:
            pass
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE_MB} MB)")
    delimiter = None
    if stored_path.lower().endswith(".csv"):
        delimiter = sniff_delimiter(stored_path)

    return UploadResponse(
        filename=filename,
        stored_path=stored_path,
        delimiter=delimiter,
        message="File uploaded successfully",
    )


