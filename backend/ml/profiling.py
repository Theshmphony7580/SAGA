# backend/ml/profiling.py

from typing import Dict, Any
from backend.database.utils import get_table_name_for_dataset, read_dataframe_from_db
from backend.ml.auto_profiler import generate_ml_profile

def generate_profile(dataset_id: str) -> Dict[str, Any]:
    table = get_table_name_for_dataset(dataset_id)
    if not table:
        raise FileNotFoundError(f"Dataset {dataset_id} not found")

    df = read_dataframe_from_db(table)

    ml_profile = generate_ml_profile(df)

    return {
        "dataset_id": dataset_id,
        "profile": ml_profile
    }


# def generate_profile(dataset_id: str) -> Dict[str, Any]:
#     """Main entry: load dataset by id from the database, profile it, return structured JSON."""
#     table_name = get_table_name_for_dataset(dataset_id)
#     if not table_name:
#         raise FileNotFoundError(f"Dataset {dataset_id} not found in the database.")

#     df = read_dataframe_from_db(table_name)
    
#     profile = basic_profile(df)
#     return {
#         "dataset_id": dataset_id,
#         "profile": profile
#     }
