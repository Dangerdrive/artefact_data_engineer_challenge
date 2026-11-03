# Example Interactions — Plan

> Mandatory deliverable: **3 to 5 conversations** in `.md`/`.txt`/image, covering varied
> scenarios. At least **one** must be non-trivial (real-time data query or policy
> application). **The final files must be in English.**

## Planned Scenarios

| # | Scenario | Type | Covers |
|---|----------|------|--------|
| 1 | "Which acoustic guitars do you have under R$1000?" | Catalog query | Tool `search_products` + price/category filter |
| 2 | "How much is the Takamine GD20?" | Price query | Tool `price_stock` |
| 3 | "What is the store address?" | General info | Policy (RAG) |
| 4 | "I changed my mind about my purchase, can I return it?" | Policy application | RAG — 7-day withdrawal right |
| 5 | "Where is my order? The code is BRAB1234567BR" | Order status/tracking | Tool `order_status` (non-trivial) |
| 6 | "Do you sell guitar strings?" | Out of scope | Scope rule (redirect) |
| 7 | "Is there a PIX discount? Is there an active promotion?" | Combined rule | Tools + non-cumulativity policy |

## Example Scripts (skeleton)

### 1. Catalog by price range

```
User:  Which acoustic guitars do you have under R$1000?
Agent: [calls search_products("acoustic guitar", max_price=1000)]
       Lists active guitars ≤ R$1000 with price, stock, and active promotion (if any).
```

### 2. Price of a specific product

```
User:  How much is the Takamine GD20?
Agent: [calls price_stock(...)] → price, availability, and active promotion.
```

### 3. Store general information

```
User:  What is the store address?
Agent: [queries policies] → address, phone, and business hours.
```

### 4. Return policy (non-trivial — policy application)

```
User:  I changed my mind about my purchase, can I return my order?
Agent: [queries policies] → explains the 7-calendar-day withdrawal right
       (original packaging, refund within 10 business days).
```

### 5. Order tracking (non-trivial — data query)

```
User:  Where is my order? The code is BRAB1234567BR.
Agent: [calls order_status("BRAB1234567BR")] → status, estimated date, and instructions.
```

### 6. Out of scope

```
User:  Do you sell guitar strings?
Agent: States that the store sells only instruments and suggests partner stores.
```

---

## Notes

- Aim for **5 conversations** (the maximum allowed), ensuring variety: catalog, price,
  general info, policy, and tracking.
- Include the final conversations with **"User"/"Agent"** headers and, when useful, a
  `[called tool X]` note to show the reasoning.
- Save the final examples in `examples/` (in English).
