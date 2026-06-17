# Rules in Plain Language (+ When NOT to Apply)

> Every rule from `reference/rules.md`, translated into human words, with the column most rule sets leave
> out: **when NOT to apply it.** Beginners over-apply rules because no one tells them where a rule
> stops paying off. Cairn does. Pair it with `reference/stack-profiles.md` (which rules fit your stack)
> and `reference/over-engineering-guardrails.md` (the judgment).
>
> "When NOT" of `—` means: this one applies essentially everywhere; don't look for an excuse to skip it.

## The Dependency Rule (the heart — R-001 to R-004)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-001 | Important logic must not know about DB/UI/framework; only the outside knows the inside. | — (the one rule you never skip) |
| R-002 | Inner code knows *nothing* about outer code. | — |
| R-003 | Inner code doesn't even name an outer thing (no imports pointing outward). | Tiny scripts with no inner/outer split. |
| R-004 | Don't pass framework/DB-shaped data (JSON, SQL rows) into the core; use plain objects. | Trivial throwaway code. |

## Dependency Inversion & Services (R-006 to R-010)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-006 | Depend on a promise (interface), not on a volatile concrete class. | When there's one fixed impl and no test seam — calling it directly is fine (over-eng trap). |
| R-007 | Don't inherit from volatile concrete classes. | Stable base classes / framework-mandated patterns. |
| R-008 | Don't override concrete methods to change behavior. | Framework hooks designed to be overridden. |
| R-009 | Keep names of concrete-and-volatile things out of stable code. | Prototypes; the Main/wiring file (which is *meant* to name them). |
| R-010 | High-level services shouldn't hardcode a low-level service's address/URI. | Single-process apps with no remote services. |

## Frameworks & Embedded (R-012 to R-015)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-012 | Business logic must run without the framework loaded. | Suppress for the framework-shaped shell itself (a React app *is* React); apply to the domain only. |
| R-013 | Use the framework; don't let it dictate your whole design. | — |
| R-014 | Code using the hardware layer shouldn't see raw hardware details. | Non-embedded projects. |
| R-015 | Keep hardware interface headers clean of implementation clutter. | Non-embedded projects. |

## SOLID (R-016 to R-020)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-016 | One module = one reason to change = one stakeholder/actor. | — (cheap, always worth it) |
| R-017 | Split code that different teams/actors change for different reasons. | When it's genuinely one actor — don't split for splitting's sake. |
| R-018 | Add new behavior by extending, not editing existing code. | When there's no real variation yet — don't pre-build extension points (YAGNI). |
| R-019 | Point dependencies so high-level policy is protected from low-level change. | — |
| R-020 | Don't make callers depend on methods they don't use; small interfaces. | Don't shatter a cohesive interface into one-method fragments. |

## Component Cohesion & Coupling (R-021 to R-025)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-021 | The unit you reuse is the unit you release/version. | Single-app code with no reuse/release story yet. |
| R-022 | Put things that change together in the same component. | — |
| R-023 | Don't drag users into depending on stuff they don't need. | — |
| R-024 | Volatile components depend on stable ones, never the reverse. | — (especially at service/module scale) |
| R-025 | The more depended-upon a component is, the more abstract it should be. | Tiny codebases where formal stability metrics are overkill. |

## Keeping Options Open (R-026 to R-028)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-026 | Delay hard-to-reverse choices (DB, framework, UI) as long as you can. | When the choice is fixed/given (e.g. mandated Firebase) — then commit and move on. |
| R-027 | Shape the system so big decisions stay changeable. | When a decision is genuinely permanent. |
| R-028 | Keep the option to decouple harder (in-process → service) later. | When you already know the final topology. |

## Details: IO, Web, DB, Hardware, OS, Frameworks (R-029 to R-035)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-029 | How data gets in/out is irrelevant to the rules. | — |
| R-030 | The web is just a delivery device; logic shouldn't care. | **Suppress** for thin serverless handlers / SPA shells — the web IS the platform there. |
| R-031 | The database is a plug-in detail, designed around the logic. | **Suppress** when the DB is a fixed managed service you'll never swap. |
| R-032 | Hardware is a detail behind an abstraction. | Non-embedded. |
| R-033 | The processor is a detail. | Non-embedded. |
| R-034 | The OS is a detail behind an abstraction. | Most app code that targets one runtime. |
| R-035 | Frameworks are tools, not religions; stay able to leave. | Suppress the "stay able to leave" effort when the framework is the locked platform. |

## Tests (R-036 to R-038)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-036 | Tests are first-class parts of the system, designed in. | — |
| R-037 | You can test business logic without the GUI/DB/framework. | — (this is the payoff of all the above) |
| R-038 | Tests shouldn't depend on volatile things (fragile selectors, real network). | — |

## Independence & Screaming Architecture (R-039 to R-042, R-057)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-039 | Organize top-level folders by what the app *does* (use cases), not by tech layer. | A library/CLI may organize by public API instead. |
| R-040 | Before removing "duplication", check it's real (same reason to change), not accidental. | — |
| R-041 | The system shouldn't reveal its delivery mechanism in its top structure. | Tiny apps. |
| R-042 | You can unit-test without spinning up frameworks. | — |
| R-057 | The folder structure should shout the system's purpose. | — |

## Packaging, Conway, Partial Boundaries, Factories (R-043 to R-047, R-056)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-043 | Minimize public types in a component; hide internals. | — |
| R-044 | Team/org shape will mirror your architecture — plan for it. | Solo projects (note it for when you grow). |
| R-045 | Use a facade as a cheap, partial boundary. | When you need a full boundary, or none at all. |
| R-046 | Use Strategy for a partial boundary. | When there's only one strategy ever. |
| R-047 | Use an abstract factory to create concretes without naming them in the core. | When direct construction in Main is simpler and there's one impl. |
| R-056 | Use a partial (cheaper) boundary when a full one isn't worth it. | When the full boundary is genuinely needed. |

## Defer Decisions (R-048 to R-050)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-048 | Don't pick the database week one. | When it's fixed/given. |
| R-049 | Don't pick the web framework week one. | When it's fixed/given (serverless platform chosen). |
| R-050 | Don't pick the framework week one. | When it's fixed/given. |

## Functional, Services, Main (R-051 to R-055)

| ID | In human words | When NOT to apply |
|----|----------------|-------------------|
| R-051 | Consider event sourcing (store events, derive state). | Most CRUD apps — heavy; only when audit/replay is a real need. |
| R-052 | Separate mutable state from immutable; shrink the mutable part. | — (cheap discipline) |
| R-053 | Services aren't automatically the best decomposition. | — (don't assume microservices = good) |
| R-054 | Prefer component-based services (clean components inside services). | — |
| R-055 | One place (Main/entry/handler) wires the real DB, framework, keys. | — (always have a single wiring point) |

## The two rules to internalize first (if you remember nothing else)

1. **R-001** — arrows point inward; rules never import plumbing.
2. **The Anti-Over-Engineering Law** — never add a boundary you can't justify with a concrete, real change.

Everything else is elaboration on those two, filtered through your stack profile.
