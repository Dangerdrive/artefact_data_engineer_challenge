"""HTTP API for the Empório da Música agent (ASGI, Vercel-ready).

Reuses the same :class:`Agent` as the CLI. Routes are path-tolerant so they keep
working behind Vercel rewrites (with or without the ``/api`` prefix).

Endpoints:
    GET  /            -> health
    GET  /health      -> health
    GET  /api/health  -> health
    POST /chat        -> chat
    POST /api/chat    -> chat
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import Agent
from .config import Settings, load_settings


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Customer message.")
    session_id: str | None = Field(
        default=None, description="Optional conversation id (best-effort in-memory history)."
    )


class ChatResponse(BaseModel):
    reply: str
    mode: str
    session_id: str | None = None


def create_app(settings: Settings | None = None, data_dir: str | None = None) -> FastAPI:
    """Build the FastAPI app.

    Passing ``settings`` (e.g. with ``api_key=None``) enables fully offline tests
    without touching the network.
    """
    app = FastAPI(title="Empório da Música Agent", version="0.1.0")
    resolved_settings = settings or load_settings()
    agents: dict[str, Agent] = {}

    def get_agent(session_id: str) -> Agent:
        agent = agents.get(session_id)
        if agent is None:
            agent = Agent(settings=resolved_settings, data_dir=data_dir)
            agents[session_id] = agent
        return agent

    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "mode": "llm" if resolved_settings.llm_enabled else "offline",
            "model": resolved_settings.model,
        }

    def handle_chat(request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or "default"
        agent = get_agent(session_id)
        reply = agent.chat(request.message)
        return ChatResponse(reply=reply, mode=agent.mode, session_id=session_id)

    app.get("/")(health)
    app.get("/health")(health)
    app.get("/api/health")(health)

    app.post("/chat", response_model=ChatResponse)(handle_chat)
    app.post("/api/chat", response_model=ChatResponse)(handle_chat)

    # Catch-all so the API works even if Vercel rewrites the path to /api/index.
    @app.post("/{full_path:path}", response_model=ChatResponse)
    def catch_all_chat(full_path: str, request: ChatRequest) -> ChatResponse:
        return handle_chat(request)

    @app.get("/{full_path:path}")
    def catch_all_health(full_path: str) -> dict[str, Any]:
        return health()

    return app


app = create_app()
