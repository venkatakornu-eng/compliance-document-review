from fastapi import FastAPI

from app.api.pii_routes import router as pii_router
from app.core.config import settings
from app.core.logging_config import configure_logging


configure_logging()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description=(
        "AI-powered compliance document review system "
        "with privacy-preserving PII masking."
    ),
)


app.include_router(
    pii_router
)


@app.get("/")
def root():

    return {
        "application": settings.APP_NAME,
        "status": "running",
        "current_service": "AI-1 PII Security Service",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }