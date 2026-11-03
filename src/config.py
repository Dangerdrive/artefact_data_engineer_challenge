"""Application configuration loaded from environment variables.

Keeps all settings (model provider, model name, API key, logging) in one place.
A tiny ``.env`` loader is included so the project runs without ``python-dotenv``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = PROJECT_ROOT / "Desafio Técnico AI Engineer 2026" / "data"

# Placeholder values that should not be treated as real credentials.
_PLACEHOLDER_KEYS = {"sk-replace-with-your-key", "sk-substitua-sua-chave", ""}


def _load_dotenv(path: Path) -> None:
    """Load key=value pairs from a .env file into os.environ (non-destructive)."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    """Resolved application settings."""

    provider: str
    model: str
    api_key: str | None
    base_url: str | None
    log_level: str
    conversation_store: str
    temperature: float = 0.3
    max_tokens: int = 512

    @property
    def llm_enabled(self) -> bool:
        """True when a usable API key is configured (enables the LLM mode)."""
        return bool(self.api_key) and self.api_key not in _PLACEHOLDER_KEYS


def load_settings(project_root: Path | None = None) -> Settings:
    """Build :class:`Settings` from the environment (loading ``.env`` if present)."""
    root = project_root or PROJECT_ROOT
    _load_dotenv(root / ".env")

    api_key = os.getenv("LLM_API_KEY")
    if api_key is not None:
        api_key = api_key.strip()

    return Settings(
        provider=os.getenv("LLM_PROVIDER", "openai"),
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=api_key or None,
        base_url=(os.getenv("LLM_BASE_URL") or None),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        conversation_store=os.getenv("CONVERSATION_STORE", "memory"),
        temperature=_env_float("LLM_TEMPERATURE", 0.3),
        max_tokens=_env_int("LLM_MAX_TOKENS", 512),
    )


def resolve_data_dir(data_dir: str | Path | None = None) -> Path:
    """Return the data directory (explicit argument, else env override, else default)."""
    if data_dir is not None:
        return Path(data_dir)
    env_dir = os.getenv("DATA_DIR")
    if env_dir:
        return Path(env_dir)
    return DEFAULT_DATA_DIR
