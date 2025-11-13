"""Shared command processing logic for Nexa."""

from __future__ import annotations

from typing import Awaitable, Callable, Dict, Optional

from pydantic import BaseModel, Field


class CommandResult(BaseModel):
    """Structured result returned after processing a command."""

    message: str = Field(..., description="Spoken response to return to the user")
    intent: str = Field(..., description="Resolved intent identifier")
    data: dict[str, str] = Field(default_factory=dict, description="Structured payload")


class CommandProcessor:
    """Central command processor ported from VocalPA."""

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[str], Awaitable[CommandResult]]] = {}
        self._fallthrough: Optional[Callable[[str], Awaitable[CommandResult]]] = None

    def register_handler(
        self,
        intent: str,
        handler: Callable[[str], Awaitable[CommandResult]],
    ) -> None:
        """Register an async handler for an intent."""
        self._handlers[intent.lower()] = handler

    def register_fallthrough(
        self,
        handler: Callable[[str], Awaitable[CommandResult]],
    ) -> None:
        """Register a fallback handler for unmatched commands."""
        self._fallthrough = handler

    async def process(
        self,
        text: str,
        *,
        locale: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> CommandResult:
        """Process text and return a CommandResult."""
        normalized = text.strip().lower()
        metadata = metadata or {}

        # TODO: implement robust NLP/intent detection ported from Kotlin.
        if "time" in normalized:
            handler = self._handlers.get("time")
            if handler:
                return await handler(normalized)

        if self._fallthrough:
            return await self._fallthrough(normalized)

        raise NotImplementedError("Command handling not yet implemented")


async def default_fallthrough(command: str) -> CommandResult:
    """Placeholder fallback handler."""
    return CommandResult(
        message=f"I heard: {command}. This feature is still being developed for Nexa.",
        intent="fallback",
    )


def get_command_processor() -> CommandProcessor:
    """Provide a configured command processor instance."""
    processor = CommandProcessor()
    processor.register_fallthrough(default_fallthrough)
    return processor

