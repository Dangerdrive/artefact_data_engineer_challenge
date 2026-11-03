# Dicionário de Dados — Empório da Música

Análise dos 6 arquivos CSV em `Desafio Técnico AI Engineer 2026/data/`.

## Visão Geral

| Arquivo | Linhas | Papel no agente |
|---------|--------|-----------------|
| `categories.csv` | 9 | Mapeia categorias de instrumentos |
| `products.csv` | 65 | Catálogo: preço, estoque, status, specs |
| `customers.csv` | 50 | Dados dos clientes (identificação em pedidos) |
| `orders.csv` | 20 | Pedidos: status, pagamento, rastreio |
| `order_items.csv` | 22 | Itens de cada pedido (N:N pedido↔produto) |
| `promotions.csv` | 25 | Promoções por produto (ativo/inativo) |

---

## `categories.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `category_id` | int | Chave primária |
| `name` | string | Nome da categoria |
| `description` | string | Descrição da categoria |

Categorias: Guitarras, Baixos, Baterias e Percussão, Teclados e Pianos, Violões,
Instrumentos de Sopro (Madeiras), Instrumentos de Sopro (Metais), Cordas Orquestrais, Ukuleles.

---

## `products.csv`

| Coluna | Tipo | Descrição | Observações |
|--------|------|-----------|-------------|
| `product_id` | int | Chave primária | |
| `price_brl` | float | Preço em R$ | Faixa: 159.9 a 19567.0 |
| `name` | string | Nome do produto | |
| `category_id` | int | FK → categories | |
| `description` | string | Descrição comercial | |
| `stock_quantity` | int | Quantidade em estoque | 2 produtos com estoque 0 |
| `status` | string | `active` (62) · `discontinued` (2) · `coming_soon` (1) | |
| `specs` | JSON (string) | Especificações técnicas | Ex.: topo, laterais, braço, cordas, escala |
| `created_at` | date | Data de criação no catálogo | |

---

## `customers.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `customer_id` | int | Chave primária |
| `name` | string | Nome completo |
| `phone` | string | Telefone (formato `(67) 9xxxx-xxxx`) |
| `email` | string | E-mail |
| `city` | string | Cidade (Campo Grande, Dourados, Três Lagoas, Corumbá, Ponta Porã) |

> **LGPD:** usar dados de clientes apenas para identificar pedidos. Nunca expor PII
> além do necessário e sempre respeitar a política de privacidade da loja.

---

## `orders.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `order_id` | int | Chave primária |
| `customer_id` | int | FK → customers |
| `order_date` | date | Data do pedido |
| `status` | string | `delivered` (7) · `confirmed` (4) · `pending` (4) · `cancelled` (4) · `shipped` (1) |
| `total_brl` | int | Total em R$ |
| `payment_method` | string | `pix`, `credit_3x`, `credit_6x`, `credit_12x`, `boleto`, `debit` |
| `tracking_code` | string | Formato `BR` + 9 alfanuméricos + `BR` (ex.: `BRAB1234567BR`) |
| `estimated_delivery` | date | Entrega estimada |
| `notes` | string | Observações |

---

## `order_items.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `order_id` | int | FK → orders |
| `quantity` | int | Quantidade |
| `product_id` | int | FK → products |

> Relacionamento N:N entre `orders` e `products`. Um pedido pode ter vários produtos.

---

## `promotions.csv`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `promotion_id` | int | Chave primária |
| `product_id` | int | FK → products |
| `discount_percent` | int | Percentual de desconto |
| `description` | string | Nome da campanha |
| `is_active` | int | `1` ativa · `0` inativa (4 ativas de 25) |

Campanhas presentes: Aniversário da Loja, Black Friday, Liquidação de Inverno,
Queima de Estoque, Oferta Especial, Promoção de Páscoa, Semana do Músico, Desconto Exclusivo.

> **Regra de negócio:** promoções **não são cumulativas**; desconto de PIX (5%)
> **não se aplica** sobre preços já promocionais.

---

## Tratamento de Dados Recomendado

1. **Padronizar tipos:** converter `price_brl`→float, `stock_quantity`→int, datas→`date`.
2. **Parsear `specs`:** JSON válido → colunas ou filtro por atributo (ex.: cordas de nylon).
3. **Filtro de catálogo:** considerar apenas `status = 'active'` para vendas.
   `discontinued`/`coming_soon` exigem tratamento especial nas respostas.
4. **Promoções:** aplicar apenas `is_active = 1`; calcular preço promocional e exibir
   junto ao preço original e ao percentual (exigência da política).
5. **Joins:** `orders ⋈ order_items ⋈ products` para compor o status/detalhe de um pedido.
6. **LGPD:** mascarar/omitir dados sensíveis desnecessários nas respostas.

## Observações de Qualidade dos Dados

- `orders.total_brl` parece estar em reais sem centavos (inteiro).
- 2 produtos com `stock_quantity = 0` (testar cenário "fora de estoque").
- 2 produtos `discontinued` e 1 `coming_soon` (testar cenários "descontinuado"/"em breve").
- Nem todos os produtos possuem promoção; nem todos os pedidos têm itens registrados
  (22 itens para 20 pedidos — possível 1 item por pedido na maioria).
