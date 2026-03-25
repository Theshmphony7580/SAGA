"""
FileIngestionManager: The central file processing engine for SAGA.

Handles high-speed CSV/XLSX ingestion, SQLite caching, and schema context
generation for LangGraph agents.
"""

import pandas as pd
import uuid
from typing import Dict, Any
from loguru import logger

from backend.database.utils import load_dataframe_to_db, insert_dataset_metadata
from backend.utils.data_utils import read_dataframe_auto, try_parse_numeric, try_parse_date
from backend.config import SCHEMA_SAMPLE_ROWS


class FileIngestionManager:
    """
    Centralized file processing pipeline used by the upload endpoint
    and all LangGraph agents.
    """

    @staticmethod
    def ingest(file_path: str, original_filename: str) -> Dict[str, Any]:
        """
        Main entry point. Orchestrates the full ingestion pipeline:
        1. Parse file -> 2. Sanitize -> 3. Type inference -> 4. SQLite cache -> 5. Schema context.

        Args:
            file_path: Absolute path to the saved file on disk.
            original_filename: The original name of the uploaded file.

        Returns:
            Dict with: dataset_id, table_name, filename, rows, columns, schema_context
        """
        logger.info(f"[FileIngestionManager] Starting ingestion: {original_filename}")

        # 1. Parse the file using the existing robust reader
        df = read_dataframe_auto(file_path)
        logger.info(f"[FileIngestionManager] Parsed {len(df)} rows, {len(df.columns)} columns")

        # 2. Sanitize column names for safe SQL usage
        df = FileIngestionManager._sanitize_columns(df)

        # 3. Attempt smart type inference (numeric/date casting)
        df = FileIngestionManager._infer_and_cast_types(df)

        # 4. Generate identifiers and cache into SQLite
        dataset_id = str(uuid.uuid4())
        table_name = f"dataset_{dataset_id.replace('-', '_')}"

        logger.info(f"[FileIngestionManager] Caching into SQLite table: {table_name}")
        load_dataframe_to_db(df, table_name)
        insert_dataset_metadata(dataset_id=dataset_id, filename=original_filename, table_name=table_name)

        # 5. Build the lightweight schema context string for LLM prompts
        schema_context = FileIngestionManager._build_schema_context(df, table_name)

        logger.info(f"[FileIngestionManager] Ingestion complete for {original_filename} -> {dataset_id}")

        return {
            "dataset_id": dataset_id,
            "table_name": table_name,
            "filename": original_filename,
            "rows": len(df),
            "columns": len(df.columns),
            "schema_context": schema_context,
        }

    @staticmethod
    def _sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Lowercases column names, replaces spaces/hyphens/dots with underscores,
        and strips leading/trailing whitespace.
        """
        df.columns = [
            str(c).strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_")
            for c in df.columns
        ]
        return df

    @staticmethod
    def _infer_and_cast_types(df: pd.DataFrame) -> pd.DataFrame:
        """
        Attempts to cast 'object' columns to numeric or datetime where possible.
        This improves SQLite storage efficiency and SQL query accuracy.
        """
        for col in df.columns:
            if df[col].dtype == "object":
                # Try numeric first (most common mistype)
                df[col] = try_parse_numeric(df[col])
                # If still object, try date
                if df[col].dtype == "object":
                    df[col] = try_parse_date(df[col])
        return df

    @staticmethod
    def _build_schema_context(df: pd.DataFrame, table_name: str) -> str:
        """
        Generates a compact, LLM-optimized schema string.

        Output format:
            TABLE dataset_abc123 (
              age INTEGER,         -- samples: 25, 30, 45
              name TEXT,           -- samples: 'Alice', 'Bob', 'Charlie'
              salary REAL,         -- samples: 50000.0, 75000.0
            )
            Rows: 15000 | Columns: 4
        """
        lines = [f"TABLE {table_name} ("]

        for col in df.columns:
            # Map pandas dtype to SQL-like type names
            sql_type = FileIngestionManager._pandas_dtype_to_sql(df[col].dtype)

            # Get sample values (non-null, unique, up to SCHEMA_SAMPLE_ROWS)
            samples = df[col].dropna().unique()[:SCHEMA_SAMPLE_ROWS]
            if sql_type == "TEXT":
                sample_str = ", ".join(f"'{s}'" for s in samples)
            else:
                sample_str = ", ".join(str(s) for s in samples)

            lines.append(f"  {col} {sql_type},  -- samples: {sample_str}")

        lines.append(")")
        lines.append(f"Rows: {len(df)} | Columns: {len(df.columns)}")

        return "\n".join(lines)

    @staticmethod
    def _pandas_dtype_to_sql(dtype) -> str:
        """Maps a pandas dtype to a simplified SQL type name for LLM context."""
        kind = dtype.kind
        if kind in ("i", "u"):  # signed/unsigned integer
            return "INTEGER"
        elif kind == "f":  # float
            return "REAL"
        elif kind == "b":  # boolean
            return "BOOLEAN"
        elif kind in ("M", "m"):  # datetime / timedelta
            return "DATETIME"
        else:
            return "TEXT"
