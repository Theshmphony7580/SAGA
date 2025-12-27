from typing import List, Dict, Any
import os
import pandas as pd
from backend.database.utils import find_cleaned_dataset_id, get_table_name_for_dataset, read_dataframe_from_db
from backend.config import REPORTS_DIR

def export_report(dataset_id: str, sections: List[Dict[str, Any]], include_charts: bool, output_format: str) -> str:
    """
    Exports a report for a given dataset to either XLSX or HTML format.
    The data is loaded from the database, using the best available version.
    """
    df = read_dataframe_from_db(get_table_name_for_dataset(dataset_id))

    # Ensure the reports directory exists
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Define output path based on dataset ID and format
    base_filename = f"report_{dataset_id}"

    if output_format == "xlsx":
        out_path = os.path.join(REPORTS_DIR, base_filename + ".xlsx")
        with pd.ExcelWriter(out_path) as writer:
            df.head(100).to_excel(writer, sheet_name="data_preview", index=False)
        return out_path

    # Default to HTML
    out_path = os.path.join(REPORTS_DIR, base_filename + ".html")
    html = [
        "<html><head><meta charset='utf-8'><title>Report</title></head><body>",
        f"<h1>AI Data Analytics Report for {dataset_id}</h1>",
        f"<p>This report was generated for the dataset with {df.shape[0]} rows and {df.shape[1]} columns.</p>",
    ]
    for s in sections:
        html.append(f"<h2>{s.get('title', 'Section')}</h2>")
        html.append(f"<p>{s.get('content', '')}</p>")
    html.append("</body></html>")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
        
    return out_path


