from typing import List, Dict
import os
from backend.utils.data_utils import read_dataframe_auto


def generate_insights(path: str) -> List[Dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    df = read_dataframe_auto(path, strict=False)
    insights: List[Dict] = []

    # Simple heuristics for baseline insights
    insights.append({
        "title": "Row and Column Count",
        "description": f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.",
        "score": 0.5,
    })

    numeric_cols = [c for c in df.columns if df[c].dtype.kind in {"i", "u", "f"}]
    if numeric_cols:
        col = numeric_cols[0]
        mean_val = df[col].dropna().mean()
        insights.append({
            "title": f"Mean of {col}",
            "description": f"Average value of {col} is {mean_val:.3f}.",
            "score": 0.6,
        })

    return insights


