# Justified Technical Decisions

This document records the project's technical decisions, as required in the final README.
Each decision from the brief is answered with **choice + justification**.

---

## 1. Agent Framework / Approach

**Choice:** hybrid — **function calling (ReAct) + RAG**.

**Justification:**
- The CSVs are **structured data**: price, stock, and order-status queries are
  deterministic and are better served by **tools/SQL** than by semantic search
  (avoids hallucinating numbers).
- The policies manual is **unstructured text** (PDF): **RAG** retrieves the exact rule
  (returns, deadlines, shipping) and the LLM answers based on the retrieved excerpt.
- The combination explicitly meets the requirement "know when to query data and when to
  consult policies": the agent picks the right tool.
- Alternatives considered:
  - *Pure RAG:* risky for price/stock (could quote wrong values).
  - *Pure SQL agent:* cannot answer policy questions.
  - *ReAct without tools:* does not guarantee correct data.

## 2. Model and Provider

**Choice:** **DeepSeek** as the default, via its **OpenAI-compatible API**
(`LLM_BASE_URL=https://api.deepseek.com`, `LLM_MODEL=deepseek-chat`); still configurable
for any OpenAI-compatible provider (OpenAI, Groq, Together, local servers).

**Justification:**
- DeepSeek is low-cost and fast, and `deepseek-chat` supports function calling (tools).
- The OpenAI-compatible interface keeps the project **swappable** across providers with no
  code changes — only environment variables.
- The key stays in `.env` (never committed); `LLM_BASE_URL` allows pointing to any
  compatible endpoint. If the call fails, the agent falls back to offline mode.

## 3. Interaction Interface

**Choice:** **CLI** as the MVP's primary interface, with an optional **FastAPI** API.

**Justification:**
- A CLI is the simplest way to demonstrate the agent working (brief requirement:
  "the focus is the agent working correctly").
- The API enables future integration (e.g. WhatsApp) without reworking the logic.
- Separating the orchestrator from the interface keeps the logic channel-independent.

## 4. Conversation History Persistence

**Choice:** **in-memory** history per session + **optional SQLite persistence**.

**Justification:**
- It makes sense for the experience: the agent must remember the conversation context
  (e.g. the customer asks about a product and later about the order).
- SQLite persistence allows resuming conversations per customer and auditability.
- Kept optional/configurable to avoid complicating the MVP.

## 5. Data Handling

**Choice:** load the CSVs into an **in-memory SQLite** database (Python stdlib) and extract
the PDF with **pypdf**, chunked into a policies index.

**Justification:**
- SQLite: serverless, zero extra dependency, and SQL joins are easy (`orders ⋈ order_items
  ⋈ products`). The dataset is tiny, so an in-memory database is more than enough.
- (DuckDB was considered but dropped to keep the project dependency-light.)
- `specs` (JSON) is parsed to allow filtering (e.g. "nylon-string acoustic guitar").
- Promotions: only `is_active = 1`; the promotional price is computed and shown with the
  original price + percentage.
- Policies: section-based chunking of the manual; semantic search (embeddings) or BM25 in the MVP.

## 6. Prompt Strategy

**Choice:** versioned system prompt with **persona + hard rules** + tools described in
JSON schema.

**Justification:**
- Hard rules in the prompt reflect store policy: *never* state price/stock/deadlines
  without querying the system; out of scope = redirect accessories.
- The prompt forces the model to **call tools before answering** about operational data.
- Versioning the prompt (dedicated file) eases experimentation and evaluation.

## 7. Evaluation and Testing

**Choice:** unit tests for the tools + an example suite (golden set) evaluated manually
and, with more time, via LLM-as-a-judge.

**Justification:**
- The tools are deterministic → unit tests guarantee correct price/stock/status.
- Example conversations serve as behavior regression tests.

---

## 8. Execution Modes (LLM + Offline Fallback)

**Choice:** a **durable dual-mode design** — an LLM function-calling mode and a
deterministic offline mode that share the exact same tools.

**Justification:**
- The offline mode guarantees the agent is **always runnable and testable**, even without an
  API key or network — ideal for the evaluator and for CI.
- The LLM mode is the general-purpose path; if a model call fails, the agent **falls back**
  to offline mode instead of breaking the conversation.
- Sharing the tool layer between both modes guarantees the numbers (price/stock/order) come
  from the same deterministic source in either mode.
- The offline responder routes policy answers by language (EN/PT) and guards against
  purchase-intent phrases ("I want to order 2 guitars") being mistaken for order-status
  lookups.

---

## Decision Summary

| Decision | Choice |
|----------|--------|
| Approach | Hybrid function calling (ReAct) + RAG |
| Model/Provider | DeepSeek `deepseek-chat` (default), configurable via OpenAI-compatible API |
| Interface | CLI (MVP) + optional FastAPI |
| History | In-memory + optional SQLite |
| Data | SQLite (CSVs) + pypdf (policies) |
| Prompt | Persona + hard rules + tools in schema |
