# # backend/ml/auto_profiler.py
# import json
# from ydata_profiling import ProfileReport

# def generate_ml_profile(df):
#     report = ProfileReport(
#         df,
#         minimal=True,
#         explorative=False
#     )

#     # ✅ VERSION-SAFE METHOD
#     profile_json = report.to_json()

#     # convert JSON string → dict
#     profile_dict = json.loads(profile_json)

#     return profile_dict



# backend/ml/auto_profiler.py

# backend/ml/auto_profiler.py
import json
from typing import Dict, Any
from ydata_profiling import ProfileReport

def generate_ml_profile(df) -> Dict[str, Any]:
    """
    Generate a structured ML-friendly profile from a dataframe.
    Version-safe and API-safe.
    """

    report = ProfileReport(
        df,
        minimal=True,
        explorative=False,
        progress_bar=False
    )

    # ✅ ALWAYS serialize first
    profile_dict = json.loads(report.to_json())

    variables = profile_dict.get("variables", {})

    numeric_cols = []
    categorical_cols = []
    missing_summary = {}
    high_cardinality = []

    for col, info in variables.items():
        col_type = info.get("type", "").lower()

        if col_type == "numeric":
            numeric_cols.append(col)
        elif col_type in ("categorical", "boolean"):
            categorical_cols.append(col)

        if info.get("p_missing", 0) > 0:
            missing_summary[col] = round(info["p_missing"], 3)

        if info.get("n_distinct", 0) > 50:
            high_cardinality.append(col)

    correlations = []
    pearson = (
        profile_dict
        .get("correlations", {})
        .get("pearson", {})
    )

    for c1, vals in pearson.items():
        for c2, corr in vals.items():
            if c1 != c2 and abs(corr) > 0.8:
                correlations.append({
                    "col1": c1,
                    "col2": c2,
                    "correlation": round(corr, 3)
                })

    return {
        "summary": {
            "rows": profile_dict.get("table", {}).get("n", 0),
            "columns": profile_dict.get("table", {}).get("n_var", 0),
        },
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "missing_summary": missing_summary,
        "high_cardinality_columns": high_cardinality,
        "strong_correlations": correlations,
    }

    # return {
    #     "num_rows": int(data["table"]["n"]),
    #     "num_columns": int(data["table"]["n_var"]),
    #     "numeric_columns": numeric_cols,
    #     "categorical_columns": categorical_cols,
    #     "missing_summary": missing_summary,
    #     "high_cardinality_columns": high_cardinality,
    #     "strong_correlations": correlations,
    #     "warnings": data.get("warnings", [])
    # }
