"""Voice pipeline endpoints and WebSocket handlers."""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/stream")
async def voice_stream(websocket: WebSocket) -> None:
    """Bidirectional channel for streaming voice events."""
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            # Echo back for now; to be replaced with real streaming logic.
            await websocket.send_text(message)
    except WebSocketDisconnect:
        # Client disconnected gracefully.
        return

