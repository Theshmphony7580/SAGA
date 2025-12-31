# backend/ml/auto_profiler.py

import pandas as pd
from typing import Dict, Any
from ydata_profiling import ProfileReport

def generate_ml_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a structured ML-friendly profile from a dataframe.
    """

    profile = ProfileReport(
        df,
        minimal=True,
        explorative=False,
        progress_bar=False
    )

    data = profile.get_description()

    columns = data["variables"]

    numeric_cols = []
    categorical_cols = []
    missing_summary = {}
    high_cardinality = []

    for col, info in columns.items():
        if info["type"] == "Numeric":
            numeric_cols.append(col)
        elif info["type"] in ("Categorical", "Boolean"):
            categorical_cols.append(col)

        if info.get("p_missing", 0) > 0:
            missing_summary[col] = round(info["p_missing"], 3)

        if info.get("n_distinct", 0) > 50:
            high_cardinality.append(col)

    correlations = []
    corr_matrix = data.get("correlations", {}).get("pearson", {})

    for c1, vals in corr_matrix.items():
        for c2, corr in vals.items():
            if abs(corr) > 0.8 and c1 != c2:
                correlations.append({
                    "col1": c1,
                    "col2": c2,
                    "correlation": round(corr, 3)
                })

    return {
        "num_rows": int(data["table"]["n"]),
        "num_columns": int(data["table"]["n_var"]),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "missing_summary": missing_summary,
        "high_cardinality_columns": high_cardinality,
        "strong_correlations": correlations,
        "warnings": data.get("warnings", [])
    }
