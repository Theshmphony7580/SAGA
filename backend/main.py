from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time
from backend.api import charts, columns, columns
from backend.config import APP_NAME, APP_VERSION, ALLOWED_ORIGINS
from backend.database.init_db import init_database

# from frontend import app


def create_app() -> FastAPI:
    init_database()

    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        logger.info(f"{request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as exc:  # Let global handler process
            logger.exception("Unhandled error")
            raise exc
        finally:
            duration_ms = int((time.time() - start) * 1000)
            logger.info(f"Completed in {duration_ms} ms")
        return response

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Global exception")
        return JSONResponse(status_code=500, content={"status": "error", "message": "Internal Server Error"})

    # Routers are imported lazily to avoid circular imports
    from backend.api import upload, profile, clean, insights, nlq, report, datasets, columns, charts_options


    # Versioned API
    api_prefix = "/v1/api"
    app.include_router(upload.router, prefix=api_prefix)
    app.include_router(profile.router, prefix=api_prefix)
    app.include_router(clean.router, prefix=api_prefix)
    app.include_router(insights.router, prefix=api_prefix)
    app.include_router(nlq.router, prefix=api_prefix)
    app.include_router(report.router, prefix=api_prefix)
    app.include_router(datasets.router, prefix=api_prefix)
    app.include_router(columns.router, prefix=api_prefix)
    app.include_router(charts_options.router, prefix=api_prefix)

    @app.get("/health")
    async def health():
        return {"status": "ok", "version": APP_VERSION}

    return app


app = create_app()



