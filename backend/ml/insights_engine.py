from typing import Any, List, Dict
import os
import pandas as pd
import numpy as np
from backend.utils.data_utils import read_dataframe_auto
from backend.utils.file_utils import get_dataset_path
from backend.ml.cleaning import load_raw_dataset as loade_raw


CLEANED_DIR = "backend/storage/cleaned"

def load_best_dataset(dataset_id: str) -> pd.DataFrame:
    cleaned_path = os.path.join(CLEANED_DIR, f"{dataset_id}.csv")
    if os.path.exists(cleaned_path):
        return pd.read_csv(cleaned_path)
    return loade_raw(dataset_id)

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
    path = get_dataset_path(dataset_id)
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    df = load_best_dataset(dataset_id)

    return {
        "dataset_id": dataset_id,
        "num_rows": int(df.shape[0]),
        "num_columns": int(df.shape[1]),
        "numeric_summary": numeric_summary(df),
        "correlations": corelation_analysis(df),
        "category_insights": category_insights(df),
        "extremes": extremes(df),
    }


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # Simple heuristics for baseline insights
    # insights.append({
    #     "title": "Row and Column Count",
    #     "description": f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.",
    #     "score": 0.5,
    # })

    # numeric_cols = [c for c in df.columns if df[c].dtype.kind in {"i", "u", "f"}]
    # if numeric_cols:
    #     col = numeric_cols[0]
    #     mean_val = df[col].dropna().mean()
    #     insights.append({
    #         "title": f"Mean of {col}",
    #         "description": f"Average value of {col} is {mean_val:.3f}.",
    #         "score": 0.6,
    #     })

    # return insights


