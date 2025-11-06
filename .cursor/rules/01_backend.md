# ⚙️ Backend Layer (FastAPI)

The backend handles routing, authentication, and communication between UI, ML, and storage layers.

## Folder Structure
```
app/
 ├── main.py
 ├── config.py
 ├── routers/
 ├── services/
 ├── db/
 └── storage/
```

### Key Rules
- Use `/services/` for all logic (no logic in routes).
- Log all API requests.
- Ensure idempotent data operations.
- Use FastAPI exceptions with clear messages.
