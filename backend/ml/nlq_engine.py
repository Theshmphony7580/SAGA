import sqlite3
from backend.config import DATABASE_FILE
from backend.database.utils import find_cleaned_dataset_id,resolve_best_table_name
from backend.ml.text2sql_engine import generate_sql
from backend.ml.sql_sanitize import validate_sql
from backend.database.utils import get_table_schema
# from backend.database.utils import get_table_name_for_dataset



    

def run_nlq(dataset_id: str, question: str):
    """
    Executes a SAFE, READ-ONLY NLQ using SQL.
    """

    cleaned_dataset_id = resolve_best_table_name(dataset_id)
    # cleaned_dataset_id = find_cleaned_dataset_id(dataset_id) #or dataset_id
    schema = get_table_schema(cleaned_dataset_id)
    raw_sql = generate_sql(schema, question)
    sql = validate_sql(raw_sql)

    conn = sqlite3.connect(DATABASE_FILE)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description] #if cur.description else []


        if not isinstance(sql, str):
            raise ValueError("Text2SQL model returned invalid output")
        return {
            "dataset_id": dataset_id,
            "table": cleaned_dataset_id,
            "sql": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
        
    
    finally:
        conn.close()



# def nlq_to_sql(question: str, table_name: str) -> str:
#     """
#     Converts a natural language question into an SQL query for the specified table.
#     This uses basic rule-based pattern matching for demo purposes.
#     """
#     q = question.lower().strip()

#     # Match: "show first 5 rows", "display first 5 rows", etc.
#     m = re.search(r"(?:show|display|give|print)?\s*(?:me\s*)?(?:the\s*)?first\s+(\d+)\s+rows?", q)
#     if m:
#         n = int(m.group(1))
#         return f'SELECT * FROM "{table_name}" LIMIT {n}'


#     # Match: "show last 5 rows", "display last 5 rows", etc.
#     m = re.search(r"(?:show|display|give|print)?\s*(?:me\s*)?(?:the\s*)?last\s+(\d+)\s+rows?", q)
#     if m:
#         n = int(m.group(1))
#         return f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT {n}"

#     # Match: "what are the columns"
#     m = re.search(r"(?:what\s+are\s+the\s+columns|list\s+the\s+columns|show\s+the\s+columns)", q)
#     if m:
#         return f"PRAGMA table_info({table_name})"

#     # Match: "describe the data"
#     m = re.search(r"(?:describe\s+the\s+data|give\s+me\s+a\s+summary\s+of\s+the\s+data)", q)
#     if m:
#         return f"SELECT COUNT(*) as row_count FROM {table_name}"

#     raise ValueError("Question not supported by NLQ engine")