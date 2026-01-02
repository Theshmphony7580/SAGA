from fastapi import APIRouter, HTTPException
from backend.database.utils import read_dataframe_from_db, get_table_name_for_dataset
from backend.ml.auto_profiler import generate_ml_profile

from backend.ml.chart_rules import recommend_chart_types

router = APIRouter(tags=["charts"])

@router.get("/charts")
def recommend_charts_api(dataset_id: str):
    """
    Recommends chart types based on the dataset's profile.
    """
    try:
        table_name = get_table_name_for_dataset(dataset_id)
        
        df = read_dataframe_from_db(table_name)
        
        profile = generate_ml_profile(df)
        
        charts = recommend_chart_types(profile)
        
        return {
            "dataset_id": dataset_id,
            "num_charts": len(charts),
            "charts": charts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))