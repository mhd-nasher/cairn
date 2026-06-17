# Stack Profiles — Apply/Suppress per Technology

> **Load this in Step 0 of every workflow.** Cairn's macro rules ("the web is an IO device",
> "the database is a detail", "defer the framework") are *correct in general* but a poor fit for stacks
> where the framework IS the deployment model. Applying them blindly is the #1 cause of over-engineering.
> This file maps each common stack to the rules that **APPLY**, the rules to **SUPPRESS** (with the
> reason), and the **default boundary level** a beginner should start with.
>
> Rule of thumb: the rules about *internal code health* (SRP, no cycles, keep logic pure & testable, point
> dependencies inward) apply almost everywhere. The rules about *swapping infrastructure* apply only when
> the infrastructure is genuinely swappable.

## How to read the boundary level

- **Minimal** — 2 layers: `core/` (pure rules) + `adapters/` (plumbing). One direction: adapters → core.
- **Standard** — 3 layers: `entities/` + `usecases/` + `adapters/`.
- **Full** — the classic 4 circles: entities → use cases → interface adapters → frameworks & drivers.

---

## Profile: Serverless / Firebase Cloud Functions / AWS Lambda

*Detect:* `firebase.json`, `functions/`, `serverless.yml`, `template.yaml`, handlers exported as `onCall`/`onRequest`/`handler`.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-001 inward-only, R-002/003/004 | **APPLY** | Keep the pure logic ignorant of the runtime; this is what makes it testable. |
| R-016 SRP, R-005 ADP (no cycles) | **APPLY** | Handlers rot into 300-line god-functions fast; split by reason-to-change. |
| R-011 no DB in core, R-037 testability | **APPLY (lightly)** | Extract pure functions (price, validation) so they test without Firestore/Stripe. |
| R-006 DIP / ports | **APPLY ONLY where you fake-for-tests or have 2 impls** | Otherwise call Firestore/Stripe directly — a port for a single fixed service is ceremony. |
| R-030 web is IO device, R-049 defer web | **SUPPRESS** | The handler *is* the delivery contract; it will never be delivered another way. |
| R-031 DB is a detail, R-048 defer DB | **SUPPRESS** | Firestore is a fixed managed service you will not swap; a swap-abstraction protects against nothing. |
| R-012/R-035 frameworks are details, R-050 defer framework | **SUPPRESS** | Firebase/Lambda IS the platform; abstracting `onCall`/`admin` away buys nothing. |
| R-055 Main is the ultimate detail | **APPLY (reframed)** | The handler file is your Main — the one place that touches the SDKs. Keep the rest pure. |

**Default boundary level: Minimal → Standard.** Beginner start: `core/` (pure: pricing, validation, policy)
+ the handler file (wires Firestore/Stripe). Add a 3rd layer only when use cases multiply.

---

## Profile: Mobile App — Flutter / React Native / native iOS/Android

*Detect:* `pubspec.yaml`, `android/` + `ios/`, `Podfile`, React Native `metro.config`.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-001 inward-only, R-016 SRP | **APPLY** | The UI is the most volatile layer; keep logic out of widgets. |
| R-023 Humble Object / Presenter (patterns) | **APPLY** | Keep widgets dumb; put formatting/decisions in testable view-models/presenters. |
| R-037 testability without GUI | **APPLY** | Business logic must test without pumping widgets. |
| R-006 DIP for services (repos behind interfaces) | **APPLY** | The network/DB layer changes; a repository interface is genuinely useful here. |
| R-031 DB is a detail | **APPLY (partial)** | Local cache vs remote vs offline are real alternative implementations — a repo abstraction earns its place. |
| R-030 web is IO device | **PARTIAL** | Treat the backend API as IO behind a service; don't leak HTTP types into logic. |
| R-012 no frameworks in core | **APPLY to domain only** | Domain models in plain Dart/Kotlin; Flutter/SwiftUI only in the UI layer. |

**Default boundary level: Standard.** Beginner start: `presentation/` (widgets+view-models) → `domain/`
(entities+usecases, pure) → `data/` (repos, API, cache). Dependencies point inward to `domain/`.

---

## Profile: Web Frontend / Next.js / SPA

*Detect:* `next.config.js`, `vite.config`, `app/` or `pages/`, React/Vue/Svelte.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-001, R-016 SRP, R-005 ADP | **APPLY** | Keep domain logic out of components; no import cycles. |
| R-023 Humble Object | **APPLY** | Components dumb; logic in hooks/services that test without rendering. |
| R-037 testability | **APPLY** | Pure logic testable without a DOM. |
| R-006 DIP for data fetching | **PARTIAL** | An API client behind an interface helps; don't over-abstract one fetch. |
| R-031/R-030 DB/web are details | **SUPPRESS** | The browser + your API ARE the platform; no swap to protect. |
| R-012 frameworks are details | **SUPPRESS for the app, APPLY for domain** | Pure domain logic shouldn't import React; the rest is React by definition. |

**Default boundary level: Minimal → Standard.** `lib/domain/` (pure) + `lib/services/` + components.

---

## Profile: Backend Monolith — Spring / Django / Rails / .NET / Express service

*Detect:* `pom.xml`/`build.gradle`, `manage.py`, `Gemfile`+Rails, `*.csproj`, a long-lived server app.

| Rule | Verdict | Reason |
|------|---------|--------|
| **Almost all rules** R-001…R-038 | **APPLY** | This is the stack the canon was written for; full Cairn architecture pays off. |
| R-031 DB is a detail, R-048 defer DB | **APPLY** | You genuinely might change DB/ORM; the repository boundary protects real change. |
| R-030 web is IO device, R-012 frameworks | **APPLY** | Keep domain free of Spring/Django so logic survives a framework upgrade/rewrite. |
| R-026 maximize decisions not made | **APPLY** | Defer DB/framework/UI; you have time and the payoff is real. |

**Default boundary level: Full** (for long-lived/team) **or Standard** (for a small service).

---

## Profile: Microservices / Distributed system

*Detect:* multiple services, `docker-compose` with many apps, k8s manifests, message brokers.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-005 ADP, R-024 SDP, R-021–R-023 component principles | **APPLY hard** | The service graph must be acyclic and depend toward stability; this is where these rules shine. |
| R-010 no physical knowledge of lower services | **APPLY** | Service discovery/config, not hardcoded URIs. |
| R-001 inward-only (within each service) | **APPLY** | Each service is internally a small Cairn architecture. |
| Over-layering *inside* a tiny service | **SUPPRESS** | A 200-line service does not need 4 internal circles. |
| Premature service-splitting | **SUPPRESS / WARN** | Don't split into services before a real scaling/team boundary exists — distributed monolith is worse than a monolith. |

**Default boundary level: Standard inside each service; the services themselves are the macro boundaries.**

---

## Profile: CLI tool / Library / SDK

*Detect:* a package with a public API, `bin/`, no server/DB.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-016 SRP, R-020 ISP, R-018 OCP | **APPLY** | A clean public API and small interfaces matter most here. |
| R-006 DIP for plugin points | **APPLY where extensibility is a goal** | Plugin architecture (R-010 plugin pattern) if users extend it. |
| R-030/R-031 web/DB are details | **SUPPRESS** | Usually no web or DB. |

**Default boundary level: Minimal.** Public API + internal core. Don't add layers a library doesn't need.

---

## Profile: Embedded / Firmware

*Detect:* C/C++ for MCUs, `platformio.ini`, RTOS, register-level code.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-032 hardware is a detail, R-033 processor, R-034 OS | **APPLY** | Clean embedded: separate firmware (hardware-aware) from software (portable). |
| R-014/R-015 (HAL, target-hardware boundary) | **APPLY** | A hardware abstraction layer is the key boundary. |
| R-031 DB is a detail | **N/A** | Usually no database. |

**Default boundary level: Standard** — software / HAL / firmware separation.

---

## Profile: Data / ML pipeline

*Detect:* notebooks, `dvc`, Airflow/DAGs, training scripts, heavy IO.

| Rule | Verdict | Reason |
|------|---------|--------|
| R-001 inward-only, R-037 testability | **APPLY** | Keep transforms pure so they test without the cluster. |
| R-016 SRP | **APPLY** | Separate extract / transform / load / train by reason to change. |
| R-030/R-031 web/DB details | **PARTIAL** | Sources/sinks behind interfaces help when they vary (S3 vs local vs warehouse). |

**Default boundary level: Minimal → Standard.** Pure transforms + IO adapters.

---

## If the stack is unknown or mixed

Default to **Minimal** boundaries and **APPLY only the internal-health rules** (R-001, R-016, R-005,
R-037). Suppress every "swap the infrastructure" rule until you confirm the infrastructure is actually
swappable. It is always cheaper to add a boundary later than to remove a wrong one.
