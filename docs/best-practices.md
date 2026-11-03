# Best Practices Included in the Project

List of best practices adopted in this project, with what was included and why.

## 1. Git Versioning

- **What:** a Git repository with a **real, incremental** commit history.
- **Why:** it is a mandatory challenge deliverable ("do not force-push everything into a
  single commit") and lets decisions be tracked over time.
- **Status:** ✅ included (`.gitignore` + incremental commits).

## 2. Secrets Outside the Code

- **What:** API keys in environment variables via `.env` (never committed).
- **Why:** prevents credential leaks in a public repository.
- **Status:** ✅ included (`.env.example` + `.env` in `.gitignore`).

## 3. Virtual Environment and Declared Dependencies

- **What:** `requirements.txt` (or `pyproject.toml`) with explicit dependencies.
- **Why:** reproducible environment for whoever evaluates the project.
- **Status:** ✅ included (`requirements.txt`).

## 4. Centralized Configuration

- **What:** all settings (model, provider, keys, flags) read from environment variables
  with safe defaults.
- **Why:** swap provider/model without touching the code.
- **Status:** ✅ included (`.env.example` + documented configuration pattern).

## 5. Type Hints and Docstrings

- **What:** type annotations on functions and docstrings in modules.
- **Why:** readability, maintainability, and static-analysis tool support.
- **Status:** ✅ applied across `src/` (type hints + docstrings).

## 6. Lint and Formatting (ruff)

- **What:** `ruff` for lint + formatting (replaces flake8/black/isort).
- **Why:** consistent code and early problem detection.
- **Status:** ✅ configured in `pyproject.toml` (`ruff`).

## 7. Automated Tests (pytest)

- **What:** unit tests for the tools (deterministic) and orchestrator tests with a mocked
  LLM (no network/key dependency).
- **Why:** guarantee that price/stock/status are never wrong.
- **Status:** ✅ 30 tests in `tests/` (offline, no network/key needed).

## 8. Structured Logging

- **What:** per-turn logs: message, tool called, latency, tokens used.
- **Why:** debugging, auditing, and token-cost control.
- **Status:** ✅ basic logging in place (fallback warnings + configurable log level).

## 9. Cross-Editor Consistency (`.editorconfig`)

- **What:** `.editorconfig` with UTF-8, LF, consistent indentation.
- **Why:** consistency regardless of editor/OS (the project runs on WSL/Windows).
- **Status:** ✅ included.

## 10. Task Shortcuts (Makefile)

- **What:** `Makefile` with `install`, `run`, `test`, `lint`, `format`.
- **Why:** reduces friction and documents the main commands.
- **Status:** ✅ included.

## 11. Living Documentation + Maintenance Skill

- **What:** `docs/planning.md` as the source of truth + the
  `.github/skills/emporio-musica-agent` skill that enforces recording the state each session.
- **Why:** work continuity and decision traceability.
- **Status:** ✅ included.

## 12. Privacy and Compliance (LGPD)

- **What:** minimize PII in responses; use customer data only to identify orders; never
  expose more than necessary.
- **Why:** the store declares LGPD compliance and the data includes PII.
- **Status:** ✅ documented in `docs/policies.md` and `docs/data.md`.

## 13. Token-Cost Control

- **What:** economical default model, token limits, caching/avoiding unnecessary calls.
- **Why:** reduce cost and latency when using an LLM via API.
- **Status:** ✅ partial (economical default, capped tool loop, low temperature).

## 14. Error Handling and Fallback

- **What:** catch LLM API failures and return a friendly unavailability message; never
  freeze the conversation.
- **Why:** robustness of the customer service experience.
- **Status:** ✅ LLM→offline fallback and safe tool-argument error handling.

---

## Status Summary

- ✅ **Included:** Git, `.gitignore`, `.env.example`, `requirements.txt`, `.editorconfig`,
  `Makefile`, living docs, maintenance skill, type hints/docstrings, ruff config, 30 pytest
  tests, basic logging, and error handling/fallback.
- 🔜 **Future:** richer token/cost instrumentation and embedding-based retrieval with
  caching.
