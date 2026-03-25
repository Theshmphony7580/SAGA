import os
from typing import List


APP_NAME: str = "AI-Powered Data Analytics Assistant"
APP_VERSION: str = "2.0"

# Directories
ROOT_DIR: str = os.getcwd()
DATA_DIR: str = os.path.join(ROOT_DIR, "data")
REPORTS_DIR: str = os.path.join(ROOT_DIR, "reports")
DATABASE_DIR = os.path.join(DATA_DIR, "db")
DATABASE_FILE: str = os.path.join(DATABASE_DIR, "analytics.db")

#models
from dotenv import load_dotenv

load_dotenv()

# LLM API Keys
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ollama (local LLM) — PLACEHOLDER: uncomment when ready to add Ollama
# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Agent config
SCHEMA_SAMPLE_ROWS: int = 3  # Number of sample rows to include in schema context for LLM

# LLM Model selection
GEMINI_FAST_MODEL: str = "gemini-2.0-flash"              # For routing, classification
GEMINI_POWER_MODEL: str = "gemini-2.0-flash"  # For code gen, deep analysis

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
ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]

# WebSocket
WS_MAX_MESSAGE_SIZE: int = 1024 * 64  # 64KB max per message

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)


