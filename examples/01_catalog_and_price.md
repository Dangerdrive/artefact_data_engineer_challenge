# Conversation 1 — Catalog search & price

**Scenario:** the customer is shopping for an entry-level acoustic guitar and asks
for options under a budget, then checks the price of a specific model.

**User:** Which acoustic guitars do you have under R$1000?

**Lira (agent):**
> Here are some options in Violões up to R$ 1,000.00:
> - Tagima Memphis AC-39 Nylon Natural — R$ 429.90 · 15 in stock
> - Rozini RC-104 Nylon Estudante — R$ 459.90 · 10 in stock
> - Shelby SN-100 Folk Aço Preto — R$ 549.00 · 5 in stock
> - Giannini GF-1R Aço Folk Sunburst — R$ 579.90 · 7 in stock
> - Yamaha C40 Nylon Natural — R$ 599.90 · 12 in stock
> - Giannini GN-15 Nylon Cedr Natural — R$ 689.00 · 6 in stock
> - Yamaha F310 Aço Natural — R$ 699.90 · 14 in stock
> - Tagima Dallas Tuner Aço Natural — R$ 749.00 · 9 in stock
>
> Want more details on any of these?

**User:** How much is the Yamaha C40?

**Lira (agent):**
> The Yamaha C40 Nylon Natural is R$ 599.90. It's in stock (12 units available).
> PIX payments get an extra 5% off the list price.

**Tools used:** `search_products` (category + price filter), `get_product` (price/stock).
