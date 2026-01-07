def recommend_chart_types(x_type: str, y_type: str | None):
    if y_type is None:
        if x_type == "numeric":
            return ["histogram", "box"]
        if x_type == "categorical":
            return ["bar", "pie"]

    if x_type == "numeric" and y_type == "numeric":
        return ["scatter", "line"]

    if x_type == "categorical" and y_type == "numeric":
        return ["bar", "box"]

    if x_type == "datetime" and y_type == "numeric":
        return ["line"]

    return []
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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