"""Command processing endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ...shared.command_processor import CommandProcessor, CommandResult, get_command_processor

router = APIRouter()


class CommandRequest(BaseModel):
    """Incoming voice/text command payload."""

    text: str = Field(..., min_length=1, description="Recognized user command")
    locale: str | None = Field(None, description="Locale/language tag of the command")
    metadata: dict[str, str] | None = Field(
        default_factory=dict, description="Additional context (device, channel, etc.)"
    )


class CommandResponse(BaseModel):
    """Response returned to the client."""

    result: CommandResult


@router.post("/", response_model=CommandResponse)
async def process_command(
    payload: CommandRequest,
    processor: CommandProcessor = Depends(get_command_processor),
) -> CommandResponse:
    """Process a command using the shared command processor."""
    try:
        outcome = await processor.process(payload.text, locale=payload.locale, metadata=payload.metadata or {})
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - captured for logging in future work
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Command processing failed",
        ) from exc

    return CommandResponse(result=outcome)

