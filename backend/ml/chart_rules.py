from typing import List, Dict, Any
import pandas as pd

def recommend_chart_types(profile: Dict[str, Any]) -> List[Dict[str, List[str]]]:
    """
    Recommend chart types based on the ML profile of the dataset.
    """

    charts = []
    
    numeric = profile.get("numeric_columns", [])
    categorical = profile.get("categorical_columns", [])
    high_card = profile.get("high_cardinality_columns", [])
    correlations = profile.get("correlations", {})
    
    if categorical and numeric:
        x = categorical[0]
        y = numeric[0]
        
        if x not in high_card:
            charts.append({
                "chart_type": "Bar Chart",
                "x": x,
                "y": y,
                "aggregation": "sum",
                "reason": "Categorical vs Numeric",
                "confidence": 0.85
            })
            
    if len(numeric) >= 2:
        charts.append({
            "chart_type": "histogram",
            "x": numeric[0],
            "reason": "Distribution of Numeric Variable",
            "confidence": 0.80
        })
        
    for corr in correlations:
        charts.append({
            "chart_type": "Scatter Plot",
            "x": corr["col1"],
            "y": corr["col2"],
            "reason": f"High correlation ({corr['correlation']}) between {corr['col1']} and {corr['col2']}",
            "confidence": 0.90
        })
        
    for cat in categorical:
        if cat not in high_card:
            charts.append({
                "chart_type": "pie",
                "x": cat,
                "aggregation": "count",
                "reason": "Low-cardinality categorical distribution",
                "confidence": 0.75
            })
            break
        
    if not charts and numeric:
        charts.append({
            "chart_type": "line",
            "x": "index",
            "y": numeric[0],
            "reason": "Fallback numeric trend",
            "confidence": 0.60
        })
        
    charts = pd.DataFrame(charts).to_dict(orient="records")

    return charts

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # recommendations = {
    #     "numeric": [],
    #     "categorical": [],
    #     "datetime": []
    # }

    # for col, info in variables.items():
    #     col_type = info.get("type", "").lower()

    #     if col_type == "numeric":
    #         recommendations["numeric"].extend([
    #             "Histogram",
    #             "Box Plot",
    #             "Scatter Plot"
    #         ])
    #     elif col_type in ("categorical", "boolean"):
    #         recommendations["categorical"].extend([
    #             "Bar Chart",
    #             "Pie Chart"
    #         ])
    #     elif col_type == "datetime":
    #         recommendations["datetime"].extend([
    #             "Time Series Line Chart",
    #             "Area Chart"
    #         ])
    # return recommendations