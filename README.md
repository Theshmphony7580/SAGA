# AI-Powered Data Analytics Assistant (Local)

This project is a local AI data analyst built with FastAPI (backend) and Streamlit (frontend). It loads CSV/XLSX files, profiles/cleans them, generates insights, runs simple NLQ, and exports basic reports.

## Folder Structure

```
/backend
  /api
    upload.py
    profile.py
    clean.py
    insights.py
    nlq.py
    report.py
  /ml
    profiling.py
    cleaning.py
    insights_engine.py
    nlq_engine.py
    report_builder.py
  /utils
    file_utils.py
    data_utils.py
    security.py
  main.py
/frontend
  app.py
/models
  model_registry.json
  trained/
requirements.txt
```

## Quickstart

1. Install dependencies

```
pip install -r requirements.txt
```

2. Run backend

```
uvicorn backend.main:app --reload
```

3. Run frontend (in a new terminal)

```
streamlit run frontend/app.py
```

4. Open Streamlit at http://localhost:8501

## Notes

- Upload accepts .csv and .xlsx.
- Cleaning currently applies simple median/mode fills as a baseline.
- NLQ uses a placeholder that returns a sample Pandas snippet (no external LLM calls yet).
- Report export writes an HTML file (pdf placeholder) or Excel workbook.
- Data files are stored in the `data/` directory created automatically on first upload.

## Environment

- Optional `.env` values:
  - `BACKEND_URL` (default: `http://127.0.0.1:8000`)
  - `GEMINI_API_KEY` (not used by stubs)

## License

Local development use. Replace models and NLQ with your own integrations as needed.


