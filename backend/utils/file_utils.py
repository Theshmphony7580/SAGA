import os
import uuid
import pathlib
import tempfile
import csv
from typing import Optional, List
from fastapi import UploadFile,HTTPException
from backend.config import DATA_DIR

DATASET_DIR = os.path.join(DATA_DIR, "datasets")
METADATA_DIR = os.path.join(DATA_DIR, "metadata")
pathlib.Path(DATASET_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(METADATA_DIR).mkdir(parents=True, exist_ok=True)

def get_extension(filename: str) -> str:
    filename = filename.lower()
    if filename.endswith(".csv"):
        return ".csv"
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return ".xlsx"
    raise HTTPException(status_code=400, detail="Unsupported file extension")

async def save_dataset(file: UploadFile) -> dict:
    ext = get_extension(file.filename)
    dataset_id = str(uuid.uuid4())
    save_path = os.path.join(DATASET_DIR,dataset_id + ext)
    # suffix = pathlib.Path(file.filename).suffix
    # fd, tmp_path = tempfile.mkstemp(prefix="upload_", suffix=suffix, dir=DATA_DIR)
    # os.close(fd)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {
        "dataset_id": dataset_id,
        "file_path": save_path,
        "extension": ext,
    }


def sniff_delimiter(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            sample = f.read(2048)
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
    except Exception:
        return None

def get_dataset_path(dataset_id:str) -> Optional[str]:
    for ext in [".csv", ".xlsx"]:
        candidate = os.path.join(DATASET_DIR, dataset_id + ext)
        if os.path.exists(candidate):
            return candidate
    return None

def list_datasets() -> List[str]:
    results = []
    for p in pathlib.Path(DATASET_DIR).glob("*"):
        results.append(p.stem)
    return list(set(results))


    # try:
    #     return [str(p) for p in pathlib.Path(DATA_DIR).glob("upload_*")]
    # except Exception:
    #     return []



