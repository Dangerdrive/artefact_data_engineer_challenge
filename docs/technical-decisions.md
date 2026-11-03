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

**Choice:** **configurable provider via an OpenAI-compatible SDK**; economical default
(e.g. `gpt-4o-mini` or a free Groq/Llama model).

**Justification:**
- The brief allows paid or free, local or API. The abstraction keeps the project
  **runnable at low cost** and **swappable** across providers (openai, groq, together…).
- For the MVP, a small/fast model is sufficient (a customer-service task with tools).
- The key stays in `.env` (never committed); `LLM_BASE_URL` allows pointing to any
  compatible endpoint.

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

**Choice:** load the CSVs into **DuckDB** (embedded) and extract the PDF with **pypdf**,
chunked into a policies index.

**Justification:**
- DuckDB: fast serverless SQL; easy typing and joins (`orders ⋈ order_items ⋈ products`).
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

## Decision Summary

| Decision | Choice |
|----------|--------|
| Approach | Hybrid function calling (ReAct) + RAG |
| Model/Provider | Configurable (OpenAI-compatible); economical default |
| Interface | CLI (MVP) + optional FastAPI |
| History | In-memory + optional SQLite |
| Data | DuckDB (CSVs) + pypdf (policies) |
| Prompt | Persona + hard rules + tools in schema |
