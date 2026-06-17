# Modern Essentials

> The Cairn core is about *structure*. On its own, structure is largely silent on the
> production concerns that separate a clean-but-toy system from a world-class one: secrets, idempotency,
> observability, security, data integrity, contracts, and the lightweight DDD vocabulary that makes
> boundaries meaningful. This file adds those — each with **"applies when"** (so beginners don't
> over-apply) and **"where it lives"** (so it composes with the Dependency Rule instead of fighting it).
>
> These extend the Cairn core. They never override R-001 (inward-only).

## How these compose with the Cairn canon

The Dependency Rule still holds: **pure business rules in the center stay ignorant of all of this.** These
concerns live at the **boundary / adapter / Main** layer, or are passed *into* the core as plain values.
A pure pricing function never reads an env var, opens a log, or starts a transaction — its caller does.

---

## 1. Configuration & Secrets (12-Factor)

**What:** Keep config (URLs, keys, flags) out of code and out of the core. Inject it at the edge.
**Applies when:** always, the moment you have more than one environment or any secret.
**Where it lives:** read in Main / the entry point; pass values inward. Secrets in a secret manager
(env vars, GCP Secret Manager, Vault) — never hardcoded, never in the repo, never in the core.
**Beginner rule:** if a string would be different in prod vs dev, or would be dangerous to leak, it is
config — pass it in, don't bake it in.

## 2. Idempotency

**What:** The same request applied twice produces the same result, not double effects.
**Applies when:** anything that charges money, sends messages, or mutates state and can be retried
(payments, webhooks, queue consumers, "submit" buttons).
**Where it lives:** an idempotency key + a check at the adapter/use-case edge before the effect.
**Beginner rule:** assume every network call can fire twice. Before charging a card or creating an order,
ask "what if this runs again right now?" — if that's bad, add an idempotency key.

## 3. Observability — Logging, Metrics, Tracing

**What:** You can see what the running system is doing and why it failed.
**Applies when:** anything deployed; scale the depth to the stakes (a side project needs logs; a payment
system needs structured logs + metrics + traces).
**Where it lives:** at boundaries (handler entry/exit, adapter calls). **Not inside pure rules** — pass a
logger in, or return events the edge logs. Log decisions and errors with context (ids), never secrets/PII.
**Beginner rule:** log at the edges, keep the middle pure and silent. If you can't answer "why did this
order fail?" from logs, add structured logging at the boundary.

## 4. Error Handling Strategy

**What:** A deliberate split between *domain errors* (a booking is invalid) and *transport errors*
(HTTP 500, network timeout).
**Applies when:** always.
**Where it lives:** core throws/returns **domain errors** (plain, framework-free). The boundary
**translates** them into HTTP status / UI messages / retries. Never throw an `HttpsError` from a pure
function (it marries the framework — violates R-012).
**Beginner rule:** rules say *what went wrong in business terms*; the edge decides *how to tell the world*.

## 5. Input Validation & Contracts

**What:** Validate and parse untrusted input into typed, trusted values *before* logic runs.
**Applies when:** any external input (API, form, file, queue message).
**Where it lives:** at the boundary (e.g. a zod/pydantic schema), producing a clean DTO the core consumes.
The core then trusts its inputs and stays free of parsing concerns (R-004: no outer data formats inward).
**Beginner rule:** never let raw request data reach your business logic. Parse at the door; pass clean
objects in. "Never trust the client."

## 6. Security Basics

**What:** Authentication (who are you), authorization (what may you do), least privilege, secret hygiene,
no trust in client-supplied authority/amounts.
**Applies when:** any multi-user system or anything touching money/PII.
**Where it lives:** authn/authz at the boundary, *before* the use case runs. The use case may re-check
business-level permissions. Critical: **recompute money/authority on the server** — never charge the
amount the client sent (a classic tamper hole).
**Beginner rule:** check identity and permission at the edge; recompute anything sensitive server-side;
give every component the *least* access it needs.

## 7. Data Integrity — Transactions & Concurrency

**What:** Multi-step state changes are atomic; concurrent updates don't corrupt or double-apply.
**Applies when:** any state that must stay consistent under retries or concurrent callers (orders,
balances, inventory, "already paid?" checks).
**Where it lives:** transactions/optimistic-concurrency in the adapter/repository; the use case expresses
the invariant ("an order is paid at most once"). Read-decide-write across a non-transactional get/update
is a race — wrap it.
**Beginner rule:** if two users (or two retries) hitting this at once would be bad, you need a transaction
or a conditional update, not a plain read-then-write.

## 8. API & Contract Design

**What:** Stable, versioned interfaces between systems; explicit DTOs, not leaking internal models.
**Applies when:** any API consumed by another team, an app, or the public.
**Where it lives:** the interface-adapter layer maps internal entities ↔ external DTOs. Version the
contract; additive changes preferred; breaking changes get a new version.
**Beginner rule:** don't expose your database rows as your API. Map to a deliberate response shape you can
evolve without breaking callers.

## 9. Async, Events & Eventual Consistency

**What:** Queues, events, and background jobs for work that needn't be synchronous; accept that some data
converges over time.
**Applies when:** slow work (email, image processing), decoupling producers/consumers, or smoothing load.
Do **not** reach for it on a simple CRUD path.
**Where it lives:** events crossing a boundary carry plain data (R-004). The publisher depends on an
interface, not the broker. Make consumers idempotent (see §2).
**Beginner rule:** start synchronous. Add a queue only when a real latency or decoupling need appears —
async adds real complexity (ordering, retries, partial failure).

## 10. DDD-Lite — Vocabulary That Makes Boundaries Mean Something

A lightweight subset of Domain-Driven Design that pairs naturally with the Cairn canon:

- **Ubiquitous language:** name code with the business's own words (a `Booking`, not a `Record`). Use cases
  and entities should read like the domain.
- **Bounded context:** a region where a term has one precise meaning; a natural place to draw a macro
  boundary (or a service split — *when justified*, see over-engineering guardrails).
- **Aggregate:** a cluster of entities changed together under one invariant, with one entry point. Maps to
  a use case's consistency boundary (see §7).

**Applies when:** the domain has real complexity and multiple stakeholders. Skip the heavy DDD machinery
(repositories-per-aggregate, domain events everywhere) on a small app — keep only the vocabulary discipline.
**Where it lives:** shapes your entities and use-case names in the inner circles.

## 11. Schema & Migration Evolution

**What:** Data models change; plan for backward/forward-compatible migrations.
**Applies when:** any persistent store past v1.
**Where it lives:** migration scripts and versioned schemas at the data/adapter layer; the core works with
the current domain model. Prefer additive, reversible migrations; dual-write/dual-read during transitions.
**Beginner rule:** never break-change a live schema in place. Add the new field, migrate, then remove the
old one in a later step.

---

## Tailoring for beginners (Mode 0)

In the guided workflow, pull from this file **only the items whose "applies when" matches the project**.
A typical money/user app includes §1, §2, §5, §4, §3 — and skips §9, §10's heavy parts, and §8 if there's
no external API yet. State out loud what you're including and what you're deliberately skipping, so the
beginner learns the judgment, not just the checklist.
