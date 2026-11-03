"""Tests for environment configuration and the LLM-enable flag.

Each test isolates ``.env`` loading by passing an empty temporary project root,
so results do not depend on a developer's local ``.env`` file.
"""

from __future__ import annotations

from pathlib import Path

from src.config import load_settings


def _settings(tmp_path: Path):
    return load_settings(project_root=tmp_path)


def test_placeholder_key_disables_llm(monkeypatch, tmp_path: Path) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_API_KEY", "sk-replace-with-your-deepseek-key")
    assert _settings(tmp_path).llm_enabled is False


def test_real_key_enables_llm(monkeypatch, tmp_path: Path) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_API_KEY", "sk-abc123")
    assert _settings(tmp_path).llm_enabled is True


def test_missing_key_disables_llm(monkeypatch, tmp_path: Path) -> None:  # noqa: ANN001
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    assert _settings(tmp_path).llm_enabled is False


def test_generation_defaults(monkeypatch, tmp_path: Path) -> None:  # noqa: ANN001
    monkeypatch.delenv("LLM_TEMPERATURE", raising=False)
    monkeypatch.delenv("LLM_MAX_TOKENS", raising=False)
    settings = _settings(tmp_path)
    assert settings.temperature == 0.3
    assert settings.max_tokens == 512


def test_deepseek_provider_defaults(monkeypatch, tmp_path: Path) -> None:  # noqa: ANN001
    monkeypatch.setenv("LLM_PROVIDER", "deepseek")
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    settings = _settings(tmp_path)
    assert settings.base_url == "https://api.deepseek.com"
    assert settings.model == "deepseek-chat"
