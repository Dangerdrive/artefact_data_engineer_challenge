"""Tests for the HTTP API (offline settings, no network)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.api import create_app
from src.config import Settings


def _client() -> TestClient:
    settings = Settings(
        provider="deepseek",
        model="deepseek-chat",
        api_key=None,  # force offline mode
        base_url="https://api.deepseek.com",
        log_level="INFO",
        conversation_store="memory",
    )
    return TestClient(create_app(settings=settings))


def test_health_endpoint() -> None:
    response = _client().get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["mode"] == "offline"


def test_chat_price() -> None:
    client = _client()
    response = client.post("/api/chat", json={"message": "How much is the Takamine GD20?"})
    assert response.status_code == 200
    body = response.json()
    assert "Takamine" in body["reply"]
    assert body["mode"] == "offline"


def test_chat_rejects_empty_message() -> None:
    response = _client().post("/api/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_path_agnostic_route() -> None:
    # Simulates Vercel rewriting arbitrary paths to the function.
    response = _client().post("/some/rewritten/path", json={"message": "hello", "session_id": "s1"})
    assert response.status_code == 200
    assert response.json()["session_id"] == "s1"


def test_session_history_is_per_session() -> None:
    client = _client()
    client.post("/api/chat", json={"message": "How much is the Takamine GD20?", "session_id": "a"})
    response = client.post("/api/chat", json={"message": "Do you have it in stock?", "session_id": "a"})
    assert "Takamine" in response.json()["reply"]
