# Conversation 5 — Order tracking & shipping (non-trivial: real-time data)

**Scenario:** the customer provides a tracking code to check the order status, then
asks about shipping times to another city.

**User:** Hi! Where is my order? The tracking code is BRAB1234567BR

**Lira (agent):**
> Order #1 is currently 'delivered'. Estimated delivery: 2025-10-25.
> Tracking code: BRAB1234567BR. Total: R$ 11,499.00. Items: 1x Martin D-28
> Dreadnought Natural.

**User:** How long does shipping take to other cities?

**Lira (agent):**
> In the Campo Grande metropolitan region, shipping is free above R$500, otherwise
> a flat R$35, delivered in 1–3 business days by our own courier. For other cities
> we ship via Correios PAC (5–12 days), SEDEX (2–5 days) or Jadlog (3–8 days), all
> with tracking and insurance. Cost is calculated by destination ZIP, weight and
> dimensions. The tracking code looks like BR + 9 characters + BR
> (e.g., BR4K7M2X9P1BR).

**Tools used:** `get_order_status` (by tracking code) and `query_policies` (shipping).
