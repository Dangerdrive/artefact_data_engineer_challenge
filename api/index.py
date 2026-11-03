"""Vercel serverless entrypoint.

Vercel's Python runtime serves the ASGI ``app`` exported here. We make sure the
repository root is importable so ``from src...`` works inside the function bundle.
"""

import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.api import app  # noqa: E402,F401
