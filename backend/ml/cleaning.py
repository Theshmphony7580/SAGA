from typing import  Tuple, Dict, Any
import numpy as np
import os
import pandas as pd
from backend.utils.file_utils import get_dataset_path,sniff_delimiter
from backend.utils.data_utils import read_dataframe_auto


CLEANED_DIR = "backend/storage/cleaned"
os.makedirs(CLEANED_DIR, exist_ok=True)

def load_raw_dataset(dataset_id: str) -> pd.DataFrame:
    path = get_dataset_path(dataset_id)
    if not path:
        raise FileNotFoundError(f"Dataset {dataset_id} not found")
    return read_dataframe_auto(path, strict=False)

def fill_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    log = {"missing_values_filled": {}}

    for col in df.columns:
        before_nulls = df[col].isnull().sum()

        if before_nulls == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].mean())

        elif pd.api.types.is_datetime64_any_dtype_any_dtype(df[col]):
            df[col] = df[col].fillna(method = "ffill")

        else:
            try:
                df[col] = df[col].fillna(df[col].mode().iloc[0])
            except:
                df[col] = df[col].fillna("Unknown")
        
        after_nulls = df[col].isnull().sum()
        log['missing_filled'][col] = {
            "before": int(before_nulls),
            "after": int(after_nulls)
        }
    return df, log

def remove_outliers(df:pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        
    log = {"outliers_removed": {}}

    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        before_count = df.shape[0]
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        after_count = df.shape[0]

        log['outliers_removed'][col] = int(before_count - after_count)

    return df, log

def save_cleaned_dataset(dataset_id: str, df: pd.DataFrame) -> str:
    cleaned_path = f"{CLEANED_DIR}/{dataset_id}.csv"
    df.to_csv(cleaned_path, index=False)
    return cleaned_path

def clean_dataset(dataset_id: str) -> Dict[str, Any]:
    df = load_raw_dataset(dataset_id)

    cleaning_log = {}

    # Fill missing values
    df, missing_log = fill_missing_values(df)
    cleaning_log.update(missing_log)

    # Remove outliers (optional behavior)
    df, outlier_log = remove_outliers(df)
    cleaning_log.update(outlier_log)

    # Save cleaned dataset
    cleaned_path = save_cleaned_dataset(dataset_id, df)

    return {
        "dataset_id": dataset_id,
        "cleaned_path": cleaned_path,
        "rows_after_cleaning": int(df.shape[0]),
        "cleaning_log": cleaning_log
    }

    #     if df[col].dtype.kind in {"i", "u", "f"}:  # numeric
    #         median_val = df[col].median()
    #         missing_before = int(df[col].isna().sum())
    #         df[col] = df[col].fillna(median_val)
    #         report["steps"].append({
    #             "column": col,
    #             "action": "fillna_median",
    #             "missing_before": missing_before,
    #             "value": None if pd.isna(median_val) else float(median_val),
    #         })
    #     else:
    #         mode_series = df[col].mode(dropna=True)
    #         mode_val = mode_series.iloc[0] if not mode_series.empty else None
    #         missing_before = int(df[col].isna().sum())
    #         if mode_val is not None:
    #             df[col] = df[col].fillna(mode_val)
    #         report["steps"].append({
    #             "column": col,
    #             "action": "fillna_mode",
    #             "missing_before": missing_before,
    #             "value": None if mode_val is None else (mode_val if isinstance(mode_val, (int, float)) else str(mode_val)),
    #         })
    # return df, report

# def check_eachshell_dtype(df):
#     type_matrix = pd.applymap(dect_NaN)
#     for col in df.columns:
#         unique_dtypes = set(type_matrix[col])
#         if 

# def clean_dataset(path: str) -> Tuple[str, Dict[str, Any]]:
#     if not os.path.exists(path):
#         raise FileNotFoundError(path)

#     df = read_dataframe_auto(path, strict=False)

#     report: Dict[str, Any] = {"steps": []}

#     # Simple baseline cleaning: fill numeric with median, object with mode
#     for col in df.columns:
#         if df[col].dtype.kind in {"i", "u", "f"}:  # numeric
#             median_val = df[col].median()
#             missing_before = int(df[col].isna().sum())
#             df[col] = df[col].fillna(median_val)
#             report["steps"].append({
#                 "column": col,
#                 "action": "fillna_median",
#                 "missing_before": missing_before,
#                 "value": None if pd.isna(median_val) else float(median_val),
#             })
#         else:
#             mode_series = df[col].mode(dropna=True)
#             mode_val = mode_series.iloc[0] if not mode_series.empty else None
#             missing_before = int(df[col].isna().sum())
#             if mode_val is not None:
#                 df[col] = df[col].fillna(mode_val)
#             report["steps"].append({
#                 "column": col,
#                 "action": "fillna_mode",
#                 "missing_before": missing_before,
#                 "value": None if mode_val is None else (mode_val if isinstance(mode_val, (int, float)) else str(mode_val)),
#             })

#     cleaned_path = _derive_output_path(path)
#     if cleaned_path.lower().endswith(".csv"):
#         df.to_csv(cleaned_path, index=False)
#     else:
#         df.to_excel(cleaned_path, index=False)

#     return cleaned_path, report


# def _derive_output_path(path: str) -> str:
#     if path.lower().endswith(".csv"):
#         return path[:-4] + ".cleaned.csv"
#     if path.lower().endswith(".xlsx"):
#         return path[:-5] + ".cleaned.xlsx"
#     raise ValueError("Unsupported file type")



