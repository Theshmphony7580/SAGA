from typing import Any, Dict
import pandas as pd
import numpy as np
from backend.database.utils import resolve_best_table_name, read_dataframe_from_db
# def load_best_dataset(dataset_id: str) -> pd.DataFrame:
#     """
#     Loads the best available version of a dataset (cleaned, if available).
#     """
#     cleaned_id = find_cleaned_dataset_id(dataset_id)
#     load_id = cleaned_id if cleaned_id else dataset_id
    
#     table_name = get_table_name_for_dataset(load_id)
#     if not table_name:
#         raise FileNotFoundError(f"Dataset with ID {load_id} not found in database.")
        
#     return read_dataframe_from_db(table_name)

def numeric_summary(df: pd.DataFrame) -> Dict[str, Any]:
    summary = {}

    for col in df.select_dtypes(include=[np.number]).columns:
        series = df[col].dropna()
        if series.empty:
            continue
        
        summary[col] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "25%": float(series.quantile(0.25)),
            "75%": float(series.quantile(0.75)),
        }

    return summary


def corelation_analysis(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return {}
    
    corr = numeric_df.corr().round(3).fillna(0)
    return corr.to_dict()

def category_insights(df: pd.DataFrame) -> Dict[str, Any]:
    insights = {}

    categorical_cols = df.select_dtypes(include=["object"]).columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for cat in categorical_cols:
        if df[cat].nunique() > 25:
            continue
        
        insights[cat] = {}
        
        for num in numeric_cols:
            try:
                group = df.groupby(cat)[num].mean().round(3).dropna()
                insights[cat][num] = group.to_dict()
            except:
                continue

    return insights


def extremes(df: pd.DataFrame) -> Dict[str, Any]:
    info = {}

    for col in df.select_dtypes(include=[np.number]).columns:
        series = df[col].dropna()
        if series.empty:
            continue
        
        info[col] = {
            "top_5": series.nlargest(5).round(3).tolist(),
            "bottom_5": series.nsmallest(5).round(3).tolist(),
        }

    return info



def generate_insights(dataset_id: str) -> Dict[str, Any]:
    """
    Generates a set of analytical insights for a given dataset from the database.
    """
    table_name = resolve_best_table_name(dataset_id)
    df = read_dataframe_from_db(table_name)

    return {
        "dataset_id": dataset_id,
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "numeric_summary": numeric_summary(df),
        "correlations": corelation_analysis(df),
        "category_insights": category_insights(df),
        "extremes": extremes(df),
    }


