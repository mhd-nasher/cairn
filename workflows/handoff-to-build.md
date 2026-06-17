# Workflow — Hand Off Design to Build

> The bridge from an approved design (Mode 0 / A / B) to verified, working code. It turns structure into an
> ordered, testable plan, drives the build simplest-thing-first, and refuses to call it done without
> evidence. Use after any design mode produces a folder tree and boundary set.

## When to use

- A Cairn design or audit just produced a structure and you (or the user) want to build it.
- An audit produced a refactoring plan and you want to execute it safely.

## Step 1: Turn the design into a plan

```
[████░░░░░░░░░░░░░░░░] 20% — Step 1/5: Writing the build plan
```

Produce an **ordered list of small, independently verifiable tasks**. For each task record:
- **What** — one concrete deliverable (a file, a function, a test).
- **Layer** — core / adapter / wiring (so the dependency direction stays inward, R-001).
- **Verify** — the one check that proves the task is done (a unit test, a passing build, a clean grep).

Ordering principle (almost always):
1. Pure logic + its tests (pricing, validation, policy) — no DB/framework.
2. Ports/interfaces **only where they earned their place** (test seam or second impl).
3. Adapters (DB, payment SDK, HTTP) implementing the ports / called directly.
4. Wiring / entry point (the one place that touches the real framework + secrets).
5. Edges: input validation, error translation, logging, idempotency (from `reference/modern-essentials.md`).

**Output:** a numbered plan, each item with its verify-check.

## Step 2: Confirm the plan (cheap gate)

```
[████████░░░░░░░░░░░░] 40% — Step 2/5: Confirming the plan
```

Show the plan. For anything touching money/user data or a one-way-door decision, get a quick confirm before
building. For trivial reversible work, proceed. (Design Gate / `reference/process-discipline.md`.)

## Step 3: Build simplest-thing-first

```
[████████████░░░░░░░░] 60% — Step 3/5: Building
```

Implement tasks in order. At each step:
- Honor the **complexity budget** from Step 0 — do not add a boundary the plan didn't justify.
- Keep `core/` pure: it must not import the DB, framework, or SDKs.
- If you discover a needed boundary mid-build, apply the **"name the change it protects against"** test
  (`reference/over-engineering-guardrails.md`) before adding it.

## Step 4: Verify with evidence (the hard gate)

```
[████████████████░░░░] 80% — Step 4/5: Verifying with evidence
```

Do not claim done without showing:
- Test runs with **actual output** (the pure-logic tests especially — they should pass with no DB running).
- `scripts/check_dependencies.py <path>` clean — no cycles (R-005).
- The relevant items from `checklists/code-review.md` checked.
- For money/user-data paths: confirmation that a **separate bug + security review** is scheduled or done —
  Cairn gives structure, not a safety guarantee.

If any evidence is missing → return to Step 3. No exceptions.

## Step 5: Record and close

```
[████████████████████] 100% — Step 5/5: Recorded
```

- Update / create the ADR (`templates/adr-template.md`) with what was built and what was deliberately kept
  simple, citing rule IDs.
- State plainly what is verified and what still needs the separate bug/security pass.

## What this workflow must never do

- Never report "done"/"working"/"passing" without showing the evidence.
- Never silently add structure the plan didn't justify.
- Never imply the result is secure or bug-free — that is a separate review.
