---
name: emporio-musica-agent
description: 'Workflow and project-state maintenance for the Empório da Música customer service agent (Artefact AI Engineer challenge). Use when: working on this project, starting or finishing tasks, recording progress, updating the planning, querying store data or policies, implementing or testing the Python customer service agent. Mandatory rule: update docs/planning.md with the project state at the end of every session.'
---

# Empório da Música — Customer Service Agent

## Objective

Keep the project **documented, traceable, and consistent** while the Empório da Música
customer service agent is planned and implemented.

The source of truth is [`docs/planning.md`](../../../docs/planning.md).
Every relevant change must be recorded there.

## When to Use

- Start or resume any work on this project.
- Implement agent features (tools, orchestrator, CLI, API, data).
- Write tests, example conversations, or documentation.
- Review technical decisions or architecture.
- Prepare the final challenge submission (English README, examples, repository).

## Procedure (mandatory every session)

1. **Read the current state** — open [`docs/planning.md`](../../../docs/planning.md)
   and read the `Project State` section before starting work.
2. **Do the task** — make the necessary code or documentation changes.
3. **Update the planning** — at the end of the session:
   - Add **one new row** to the `Session Log` table with: date, work done, decisions
     taken, and pending/next step.
   - Update the `Current State (summary)` section by checking/unchecking the checkboxes.
   - Update the `Next Step` section with what should be done next.
4. **Update phases** — if a phase in `Implementation Phases` changes status, reflect it
   in the table.
5. **Sync auxiliary docs** — if data, policies, architecture, or decisions change, update
   the corresponding file in `docs/`.

## Session Log Format

| Date | Work done | Decisions | Pending / next step |
|------|-----------|-----------|---------------------|
| YYYY-MM-DD | … | … | … |

## Project Resources

- Planning (source of truth): [`docs/planning.md`](../../../docs/planning.md)
- Data dictionary: [`docs/data.md`](../../../docs/data.md)
- Store policies: [`docs/policies.md`](../../../docs/policies.md)
- Architecture: [`docs/architecture.md`](../../../docs/architecture.md)
- Technical decisions: [`docs/technical-decisions.md`](../../../docs/technical-decisions.md)
- Best practices: [`docs/best-practices.md`](../../../docs/best-practices.md)
- Example interactions: [`docs/example-interactions.md`](../../../docs/example-interactions.md)

## Golden Rules

- **Never finish a session without recording** progress in `docs/planning.md`.
- **All deliverables in English** (README and example conversations).
- **Never invent price, stock, or deadlines** — always query the tools/data (store policy).
- Keep the Git commit history **real and incremental** (never force-push a single commit).
