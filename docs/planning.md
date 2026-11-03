# Implementation Plan — "Empório da Música" Customer Service Agent

> **Living document.** This file is the single source of truth for the project.
> At the end of **every work session**, update the
> [Project State](#10-project-state) section (see the `emporio-musica-agent` skill).

Challenge: **AI Engineer — Artefact (2026)** · Written for the Empório da Música technical case.

---

## 1. Context and Objective

**Empório da Música** is a fictional musical-instruments store in Campo Grande/MS, Brazil.
Customer service is currently 100% human, and the team is overwhelmed by recurring
questions (business hours, order status, price and availability, return rules, etc.).

**Mission:** prototype a **Python** text-messaging agent that assists the team with
customer service.

### Agent objectives

| ID | Objective |
|----|-----------|
| O1 | Assume a **persona** aligned with the store's identity and tone (informal but professional). |
| O2 | Receive and reply to messages based on the **provided context**. |
| O3 | Know **when to query data** (price, stock, order status) — never guess. |
| O4 | Know **when to consult policies** (returns, hours, payment, shipping). |
| O5 | Properly handle questions that are **out of scope** for the store. |

---

## 2. Scope and Requirements

### Functional requirements (derived from the brief)

- **R1 — Persona:** reply in the store's tone (informal, welcoming, "like a friend who knows music").
- **R2 — Context:** use the data (`data/*.csv`) and the policies (`políticas_da_loja.pdf`).
- **R3 — Data queries:** price, availability, stock, active promotions, order status and tracking.
- **R4 — Policy queries:** returns/exchanges, hours, payment methods, shipping, warranty.
- **R5 — Out of scope:** state that the store sells **exclusively musical instruments** and
  politely redirect accessory requests (strings, cables, reeds, pedals, amps, cases).

### Mandatory technical constraint

- **Python** as the primary language.

### Open decisions (must be justified in the final README)

| Decision | Possible options |
|----------|------------------|
| Agent approach | RAG, function calling, ReAct, SQL agent, hybrid… |
| Model and provider | Paid or free; local or API |
| Interaction interface | CLI, notebook, API or simple UI |
| Conversation history persistence | Implement if it makes sense |
| Data handling | Free, as needed |

---

## 3. Available Materials

| File | Content | Detailed analysis |
|------|---------|-------------------|
| `data/*.csv` (6 tables) | Products, orders, items, customers, categories, promotions | [docs/data.md](data.md) |
| `data/políticas_da_loja.pdf` | Policies and procedures manual (v2.1, 8 pages) | [docs/policies.md](policies.md) |

> **Note:** you are not required to use all the data — use what is needed for the best
> customer experience.

---

## 4. Proposed Technical Decisions (summary)

> Full details and justifications in [docs/technical-decisions.md](technical-decisions.md).

| Decision | Proposal | Short rationale |
|----------|----------|-----------------|
| Approach | **Hybrid: function calling + RAG** | Structured data (CSV) via tools/SQL; unstructured policies (PDF) via retrieval. |
| Model/Provider | **Configurable (OpenAI-compatible)**; economical default (e.g. `gpt-4o-mini` or Groq Llama) | Low cost, easy provider swap without refactoring. |
| Interface | **CLI** as MVP + optional **FastAPI** | Simple to run and demo; API ready to evolve. |
| History | **In-memory + optional SQLite persistence** | Multi-turn context per customer; persistence enables continuity. |
| Data handling | Load CSVs into **DuckDB/SQLite**; extract PDF into a RAG index | Fast, deterministic queries; semantic policies. |

---

## 5. Architecture (summary)

> Full diagram and component description in [docs/architecture.md](architecture.md).

```mermaid
flowchart LR
    U[User] --> I[Interface CLI/API]
    I --> O[Agent Orchestrator<br/>ReAct + function calling]
    O --> T1[Tool: product search]
    O --> T2[Tool: price & stock]
    O --> T3[Tool: orders & tracking]
    O --> T4[Tool: policies RAG]
    T1 & T2 & T3 --> DB[(DuckDB/SQLite<br/>CSV data)]
    T4 --> V[(Vector Store<br/>policies PDF)]
    O --> L[LLM Provider]
    O --> H[(Conversation History)]
```

---

## 6. Project Structure (proposed)

```
Artefact_Data_Engineer/
├── README.md                       # setup + decisions + limitations (mandatory)
├── docs/                           # project documentation
│   ├── planning.md                 # this file (source of truth)
│   ├── data.md                     # data dictionary
│   ├── policies.md                 # store policies digest
│   ├── architecture.md             # solution architecture
│   ├── technical-decisions.md      # justified technical decisions
│   ├── best-practices.md           # included best practices
│   └── example-interactions.md     # example conversations plan
├── src/                            # agent source code
│   ├── agent/                      # orchestrator, prompt, tools
│   │   ├── orchestrator.py         # LLM (function calling) + offline fallback
│   │   ├── prompt.py               # system prompt (persona + rules)
│   │   └── tools.py                # tool schemas + implementations
│   ├── data/                       # data layer (SQLite) + policy retrieval
│   │   ├── store.py                # CSV → in-memory SQLite + queries
│   │   ├── policies.py             # PDF extraction + keyword retrieval
│   │   └── text.py                 # normalization helpers
│   ├── config.py                   # env-based settings
│   └── cli.py                      # CLI entry point
├── tests/                          # pytest suite (store, policies, tools, agent)
├── examples/                       # 5 example conversations (deliverable)
├── pyproject.toml                  # project metadata, pytest & ruff config
├── requirements.txt                # dependencies
├── .env.example                    # environment configuration template
├── Makefile                        # shortcuts: install, run, test, lint
└── .github/skills/                 # planning-maintenance skill
```

---

## 7. Implementation Phases

| Phase | Description | Status |
|-------|-------------|--------|
| F0 | Challenge, data and policy analysis | ✅ Done |
| F1 | Planning documentation + best practices | ✅ Done |
| F2 | Project scaffold (structure, dependencies, env, git) | ✅ Done |
| F3 | Data layer (CSVs → SQLite; PDF extraction) | ✅ Done |
| F4 | Agent tools (catalog, stock, orders, policies) | ✅ Done |
| F5 | Orchestrator + prompt + persona | ✅ Done |
| F6 | CLI and API | ✅ Done (CLI; API deferred) |
| F7 | Automated tests | ✅ Done (30 tests) |
| F8 | Example interactions (3–5 conversations) | ✅ Done (5 examples) |
| F9 | Final README + review + submission | ⬜ Pending |

---

## 8. Deliverables and Checklist

- [x] **Public Git repository** on GitHub with a real commit history (initialized locally; publish to GitHub).
- [x] **README.md** with:
  - [x] Run instructions (environment, model provider, commands).
  - [x] Justification of technical decisions (framework, LLM, retrieval, prompt).
  - [x] Known limitations + what you would do with more time.
  - [x] Use of code assistants (which one and how it was used — workflow).
- [x] **3 to 5 example conversations** (`.md`/`.txt`/image), including at least one
      **non-trivial** scenario (real-time data query or policy application).
- [ ] **Do not modify** the repository after the submission deadline.

> ⚠️ **Important:** all responses and deliverables must be in **English**.

---

## 9. Included Best Practices

Summary of the adopted and documented best practices in
[docs/best-practices.md](best-practices.md):

1. Git versioning with a real commit history.
2. Secrets outside the code (`.env.example` + ignored `.env`).
3. Virtual environment + dependencies in `requirements.txt`.
4. Centralized configuration via environment variables.
5. Type hints + docstrings in Python code.
6. Lint and formatting (ruff).
7. Automated tests (pytest) with a mocked LLM.
8. Structured logging.
9. `.editorconfig` for cross-editor consistency.
10. `Makefile` for common task shortcuts.
11. Living documentation (this plan + maintenance skill).
12. Privacy/LGPD and token-cost control.

---

## 10. Project State

> **Rule:** every session must end with a new row in this log.

### Session Log

| Date | Work done | Decisions | Pending / next step |
|------|-----------|-----------|---------------------|
| 2026-11-03 | Read the challenge (PDF), the policies manual (PDF) and the schema of the 6 CSVs; created the plan, the data/policies/architecture/decisions/best-practices docs, the maintenance skill, the root README and the best-practice files | Hybrid approach (function calling + RAG); configurable provider; CLI + API; DuckDB for data; SQLite for history | Create the Python project scaffold (F2) and implement the data layer (F3) |
| 2026-11-03 | Converted all documentation, filenames, and config comments to English | English-only project (docs, filenames, and deliverables) | Create the Python project scaffold (F2) and implement the data layer (F3) |
| 2026-11-03 | Implemented the Python agent: env config, SQLite data layer, policy retrieval, tools, dual-mode orchestrator (LLM + offline), CLI, 30 pytest tests and 5 example conversations; updated the README | SQLite (stdlib) instead of DuckDB for a zero-dependency data layer; deterministic offline fallback; pronoun follow-ups in offline mode | Publish the repo publicly and do a final review (F9) |
| 2026-11-03 | Review/improvement pass: fixed ruff E501 (line-length 120), added an input-length guard, configurable `temperature`/`max_tokens`, an LLM history window, a CI workflow, an MIT license, an examples README and 7 new tests (37 total) | Ruff line-length 120 for verbose tool schemas; added CI + license; configurable generation params | Publish repo; optional FastAPI + persistence + embeddings |

### Current State (summary)

- [x] Challenge and materials analyzed
- [x] Planning documentation created
- [x] Python project scaffold (`src/`, `tests/`, `requirements.txt`, `pyproject.toml`)
- [x] Data layer (CSV → SQLite, PDF extraction)
- [x] Agent tools
- [x] Orchestrator and prompt
- [x] Interface (CLI; API deferred)
- [x] Tests (37 passing) + ruff clean + CI workflow
- [x] Example conversations (5)
- [x] Final README, docs and license

---

## 11. Next Step

1. Publish the repository publicly on GitHub with the current commit history.
2. Final review: run the tests, re-check the examples, and polish the README.
3. Optional next iterations: FastAPI endpoint, SQLite conversation persistence, and
   embedding-based policy retrieval.
