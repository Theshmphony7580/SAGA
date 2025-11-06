import os
from typing import List


APP_NAME: str = "AI-Powered Data Analytics Assistant"
APP_VERSION: str = "2.0"

# Directories
ROOT_DIR: str = os.getcwd()
DATA_DIR: str = os.path.join(ROOT_DIR, "data")
REPORTS_DIR: str = os.path.join(ROOT_DIR, "reports")

# Upload constraints
MAX_FILE_SIZE_MB: int = 200
ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx"]
ALLOWED_MIME_TYPES: List[str] = [
    "text/csv",  # common for .csv
    "application/csv",  # sometimes sent by clients
    "text/plain",  # some browsers label small CSVs as plain text
    "application/octet-stream",  # requests default when content-type is omitted
    "application/vnd.ms-excel",  # legacy Excel and sometimes CSV
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
]

# CORS
ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://127.0.0.1:8501", "*"]

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


