# SAGA (Semantic & Autonomous Generative Analytics)

A production-ready, AI-driven data analytics platform built with FastAPI (backend) and Streamlit (frontend). Upload datasets, automatically profile and clean data, generate insights, ask natural language questions, and create visualizations—all through an intuitive interface.

---

## 🌟 Features

### Core Capabilities
- **📤 Smart Upload**: Support for CSV and XLSX files with automatic validation and encoding detection
- **🔍 Intelligent Profiling**: ML-powered dataset analysis using `ydata-profiling`
- **🧹 Auto-Cleaning**: Automatic missing value imputation, outlier detection, and data normalization
- **💡 AI Insights**: Correlation analysis, statistical summaries, categorical breakdowns, and anomaly detection
- **💬 Natural Language Queries (NLQ)**: Ask questions in plain English, get SQL results instantly
- **📊 Dynamic Visualizations**: Interactive charts with automatic type recommendations
- **📝 Report Generation**: Export analysis reports in HTML or Excel format

### Technical Highlights
- **Database-First Architecture**: SQLite-backed persistence with full ACID compliance
- **Production-Ready**: Comprehensive logging, error handling, CORS security, and health checks
- **Modular Design**: Clean separation of concerns across API, ML, database, and utility layers
- **Type-Safe**: Pydantic models for request/response validation
- **Extensible**: Plugin-ready architecture for custom ML models and data sources

---

## 🏗️ Architecture

```
├── backend/
│   ├── api/              # FastAPI route handlers
│   │   ├── upload.py     # Dataset upload endpoint
│   │   ├── profile.py    # ML-powered profiling
│   │   ├── clean.py      # Data cleaning pipeline
│   │   ├── insights.py   # Statistical analysis
│   │   ├── nlq.py        # Natural language queries
│   │   ├── charts.py     # Visualization recommendations
│   │   └── report.py     # Report generation
│   ├── ml/               # Machine learning modules
│   │   ├── auto_profiler.py    # ydata-profiling integration
│   │   ├── cleaning.py         # Imputation & outlier removal
│   │   ├── insights_engine.py  # Statistical insights
│   │   ├── nlq_engine.py       # NLQ → SQL conversion
│   │   └── chart_rules.py      # Chart type logic
│   ├── database/         # SQLite utilities
│   │   ├── init_db.py    # Schema initialization
│   │   └── utils.py      # CRUD operations
│   ├── utils/            # Helper functions
│   │   ├── file_utils.py       # File I/O operations
│   │   ├── data_utils.py       # CSV parsing & validation
│   │   └── security.py         # Input sanitization
│   ├── config.py         # Configuration constants
│   └── main.py           # FastAPI application
├── frontend/
│   └── app.py            # Streamlit UI
├── data/
│   ├── db/               # SQLite database
│   └── datasets/         # Uploaded files (temporary)
├── reports/              # Generated reports
└── requirements.txt
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-data-analytics-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python -m backend.database.init_db
   ```

### Running Locally

**Option 1: Separate terminals**

Terminal 1 (Backend):
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
streamlit run frontend/app.py
```

**Option 2: Using the entry point**
```bash
python -m backend  # Starts backend on port 8000
streamlit run frontend/app.py  # In another terminal
```

**Access the application:**
- Frontend: http://localhost:8501
- Backend API Docs: http://localhost:8000/docs

---

## 📖 Usage Guide

### 1. Upload Dataset
- Click "Upload CSV or XLSX"
- Select your file (max 200 MB)
- Click "Upload" to process

### 2. Profile Your Data
- Click "Generate Profile"
- View summary statistics, column types, missing values, and correlations

### 3. Clean Data
- Click "Run Cleaning"
- Automatically handles:
  - Missing values (mean/mode imputation)
  - Outliers (IQR-based removal)
  - Data type inference

### 4. Generate Insights
- Click "Generate Insights"
- Explore:
  - Numeric summaries (mean, median, std, min, max, quartiles)
  - Correlation matrices
  - Category-wise breakdowns
  - Top/bottom extreme values

### 5. Ask Questions (NLQ)
Supported queries:
- "Show first 10 rows"
- "What are the columns?"
- "Display last 5 rows"
- More patterns in `backend/ml/nlq_engine.py`

### 6. Create Charts
- Select X and Y axes
- Choose chart type (line, bar, scatter)
- Click "Generate Chart"

### 7. Export Reports
- Select sections to include
- Choose format (HTML or Excel)
- Download from `reports/` directory

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```bash
BACKEND_URL=http://127.0.0.1:8000  # For frontend connection
MAX_FILE_SIZE_MB=200
```

### Backend Config (`backend/config.py`)
```python
MAX_FILE_SIZE_MB = 200
ALLOWED_EXTENSIONS = [".csv", ".xlsx"]
ALLOWED_ORIGINS = ["http://localhost:8501"]
```

---

## 🧪 API Reference

### Base URL: `/v1/api`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload CSV/XLSX file |
| `/profile` | GET | Generate data profile |
| `/clean/{dataset_id}` | POST | Clean dataset |
| `/insights/{dataset_id}` | POST | Generate insights |
| `/nlq/run` | POST | Execute NLQ query |
| `/columns` | GET | List dataset columns |
| `/charts/plot` | POST | Generate chart data |
| `/report/export` | POST | Export analysis report |
| `/datasets/{dataset_id}` | GET | Fetch dataset metadata |
| `/datasets/{dataset_id}` | DELETE | Delete dataset |
| `/health` | GET | Health check |

**Example Request (cURL):**
```bash
# Upload file
curl -X POST "http://localhost:8000/v1/api/upload" \
  -F "file=@data.csv"

# Run NLQ
curl -X POST "http://localhost:8000/v1/api/nlq/run" \
  -H "Content-Type: application/json" \
  -d '{"dataset_id": "abc-123", "question": "show first 5 rows"}'
```

---

## 🛠️ Development

### Running Tests
```bash
pytest tests/  # (Tests directory to be created)
```

### Code Style
```bash
black backend/ frontend/
isort backend/ frontend/
```

### Database Schema
```sql
CREATE TABLE datasets (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    table_name TEXT NOT NULL,
    is_cleaned BOOLEAN DEFAULT FALSE,
    source_dataset_id TEXT,
    FOREIGN KEY (source_dataset_id) REFERENCES datasets(id)
);
```

---

## 🚢 Deployment

### Docker (Recommended)
```dockerfile
# Dockerfile (to be created)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Platforms
- **Render**: Connect GitHub repo → Auto-deploy
- **Railway**: One-click FastAPI + SQLite deployment
- **Google Cloud Run**: Containerized deployment

---

## 📚 Tech Stack

### Backend
- **FastAPI** - High-performance API framework
- **Pandas** - Data manipulation
- **ydata-profiling** - Advanced dataset profiling
- **SQLite** - Embedded database
- **Loguru** - Production logging

### Frontend
- **Streamlit** - Interactive web interface
- **Plotly** - Interactive visualizations
- **Requests** - HTTP client

### ML/Analytics
- **NumPy** - Numerical computing
- **SciPy** - Statistical analysis
- **Scikit-learn** - Outlier detection (future: IsolationForest)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed for local development use. For production deployment, please review and add an appropriate license (MIT, Apache 2.0, etc.).

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Dataset not found"
- **Solution**: Verify `dataset_id` matches UUID format, not table name

**Issue**: CSV parsing fails
- **Solution**: Check encoding (UTF-8 recommended), ensure consistent column counts

**Issue**: Backend unreachable
- **Solution**: Confirm `BACKEND_URL` in frontend matches running backend port

**Issue**: File upload fails (413 error)
- **Solution**: File exceeds `MAX_FILE_SIZE_MB` (default 200MB)

---

## 📞 Support

- **Issues**: [GitHub Issues](your-repo-url/issues)
- **Discussions**: [GitHub Discussions](your-repo-url/discussions)
- **Email**: your-email@example.com

---