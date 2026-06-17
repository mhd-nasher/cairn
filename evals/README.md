# Cairn Evals — Skill-TDD (RED · GREEN · REFACTOR)

Cairn is only as trustworthy as its last passing eval. These tests treat the skill itself like production
code: you write the test, watch it fail without the guidance, add the guidance, watch it pass, then close
the next loophole.

## Files

- **`trigger-eval.json`** — activation tests. Prompts that **should** invoke Cairn (design / structure /
  review / "how do I build this") and prompts that should **not** (a regex, a CSS bug, a translation).
  Catches both under-triggering and over-triggering.
- **`evals.json`** — behavior tests. Real prompts with `expectations` Cairn's answer must satisfy: Step 0
  stack detection, stack-aware suppression, beginner guidance, over-engineering defense, full rigor on a
  long-lived monolith.

## The loop

1. **RED** — run a scenario WITHOUT the relevant Cairn guidance (or against an assistant that hasn't loaded
   it). Record the exact failure and the rationalizations used (e.g. "I'll wrap Firestore in a repository
   to stay clean", or claiming "done" with no test output).
2. **GREEN** — add or sharpen the guidance that addresses *those specific* failures. Re-run. Confirm the
   behavior changes.
3. **REFACTOR** — find the new rationalization the guidance didn't anticipate, close it, re-verify. Repeat
   until the scenario passes cleanly.

## How to run

Trigger and behavior evals are prompt-level checks — run each `query` / `prompt` through an assistant that
has Cairn available and grade the result against `should_trigger` / `expectations`. A simple harness:
spawn one subagent per case with the skill loaded, have it answer, then grade the answer (a separate grader
agent, or a human) against the expected items. Validate the JSON itself with:

```bash
python3 -c "import json; json.load(open('trigger-eval.json')); json.load(open('evals.json')); print('OK')"
```

## When to re-run

After **any** change to `SKILL.md`, the workflows, the stack profiles, or the guardrails. A change that
makes one scenario pass often regresses another — the eval set is the regression net. Add a new case
whenever you discover a failure mode the current set doesn't cover.
