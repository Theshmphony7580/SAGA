import re 
import pandas as pd 
from typing import Dict, Any
# import os
# from backend.database.utils import get_table_name_for_dataset, read_dataframe_from_db

def infer_semantic_type(series: pd.Series) -> str:
    sampale = series.dropna().astype(str)
    if sampale.empty:
        return "unknown"
    first = sampale.iloc[0]
    if re.match(r'[^@]+@[^@]+\.[^@]+', first):
        return "email"
    try :
        pd.to_datetime(first)
        return "date"
    except Exception :
        pass
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if series.nunique() <=20:
        return "category"
    
    return "text"


def basic_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """Produce basic stats + semantic type per column."""
    profile: Dict[str, Any] = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "columns": {}
    }

    for col in df.columns:
        col_data = df[col]
        profile["columns"][col] = {
            "dtype": str(col_data.dtype),
            "missing_count": int(col_data.isna().sum()),
            "missing_pct": round(float(col_data.isna().mean()), 3),
            "unique_count": int(col_data.nunique(dropna=True)),
            "semantic_type": infer_semantic_type(col_data),
            # "sample_values": col_data.dropna().head(20).tolist()
        }

    return profile


# def generate_profile(dataset_id: str) -> Dict[str, Any]:
#     """Main entry: load dataset by id from the database, profile it, return structured JSON."""
#     table_name = get_table_name_for_dataset(dataset_id)
#     if not table_name:
#         raise FileNotFoundError(f"Dataset {dataset_id} not found in the database.")

#     df = read_dataframe_from_db(table_name)
    
#     profile = basic_profile(df)
#     return {
#         "dataset_id": dataset_id,
#         "profile": profile
#     }
