from typing import Tuple, Optional, Dict, Any
import pandas as pd
import re
import sqlite3

from streamlit import table
from backend.config import DATABASE_FILE
from backend.database.utils import find_cleaned_dataset_id , get_table_name_for_dataset

def nlq_to_sql(question: str, table_name: str) -> str:
    """
    Converts a natural language question into an SQL query for the specified table.
    This uses basic rule-based pattern matching for demo purposes.
    """
    q = question.lower().strip()

    # Match: "show first 5 rows", "display first 5 rows", etc.
    m = re.search(r"(?:show|display|give|print)?\s*(?:me\s*)?(?:the\s*)?first\s+(\d+)\s+rows?", q)
    if m:
        n = int(m.group(1))
        return f'SELECT * FROM "{table_name}" LIMIT {n}'


    # Match: "show last 5 rows", "display last 5 rows", etc.
    m = re.search(r"(?:show|display|give|print)?\s*(?:me\s*)?(?:the\s*)?last\s+(\d+)\s+rows?", q)
    if m:
        n = int(m.group(1))
        return f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT {n}"

    # Match: "what are the columns"
    m = re.search(r"(?:what\s+are\s+the\s+columns|list\s+the\s+columns|show\s+the\s+columns)", q)
    if m:
        return f"PRAGMA table_info({table_name})"

    # Match: "describe the data"
    m = re.search(r"(?:describe\s+the\s+data|give\s+me\s+a\s+summary\s+of\s+the\s+data)", q)
    if m:
        return f"SELECT COUNT(*) as row_count FROM {table_name}"

    raise ValueError("Question not supported by NLQ engine")


    

def run_nlq(dataset_id: str, question: str) -> Dict[str, Any]:
    """
    Executes a SAFE, READ-ONLY NLQ using SQL.
    """

    cleaned_dataset_id = find_cleaned_dataset_id(dataset_id) or dataset_id
    from backend.database.utils import get_table_name_for_dataset
    table = get_table_name_for_dataset(cleaned_dataset_id)
    if not table:
        raise ValueError(f"No table found for dataset ID: {cleaned_dataset_id}")
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


