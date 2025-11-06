from typing import List, Dict, Any
import os
import pandas as pd
from backend.utils.data_utils import read_dataframe_auto


def export_report(dataset_path: str, sections: List[Dict[str, Any]], include_charts: bool, output_format: str) -> str:
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(dataset_path)

    df = read_dataframe_auto(dataset_path, strict=False)

    base = dataset_path.rsplit(".", 1)[0]
    if output_format == "xlsx":
        out_path = base + ".report.xlsx"
        with pd.ExcelWriter(out_path) as writer:
            df.head(100).to_excel(writer, sheet_name="data_preview", index=False)
        return out_path

    # default pdf: write a very simple HTML and return path (placeholder)
    out_path = base + ".report.html"
    html = [
        "<html><head><meta charset='utf-8'><title>Report</title></head><body>",
        "<h1>AI Data Analytics Report</h1>",
        f"<p>Rows: {df.shape[0]}, Columns: {df.shape[1]}</p>",
    ]
    for s in sections:
        html.append(f"<h2>{s.get('title','Section')}</h2>")
        html.append(f"<p>{s.get('content','')}</p>")
    html.append("</body></html>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    return out_path


