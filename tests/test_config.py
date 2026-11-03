"""Tests for environment configuration and the LLM-enable flag."""

from __future__ import annotations

from src.config import load_settings


def test_placeholder_key_disables_llm(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_API_KEY", "sk-replace-with-your-key")
    settings = load_settings()
    assert settings.llm_enabled is False


def test_real_key_enables_llm(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_API_KEY", "sk-abc123")
    settings = load_settings()
    assert settings.llm_enabled is True


def test_missing_key_disables_llm(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    settings = load_settings()
    assert settings.llm_enabled is False


def test_generation_defaults(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.delenv("LLM_TEMPERATURE", raising=False)
    monkeypatch.delenv("LLM_MAX_TOKENS", raising=False)
    settings = load_settings()
    assert settings.temperature == 0.3
    assert settings.max_tokens == 512


def test_deepseek_provider_defaults(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_PROVIDER", "deepseek")
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    settings = load_settings()
    assert settings.base_url == "https://api.deepseek.com"
    assert settings.model == "deepseek-chat"
