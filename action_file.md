# 🧠 AI Data Analyst Backend — Full Action Roadmap

This document defines **all development actions** required to evolve the current backend into a **production-grade AI-powered Data Analytics Assistant**.

---

## ⚙️ 1. Core System Setup

**Goal:** Make the backend self-contained, configurable, and deployable.

* [ ] Create `backend/config.py` with constants: `DATA_DIR`, `MAX_FILE_SIZE_MB`, `ALLOWED_EXTENSIONS`.
* [ ] Add `requirements.txt` listing dependencies (`fastapi`, `uvicorn`, `pandas`, `loguru`, etc.).
* [ ] Add `run.py` or `backend/__main__.py` to start the server via Uvicorn.
* [ ] Ensure consistent folder structure and absolute imports.

---

## 🧩 2. Logging, Monitoring, and Security

**Goal:** Transparency, observability, and safety.

* [ ] Integrate `loguru` for request and error logging.
* [ ] Add global exception handler (`app.exception_handler`).
* [ ] Enforce file size validation in `upload.py`.
* [ ] Sanitize all text inputs via `security.sanitize_text`.
* [ ] Verify MIME type and file extension before saving.
* [ ] Extend `mask_pii` for email/phone auto-masking.
* [ ] Add `/health` endpoint to report uptime and version.

---

## 🧠 3. Data Pipeline Enhancements

**Goal:** Upgrade core ML modules from placeholders to intelligent analytics.

### cleaning.py

* [ ] Add datatype inference (`datetime`, `category`, `boolean`).
* [ ] Add outlier detection using `IsolationForest`.
* [ ] Add smart imputation via KNN or regression model.
* [ ] Log detailed cleaning steps with before/after metrics.

### profiling.py

* [ ] Compute mean, std, skewness, kurtosis for numeric columns.
* [ ] Detect columns with high missing values.
* [ ] Add frequent value sampling.
* [ ] Auto-detect datetime and categorical columns.

### insights_engine.py

* [ ] Add correlation-based insights.
* [ ] Identify top 3 numeric trends or anomalies.
* [ ] Rank insights by significance or confidence.
* [ ] Expand output schema for visualization.

### nlq_engine.py

* [ ] Integrate GPT or Gemini 2.5 Pro for real Pandas code generation.
* [ ] Sandbox code execution to prevent injection.
* [ ] Generate chart recommendations with output JSON.
* [ ] Return user-friendly error messages.

### report_builder.py

* [ ] Use Jinja2 templates for clean HTML layout.
* [ ] Integrate Plotly charts (convert to embeddable HTML).
* [ ] Offer PDF export (via WeasyPrint or ReportLab).
* [ ] Embed metadata (dataset name, version, date).

---

## 🧰 4. Utility Layer Improvements

**Goal:** Increase reliability and modularity.

* [ ] Move `DATA_DIR` to config file.
* [ ] Implement file retention policy (delete old uploads).
* [ ] Add helper to list uploaded files.
* [ ] Extend `data_utils` for auto-type parsing (`try_parse_date`, etc.).
* [ ] Normalize column names (lowercase, underscores).
* [ ] Add regex-based PII detection in `security.py`.

---

## 🧮 5. API Layer Upgrades

**Goal:** Make endpoints production-ready and developer-friendly.

* [ ] Add versioning: `/v1/` prefix to all routes.
* [ ] Add `tags` metadata for API docs organization.
* [ ] Convert Pandas-heavy operations to `async` via background threads.
* [ ] Add `/progress` WebSocket for long-running task updates.
* [ ] Add input validation for dataset schema and NLQ query length.

---

## 📦 6. Report & Artifact Management

**Goal:** Centralized output handling.

* [ ] Create `reports/` directory.
* [ ] Timestamp all report filenames.
* [ ] Add `/reports/list` and `/reports/download` endpoints.
* [ ] Add option to zip cleaned dataset + report together.

---

## 🧪 7. Testing and QA

**Goal:** Guarantee correctness and maintain reliability.

* [ ] Create `tests/` directory with `pytest`.
* [ ] Write unit tests for each module (upload, clean, profile, etc.).
* [ ] Add mock datasets for regression testing.
* [ ] Validate API response schemas.

---

## 🌐 8. Frontend Integration Prep

**Goal:** Prepare for Streamlit or Gemini-based frontend.

* [ ] Define standard API response schema (`status`, `message`, `data`).
* [ ] Add `/info` endpoint listing all features.
* [ ] Restrict CORS to whitelisted origins.
* [ ] Verify `/docs` OpenAPI renders properly.

---

## 🚀 9. Deployment & Scaling

**Goal:** Production readiness and scalability.

* [ ] Create `Dockerfile` (multi-stage build).
* [ ] Add `gunicorn` or `uvicorn` production command.
* [ ] Externalize config via `.env` variables.
* [ ] Add CI/CD workflow (GitHub Actions → test + deploy).
* [ ] Deploy to Render, Railway, or Cloud Run.

---

## 📖 10. Documentation & Developer Experience

**Goal:** Clarity for both humans and AI agents.

* [ ] Write `README.md` with setup, usage, and API examples.
* [ ] Create `CURSOR.md` for AI agent build instructions.
* [ ] Add `.env.example` and `.gitignore`.
* [ ] Include architectural diagram or flowchart.

---

### 🧩 Priority Map

| Priority | Focus Area            | Description                    |
| -------- | --------------------- | ------------------------------ |
| 🥇       | Config + Logging      | Foundation for reliability     |
| 🥈       | Cleaning + Profiling  | Core analytical logic          |
| 🥉       | NLQ Engine            | AI code generation & reasoning |
| 🏅       | Report Builder        | User-facing data products      |
| 🔒       | Security + Validation | Data safety and integrity      |
| 🚀       | CI/CD + Testing       | Deployment and scalability     |

---

**End of Roadmap**

> This roadmap defines the end-to-end transformation of your backend into a complete, intelligent, production-grade analytics engine.
