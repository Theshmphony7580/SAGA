from typing import Dict, Any
import os
from backend.utils.data_utils import read_dataframe_auto


def generate_profile(path: str) -> Dict[str, Any]:
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


