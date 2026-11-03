"""Data layer: CSV loading, SQLite access, and policy retrieval."""

from .policies import PolicyIndex, extract_sections
from .store import DataStore
from .text import normalize

__all__ = ["DataStore", "PolicyIndex", "extract_sections", "normalize"]
