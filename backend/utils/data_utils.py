from typing import Optional, Tuple, List
import pandas as pd
import os
import csv
import chardet
from pandas.errors import ParserError
from backend.utils.file_utils import sniff_delimiter


class CSVValidationError(Exception):
    """Raised when CSV validation fails with specific details."""
    pass


def detect_encoding(path: str) -> str:
    """Detect file encoding using chardet."""
    try:
        with open(path, "rb") as f:
            raw_data = f.read(10000)  # Sample first 10KB
        result = chardet.detect(raw_data)
        encoding = result.get("encoding", "utf-8")
        # Fallback to common encodings if detection is uncertain
        if result.get("confidence", 0) < 0.7:
            return "utf-8"
        return encoding.lower() if encoding else "utf-8"
    except Exception:
        return "utf-8"


def validate_csv_structure(path: str, delimiter: str, encoding: str) -> Tuple[bool, Optional[str], List[int]]:
    """
    Validate CSV structure before reading.
    Returns: (is_valid, error_message, problematic_lines)
    """
    problematic_lines = []
    try:
        with open(path, "r", encoding=encoding, newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader, None)
            if not header:
                return False, "CSV file is empty", []
            expected_fields = len(header)
            
            for line_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                if len(row) != expected_fields:
                    problematic_lines.append(line_num)
                    if len(problematic_lines) > 10:  # Limit to first 10 issues
                        break
    except UnicodeDecodeError as e:
        return False, f"Encoding error: {str(e)}. Try a different encoding.", []
    except Exception as e:
        return False, f"Validation error: {str(e)}", []
    
    if problematic_lines:
        return False, f"CSV has inconsistent column counts. Expected {expected_fields} columns. Issues at lines: {problematic_lines[:10]}", problematic_lines
    
    return True, None, []


def read_csv_robust(path: str, strict: bool = False) -> pd.DataFrame:
    """
    Robust CSV reader that handles encoding, delimiter detection, and validation.
    
    Args:
        path: Path to CSV file
        strict: If True, fail on validation errors. If False, skip bad lines.
    
    Returns:
        DataFrame
    
    Raises:
        CSVValidationError: If validation fails and strict=True
        ParserError: If pandas cannot parse the file
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    # Step 1: Detect encoding
    encoding = detect_encoding(path)
    
    # Step 2: Detect delimiter
    delimiter = sniff_delimiter(path)
    if not delimiter:
        # Try common delimiters
        for delim in [",", ";", "\t", "|"]:
            try:
                with open(path, "r", encoding=encoding, newline="") as f:
                    sample = f.read(1024)
                    if delim in sample:
                        delimiter = delim
                        break
            except Exception:
                continue
        if not delimiter:
            delimiter = ","  # Default fallback
    
    # Step 3: Validate structure
    is_valid, error_msg, bad_lines = validate_csv_structure(path, delimiter, encoding)
    
    if not is_valid and strict:
        raise CSVValidationError(error_msg)
    
    # Step 4: Read with appropriate settings
    read_kwargs = {
        "sep": delimiter,
        "encoding": encoding,
        "engine": "python",  # More forgiving than C engine
        "on_bad_lines": "skip" if not strict else "error",
        "quotechar": '"',
        "skipinitialspace": True,
    }
    
    # Try reading with detected settings
    try:
        df = pd.read_csv(path, **read_kwargs)
        if df.empty:
            raise ValueError("CSV file appears to be empty or could not be parsed")
        return df
    except ParserError as e:
        # Try with different quote handling
        try:
            read_kwargs["quotechar"] = "'"
            df = pd.read_csv(path, **read_kwargs)
            if df.empty:
                raise ValueError("CSV file appears to be empty or could not be parsed")
            return df
        except Exception:
            # Final attempt: let pandas auto-detect everything
            try:
                df = pd.read_csv(path, encoding=encoding, engine="python", on_bad_lines="skip")
                if df.empty:
                    raise ValueError("CSV file appears to be empty or could not be parsed")
                return df
            except Exception as final_e:
                raise ParserError(f"Failed to parse CSV after multiple attempts. Original error: {str(e)}. Final error: {str(final_e)}")


def read_dataframe_auto(path: str, strict: bool = False) -> pd.DataFrame:
    """
    Universal dataframe reader for CSV and Excel files.
    
    Args:
        path: Path to file
        strict: If True, fail on CSV validation errors
    
    Returns:
        DataFrame
    """
    if path.lower().endswith(".csv"):
        return read_csv_robust(path, strict=strict)
    if path.lower().endswith(".xlsx"):
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path}")


def try_parse_numeric(series: pd.Series) -> pd.Series:
    try:
        return pd.to_numeric(series, errors="ignore")
    except Exception:
        return series


def try_parse_date(series: pd.Series) -> pd.Series:
    """Try to parse a series as dates."""
    try:
        return pd.to_datetime(series, errors="ignore", infer_datetime_format=True)
    except Exception:
        return series




