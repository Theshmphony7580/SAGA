from typing import Tuple, Dict, Any
import os
import pandas as pd
from backend.utils.data_utils import read_dataframe_auto


def clean_dataset(path: str) -> Tuple[str, Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    df = read_dataframe_auto(path, strict=False)

    report: Dict[str, Any] = {"steps": []}

    # Simple baseline cleaning: fill numeric with median, object with mode
    for col in df.columns:
        if df[col].dtype.kind in {"i", "u", "f"}:  # numeric
            median_val = df[col].median()
            missing_before = int(df[col].isna().sum())
            df[col] = df[col].fillna(median_val)
            report["steps"].append({
                "column": col,
                "action": "fillna_median",
                "missing_before": missing_before,
                "value": None if pd.isna(median_val) else float(median_val),
            })
        else:
            mode_series = df[col].mode(dropna=True)
            mode_val = mode_series.iloc[0] if not mode_series.empty else None
            missing_before = int(df[col].isna().sum())
            if mode_val is not None:
                df[col] = df[col].fillna(mode_val)
            report["steps"].append({
                "column": col,
                "action": "fillna_mode",
                "missing_before": missing_before,
                "value": None if mode_val is None else (mode_val if isinstance(mode_val, (int, float)) else str(mode_val)),
            })

    cleaned_path = _derive_output_path(path)
    if cleaned_path.lower().endswith(".csv"):
        df.to_csv(cleaned_path, index=False)
    else:
        df.to_excel(cleaned_path, index=False)

    return cleaned_path, report


def _derive_output_path(path: str) -> str:
    if path.lower().endswith(".csv"):
        return path[:-4] + ".cleaned.csv"
    if path.lower().endswith(".xlsx"):
        return path[:-5] + ".cleaned.xlsx"
    raise ValueError("Unsupported file type")


