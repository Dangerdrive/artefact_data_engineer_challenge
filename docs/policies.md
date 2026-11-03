# Store Policies Digest (Manual v2.1, June 2025)

Source: `Desafio Técnico AI Engineer 2026/data/políticas_da_loja.pdf` (8 pages).
This digest is the basis for the **policies RAG** and the agent prompt.

---

## 1. Company Identity and Details

| Field | Information |
|-------|-------------|
| Trade name | Empório da Música |
| Legal name | Empório da Música Instrumentos Musicais Ltda. |
| CNPJ | 12.345.678/0001-90 |
| Address | Rua 14 de Maio, 3200 — Centro, Campo Grande-MS, ZIP 79202-333 |
| Phone / WhatsApp | (67) 3341-4444 |
| WhatsApp service channel | (67) 3321-4500 |
| Email | contato@emporiodamusica.com.br |
| Founded | 2008 |

**Scope:** sells **exclusively musical instruments** (guitars, basses, acoustic guitars,
drums, keyboards, winds, orchestral strings, ukuleles).
**Does not sell accessories** (strings, reeds, cables, cases, pedals, amplifiers).

---

## 2. Business Hours

| Day | Hours |
|-----|-------|
| Monday to Friday | 09:00 to 18:00 |
| Saturday | 09:00 to 13:00 |
| Sunday and holidays | Closed |

- Outside business hours: automated replies stating the return time.
- Special dates may have extended hours (announced on social media).

---

## 3. Payment Methods

| Method | Condition | Notes |
|--------|-----------|-------|
| PIX | Upfront | **5% discount** on the list price |
| Debit card | Upfront | All brands accepted |
| Credit card | Up to 12x interest-free | Minimum installment of R$ 100.00 |
| Bank slip (boleto) | Upfront | Clears within 3 business days |

### Installment rules

- Up to **3x**: interest-free, no minimum (except installments below R$ 50.00).
- **4x to 6x**: interest-free, minimum installment of R$ 80.00.
- **7x to 12x**: interest-free, minimum installment of R$ 100.00.
- **Combined methods** (e.g. PIX + card): allowed for purchases above R$ 2,000.00.

---

## 4. Returns and Exchanges

- **Right of withdrawal (online):** return within **7 calendar days** of receipt, no
  justification needed; product in original packaging; refund via the original payment
  method within **10 business days**; return shipping paid by the store.
- **Defect:** exchange within **30 calendar days** of purchase; after 30 days, claim the
  manufacturer warranty (the store may intermediate).
- **Preference (color/model/size):** within **7 days**, subject to availability; price
  differences charged or refunded.
- **Not eligible:** custom/made-to-order instruments; "final sale" items; wind instrument
  mouthpieces (hygiene).

---

## 5. Shipping and Delivery

- **Campo Grande (metropolitan region):**
  - Free shipping above R$ 500.00; below that, flat fee of R$ 35.00.
  - Delivery in 1 to 3 business days; delivered by the store's own courier.
- **Other cities (Correios/Jadlog):**

| Modality | Time | Tracking | Insurance |
|----------|------|----------|-----------|
| PAC | 5–12 business days | Yes | Included |
| SEDEX | 2–5 business days | Yes | Included |
| Jadlog (.package) | 3–8 business days | Yes | Included |

- Cost calculated by destination ZIP, weight, and dimensions; large instruments require
  individual quotes.
- **Tracking:** code in the format `BR` + 9 alphanumerics + `BR` (e.g. `BR4K7M2X9P1BR`),
  sent by email/WhatsApp once shipped.

---

## 6. Promotions and Discounts

- Campaigns: Store Anniversary (August, 10–25%), Black Friday (November, 15–30%),
  Back to School (February), Stock Clearance, Musician's Week (Nov 22).
- **Not cumulative.**
- PIX discount (5%) **does not apply** to promotional prices.
- No price rain checks for products sold out during a promotion.
- Always show the promotional price **together with** the original price and the percentage.

---

## 7. WhatsApp Customer Service

- **Tone of voice:** informal yet professional; welcoming, "like a friend who knows music".
  Avoid robotic language.
- **Response time:** up to 5 minutes during business hours.
- **Accuracy:** never state price, stock, or deadlines **without querying the system**.
- **Out of scope:** state that the store only sells instruments; politely redirect
  accessory requests (suggest partner stores when possible).

### Standard flow

1. Greeting (name, if available) + "how can I help?"
2. Understanding the need (product, question, tracking, complaint).
3. Querying the system.
4. Clear, objective reply with prices and conditions.
5. Courteous closing.

### Special situations

- **Out of stock:** state temporary unavailability + suggest alternatives.
  Never confirm availability without checking.
- **Discontinued:** state it is no longer in the catalog + offer successors/equivalents.
- **Expired promotion:** state transparently and show the current price.
- **Complaint:** listen with empathy, log it, and forward; follow-up within **24 business hours**.

---

## 8. Warranty

- **Legal:** 90 days against manufacturing defects (Brazilian Consumer Code), from receipt.
- **Manufacturer:** 6 months to 2 years (per certificate).
- **Not covered:** natural wear (frets, strings, felt, reeds), misuse/drops/extreme exposure,
  unauthorized modifications, cosmetic damage without functional impact.

---

## 9. Privacy (LGPD)

- Personal data used only to: process/deliver orders, communicate status/tracking, send
  promotions (with consent), and comply with legal obligations.
- Do not share with third parties for marketing.
- Customers may request data deletion at any time.

---

## Notes for the Agent

- The manual is an **internal document**; the virtual assistant must follow it as a reference.
- When in doubt about a policy, "consult management" before answering.
