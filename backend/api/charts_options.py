# from fastapi import APIRouter, HTTPException
# from backend.ml.chart_rules import recommend_chart_types
# from fastapi import APIRouter, HTTPException
# import plotly.express as px
# from backend.database.utils import (
#     get_table_name_for_dataset,
#     find_cleaned_dataset_id,
#     read_dataframe_from_db
# )

# router = APIRouter(tags=["charts"])

# @router.get("/charts/options")
# def chart_options(x_type: str, y_type: str | None = None):
#     options = recommend_chart_types(x_type, y_type)

#     if not options:
#         raise HTTPException(400, "No valid charts for this column combination")

#     return {
#         "options": options
#     }



from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database.utils import read_dataframe_from_db, get_table_name_for_dataset

router = APIRouter(tags=["charts"])

class ChartRequest(BaseModel):
    dataset_id: str
    x: str
    y: str
    chart_type: str

@router.post("/charts/plot")
def plot_chart(req: ChartRequest):
    table = get_table_name_for_dataset(req.dataset_id)
    if not table:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = read_dataframe_from_db(table)

    if req.x not in df.columns or req.y not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid columns")

    return {
        "x": df[req.x].tolist(),
        "y": df[req.y].tolist()
    }
