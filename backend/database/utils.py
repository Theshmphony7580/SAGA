import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional

from backend.config import DATABASE_FILE

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def load_dataframe_to_db(df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
    """
    Loads a pandas DataFrame into a specified SQLite table.

    Args:
        df: The DataFrame to load.
        table_name: The name of the table to create or replace.
        if_exists: Action to take if the table already exists ('replace', 'append', 'fail').
    """
    conn = get_db_connection()
    try:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    finally:
        conn.close()

def insert_dataset_metadata(dataset_id: str, filename: str, table_name: str, is_cleaned: bool = False, source_dataset_id: Optional[str] = None):
    """
    Inserts metadata about a new dataset into the 'datasets' table.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO datasets (id, filename, table_name, is_cleaned, source_dataset_id) VALUES (?, ?, ?, ?, ?)",
            (dataset_id, filename, table_name, is_cleaned, source_dataset_id)
        )
        conn.commit()
    finally:
        conn.close()

def read_dataframe_from_db(table_name: str) -> pd.DataFrame:
    """
    Reads a table from the SQLite database into a pandas DataFrame.

    Args:
        table_name: The name of the table to read.

    Returns:
        A pandas DataFrame with the table's content.
    """
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        return df
    finally:
        conn.close()

def list_datasets_from_db() -> List[Dict[str, Any]]:
    """
    Lists all datasets from the 'datasets' metadata table.

    Returns:
        A list of dictionaries, where each dictionary represents a dataset.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, upload_date FROM datasets ORDER BY upload_date DESC")
        datasets = [dict(row) for row in cursor.fetchall()]
        return datasets
    finally:
        conn.close()

def get_dataset_metadata(dataset_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves metadata for a specific dataset.

    Args:
        dataset_id: The ID of the dataset to look up.

    Returns:
        A dictionary containing the dataset's metadata, or None if not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, upload_date, table_name FROM datasets WHERE id = ?", (dataset_id,))
        metadata = cursor.fetchone()
        return dict(metadata) if metadata else None
    finally:
        conn.close()

def get_table_name_for_dataset(dataset_id: str) -> Optional[str]:
    """
    Retrieves the database table name for a given dataset ID.
    """
    metadata = get_dataset_metadata(dataset_id)
    return metadata['table_name'] if metadata else None

def find_cleaned_dataset_id(source_dataset_id: str) -> Optional[str]:
    """
    Finds the most recent cleaned dataset ID for a given source dataset.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM datasets WHERE source_dataset_id = ? AND is_cleaned = TRUE ORDER BY upload_date DESC LIMIT 1",
            (source_dataset_id,)
        )
        result = cursor.fetchone()
        return result['id'] if result else None
    finally:
        conn.close()
        
def delete_dataset(dataset_id: str) -> bool:
    """
    Deletes dataset metadata and drops the associated table.
    Returns True if deleted, False if not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Fetch dataset metadata
        cursor.execute(
            "SELECT table_name FROM datasets WHERE id = ?",
            (dataset_id,)
        )
        row = cursor.fetchone()
        if not row:
            return False

        table_name = row["table_name"]

        # Drop dataset table
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Delete metadata
        cursor.execute(
            "DELETE FROM datasets WHERE id = ?",
            (dataset_id,)
        )

        conn.commit()
        return True
    finally:
        conn.close()

