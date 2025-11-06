# 🧠 AI-Powered Data Analytics Assistant (Unified PRD v2.0)

**Author:** Mohit
**Version:** 2.0 (Cursor-Optimized)
**Build Target:** FastAPI + Streamlit (Local AI Tool)
**Core AI Engine:** Gemini 2.5 Pro

---

## 1️⃣ Vision

Create an **autonomous AI data analyst** that can **load, clean, analyze, and visualize any dataset** intelligently — with zero manual coding.

This system acts as a personal assistant for data analytics: you upload a CSV or Excel file, and it does everything — profiling, cleaning, analyzing, generating insights, and creating visual dashboards — powered by ML and natural language interaction.

---

## 2️⃣ Mission

Automate **90% of the manual data analytics workflow** using an ML-guided pipeline and conversational AI.
Turn messy data → structured insights → reports — seamlessly.

---

## 3️⃣ Core Goals

1. File Upload & Validation
2. Intelligent Data Profiling (ML-based semantic understanding)
3. ML-driven Cleaning (Missing values, Outliers, Formatting)
4. Conversational Analytics (Natural language → Code execution)
5. Autonomous Insights & Visualizations
6. Report Generation (PDF/Excel)
7. Local persistence & history (SQLite)

---

## 4️⃣ System Architecture

**Frontend:** Streamlit
**Backend:** FastAPI
**ML Layer:** scikit-learn, LightGBM, SentenceTransformers, XGBoost
**LLM Engine:** Gemini 2.5 Pro
**Storage:** SQLite (local DB), local file storage
**Visualization:** Plotly, Matplotlib
**Reporting:** WeasyPrint (PDF), Jinja2 (HTML)

---

### 🧩 Data Flow

```
User Uploads File (.csv/.xlsx)
       ↓
Data Validation + Preview
       ↓
ML-driven Profiling (Semantic Classification)
       ↓
Automated Cleaning (Missing, Outliers, Formatting)
       ↓
Insight Generation (Correlations, Trends)
       ↓
Conversational Query (Gemini → Pandas/Plotly code)
       ↓
Interactive Visualization Dashboard
       ↓
Report Export (PDF/Excel)
```

---

## 5️⃣ API Endpoints (FastAPI)

| Endpoint         | Method | Description                                         |
| ---------------- | ------ | --------------------------------------------------- |
| `/upload`        | POST   | Uploads CSV/XLSX file and validates schema          |
| `/profile`       | POST   | Performs ML-based dataset profiling                 |
| `/clean`         | POST   | Cleans data using ML imputation & outlier detection |
| `/insights/auto` | POST   | Generates automated dataset insights                |
| `/nlq/run`       | POST   | Executes natural language queries using Gemini      |
| `/report/export` | POST   | Exports insights and visuals to PDF/Excel           |

---

## 6️⃣ ML & AI Models

| Module                     | Model                            | Purpose                                          |
| -------------------------- | -------------------------------- | ------------------------------------------------ |
| Column Type Classification | MiniLM (SentenceTransformers)    | Detects semantic meaning of each column          |
| Missing Value Strategy     | LightGBM Meta-Model              | Predicts best imputation strategy per column     |
| Outlier Detection          | Isolation Forest / One-Class SVM | Removes or marks anomalies                       |
| Insight Generator          | Meta-learning Recommender        | Suggests statistical and visual insights         |
| NLQ Engine                 | Gemini 2.5 Pro                   | Converts user questions → Pandas/Plotly code     |
| Chart Recommendation       | ML Classifier                    | Suggests best chart type based on data and query |

---

## 7️⃣ Security & Privacy

* Local sandboxed code execution
* Mask PII (email, phone, address)
* Local storage only (no external API calls unless enabled)
* Logging of actions with anonymized records

---

## 8️⃣ Performance Metrics

| Metric                  | Target |
| ----------------------- | ------ |
| Profiling accuracy      | ≥ 90%  |
| Cleaning accuracy       | ≥ 85%  |
| Query success rate      | ≥ 90%  |
| Insight generation time | < 15s  |
| Report generation time  | < 10s  |

---

## 9️⃣ Frontend (Streamlit)

### Key UI Components:

* File uploader (CSV/XLSX)
* Dataset preview table
* Profiling summary section
* Interactive visualizations (Plotly)
* Chat-like NLQ interface
* Downloadable PDF/Excel report button

### UX Flow:

1. User uploads dataset
2. Assistant performs profiling & cleaning automatically
3. User can ask questions in chat (e.g., “Show top 5 sales regions”)
4. Gemini executes and visualizes
5. User exports report

---

## 🔟 Future Extensions (Optional Modules)

| Module                  | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| Voice Query Interface   | Enable voice-based interaction                                        |
| AutoML Integration      | Train and test predictive models automatically                        |
| Fine-Tuned Gemini Model | Personal dataset-adapted LLM for domain insights                      |
| SaaS Upgrade            | Convert into multi-user web app with billing, history, and dashboards |
| Cloud Connectors        | Google Sheets, SQL DBs, BigQuery                                      |

---

## 11️⃣ Development Guidelines for AI Agents (Cursor)

* Generate modular code per endpoint — separate Python files for `upload`, `profile`, `clean`, etc.
* Maintain function docstrings and response schemas.
* All ML logic goes inside `/ml/` module; reusable helper functions in `/utils/`.
* Streamlit frontend should use `requests` to call FastAPI endpoints.
* Keep all configurations in a `.env` file (local setup).
* Implement minimal CLI logs for debugging (print-style, not production logging).
* Preserve folder structure:

```
/backend
    /api
    /ml
    /utils
    main.py
/frontend
    app.py (Streamlit)
```

---

## 12️⃣ Local Deployment Flow

1. `pip install -r requirements.txt`
2. Run backend: `uvicorn backend.main:app --reload`
3. Run frontend: `streamlit run frontend/app.py`
4. Access via `http://localhost:8501`

---

## 13️⃣ Summary

The **AI-Powered Data Analytics Assistant** is a **personal, local AI analyst** that:

* Understands and cleans any dataset intelligently
* Responds to natural language queries
* Generates insights and visualizations
* Exports professional PDF/Excel reports

Built using **FastAPI + Streamlit + Gemini 2.5 Pro**, it blends **machine learning pipelines with conversational intelligence** to automate end-to-end data analytics.

This PRD (v2.0) is optimized for **autonomous development by AI agents in Cursor** — every module is explicit, measurable, and buildable without ambiguity.
