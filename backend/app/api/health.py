"""Health / readiness endpoints for My-Agent-Too."""

from fastapi import APIRouter

from app.core.config import settings
from app.models.agent import HealthResponse
from app.services.nanda_client import nanda

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Return service health including NANDA connectivity."""
    nanda_ok = False
    try:
        result = await nanda.health()
        nanda_ok = result.get("status") == "ok"
    except Exception:
        pass

    return HealthResponse(
        status="ok",
        version=settings.app_version,
        nanda_connected=nanda_ok,
    )

