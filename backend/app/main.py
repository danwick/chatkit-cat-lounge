"""FastAPI entrypoint wiring the ChatKit server and REST endpoints."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from chatkit.server import StreamingResult
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from .server import CatAssistantServer, create_chatkit_server

app = FastAPI(title="ChatKit API")

# Serve static files in production
# Look for static dir in multiple locations
static_dir = Path(__file__).parent.parent.parent / "static"
if not static_dir.exists():
    static_dir = Path(__file__).parent.parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

_chatkit_server: CatAssistantServer | None = create_chatkit_server()


def get_chatkit_server() -> CatAssistantServer:
    if _chatkit_server is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "ChatKit dependencies are missing. Install the ChatKit Python "
                "package to enable the conversational endpoint."
            ),
        )
    return _chatkit_server


@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request, server: CatAssistantServer = Depends(get_chatkit_server)
) -> Response:
    payload = await request.body()
    result = await server.process(payload, {"request": request})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")
    return JSONResponse(result)


@app.get("/cats/{thread_id}")
async def read_cat_state(
    thread_id: str,
    server: CatAssistantServer = Depends(get_chatkit_server),
) -> dict[str, Any]:
    state = await server.cat_store.load(thread_id)
    return {"cat": state.to_payload(thread_id)}


# Serve index.html for SPA routes (must be last)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve the SPA index.html for all unmatched routes."""
    index_file = static_dir / "index.html"
    if static_dir.exists() and index_file.exists():
        return FileResponse(index_file)
    return {"message": "API is running. Frontend not available."}
