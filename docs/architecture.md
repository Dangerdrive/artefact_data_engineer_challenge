# Proposed Architecture — Customer Service Agent

## 1. Overview

**Hybrid** approach: `function calling` (tools) for structured CSV data and **RAG** for
the unstructured policies PDF. An orchestrator loop decides, each turn, whether to reply
directly, call a tool, or query policies.

```mermaid
flowchart LR
    U[User] --> I[Interface<br/>CLI / FastAPI]
    I --> O[Orchestrator<br/>ReAct + function calling]
    O --> P[System prompt<br/>persona + rules]
    O --> T1[Tool: search_products]
    O --> T2[Tool: price_stock]
    O --> T3[Tool: order_status]
    O --> T4[Tool: query_policies]
    T1 & T2 & T3 --> DB[(DuckDB / SQLite<br/>loaded CSVs)]
    T4 --> V[(Semantic index<br/>policies PDF)]
    O --> L[LLM Provider<br/>configurable]
    O --> H[(Conversation history<br/>in-memory / SQLite)]
```

## 2. Components

| Component | Responsibility | Suggested tech |
|-----------|----------------|----------------|
| **Interface** | Receive/send messages | CLI (`argparse`/`rich`) + optional FastAPI |
| **Orchestrator** | Agent loop: decide tool vs. reply | ReAct + function calling via provider SDK |
| **System prompt** | Persona, tone, scope and accuracy rules | Versioned template (Jinja2 or f-string) |
| **Tools** | Deterministic data queries | Python + SQL over DuckDB |
| **Data layer** | Load CSVs → DuckDB; extract PDF | `pandas`/`duckdb` + `pypdf` |
| **Policies RAG** | Retrieve relevant manual sections | Chunking + embeddings + search (or BM25 for MVP) |
| **History** | Multi-turn context per customer | In-memory + optional SQLite persistence |
| **Config** | Provider, model, keys, flags | `python-dotenv` + `.env` |

## 3. Message Flow

```mermaid
sequenceDiagram
    participant U as User
    participant I as Interface
    participant O as Orchestrator
    participant T as Tools
    participant L as LLM
    U->>I: "How much is the Takamine GD20?"
    I->>O: message + history
    O->>L: prompt + available tools
    L-->>O: tool call: search_products("Takamine GD20")
    O->>T: search_products(...)
    T-->>O: {price, stock, promotion}
    O->>L: tool result
    L-->>O: final answer (persona)
    O->>I: answer
    I->>U: formatted answer
```

## 4. Tools (initial contract)

| Tool | Signature | Source |
|------|-----------|--------|
| `search_products` | `(query: str, max_price?: float, category?: str)` → list | `products` + `categories` + `promotions` |
| `price_stock` | `(product_id: int)` → `{price, stock, status, promotion}` | `products` + `promotions` |
| `order_status` | `(order_id: int \| tracking: str)` → status/dates/tracking | `orders` + `order_items` + `products` |
| `query_policies` | `(question: str)` → relevant excerpts | policies PDF RAG index |
| `calc_shipping` | `(city: str, total: float)` → shipping rule | policies (fixed rules) |

## 5. Key Architecture Decisions

1. **DuckDB (embedded, no server):** fast SQL over CSVs without infrastructure.
2. **Tools = Python functions with JSON schema:** allow swapping the LLM provider without
   changing the data logic.
3. **RAG separate from tools:** policies change per document; data changes per query.
   Separation keeps each path testable.
4. **Provider-agnostic:** SDK compatible with the OpenAI API (OpenAI, Groq, Together, etc.).
5. **CLI-first MVP:** quick, demonstrable delivery; API added later with no rework.

## 6. Observability and Quality

- Per-turn logs (tool called, latency, tokens).
- Basic metrics: number of tool calls, tokens/turn, fallback rate.
- Unit tests for tools (deterministic data) and orchestrator tests with a mocked LLM.
