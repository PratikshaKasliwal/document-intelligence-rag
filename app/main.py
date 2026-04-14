from fastapi import FastAPI
from app.core.config import settings
from app.models.schemas import HealthResponse
from app.api import ingest, query
import uvicorn

app = FastAPI(
    title=settings.APP_NAME,
    description="RAG-based document ingestion and retrieval service",
    version="1.0.0"
)

# Health check
@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", env=settings.ENV)

# Register API routers
app.include_router(ingest.router)
app.include_router(query.router)


# uvicorn app.main:app --reload  python -m app.main  uvicorn app.main:app --reload --port 8080