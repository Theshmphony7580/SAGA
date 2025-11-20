from typing import Tuple, Optional, Dict, Any
import os
import pandas as pd
from backend.utils.data_utils import read_dataframe_auto
from backend.utils.file_utils import get_dataset_path

CLEANED_DIR = "backend/storage/cleaned"


def load_best_dataset(dataset_id: str) -> pd.DataFrame:
    cleaned_path = os.path.join(CLEANED_DIR, f"{dataset_id}.csv")
    if os.path.exists(cleaned_path):
        return read_dataframe_auto(cleaned_path, strict=False)
    
    raw_path = get_dataset_path(dataset_id)
    return read_dataframe_auto(raw_path, strict=False)





def run_nlq(dataset_id: str, question: str) -> Tuple[str, Optional[str], Optional[Dict[str, Any]]]:
    dataset_path = get_dataset_path(dataset_id)

    if not dataset_path:
        raise FileNotFoundError(f"Dataset {dataset_id} not found: {dataset_path}")
    
    df = load_best_dataset(dataset_id)


  
    # Placeholder: In production, call Gemini 2.5 Pro to produce code
    # For now, we return a trivial Pandas snippet
    code = (
        "# Example generated code (place holder)\n"
        "import pandas as pd\n"
        f"df = pd.read_csv('{dataset_path.replace('\\\\', '/')}')\n"
        "result = df.head(5)\n"
        "result\n"
    )

    preview = df.head(5)
    result_summary = f"Preview of first 5 rows (columns: {', '.join(df.columns[:5])})"

    preview_records = preview.to_dict(orient="records")


    return code, result_summary, preview_records


















    # # Execute a safe preview to simulate a response summary
    # df = read_dataframe_auto(path, strict=False)
    # preview = df.head(5)
    # result_summary = f"Preview of first 5 rows (columns: {', '.join(df.columns[:5])})"

    # No figure for the placeholder


