import re 
import pandas as pd 
from backend.utils.file_utils import get_dataset_path,sniff_delimiter
from typing import Dict, Any
import os
from backend.utils.data_utils import read_dataframe_auto

def infer_sementic_type(series: pd.Series) -> str:
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
            "sample_values": col_data.dropna().head(20).tolist()
        }

    return profile



def generate_profile(dataset_id: str) -> Dict[str, Any]:
    """Main entry: load dataset by id, profile it, return structured JSON."""
    path = get_dataset_path(dataset_id)
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Dataset {dataset_id} not found at path {path}")

    # optionally adjust delimiter if CSV
    if path.lower().endswith(".csv"):
        delim = sniff_delimiter(path)
        df = pd.read_csv(path, delimiter=delim or ",")
    else:
        df = pd.read_excel(path)

    # or use read_dataframe_auto
    # df = read_dataframe_auto(path, strict=False)

    profile = basic_profile(df)
    return {
        "dataset_id": dataset_id,
        "profile": profile
    }




#def generate_profile(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    df = read_dataframe_auto(path, strict=False)

    summary: Dict[str, Any] = {
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "columns": {},
    }

    for col in df.columns:
        col_data = df[col]
        summary["columns"][col] = {
            "dtype": str(col_data.dtype),
            "missing": int(col_data.isna().sum()),
            "unique": int(col_data.nunique(dropna=True)),
            "sample": col_data.dropna().head(3).tolist(),
        }

    return summary


