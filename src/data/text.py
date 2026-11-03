"""Text normalization helpers used for accent/case-insensitive matching."""

from __future__ import annotations

import re
import unicodedata


def normalize(text: str) -> str:
    """Lowercase, strip accents, and collapse non-alphanumeric runs to single spaces."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = decomposed.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", " ", ascii_text)
    return ascii_text.strip()


def tokens(text: str) -> set[str]:
    """Return the set of normalized word tokens in ``text``."""
    return set(normalize(text).split())
