"""Application factory for the Nexa FastAPI backend."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .routes import api_router

logger = logging.getLogger("nexa.backend")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifecycle manager to initialize and tear down resources."""
    settings = get_settings()
    logger.info("Starting Nexa backend | environment=%s", settings.environment)

    # TODO: initialize connections (DB, Redis, etc.)

    yield

    # TODO: gracefully close connections
    logger.info("Shutting down Nexa backend")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Return a configured FastAPI application."""
    settings = settings or get_settings()

    app = FastAPI(
        title="Nexa Voice Assistant",
        description="Python backend powering the Nexa voice assistant platform",
        version=settings.version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        """Simple health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()

