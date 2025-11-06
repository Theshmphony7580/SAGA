from typing import Tuple, Optional, Dict, Any
import os
from backend.utils.data_utils import read_dataframe_auto


def run_nlq(path: str, question: str) -> Tuple[str, Optional[str], Optional[Dict[str, Any]]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    # Placeholder: In production, call Gemini 2.5 Pro to produce code
    # For now, we return a trivial Pandas snippet
    code = (
        "# Example generated code\n"
        "import pandas as pd\n"
        f"df = pd.read_csv('{path.replace('\\\\', '/')}')\n"
        "result = df.head(5)\n"
        "result\n"
    )

    # Execute a safe preview to simulate a response summary
    df = read_dataframe_auto(path, strict=False)
    preview = df.head(5)
    result_summary = f"Preview of first 5 rows (columns: {', '.join(df.columns[:5])})"

    # No figure for the placeholder
    return code, result_summary, None


