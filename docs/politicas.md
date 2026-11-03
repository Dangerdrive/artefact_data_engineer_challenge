# Políticas da Loja — Resumo (Manual v2.1, Junho/2025)

Fonte: `Desafio Técnico AI Engineer 2026/data/políticas_da_loja.pdf` (8 páginas).
Este resumo serve de base para o **RAG de políticas** e para o prompt do agente.

---

## 1. Identidade e Dados da Empresa

| Campo | Informação |
|-------|------------|
| Nome fantasia | Empório da Música |
| Razão social | Empório da Música Instrumentos Musicais Ltda. |
| CNPJ | 12.345.678/0001-90 |
| Endereço | Rua 14 de Maio, 3200 — Centro, Campo Grande-MS, CEP 79202-333 |
| Telefone / WhatsApp | (67) 3341-4444 |
| Canal de atendimento WhatsApp | (67) 3321-4500 |
| E-mail | contato@emporiodamusica.com.br |
| Fundação | 2008 |

**Escopo:** vende **exclusivamente instrumentos musicais** (guitarras, baixos, violões,
baterias, teclados, sopro, cordas orquestrais, ukuleles).
**Não vende acessórios** (cordas, palhetas, cabos, cases, pedais, amplificadores).

---

## 2. Horário de Funcionamento

| Dia | Horário |
|-----|---------|
| Segunda a Sexta | 09:00 às 18:00 |
| Sábado | 09:00 às 13:00 |
| Domingo e feriados | Fechado |

- Fora do expediente: respostas automáticas informando o horário de retorno.
- Datas especiais podem ter horário estendido (comunicado nas redes sociais).

---

## 3. Formas de Pagamento

| Forma | Condição | Observações |
|-------|----------|-------------|
| PIX | À vista | **5% de desconto** sobre o preço de tabela |
| Cartão de Débito | À vista | Todas as bandeiras |
| Cartão de Crédito | Até 12x sem juros | Parcela mínima R$ 100,00 |
| Boleto | À vista | Compensação em até 3 dias úteis |

### Regras de parcelamento

- Até **3x**: sem juros, sem valor mínimo (exceto parcela abaixo de R$ 50,00).
- **4x a 6x**: sem juros, parcela mínima R$ 80,00.
- **7x a 12x**: sem juros, parcela mínima R$ 100,00.
- **Combinação** (ex.: PIX + cartão): permitida para compras acima de R$ 2.000,00.

---

## 4. Trocas e Devoluções

- **Arrependimento (online):** devolução em até **7 dias corridos** após o recebimento,
  sem justificativa; produto na embalagem original; reembolso na mesma forma de pagamento
  em até **10 dias úteis**; frete de devolução por conta da loja.
- **Defeito:** troca em até **30 dias corridos** após a compra; após 30 dias, acionar
  garantia do fabricante (a loja pode intermediar).
- **Preferência (cor/modelo/tamanho):** até **7 dias**, mediante disponibilidade;
  diferenças de valor cobradas ou reembolsadas.
- **Não elegíveis:** instrumentos personalizados/sob encomenda; itens de "venda final";
  boquilhas de sopro (higiene).

---

## 5. Frete e Entregas

- **Campo Grande (região metropolitana):**
  - Frete grátis acima de R$ 500,00; abaixo disso, taxa fixa de R$ 35,00.
  - Prazo: 1 a 3 dias úteis; entrega por motoboy próprio.
- **Outras cidades (Correios/Jadlog):**

| Modalidade | Prazo | Rastreio | Seguro |
|------------|-------|----------|--------|
| PAC | 5–12 dias úteis | Sim | Incluído |
| SEDEX | 2–5 dias úteis | Sim | Incluído |
| Jadlog (.package) | 3–8 dias úteis | Sim | Incluído |

- Valor calculado por CEP, peso e dimensões; instrumentos de grande porte exigem cotação individual.
- **Rastreio:** código no formato `BR` + 9 alfanuméricos + `BR` (ex.: `BR4K7M2X9P1BR`),
  enviado por e-mail/WhatsApp após despacho.

---

## 6. Promoções e Descontos

- Campanhas: Aniversário da Loja (agosto, 10–25%), Black Friday (novembro, 15–30%),
  Volta às Aulas (fevereiro), Queima de Estoque, Semana do Músico (22/nov).
- **Não cumulativas.**
- Desconto de PIX (5%) **não se aplica** a preços promocionais.
- Sem reserva de preço (rain check) para produto esgotado em promoção.
- Sempre exibir preço promocional **junto** do original e do percentual.

---

## 7. Atendimento via WhatsApp

- **Tom de voz:** informal, mas profissional; acolhedor, "como um amigo que entende de música".
  Evitar linguagem robotizada.
- **Tempo de resposta:** até 5 min no expediente.
- **Precisão:** nunca informar preço, estoque ou prazo **sem consultar o sistema**.
- **Fora de escopo:** informar que a loja só vende instrumentos; redirecionar acessórios
  educadamente (sugerir lojas parceiras quando possível).

### Fluxo padrão

1. Saudação (nome, se disponível) + "como posso ajudar?"
2. Entendimento da necessidade (produto, dúvida, rastreamento, reclamação).
3. Consulta ao sistema.
4. Resposta clara e objetiva com preços e condições.
5. Fechamento cordial.

### Situações especiais

- **Fora de estoque:** informar indisponibilidade temporária + sugerir alternativas.
  Nunca confirmar disponibilidade sem verificar.
- **Descontinuado:** informar saída do catálogo + oferecer sucessores/equivalentes.
- **Promoção expirada:** informar com transparência e apresentar preço atual.
- **Reclamação:** ouvir com empatia, registrar e encaminhar; retorno em **24h úteis**.

---

## 8. Garantia

- **Legal:** 90 dias contra defeitos de fabricação (CDC), a partir do recebimento.
- **Fabricante:** 6 meses a 2 anos (conforme certificado).
- **Não cobre:** desgaste natural (trastes, cordas, feltros, palhetas), mau uso/quedas/
  exposição extrema, modificações por terceiros, danos estéticos sem prejuízo funcional.

---

## 9. Privacidade (LGPD)

- Dados pessoais usados apenas para: processar/entregar pedidos, comunicar status/rastreio,
  enviar promoções (com consentimento) e cumprir obrigações legais.
- Não compartilhar com terceiros para marketing.
- Cliente pode pedir exclusão dos dados a qualquer momento.

---

## Observações para o Agente

- O manual é um **documento interno**; o assistente virtual deve segui-lo como referência.
- Em caso de dúvida sobre política, "consultar a gerência" antes de responder.
