---
name: emporio-musica-agent
description: 'Fluxo de trabalho e manutenção do estado do projeto do agente de atendimento da Empório da Música (desafio Artefact AI Engineer). Use quando: trabalhar neste projeto, iniciar ou concluir tarefas, registrar progresso, atualizar o planejamento, consultar dados ou políticas da loja, implementar ou testar o agente Python de atendimento ao cliente. Regra obrigatória: atualizar docs/planejamento.md com o estado do projeto ao final de toda sessão.'
---

# Agente de Atendimento — Empório da Música

## Objetivo

Manter o projeto **documentado, rastreável e consistente** enquanto o agente de
atendimento da Empório da Música é planejado e implementado.

O documento-fonte de verdade é [`docs/planejamento.md`](../../../docs/planejamento.md).
Toda mudança relevante deve ser registrada nele.

## Quando Usar

- Iniciar ou retomar qualquer trabalho neste projeto.
- Implementar features do agente (tools, orquestrador, CLI, API, dados).
- Escrever testes, exemplos de conversa ou documentação.
- Revisar decisões técnicas ou arquitetura.
- Preparar a entrega final do desafio (README em inglês, exemplos, repositório).

## Procedimento (obrigatório em toda sessão)

1. **Ler o estado atual** — abrir [`docs/planejamento.md`](../../../docs/planejamento.md)
   e ler a seção `Estado do Projeto` antes de começar a trabalhar.
2. **Executar a tarefa** — fazer as alterações de código ou documentação necessárias.
3. **Atualizar o planejamento** — ao final da sessão:
   - Adicionar **uma nova linha** na tabela `Registro de Sessões` com:
     data, atividades realizadas, decisões tomadas e pendências/próximo passo.
   - Atualizar a seção `Estado Atual (resumo)` marcando/desmarcando os checkboxes.
   - Atualizar a seção `Próximo Passo` com o que deve ser feito em seguida.
4. **Atualizar fases** — se uma fase de `Fases de Implementação` mudar de status,
   refletir isso na tabela.
5. **Sincronizar docs auxiliares** — se dados, políticas, arquitetura ou decisões
   mudarem, atualizar o respectivo arquivo em `docs/`.

## Formato do Registro de Sessão

| Data | Atividades realizadas | Decisões tomadas | Pendências / próximo passo |
|------|----------------------|------------------|----------------------------|
| AAAA-MM-DD | … | … | … |

## Recursos do Projeto

- Planejamento (fonte de verdade): [`docs/planejamento.md`](../../../docs/planejamento.md)
- Dicionário de dados: [`docs/dados.md`](../../../docs/dados.md)
- Políticas da loja: [`docs/politicas.md`](../../../docs/politicas.md)
- Arquitetura: [`docs/arquitetura.md`](../../../docs/arquitetura.md)
- Decisões técnicas: [`docs/decisoes_tecnicas.md`](../../../docs/decisoes_tecnicas.md)
- Boas práticas: [`docs/boas_praticas.md`](../../../docs/boas_praticas.md)
- Exemplos de interação: [`docs/exemplos_interacoes.md`](../../../docs/exemplos_interacoes.md)

## Regras de Ouro

- **Nunca terminar uma sessão sem registrar** o progresso em `docs/planejamento.md`.
- **Entregáveis finais em inglês** (README e exemplos de conversa); docs internas em português.
- **Nunca inventar preço, estoque ou prazo** — sempre consultar as tools/dados (política da loja).
- Manter o histórico de commits Git **real e incremental** (nunca force-push de um commit único).
