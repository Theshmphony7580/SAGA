# 🧠 ML Engine

This engine powers profiling, cleaning, and insight generation.

### Modules
- `profiler.py` → semantic type detection
- `cleaner.py` → ML-based imputation and outlier removal
- `insight_engine.py` → insights and anomalies
- `chart_recommender.py` → best chart predictor

### ML Models
| Task | Model |
|------|-------|
| Column Semantics | SentenceTransformers |
| Imputation | XGBoost |
| Outlier Detection | IsolationForest |
| Chart Type | Logistic Regression |

### Rules
- Log every cleaning decision.
- Preserve `_raw` columns for lineage.
- Store results as JSON change logs.
