"""API routing for Nexa backend."""

from fastapi import APIRouter

from .routers import commands, status, voice

api_router = APIRouter()

api_router.include_router(status.router, tags=["status"])
api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])

