# Technical Review — Additional Findings & Justifications

> Companion to [`planning.md`](planning.md) (session log) and the final README.
> This document records the review findings that were **deliberately not changed**,
> together with the justification to defend each choice in a technical interview.

## Scope and date

- **2026-11-03** — full repository review (`docs/`, `src/`, `tests/`, `examples/`, `data/`).

## What was already fixed

1. **Order-intent false positive** (`src/agent/orchestrator.py::_try_order`): a
   purchase-phrase guard (`_is_purchase_intent`) prevents *"I want to order 2 guitars"*
   from being treated as an order-status lookup.
2. **Bilingual offline policy answers** (`src/data/policies.py::POLICY_KB_PT` +
   `Agent._is_portuguese`): offline policy replies are returned in Portuguese when the
   question is Portuguese.
3. **Documentation consistency**: removed residual "DuckDB" references and corrected the
   category names in `docs/data.md` to match the CSVs (Portuguese).
4. **Two regression tests added** (`test_purchase_intent_is_not_treated_as_order_status`,
   `test_portuguese_policy_answer`) — 42 tests total.

## Findings kept as design choices (with justification)

| # | Finding | Justification |
|---|---------|---------------|
| 1 | `CONVERSATION_STORE` is read from the environment but no persistence is implemented | Intentional evolution hook: keeping the variable documents the upgrade path without dead code. Persistence is an explicit "next step"; the orchestrator already isolates `history`, so SQLite can be plugged in later without refactoring. |
| 2 | "RAG" for policies is keyword retrieval, not embeddings | The `.env.example` and docs already call it "BM25-style keyword retrieval" as the MVP. `PolicyIndex.search()` is the swappable interface — embeddings enter there without touching the rest. "RAG" is kept as the architectural pattern (retrieve → generate). |
| 3 | Offline greeting/price/out-of-scope replies remain English-only | The challenge deliverables and example conversations are in English. The offline mode is a deterministic demo/fallback; the LLM mode serves both languages via the prompt. The policy KB — the highest-value information — was made bilingual. |
| 4 | `get_product(name=...)` returns the cheapest match when ambiguous | Deterministic and predictable tie-breaking (no randomness). Real queries use a specific model ("Takamine GD20"); for ambiguous names the next step is to ask for clarification. |
| 5 | LLM fallback is silent | Graceful degradation beats an error for the end user; the failure is recorded via logging. Surfacing a "degraded mode" indicator is future UX work, not a correction. |
| 6 | `max_tokens=512` can truncate long answers | The model summarizes; the data itself comes from tool results (JSON), not from generation. 512 balances cost/latency and is configurable via environment. |
| 7 | Tests hardcode product ids and prices (95, 94, 96…) | The challenge dataset is a fixed, versioned fixture. Exact values make tests assert *correctness*, not just shape; updating constants would be trivial if the data changed. |
| 8 | `requirements.txt` mixes runtime and dev dependencies | Maximizes evaluator convenience: a single `pip install -r requirements.txt` runs everything. The proper separation already exists in `pyproject.toml` (`llm`, `dev` optional groups). |
| 9 | No prompt-injection defense | The system prompt enforces hard rules and function calling constrains operational facts to the tools (the model cannot invent price/stock). Additional guardrails (I/O filters, moderation) are a documented next step. |
| 10 | `calc_shipping` is never called in offline mode | The tool serves the LLM mode; offline shipping questions route to the policy KB, which contains the same rules. Keeping the tool gives the LLM a structured path for the calculation (e.g. the R$ 500 free-shipping threshold). |
| 11 | No golden set / LLM-as-a-judge evaluation | Documented as a next step. The deterministic tools have unit tests and the 5 example conversations act as manual regression tests; a full evaluation harness is out of MVP scope. |

## Security note before publishing

- **API key exposure (verified 2026-11-03 — no history rewrite needed).** A scan of every
  commit and blob found **no real key in the Git history**: only `.env.example` (placeholder
  values) is tracked, and `.env` is gitignored/untracked. A real key was briefly pasted in a
  working copy and shared in chat, but it never reached a commit. Recommended action:
  **rotate the key** as a precaution, then set the new key only in `.env` / Vercel
  environment variables — never in tracked files.
