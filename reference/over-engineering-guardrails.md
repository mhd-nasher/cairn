# Over-Engineering Guardrails — The Judgment Layer

> Cairn tells you *how* to add boundaries. It does not, on its own, tell you *when not to*. A naive,
> maximalist reading produces the opposite of clean: layers that only pass data through, interfaces with
> one implementation, abstractions built for a future that never arrives. This file is the missing
> judgment. **Apply it at every step of every workflow.**

## The Law

> **A boundary, interface, or abstraction must earn its place. If you cannot name the concrete change it
> protects against, do not add it.**

Architecture has two failure modes, not one:
- **Under-engineering (chaos):** everything coupled, nothing testable. The beginner's default.
- **Over-engineering (ceremony):** indirection nobody needs. The default of someone who has learned the rules but not the judgment.

The goal is the *minimum structure that keeps the system changeable* — no less, no more.

## The "name the change" test

Before adding any port, interface, layer, or generic abstraction, answer in one concrete sentence:
**"This protects against ___ , which is real because ___ ."**

- ✅ "This `PaymentCharger` port lets me swap Stripe for Adyen, which is real because we're piloting Adyen next quarter."
- ✅ "This `OrderStore` interface lets me use an in-memory fake in tests, which is real because I test pricing 50×/day."
- ❌ "This abstraction gives us flexibility." — Flexibility against *what*? Name it or drop it.
- ❌ "We might need it later." — Not a change. Not real yet. Add it later, when it is.

If you cannot fill both blanks with something concrete, **do not build it.**

## The three (and only three) reasons to add a boundary

1. **Two real implementations** exist now or are imminent (a swap, a fake-for-tests, A/B).
2. **A team / release split** — two groups must build and deploy independently.
3. **Testability** genuinely requires isolating something slow, external, or non-deterministic.

No third-party hypothetical counts. No "good practice in the abstract" counts.

## Complexity budget

Set this in Step 0 and spend it deliberately:

| Project shape | Budget | Means |
|---------------|--------|-------|
| Solo / MVP / spike | **Minimal** | 2 layers max. Direct calls to fixed infra. Ports only for test seams. |
| Team app, long-lived | **Standard** | 3 layers. Ports for genuinely variable infra. |
| Large / regulated / many teams | **Full** | 4 circles, full DIP, formal boundaries. |

Spending above budget is over-engineering even if a rule seems to demand it.

## Smells you are over-engineering (catch these in review)

- An interface with exactly **one** implementation and no test fake — delete the interface, use the class.
- A layer whose methods only **forward** calls to the next layer (pass-through / lasagna code).
- A **repository/gateway around a fixed managed service** you'll never swap (Firestore, S3) with no test need.
- A hand-rolled **DI container / plugin framework** for an app with three wires.
- **Generic "manager/handler/processor"** classes that abstract a single concrete use.
- **Microservices** before any scaling or team boundary demands them (distributed monolith).
- **Premature config**: every constant turned into an env var "for flexibility."
- Event sourcing / CQRS / hexagonal-everything on a CRUD app.
- Abstractions justified only by the words "flexible", "scalable", "future-proof", "best practice."

## What an abstraction actually costs

Every boundary you add charges rent forever:
- **Indirection** — readers must hop through layers to follow one call.
- **Cognitive load** — more names, files, and concepts to hold in mind.
- **Friction** — a simple change now touches several files.
- **False safety** — a wrong abstraction is harder to remove than no abstraction.

A boundary is worth it only when the protection it buys exceeds this rent. Most don't.

## Reversibility heuristic (one-way vs two-way doors)

- **Two-way door** (easy to reverse: a function split, a renamed folder): just do the simple thing now;
  change it freely later. Don't agonize, don't pre-abstract.
- **One-way door** (hard to reverse: database choice, public API shape, service split, data model):
  *these* deserve care and deferral (R-026). Spend your design effort here, not on internal plumbing.

## The decision recipe (use inline during design)

```
Considering a boundary/abstraction?
  ├─ Can I name a concrete change it protects against?      ── no → DON'T build it
  ├─ Is that change real now or imminent (not hypothetical)? ── no → DON'T build it
  ├─ Does it fit the complexity budget for this project?     ── no → DON'T build it
  ├─ Does the protection exceed the indirection cost?        ── no → DON'T build it
  └─ all yes → build it, and write down the change it protects (ADR)
```

## Stack-specific over-engineering traps

- **Firebase/serverless:** wrapping Firestore/Stripe in gateways "to stay clean" when you'll never swap
  them and can mock the SDK directly. Keep logic pure; call the SDK directly from the handler.
- **Mobile:** a use-case class per trivial action that just calls one repository method — collapse it.
- **Web:** an abstraction layer over `fetch` for a three-endpoint app.
- **Microservices:** splitting by noun ("user service", "email service") before any real boundary exists.

## The one-line reminder for beginners

> "Build the simplest thing your stack allows. Add a boundary the day a real change demands one — not before.
> You can always add structure later; removing the wrong structure is the expensive mistake."
