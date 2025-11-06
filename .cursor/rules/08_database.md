# 🗄️ Database & Storage Layer

Stores all datasets, insights, and logs.

### Schema
| Table | Description |
|--------|-------------|
| datasets | File metadata |
| profiles | Profiling info |
| cleaned_data | Cleaned outputs |
| insights | Insights JSON |
| reports | Exported reports |

### Rules
- Never delete raw data.
- Version all outputs.
- Maintain lineage links.
