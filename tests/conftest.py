"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from src.agent import Agent
from src.config import Settings
from src.data.policies import POLICY_PDF_NAME, PolicyIndex
from src.data.store import DataStore


@pytest.fixture(scope="session")
def store() -> DataStore:
    data_store = DataStore()
    yield data_store
    data_store.close()


@pytest.fixture(scope="session")
def policies(store: DataStore) -> PolicyIndex:
    return PolicyIndex(store.data_dir / POLICY_PDF_NAME)


@pytest.fixture()
def agent() -> Agent:
    settings = Settings(
        provider="openai",
        model="gpt-4o-mini",
        api_key=None,  # force deterministic offline mode in tests
        base_url=None,
        log_level="INFO",
        conversation_store="memory",
    )
    test_agent = Agent(settings=settings)
    yield test_agent
    test_agent.close()
