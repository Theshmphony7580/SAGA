import os
import pathlib
import tempfile
import csv
from typing import Optional, List
from fastapi import UploadFile
from backend.config import DATA_DIR


pathlib.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


async def save_temp_file(file: UploadFile) -> str:
    suffix = pathlib.Path(file.filename).suffix
    fd, tmp_path = tempfile.mkstemp(prefix="upload_", suffix=suffix, dir=DATA_DIR)
    os.close(fd)
    with open(tmp_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return tmp_path


def sniff_delimiter(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            sample = f.read(2048)
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
    except Exception:
        return None


def list_uploaded_files() -> List[str]:
    try:
        return [str(p) for p in pathlib.Path(DATA_DIR).glob("upload_*")]
    except Exception:
        return []



