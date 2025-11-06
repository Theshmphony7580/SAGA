# CURSOR.md

**Project:** AI-Powered Data Analytics Assistant
**Version:** 2.0 (Cursor-Optimized)
**Author:** Mohit
**Type:** Local AI Tool
**Stack:** FastAPI + Streamlit + Gemini 2.5 Pro

---

## 🚀 Objective

Build a **personal AI data analyst** that automatically:

1. Loads & validates CSV/XLSX files
2. Profiles and cleans datasets using ML
3. Generates insights, visualizations, and reports
4. Allows natural language queries (via Gemini 2.5 Pro → Pandas/Plotly code)

Runs **locally** with all models and data stored on the user’s machine.

---

## 🧩 System Overview

**Architecture:**
`Frontend (Streamlit)` → `Backend (FastAPI)` → `ML Layer` → `Gemini 2.5 Pro Engine` → `Report Generator`

**Flow:**

1. Upload → 2. Profiling → 3. Cleaning → 4. Insights → 5. Query → 6. Visualization → 7. Report

---

## ⚙️ Core Features

| Module        | Description                                              |
| ------------- | -------------------------------------------------------- |
| File Upload   | Accept CSV/XLSX, validate schema                         |
| Profiling     | ML-based semantic column typing                          |
| Cleaning      | Predict best imputation + outlier handling               |
| Insights      | Auto-detect trends, correlations                         |
| NLQ           | Gemini 2.5 converts text → executable Pandas/Plotly code |
| Visualization | Render charts dynamically in Streamlit                   |
| Reporting     | Export as PDF/Excel via WeasyPrint & Jinja2              |

---

## 🧠 Models & AI Components

| Component           | Model                            | Purpose                        |
| ------------------- | -------------------------------- | ------------------------------ |
| Column Semantics    | SentenceTransformer (MiniLM)     | Infer meaning of columns       |
| Imputation Selector | LightGBM                         | Predict missing-value strategy |
| Outlier Detector    | Isolation Forest / One-Class SVM | Detect anomalies               |
| Insight Engine      | Meta-learning Recommender        | Suggest patterns & visuals     |
| LLM Query Engine    | Gemini 2.5 Pro                   | NLQ → Executable Python        |
| Chart Selector      | ML Classifier                    | Recommend visualization type   |

---

## 🛠️ Tech Stack

**Backend:** FastAPI, scikit-learn, LightGBM, XGBoost, SentenceTransformers
**Frontend:** Streamlit
**Visualization:** Plotly, Matplotlib
**Storage:** SQLite, local filesystem
**Reporting:** WeasyPrint, Jinja2
**LLM:** Gemini 2.5 Pro

---

## 📦 Folder Structure (AI Agent: follow strictly)

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
    chart_recommender.py
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
.env
requirements.txt
README.md
CURSOR.md
```

---

## 🧰 API Design

| Endpoint         | Method | Description                           |
| ---------------- | ------ | ------------------------------------- |
| `/upload`        | POST   | Upload and validate dataset           |
| `/profile`       | POST   | ML-based profiling                    |
| `/clean`         | POST   | Run ML imputation & outlier detection |
| `/insights/auto` | POST   | Auto-generate insights                |
| `/nlq/run`       | POST   | Process NLQ via Gemini 2.5 Pro        |
| `/report/export` | POST   | Generate PDF/Excel report             |

---

## 🖥️ Streamlit Frontend Tasks

* Build UI for file upload + preview
* Display dataset profile summary
* Allow chat-style NLQ input
* Render Plotly charts dynamically
* Show insight cards
* Add “Export Report” button

---

## 🔒 Security

* Local sandbox execution
* Mask PII (emails, phones, addresses)
* No external calls unless user opts in
* Basic input sanitization

---

## 📊 Performance Targets

| Metric             | Target |
| ------------------ | ------ |
| Profiling accuracy | ≥ 90%  |
| Cleaning accuracy  | ≥ 85%  |
| Query success rate | ≥ 90%  |
| Insight latency    | < 15s  |
| Report generation  | < 10s  |

---

## 🧱 Development Instructions (for AI Agent)

* Implement one API per file.
* Reuse ML utilities from `/ml/`.
* Document all endpoints with Pydantic schemas.
* Use Gemini API calls for NLQ.
* Maintain stateless backend.
* Store temp data in `/data/` or `/tmp/`.
* Connect Streamlit UI → FastAPI endpoints using `requests`.

---

## 🧭 Run Locally

```
pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run frontend/app.py
```

Open: `http://localhost:8501`

---

## 🧩 Future Roadmap

* Voice Query Interface
* AutoML Predictive Modeling
* Custom Gemini Fine-tuning
* SaaS Expansion (multi-user)
* Cloud Connectors (Google Sheets, SQL, BigQuery)

---

**End of CURSOR.md**
