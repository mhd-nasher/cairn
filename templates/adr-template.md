# Architecture Decision Record (ADR) Template

> Use this template to record architectural decisions. Each ADR should be concise, decision-focused, and traceable to the Cairn principles and rules.

---

## ADR-XXX: [Short Title of the Decision]

**Status:** Proposed / Accepted / Deprecated / Superseded by ADR-YYY

**Date:** YYYY-MM-DD

**Context:**
[Describe the forces at play, including technological, political, social, and project-local. Describe the problem the decision addresses.]

**Decision:**
[State the decision in a single, clear sentence. Be specific.]

**Consequences:**
[Describe the resulting context after applying the decision. List all consequences, both positive and negative.]

**Principles Applied:**
- [List the Cairn principles that support this decision, e.g., Dependency Rule, SRP, OCP, etc.]

**Rules Referenced:**
- [List the rule IDs that this decision satisfies or enforces, e.g., R-001, R-016, etc.]

**Anti-Patterns Avoided:**
- [List the anti-patterns this decision prevents, e.g., Framework-Centric Architecture, Database-Centric Architecture, etc.]

**Deferred Decisions:**
- [List any decisions that were intentionally deferred, per R-026 (Maximize Decisions Not Made).]

**Alternatives Considered:**
- [Describe the alternatives that were considered and why they were rejected.]

**Related ADRs:**
- [Link to related ADRs.]

---

## Example: ADR-001: Package by Component

**Status:** Accepted

**Date:** 2024-01-15

**Context:**
The current codebase is organized by technical layer (`controllers/`, `models/`, `views/`). This makes it impossible to tell what the system does by looking at the directory structure. It also creates a framework-centric architecture where the framework is the primary organizing principle.

**Decision:**
We will reorganize the codebase into top-level packages named after business components (e.g., `order_processing/`, `billing/`, `shipping/`). Each package will contain all the code for that component — Entities, Use Cases, Interface Adapters, and framework-specific code — with a small, stable public API.

**Consequences:**
- Positive: The architecture screams its intent. New developers can understand the system by looking at the top-level directories.
- Positive: The number of public types is minimized, reducing the coupling surface area.
- Negative: Some duplication may exist between components. We will verify that duplication is real before eliminating it (R-040).
- Negative: The reorganization is a large refactoring effort.

**Principles Applied:**
- Screaming Architecture
- Package by Component
- SRP
- CCP

**Rules Referenced:**
- R-057 (Architecture Should Scream Intent)
- R-039 (Use Cases Divide the System)
- R-043 (Minimize Public Types)
- R-040 (Verify Duplication Is Real)

**Anti-Patterns Avoided:**
- Big Ball of Mud
- Framework-Centric Architecture

**Deferred Decisions:**
- Whether to deploy as a monolith or as services (R-028).
- Which database to use (R-048).
- Which web framework to use (R-049).

**Alternatives Considered:**
- Package by Layer: Rejected because it screams "Spring!" instead of "Order Processing!"
- Package by Feature: Rejected because it does not provide enough encapsulation at the component level.
- Ports and Adapters: Accepted as the internal structure within each component, but not as the top-level organizing principle.

**Related ADRs:**
- ADR-002: Database Gateway Pattern
- ADR-003: Presenter/View Humble Object Pattern
