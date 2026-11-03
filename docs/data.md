# Data Dictionary — Empório da Música

Analysis of the 6 CSV files in `Desafio Técnico AI Engineer 2026/data/`.

## Overview

| File | Rows | Role in the agent |
|------|------|-------------------|
| `categories.csv` | 9 | Maps instrument categories |
| `products.csv` | 65 | Catalog: price, stock, status, specs |
| `customers.csv` | 50 | Customer data (identification in orders) |
| `orders.csv` | 20 | Orders: status, payment, tracking |
| `order_items.csv` | 22 | Items of each order (N:N order↔product) |
| `promotions.csv` | 25 | Per-product promotions (active/inactive) |

---

## `categories.csv`

| Column | Type | Description |
|--------|------|-------------|
| `category_id` | int | Primary key |
| `name` | string | Category name |
| `description` | string | Category description |

Categories: Guitarras, Baixos, Baterias e Percussão, Teclados e Pianos, Violões,
Instrumentos de Sopro (Madeiras), Instrumentos de Sopro (Metais), Cordas Orquestrais, Ukuleles.

---

## `products.csv`

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `product_id` | int | Primary key | |
| `price_brl` | float | Price in BRL | Range: 159.9 to 19567.0 |
| `name` | string | Product name | |
| `category_id` | int | FK → categories | |
| `description` | string | Commercial description | |
| `stock_quantity` | int | Quantity in stock | 2 products with 0 stock |
| `status` | string | `active` (62) · `discontinued` (2) · `coming_soon` (1) | |
| `specs` | JSON (string) | Technical specifications | e.g. top, back/sides, neck, strings, scale |
| `created_at` | date | Catalog creation date | |

---

## `customers.csv`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | int | Primary key |
| `name` | string | Full name |
| `phone` | string | Phone (`(67) 9xxxx-xxxx`) |
| `email` | string | Email |
| `city` | string | City (Campo Grande, Dourados, Três Lagoas, Corumbá, Ponta Porã) |

> **LGPD (Brazilian data privacy law):** use customer data only to identify orders.
> Never expose PII beyond what is necessary and always follow the store's privacy policy.

---

## `orders.csv`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | int | Primary key |
| `customer_id` | int | FK → customers |
| `order_date` | date | Order date |
| `status` | string | `delivered` (7) · `confirmed` (4) · `pending` (4) · `cancelled` (4) · `shipped` (1) |
| `total_brl` | int | Total in BRL |
| `payment_method` | string | `pix`, `credit_3x`, `credit_6x`, `credit_12x`, `boleto`, `debit` |
| `tracking_code` | string | Format `BR` + 9 alphanumerics + `BR` (e.g. `BRAB1234567BR`) |
| `estimated_delivery` | date | Estimated delivery |
| `notes` | string | Remarks |

---

## `order_items.csv`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | int | FK → orders |
| `quantity` | int | Quantity |
| `product_id` | int | FK → products |

> N:N relationship between `orders` and `products`. An order can contain several products.

---

## `promotions.csv`

| Column | Type | Description |
|--------|------|-------------|
| `promotion_id` | int | Primary key |
| `product_id` | int | FK → products |
| `discount_percent` | int | Discount percentage |
| `description` | string | Campaign name |
| `is_active` | int | `1` active · `0` inactive (4 active of 25) |

Campaigns present: Store Anniversary, Black Friday, Winter Sale, Stock Clearance,
Special Offer, Easter Promotion, Musician's Week, Exclusive Discount.

> **Business rule:** promotions are **not cumulative**; the PIX discount (5%) **does not
> apply** to prices already on promotion.

---

## Recommended Data Handling

1. **Normalize types:** convert `price_brl`→float, `stock_quantity`→int, dates→`date`.
2. **Parse `specs`:** valid JSON → columns or attribute filtering (e.g. nylon strings).
3. **Catalog filter:** consider only `status = 'active'` for sales.
   `discontinued`/`coming_soon` require special handling in responses.
4. **Promotions:** apply only `is_active = 1`; compute the promotional price and display
   it next to the original price and the percentage (policy requirement).
5. **Joins:** `orders ⋈ order_items ⋈ products` to build an order's status/details.
6. **LGPD:** mask/omit sensitive data that is not needed in responses.

## Data Quality Notes

- `orders.total_brl` appears to be in whole reais.
- 2 products with `stock_quantity = 0` (test the "out of stock" scenario).
- 2 `discontinued` and 1 `coming_soon` products (test "discontinued"/"coming soon" scenarios).
- Not every product has a promotion; not every order has recorded items
  (22 items for 20 orders — likely one item per order in most cases).
