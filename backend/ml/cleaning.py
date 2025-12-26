from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd


def fill_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    log = {"missing_values_filled": {}}
    df_cleaned = df.copy()

    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
            fill_value = df_cleaned[col].mean()
            df_cleaned[col] = df_cleaned[col].fillna(fill_value)

        elif pd.api.types.is_datetime64_any_dtype(df_cleaned[col]):
            df_cleaned[col] = df_cleaned[col].fillna(method="ffill").fillna(method="bfill")

        else:
            try:
                fill_value = df_cleaned[col].mode().iloc[0]
                df_cleaned[col] = df_cleaned[col].fillna(fill_value)
            except IndexError:
                df_cleaned[col] = df_cleaned[col].fillna("Unknown")

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
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        before = len(df_cleaned)
        df_cleaned = df_cleaned[(df_cleaned[col] >= lower) & (df_cleaned[col] <= upper)]
        after = len(df_cleaned)

        if before > after:
            log["outliers_removed"][col] = before - after

    return df_cleaned, log


def clean_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    PURE ML ENTRY POINT
    """
    df_cleaned, missing_log = fill_missing_values(df)
    df_cleaned, outlier_log = remove_outliers(df_cleaned)

    return df_cleaned, {
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        **missing_log,
        **outlier_log
    }
