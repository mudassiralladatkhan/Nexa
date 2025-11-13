"""Status endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def service_status() -> dict[str, str]:
    """Return overall service status."""
    return {"service": "nexa-backend", "state": "online"}

