"""Tests for the LLM (function calling) mode using a fake OpenAI-compatible client.

This validates the tool-calling loop and the DeepSeek configuration without
network access or a real API key.
"""

from __future__ import annotations

import sys
import types

from src.agent import Agent
from src.config import Settings

_CREATED: list[dict] = []
_RESPONSES: list = []


class _FakeFunction:
    def __init__(self, name: str, arguments: str) -> None:
        self.name = name
        self.arguments = arguments


class _FakeToolCall:
    def __init__(self, call_id: str, name: str, arguments: str) -> None:
        self.id = call_id
        self.function = _FakeFunction(name, arguments)


class _FakeMessage:
    def __init__(self, content: str | None = None, tool_calls=None) -> None:  # noqa: ANN001
        self.content = content
        self.tool_calls = tool_calls


class _FakeResponse:
    def __init__(self, message: _FakeMessage) -> None:
        self.choices = [types.SimpleNamespace(message=message)]


class _FakeCompletions:
    def create(self, **kwargs):  # noqa: ANN003, ANN201
        _CREATED.append(kwargs)
        return _RESPONSES.pop(0)


class _FakeOpenAI:
    last_kwargs: dict = {}

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        _FakeOpenAI.last_kwargs = kwargs
        self.chat = types.SimpleNamespace(completions=_FakeCompletions())


def _install_fake_openai(monkeypatch, responses: list) -> None:  # noqa: ANN001
    global _RESPONSES
    _RESPONSES = responses
    module = types.ModuleType("openai")
    module.OpenAI = _FakeOpenAI
    monkeypatch.setitem(sys.modules, "openai", module)


def test_llm_function_calling_loop_with_deepseek(monkeypatch) -> None:  # noqa: ANN001
    _CREATED.clear()
    tool_call = _FakeToolCall("call_1", "get_product", '{"name": "Takamine GD20"}')
    responses = [
        _FakeResponse(_FakeMessage(content=None, tool_calls=[tool_call])),
        _FakeResponse(_FakeMessage(content="The Takamine GD20 is R$ 2,199.00.", tool_calls=None)),
    ]
    _install_fake_openai(monkeypatch, responses)

    settings = Settings(
        provider="deepseek",
        model="deepseek-chat",
        api_key="sk-test-key",
        base_url="https://api.deepseek.com",
        log_level="INFO",
        conversation_store="memory",
    )
    agent = Agent(settings=settings)
    try:
        reply = agent.chat("How much is the Takamine GD20?")
        history_len = len(agent.history)
    finally:
        agent.close()

    assert "2,199" in reply
    assert history_len == 2  # user + assistant (tool messages are not persisted)

    # The client was created pointing at the DeepSeek endpoint.
    assert _FakeOpenAI.last_kwargs["base_url"] == "https://api.deepseek.com"

    # Two model calls: one to request the tool, one to produce the final answer.
    assert len(_CREATED) == 2
    assert _CREATED[1]["model"] == "deepseek-chat"

    # The tool result was fed back to the model.
    tool_messages = [m for m in _CREATED[1]["messages"] if m["role"] == "tool"]
    assert tool_messages
    assert "Takamine" in tool_messages[0]["content"]


def test_llm_mode_falls_back_to_offline_on_error(monkeypatch) -> None:  # noqa: ANN001
    module = types.ModuleType("openai")

    class _BrokenOpenAI:
        def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
            raise RuntimeError("provider unavailable")

    module.OpenAI = _BrokenOpenAI
    monkeypatch.setitem(sys.modules, "openai", module)

    settings = Settings(
        provider="deepseek",
        model="deepseek-chat",
        api_key="sk-test-key",
        base_url="https://api.deepseek.com",
        log_level="INFO",
        conversation_store="memory",
    )
    agent = Agent(settings=settings)
    try:
        reply = agent.chat("How much is the Takamine GD20?")
    finally:
        agent.close()

    # Fell back to the deterministic offline responder.
    assert "Takamine" in reply
