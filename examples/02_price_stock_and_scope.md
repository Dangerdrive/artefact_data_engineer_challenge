# Conversation 2 — Price, stock follow-up & out-of-scope

**Scenario:** the customer asks for a specific model's price, then a follow-up about
stock using a pronoun ("it"), and finally asks for an accessory the store does not sell.

**User:** How much is the Takamine GD20?

**Lira (agent):**
> The Takamine GD20 Dreadnought Natural is R$ 2,199.00. It's in stock
> (5 units available). PIX payments get an extra 5% off the list price.

**User:** Do you have it in stock?

**Lira (agent):**
> The Takamine GD20 Dreadnought Natural is R$ 2,199.00. It's in stock
> (5 units available). PIX payments get an extra 5% off the list price.

**User:** Do you sell guitar strings for it?

**Lira (agent):**
> Great question! We're a musical-instrument store, so we don't carry accessories
> like strings, cables, reeds, pedals, amps or cases. I'd be glad to help you find
> an instrument, though — and for accessories I recommend checking a partner store.

**Tools / behaviors:** `get_product` (price + stock), pronoun resolution to the
previously discussed product, and the out-of-scope (accessories) policy.
