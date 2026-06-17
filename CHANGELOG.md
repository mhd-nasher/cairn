# Changelog

All notable changes to Cairn are documented here.

## [1.0.0] — 2026-06-17

### Cairn is born — the architecture compass that turns anyone into a system designer

First release of Cairn as an independent, self-contained system-design engine.

- **Three modes:** Mode 0 — Guided Build for beginners (interview-driven, plain language, stop-guards);
  Mode A — New Design; Mode B — Audit / Refactor.
- **Mandatory Step 0 discovery** — detect the stack and the user's level before applying any rule.
- **Stack-aware rule engine** (`reference/stack-profiles.md`) — per-stack APPLY/SUPPRESS tables and default
  boundary level for Firebase/serverless, mobile/Flutter, web, monolith, microservices, CLI/library,
  embedded, and data/ML. Rules that don't fit the stack are suppressed with a stated reason — so Cairn
  never over-engineers.
- **The Anti-Over-Engineering Law + guardrails** (`reference/over-engineering-guardrails.md`) — the judgment
  layer: the "name the change it protects against" test, complexity budgets, smells, and the decision recipe.
- **Full lifecycle:** design → plan → build → verify, with three gates (`reference/process-discipline.md`)
  and a hand-off workflow (`workflows/handoff-to-build.md`). Nothing is "done" without evidence.
- **57 enforceable rules** with stable IDs (R-001 … R-057) and a plain-language layer
  (`reference/rules-plain-language.md`) — every rule in human words plus *when NOT to apply it*.
- **World-class production extras** (`reference/modern-essentials.md`) — secrets/config, idempotency,
  observability, error handling, validation, security, data integrity, contracts, async, DDD-lite — each
  with an "applies when".
- **Reference library:** principles, patterns, anti-patterns, glossary.
- **Checklists** (design-review, code-review), **ADR template**, **worked examples**, and a
  **circular-dependency checker** (`scripts/check_dependencies.py`).
- **Verifiable by design:** `evals/` contains activation tests (`trigger-eval.json`), behavior tests
  (`evals.json`), and a skill-TDD guide (`evals/README.md`).
