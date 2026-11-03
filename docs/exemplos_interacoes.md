# Exemplos de Interação — Planejamento

> Entregável obrigatório: **3 a 5 conversas** em `.md`/`.txt`/imagem, cobrindo cenários
> variados. Pelo menos **uma** deve ser não trivial (consulta de dados em tempo real ou
> aplicação de política). **Os arquivos finais devem estar em inglês.**

## Cenários Planejados

| # | Cenário | Tipo | Cobre |
|---|---------|------|-------|
| 1 | "Quais violões disponíveis custando até R$1000?" | Consulta de catálogo | Tool `buscar_produtos` + filtro por preço/categoria |
| 2 | "Quanto custa o Takamine GD20?" | Consulta de preço | Tool `preco_estoque` |
| 3 | "Qual o endereço da loja?" | Informação geral | Política (RAG) |
| 4 | "Me arrependi da minha compra, posso devolver?" | Aplicação de política | RAG — arrependimento 7 dias |
| 5 | "Cadê meu pedido? Meu código é BRAB1234567BR" | Status/rastreio | Tool `status_pedido` (não trivial) |
| 6 | "Vocês vendem cordas para violão?" | Fora de escopo | Regra de escopo (redirecionar) |
| 7 | "Esse produto tem desconto no PIX? Tem promoção ativa?" | Regra combinada | Tools + política de não cumulatividade |

## Roteiro dos Exemplos (esqueleto)

### 1. Catálogo por faixa de preço

```
Usuário: Quais opções de violões disponíveis custando até R$1000?
Agente:  [chama buscar_produtos("violão", preco_max=1000)]
         Lista violões ativos ≤ R$1000, com preço, estoque e promoção ativa (se houver).
```

### 2. Preço de um produto específico

```
Usuário: Quanto custa o Takamine GD20?
Agente:  [chama preco_estoque(...)] → preço, disponibilidade e promoção ativa.
```

### 3. Informação geral da loja

```
Usuário: Qual o endereço da loja?
Agente:  [consulta políticas] → endereço, telefone e horário.
```

### 4. Política de devolução (não trivial — aplicação de política)

```
Usuário: Me arrependi da minha compra, posso devolver meu pedido?
Agente:  [consulta políticas] → explica direito de arrependimento (7 dias corridos,
         embalagem original, reembolso em até 10 dias úteis).
```

### 5. Rastreio de pedido (não trivial — consulta de dados)

```
Usuário: Onde está meu pedido? O código é BRAB1234567BR.
Agente:  [chama status_pedido("BRAB1234567BR")] → status, data prevista e link/instruções.
```

### 6. Fora de escopo

```
Usuário: Vocês vendem cordas para violão?
Agente:  Informa que a loja vende apenas instrumentos e sugere lojas parceiras.
```

---

## Observações

- Priorizar **5 conversas** (máximo permitido), garantindo variedade: catálogo, preço,
  informação geral, política e rastreio.
- Incluir nas conversas finais os **cabeçalhos "Usuário"/"Agente"** e, quando útil, uma
  nota `[chamou a tool X]` para evidenciar o raciocínio.
- Salvar os exemplos finais em `examples/` (em inglês).
