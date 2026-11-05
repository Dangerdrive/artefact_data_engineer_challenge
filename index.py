"""Vercel entrypoint for the Empório da Música FastAPI app.

Vercel detects FastAPI from ``requirements.txt`` and serves the top-level ``app``
exported by this module. The application itself lives in ``src/api.py``.
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from src.api import app  # noqa: E402,F401
