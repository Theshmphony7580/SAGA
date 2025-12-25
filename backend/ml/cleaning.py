from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import uuid

from backend.database.utils import (
    get_table_name_for_dataset,
    read_dataframe_from_db,
    load_dataframe_to_db,
    insert_dataset_metadata,
    get_dataset_metadata
)

def fill_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    log = {"missing_values_filled": {}}
    df_cleaned = df.copy()

    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
            fill_value = df_cleaned[col].mean()
            df_cleaned[col].fillna(fill_value, inplace=True)
        elif pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
            df_cleaned[col].fillna(method="ffill", inplace=True)
            df_cleaned[col].fillna(method="bfill", inplace=True) # Handle cases where first value is null
        else:
            try:
                fill_value = df_cleaned[col].mode().iloc[0]
                df_cleaned[col].fillna(fill_value, inplace=True)
            except IndexError:
                 df_cleaned[col].fillna("Unknown", inplace=True)

        log["missing_values_filled"][col] = {
            "filled_values": int(df[col].isnull().sum() - df_cleaned[col].isnull().sum())
        }

    return df_cleaned, log

def remove_outliers(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    log = {"outliers_removed": {}}
    df_cleaned = df.copy()

    for col in df_cleaned.select_dtypes(include=np.number).columns:
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        before_count = len(df_cleaned)
        df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
        after_count = len(df_cleaned)
        
        if before_count > after_count:
            log["outliers_removed"][col] = int(before_count - after_count)
            
    return df_cleaned, log

def clean_dataset(dataset_id: str) -> Dict[str, Any]:
    """
    Loads a dataset from the database, cleans it, and saves it as a new version.
    """
    # Load original dataset
    original_metadata = get_dataset_metadata(dataset_id)
    if not original_metadata:
        raise FileNotFoundError(f"Dataset {dataset_id} not found.")
    
    table_name = original_metadata['table_name']
    df = read_dataframe_from_db(table_name)
    
    cleaning_log = {}

    # Perform cleaning
    df_cleaned, missing_log = fill_missing_values(df)
    cleaning_log.update(missing_log)
    
    df_cleaned, outlier_log = remove_outliers(df_cleaned)
    cleaning_log.update(outlier_log)

    # Generate new ID and save cleaned data
    cleaned_dataset_id = str(uuid.uuid4())
    cleaned_table_name = f"dataset_{cleaned_dataset_id.replace('-', '_')}"
    
    load_dataframe_to_db(df_cleaned, cleaned_table_name)

    # Create metadata for the new cleaned dataset
    insert_dataset_metadata(
        dataset_id=cleaned_dataset_id,
        filename=f"cleaned_{original_metadata['filename']}",
        table_name=cleaned_table_name,
        is_cleaned=True,
        source_dataset_id=dataset_id
    )

    return {
        "original_dataset_id": dataset_id,
        "cleaned_dataset_id": cleaned_dataset_id,
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        "cleaning_log": cleaning_log
    }
