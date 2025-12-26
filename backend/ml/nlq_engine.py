from typing import Tuple, Optional, Dict, Any
import pandas as pd
import re
import sqlite3
from backend.config import DATABASE_FILE
from backend.database.utils import find_cleaned_dataset_id

def nlq_to_sql (question: str, table_name: str) -> str:
    """
    Converts a natural language question into an SQL query for the specified table.
    This is a placeholder function. In a real application, this would use an NLP model.
    """
    # Simple rule-based NLQ to SQL conversion (for demonstration purposes)
    q = question.lower().strip()
    
    
    # show first N rows
    m = re.match(r"show the first (\d+) rows", q)
    if m:
        n = int(m.group(1))
        return f"SELECT * FROM {table_name} LIMIT {n}"

    # show last N rows (SQLite-safe)
    m = re.match(r"show the last (\d+) rows", q)
    if m:
        n = int(m.group(1))
        return f"""
            SELECT * FROM {table_name}
            ORDER BY rowid DESC
            LIMIT {n}
        """

    # what are the columns
    if q == "what are the columns":
        return f"PRAGMA table_info({table_name})"

    # describe the data
    if q == "describe the data":
        return f"""
            SELECT
              COUNT(*) as row_count
            FROM {table_name}   
              COUNT(*) as row_count
            FROM {table_name}
        """

    raise ValueError("Question not supported by NLQ engine")

    

def run_nlq(dataset_id: str, question: str) -> Dict[str, Any]:
    """
    Executes a SAFE, READ-ONLY NLQ using SQL.
    """

    table = find_cleaned_dataset_id(dataset_id)
    sql = nlq_to_sql(question, table)

    conn = sqlite3.connect(DATABASE_FILE)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description] if cur.description else []

        return {
            "dataset_id": dataset_id,
            "table": table,
            "sql": sql.strip(),
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
    finally:
        conn.close()


