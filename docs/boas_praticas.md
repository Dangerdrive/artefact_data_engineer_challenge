# Boas Práticas Incluídas no Projeto

Lista de boas práticas adotadas neste projeto, com o que foi incluído e por quê.

## 1. Versionamento com Git

- **O quê:** repositório Git com histórico de commits **real e incremental**.
- **Por quê:** é entregável obrigatório do desafio ("não faça force-push de tudo em um
  único commit") e permite rastrear decisões ao longo do tempo.
- **Estado:** ✅ incluído (`.gitignore` + commits incrementais).

## 2. Segredos fora do código

- **O quê:** chaves de API em variáveis de ambiente, via `.env` (nunca versionado).
- **Por quê:** evita vazamento de credenciais em repositório público.
- **Estado:** ✅ incluído (`.env.example` + `.env` no `.gitignore`).

## 3. Ambiente virtual e dependências declaradas

- **O quê:** `requirements.txt` (ou `pyproject.toml`) com dependências explícitas.
- **Por quê:** reprodutibilidade do ambiente para quem for avaliar o projeto.
- **Estado:** ✅ incluído (`requirements.txt`).

## 4. Configuração centralizada

- **O quê:** todas as configurações (modelo, provedor, chaves, flags) lidas de
  variáveis de ambiente com valores padrão seguros.
- **Por quê:** trocar de provedor/modelo sem tocar no código.
- **Estado:** ✅ incluído (`.env.example` + padrão de configuração documentado).

## 5. Type hints e docstrings

- **O quê:** anotações de tipo em funções e docstrings nos módulos.
- **Por quê:** legibilidade, manutenção e suporte a ferramentas de análise estática.
- **Estado:** 📌 a aplicar no código-fonte (Fase F2/F3 em diante).

## 6. Lint e formatação (ruff)

- **O quê:** `ruff` para lint + formatação (substitui flake8/black/isort).
- **Por quê:** código consistente e detecção precoce de problemas.
- **Estado:** ✅ dependência incluída; config/CI a adicionar com o scaffold.

## 7. Testes automatizados (pytest)

- **O quê:** testes unitários das tools (determinísticos) e testes do orquestrador com
  LLM mockado (sem depender de rede/chave).
- **Por quê:** garantir que preço/estoque/status nunca sejam incorretos.
- **Estado:** 📌 a implementar (Fase F7); dependência já listada.

## 8. Logging estruturado

- **O quê:** logs por turno: mensagem, tool chamada, latência, tokens usados.
- **Por quê:** depuração, auditoria e controle de custo de tokens.
- **Estado:** 📌 a implementar.

## 9. Padronização entre editores (`.editorconfig`)

- **O quê:** `.editorconfig` com charset UTF-8, LF, indentação consistente.
- **Por quê:** consistência independente do editor/OS (o projeto roda em WSL/Windows).
- **Estado:** ✅ incluído.

## 10. Atalhos de tarefas (Makefile)

- **O quê:** `Makefile` com `install`, `run`, `test`, `lint`, `format`.
- **Por quê:** reduz fricção e documenta os comandos principais.
- **Estado:** ✅ incluído.

## 11. Documentação viva + skill de manutenção

- **O quê:** `docs/planejamento.md` como fonte de verdade + skill
  `.github/skills/emporio-musica-agent` que obriga a registrar o estado a cada sessão.
- **Por quê:** continuidade do trabalho e rastreabilidade de decisões.
- **Estado:** ✅ incluído.

## 12. Privacidade e conformidade (LGPD)

- **O quê:** minimizar PII nas respostas; usar dados do cliente apenas para identificar
  pedidos; não expor dados além do necessário.
- **Por quê:** a loja declara conformidade com a LGPD e os dados incluem PII.
- **Estado:** ✅ documentado em `docs/politicas.md` e `docs/dados.md`.

## 13. Controle de custo de tokens

- **O quê:** modelo padrão econômico, limite de tokens, cache/evitação de chamadas
  desnecessárias.
- **Por quê:** reduzir custo e latência no uso de LLM via API.
- **Estado:** 📌 a implementar.

## 14. Tratamento de erros e fallback

- **O quê:** capturar falhas de API do LLM e retornar mensagem amigável de
  indisponibilidade; nunca travar a conversa.
- **Por quê:** robustez da experiência de atendimento.
- **Estado:** 📌 a implementar.

---

## Resumo de Status

- ✅ **Já incluído:** Git, `.gitignore`, `.env.example`, `requirements.txt`,
  `.editorconfig`, `Makefile`, docs vivas, skill de manutenção.
- 📌 **A incluir com o código:** type hints, ruff, pytest, logging, controle de tokens,
  tratamento de erros.
