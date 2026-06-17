# Mode 0 — Guided Build for Beginners

> The headline workflow. For someone who says "I don't know how to design this." It is an **interview**:
> you ask plain-language questions, make the structural decisions *for* the user (explaining each one in
> human terms), draw the boundaries, name the actual files/folders, and — critically — tell them **when to
> stop**. No architecture vocabulary is required from the user. You translate everything.

## Operating principles for this mode

1. **One question at a time.** Never dump a checklist on a beginner. Ask, wait, react.
2. **Plain language only.** Say "the part that knows your business rules" not "the use-case layer."
   Introduce a term *after* the user already understands the idea, in parentheses.
3. **Decide for them, then explain.** A beginner can't choose between "partial boundary" and "full
   boundary." You choose, then say why in one sentence.
4. **Default to simple.** Apply the Anti-Over-Engineering Law (`reference/over-engineering-guardrails.md`)
   at every step. The first answer is always the *smallest* structure that works for their stack.
5. **Show a progress gauge every step** so they always know where they are.
6. **End with something concrete:** a folder tree they can create, an ADR, and a "what to do next" list.

---

## Step 0: Discovery

```
[██░░░░░░░░░░░░░░░░░░] 10% — Step 0/8: Understanding what you're building
```

Ask, in plain language:
1. "In one or two sentences, what does this app or service do?"
2. "What are you building it with — do you know the language/framework/database? (It's fine if you don't.)"
3. "Is this a quick solo project / MVP, or something a team will maintain for years?"

From the answers:
- Detect the stack and **load `reference/stack-profiles.md`** for the matching profile. Note which rules
  to SUPPRESS and the **default boundary level** for that stack.
- Set the **complexity budget**: solo/MVP → *minimal*; team/long-lived → *standard*; large/regulated → *full*.
- If they don't know the stack yet — good. Tell them: "Perfect, we'll design the logic first and pick the
  database/framework later — that's exactly the right order (R-026)."

**Output:** one-line summary you'll reuse: *"A [what] built on [stack], scoped as [budget]."*

---

## Step 1: Find the "jobs" the system does (use cases)

```
[████░░░░░░░░░░░░░░░░] 22% — Step 1/8: Listing what the system actually does
```

Ask: "What are the main things a user (or another system) can *do* with this?" Get verbs, not nouns —
"book a cleaning", "pay for an order", "cancel a booking".

- Each verb is a **use case**. These — not "models" or "controllers" — become your top-level folders.
- Explain: "We name folders after *what the app does*, so anyone opening the project instantly sees its
  purpose. That's called a screaming architecture (R-057)."

**Output:** a list of use cases → proposed top-level folders, e.g. `book_cleaning/`, `pay_order/`, `cancel_booking/`.

**STOP-guard:** if there's only one tiny job, say so — "one folder is enough here; don't invent layers."

---

## Step 2: Separate the rules from the plumbing

```
[██████░░░░░░░░░░░░░░] 35% — Step 2/8: Separating your logic from the plumbing
```

For each use case, sort everything into two buckets, in plain words:
- **The rules (your business logic):** the decisions only your app makes — "a booking under £10 isn't
  allowed", "commission is 20%". *This is the valuable part.*
- **The plumbing (details):** database, web/HTTP, the payment provider's SDK, the UI, files. *Replaceable.*

Explain: "We keep the rules clean and ignorant of the plumbing. The rules never import the database or the
framework (R-011, R-012). Why? So you can test your logic in seconds without a real database, and change
the database later without touching your rules."

**Stack-aware note:** if the profile says SUPPRESS R-031/R-030 (e.g. fixed Firebase), tell the truth:
"Your database is fixed, so we won't build a swap-the-database abstraction — that'd be wasted work
(over-engineering). We still keep the *logic* in pure functions so you can test it."

**Output:** for each use case, a two-column list: Rules | Plumbing.

---

## Step 3: Draw the layers (only as many as the budget allows)

```
[████████░░░░░░░░░░░░] 48% — Step 3/8: Drawing the layers
```

Translate the four circles into the *minimum* the stack needs. Use the profile's default boundary level:

- **Minimal (solo/MVP/serverless):** two layers — `core/` (rules, pure, no imports of plumbing) and
  `adapters/` (plumbing). That's it. One direction of dependency: adapters → core, never the reverse (R-001).
- **Standard (team app):** three — `entities/` (long-lived rules), `usecases/` (app-specific rules),
  `adapters/` (plumbing). Same inward-only rule.
- **Full (large/long-lived):** the classic four circles (entities → use cases → interface adapters →
  frameworks & drivers).

Explain the one rule that matters: "Arrows point **inward**. Plumbing can call your rules; your rules can
NEVER call the plumbing. That single rule is 80% of sound architecture (R-001)."

**STOP-guard:** never propose more layers than the budget. If unsure, choose fewer. Adding a layer later
is easy; removing a wrong one is painful.

**Output:** the chosen layer set + a one-line dependency rule.

---

## Step 4: Connect to plumbing through "ports" (only where you need to swap or test)

```
[██████████░░░░░░░░░░] 60% — Step 4/8: Defining the seams (ports)
```

For each piece of plumbing the rules must reach (save an order, charge a card), define a small interface
named after the *need*, not the tech: `OrderStore`, `PaymentCharger` — not `FirestoreDao`, `StripeClient`.

Explain: "The rules talk to `OrderStore` (a promise of what it does). The real Firestore code *implements*
that promise out in the plumbing. Now your tests can use a fake `OrderStore` in memory (R-006, R-011)."

**Anti-over-engineering check (apply hard here):** only create a port if —
- you will have a fake version for tests, OR
- a second real implementation exists/is imminent.
Otherwise call the plumbing directly and move on. Say so out loud: "No port here — you'll only ever use
Firestore for this and we test it another way; a port would be ceremony."

**Output:** the short list of ports that earned their place, with one-line signatures.

---

## Step 5: Make the rules testable

```
[████████████░░░░░░░░] 72% — Step 5/8: Making it testable
```

- Pull the pure decision logic into plain functions that take inputs and return outputs — no database, no
  HTTP, no SDK inside them. (e.g. `computePrice(...)`, `validateBooking(...)`.)
- Explain: "If you can test your money math without starting Firebase or Stripe, your architecture is
  working (R-037). If you can't, the logic is tangled in plumbing — pull it out."

**Output:** the list of pure functions to write first, each with one example test.

---

## Step 6: Add the world-class essentials that fit (not all of them)

```
[██████████████░░░░░░] 82% — Step 6/8: Adding the production essentials
```

Open `reference/modern-essentials.md` and pull ONLY the items whose "applies when" matches this project.
For a typical app handling money/users, that's usually:
- **Secrets/config** out of code (12-factor) — keys in env/secret manager.
- **Idempotency** on anything that charges money or mutates twice on retry.
- **Input validation** at the edge before logic runs.
- **Error handling**: rules throw domain errors; the edge translates them to HTTP/UI.
- **Logging** at the boundary, not inside pure rules.

Explain each in one line and skip the rest. **STOP-guard:** don't bolt on event sourcing, CQRS, or
microservices for a small app — note they exist and are out of scope for this budget.

**Output:** a short "essentials to include" list tailored to the project.

---

## Step 7: Wire it together in one place (Main)

```
[████████████████░░░░] 92% — Step 7/8: Wiring it all together
```

- There is exactly one place that knows the real database, framework, and keys, and plugs the real
  implementations into the ports: the entry point (`main`, the Cloud Function handler, `index.ts`).
- Explain: "Everything else stays ignorant of the concrete tech. Only this one file marries the
  framework (R-055). That's why the rest is testable and swappable."

**Output:** a description of the entry point and what it wires.

---

## Step 8: Deliver the concrete result

```
[████████████████████] 100% — Step 8/8: Done — here's your blueprint
```

Produce, concretely:
1. **A folder tree** the user can create right now (real names, matching their stack).
2. **A build order**: which files to write first (pure functions → ports → adapters → wiring).
3. **A short ADR** (`templates/adr-template.md`) recording the key decisions and what was deliberately
   left simple, citing rule IDs.
4. **A "you're done when" checklist** drawn from `checklists/design-review.md`, in plain language.
5. **One sentence of reassurance + the next step**: "This structure is correct and not over-built. Start
   with [first file]."

---

## Beginner translation cheat-sheet (use these phrasings)

| Cairn term | Say this to a beginner |
|-----------|------------------------|
| Entities / Use cases | "your business rules / what the app does" |
| Interface Adapters / Frameworks & Drivers | "the plumbing / the outside tech" |
| Dependency Rule | "arrows point inward — plumbing calls rules, never the reverse" |
| Port / Gateway | "a promise of what a piece of plumbing does, so you can fake it in tests" |
| Dependency Inversion | "the rules depend on a promise, not on the real Firebase/Stripe" |
| Defer decisions | "design the logic first, pick the database/framework later" |
| Humble Object | "keep the untestable bits (UI, SDK calls) thin and dumb" |

## What this mode must never do

- Never use jargon without translating it.
- Never propose more structure than the complexity budget allows.
- Never create a port/abstraction that can't name the change it protects against.
- Never claim the design is "secure" or "bug-free" — this mode produces *structure*. Tell the user to run a
  bug/security review separately before shipping anything that touches money or user data.
