import re

def validate_sql(sql: str) -> str:
    sql = sql.strip()

    # remove markdown
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "")

    # remove trailing semicolon duplicates
    sql = sql.strip().rstrip(";")

    # enforce SELECT only
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries allowed")

    return sql + ";"
