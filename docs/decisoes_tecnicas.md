# Decisões Técnicas Justificadas

Este documento registra as decisões técnicas do desafio, conforme exigido no README
final. Cada decisão do enunciado é respondida com **escolha + justificativa**.

---

## 1. Framework / Abordagem do Agente

**Escolha:** híbrida — **function calling (ReAct) + RAG**.

**Justificativa:**
- Os CSVs são **dados estruturados**: consultas de preço, estoque e status de pedido
  são determinísticas e ficam melhores como **tools/SQL** do que como busca semântica
  (evita alucinação de números).
- O manual de políticas é **texto não estruturado** (PDF): o **RAG** recupera a regra
  exata (troca, prazo, frete) e o LLM responde com base no trecho recuperado.
- A combinação atende ao requisito "saber quando consultar dados e quando consultar
  políticas" de forma explícita: o agente escolhe a ferramenta certa.
- Alternativas descartadas:
  - *RAG puro:* arriscado para preço/estoque (poderia citar valores errados).
  - *Agente de SQL puro:* não resolve as perguntas sobre políticas.
  - *ReAct sem tools:* não garante dados corretos.

## 2. Modelo e Provedor

**Escolha:** provedor **configurável via SDK OpenAI-compatible**; default econômico
(ex.: `gpt-4o-mini` ou modelo gratuito Groq/Llama).

**Justificativa:**
- O enunciado permite pagos ou gratuitos, locais ou API. A abstração mantém o projeto
  **rodável sem custo alto** e **trocável** entre provedores (openai, groq, together…).
- Para o MVP, um modelo pequeno/rápido é suficiente (tarefa de atendimento com tools).
- A chave fica em `.env` (nunca versionada); `LLM_BASE_URL` permite apontar para
  qualquer endpoint compatível.

## 3. Interface de Interação

**Escolha:** **CLI** como interface principal do MVP, com **API FastAPI** opcional.

**Justificativa:**
- CLI é a forma mais simples de demonstrar o agente funcionando (requisito do enunciado:
  "o foco é o agente funcionando corretamente").
- A API permite evoluir para integração futura (ex.: WhatsApp), sem retrabalho na lógica.
- Separar orquestrador da interface mantém a lógica independente do canal.

## 4. Persistência do Histórico de Conversa

**Escolha:** histórico **em memória** por sessão + **persistência SQLite opcional**.

**Justificativa:**
- Faz sentido para a experiência: o agente precisa lembrar o contexto da conversa
  (ex.: cliente perguntou sobre um produto e depois sobre o pedido).
- Persistência em SQLite permite retomar conversas por cliente e auditabilidade.
- Mantida como recurso opcional/configurável para não complicar o MVP.

## 5. Tratamento dos Dados

**Escolha:** load dos CSVs para **DuckDB** (embutido) e extração do PDF com **pypdf**,
segmentado em chunks para o índice de políticas.

**Justificativa:**
- DuckDB: SQL rápido e sem servidor; tipagem e joins fáceis (`orders ⋈ order_items ⋈ products`).
- `specs` (JSON) é parseado para permitir filtros (ex.: "violão de cordas de nylon").
- Promoções: apenas `is_active = 1`; preço promocional calculado e exibido com original + %.
- Políticas: chunking por seção do manual; busca semântica (embeddings) ou BM25 no MVP.

## 6. Estratégia de Prompt

**Escolha:** prompt de sistema versionado com **persona + regras duras** + tools
descritas em schema JSON.

**Justificativa:**
- Regras duras no prompt refletem a política da loja: *nunca* informar preço/estoque/
  prazo sem consultar o sistema; fora de escopo = redirecionar acessórios.
- O prompt força o modelo a **chamar tools antes de responder** sobre dados operacionais.
- Versionar o prompt (arquivo dedicado) facilita experimentos e avaliação.

## 7. Avaliação e Testes

**Escolha:** testes unitários das tools + suíte de exemplos (golden set) avaliada
manualmente e, com tempo, via LLM-as-a-judge.

**Justificativa:**
- As tools são determinísticas → testes unitários garantem preço/estoque/status corretos.
- Conversas de exemplo funcionam como regressão de comportamento.

---

## Resumo das Decisões

| Decisão | Escolha |
|---------|---------|
| Abordagem | Function calling (ReAct) + RAG híbrido |
| Modelo/Provedor | Configurável (OpenAI-compatible); default econômico |
| Interface | CLI (MVP) + API FastAPI opcional |
| Histórico | Em memória + SQLite opcional |
| Dados | DuckDB (CSVs) + pypdf (políticas) |
| Prompt | Persona + regras duras + tools em schema |
