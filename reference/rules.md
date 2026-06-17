# Cairn Rules

> This file is the enforceable rule layer of the Cairn architecture engine. Each rule has a stable ID, the rule text, and its rationale. These IDs are referenced by Cairn's checklists and workflows.

---

## MUST / MUST NOT (Non-Negotiables)

### R-001 — Dependency Rule: Inward Only
**Rule:** Source code dependencies must point only inward, toward higher-level policies.
**Rationale:** The inner circles contain the highest-level, most stable business rules. The outer circles contain volatile details. If inner circles depend on outer circles, a change to a detail forces a change to the business rules.

### R-002 — Dependency Rule: No Knowledge of Outer Circles
**Rule:** Nothing in an inner circle can know anything at all about something in an outer circle.
**Rationale:** Knowledge of an outer circle creates a dependency on it. The Dependency Rule forbids this.

### R-003 — Dependency Rule: No Names from Outer Circles
**Rule:** The name of something declared in an outer circle must not be mentioned by the code in an inner circle.
**Rationale:** Mentioning a name creates a compile-time dependency. Even an import statement is a violation.

### R-004 — Dependency Rule: No Outer Data Formats
**Rule:** Data formats declared in an outer circle should not be used by an inner circle.
**Rationale:** Data formats (e.g., JSON, XML, SQL result sets) are details of the outer circle. The inner circle should use simple data structures (DTOs, structs, maps) that are not tied to any outer technology.

### R-005 — ADP: No Cycles in Component Dependencies
**Rule:** Allow no cycles in the component dependency graph.
**Rationale:** Cycles force all components in the cycle to be released together, defeating independent testability, releasability, and understandability.

### R-006 — DIP: No References to Volatile Concrete Classes
**Rule:** Don't refer to volatile concrete classes. Refer to abstract interfaces instead.
**Rationale:** Stable, high-level policies should not depend on volatile, low-level details. The direction of dependency should be inverted.

### R-007 — DIP: No Derivation from Volatile Concrete Classes
**Rule:** Don't derive from volatile concrete classes.
**Rationale:** Derivation creates a compile-time dependency. If the base class changes, the derived class may break.

### R-008 — DIP: No Override of Concrete Functions
**Rule:** Don't override concrete functions.
**Rationale:** Overriding a concrete function is a fragile form of extension. The base class may change its implementation, breaking the override.

### R-009 — DIP: Never Mention Concrete and Volatile
**Rule:** Never mention the name of anything concrete and volatile.
**Rationale:** This is the most aggressive form of DIP. If a name is concrete and volatile, it must not appear in any stable code.

### R-010 — Services: No Physical Knowledge of Lower-Level Services
**Rule:** The source code of higher-level services must not contain any specific physical knowledge (e.g., a URI) of any lower-level service.
**Rationale:** Physical knowledge creates a deployment-time dependency. The higher-level service cannot be moved or reconfigured without changing the lower-level service's URI.

### R-011 — Database: No SQL in Use Cases or Entities
**Rule:** No code inward of the Interface Adapters layer should know anything at all about the database. If the database is SQL, all SQL should be restricted to the Interface Adapters layer. We do not allow SQL in the use cases layer.
**Rationale:** The database is a detail. The use cases and entities are high-level policy. SQL is a low-level detail.

### R-012 — Frameworks: No Frameworks in Core Code
**Rule:** Don't let frameworks into your core code. Your business objects should not know about Spring, Rails, Django, React, or any other framework.
**Rationale:** Frameworks are volatile. They evolve rapidly. They may become obsolete. If business rules depend on a framework, the business rules are volatile too.

### R-013 — Frameworks: Don't Marry the Framework
**Rule:** Don't marry the framework!
**Rationale:** Using a framework is fine. Letting the framework dictate your architecture is not. The framework should be a plugin, not a spouse.

### R-014 — Embedded: No Hardware Details in HAL Users
**Rule:** Don't reveal hardware details to the user of the HAL.
**Rationale:** The Hardware Abstraction Layer exists to hide hardware details. If users of the HAL see hardware details, the abstraction is broken.

### R-015 — Embedded: No Clutter in Interface Headers
**Rule:** Don't clutter interface header files with data structures needed only by the implementation.
**Rationale:** Interface headers are part of the contract. Implementation details in the header leak information to the user.

---

## SHOULD / SHOULD NOT (Strong Preferences)

### R-016 — SRP: One Actor per Module
**Rule:** A module should be responsible to one, and only one, actor.
**Rationale:** A module serving multiple actors suffers from accidental duplication and merge conflicts. The best structure is influenced by the social structure of the organization (Conway's Law).

### R-017 — SRP: Separate Code for Different Actors
**Rule:** Separate the code that different actors depend on.
**Rationale:** If two actors depend on the same module, a change for one actor may break the other.

### R-018 — OCP: Open for Extension, Closed for Modification
**Rule:** A software artifact should be open for extension but closed for modification.
**Rationale:** The most important reason to change a system is to add new features. If adding a feature requires touching existing, working code, the risk of breakage is high.

### R-019 — OCP: Directional Control
**Rule:** If component A should be protected from changes in component B, then component B should depend on component A.
**Rationale:** The interface between them should be owned by A. New features are added by extending B, not by modifying A.

### R-020 — ISP: Don't Depend on Things You Don't Use
**Rule:** Depending on something that carries baggage that you don't need can cause you troubles that you didn't expect.
**Rationale:** Unnecessary dependencies cause unnecessary recompilation, redeployment, and fragility.

### R-021 — REP: Granule of Reuse Is Granule of Release
**Rule:** The granule of reuse is the granule of release.
**Rationale:** Reuse requires trust. Trust requires tracking. Tracking requires releases. Therefore, the unit of reuse is the unit of release.

### R-022 — CCP: Gather by Change Reason
**Rule:** Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons.
**Rationale:** If a component contains classes that change for different reasons, the component will be released more often than necessary, causing cascading work.

### R-023 — CRP: Don't Force Unnecessary Dependencies
**Rule:** Don't force users of a component to depend on things they don't need.
**Rationale:** If a component depends on another component, it should depend on every class in that component — otherwise, the dependency is too broad.

### R-024 — SDP: Depend in the Direction of Stability
**Rule:** Depend in the direction of stability.
**Rationale:** Volatile components should not be depended upon by stable components. If a stable component depends on a volatile one, every change to the volatile component forces the stable component to change.

### R-025 — SAP: Abstractness Proportional to Stability
**Rule:** A component should be as abstract as it is stable.
**Rationale:** Stable components are hard to change. To make them easy to extend without changing them, they should be abstract.

### R-026 — Architecture: Maximize Decisions Not Made
**Rule:** A good architect maximizes the number of decisions not made.
**Rationale:** Every decision is a commitment. The more commitments, the fewer options. A good architect pretends that the decision has not been made, and shapes the system such that those decisions can still be deferred or changed for as long as possible.

### R-027 — Architecture: Leave Options Open
**Rule:** A good architecture makes the system easy to change, in all the ways that it must change, by leaving options open.
**Rationale:** The best architecture is the one that allows the system to be deployed as a monolith today and as microservices tomorrow, without changing the business rules.

### R-028 — Architecture: Leave Decoupling Mode Open
**Rule:** A good architecture leaves the decoupling mode open as an option.
**Rationale:** The architecture should not force a decision between monolith, components, services, threads, or processes. The business rules should be decoupled from the deployment mode.

### R-029 — Boundaries: The IO Is Irrelevant
**Rule:** The IO is irrelevant.
**Rationale:** The web is an IO device. The database is an IO device. Frameworks are IO devices. The business rules should not care about the IO mechanism.

### R-030 — Web: The Web Is an IO Device
**Rule:** The web is an IO device. The architecture of a system should treat the web as an IO device.
**Rationale:** The delivery mechanism changes (desktop → web → mobile → API). The business rules should not change with it.

### R-031 — Database: The Database Is a Detail
**Rule:** The database is a detail.
**Rationale:** The database is a technology for moving data across a boundary. It is not the architecture. The data model is not the architecture.

### R-032 — Hardware: The Hardware Is a Detail
**Rule:** The hardware is a detail.
**Rationale:** The hardware is a volatile detail. It may change from one processor to another, from one board to another. The business rules should not care.

### R-033 — Processor: The Processor Is a Detail
**Rule:** The processor is a detail.
**Rationale:** The processor is a volatile detail. It may change from one architecture to another. The business rules should not care.

### R-034 — OS: The Operating System Is a Detail
**Rule:** The operating system is a detail.
**Rationale:** The OS is a volatile detail. It may change from one version to another, from one vendor to another. The business rules should not care.

### R-035 — Frameworks: Frameworks Are Tools, Not Ways of Life
**Rule:** Frameworks are tools, not ways of life. Architectures should not be supplied by frameworks.
**Rationale:** A framework-centric architecture tells you nothing about the system's purpose. The architecture should be about the use cases.

### R-036 — Tests: Tests Are Parts of the System
**Rule:** Tests are not outside the system; they are parts of the system.
**Rationale:** If tests are treated as external, they may be coupled to the UI or database. If they are treated as internal, they drive the architecture toward testability.

### R-037 — Tests: Design for Testability Without GUI
**Rule:** Design the system so that business rules can be tested without using the GUI.
**Rationale:** GUI tests are slow and brittle. Business rules should be unit-testable in isolation.

### R-038 — Tests: Don't Depend on Volatile Things in Tests
**Rule:** Don't depend on volatile things.
**Rationale:** If tests depend on volatile components (database, UI, framework), the tests become brittle and slow.

### R-039 — Independence: Use Cases Divide the System
**Rule:** Use cases are a very natural way to divide the system.
**Rationale:** Use cases align with business functions. They are a natural axis of change and a natural boundary.

### R-040 — Independence: Verify Duplication Is Real
**Rule:** Resist the temptation to commit the sin of knee-jerk elimination of duplication. Make sure the duplication is real.
**Rationale:** Two pieces of code that look the same may change for different reasons. Premature elimination of duplication creates coupling.

### R-041 — Screaming Architecture: System Ignorant of Delivery
**Rule:** Your system should be as ignorant as possible about how it will be delivered.
**Rationale:** The delivery mechanism is a detail. The system should not know whether it is delivered via web, mobile, desktop, or API.

### R-042 — Screaming Architecture: Unit-Test Without Frameworks
**Rule:** If your architecture is all about the use cases, you should be able to unit-test all those use cases without any of the frameworks in place.
**Rationale:** Frameworks are details. If the use cases depend on frameworks, the architecture is framework-centric, not use-case-centric.

### R-043 — Package by Component: Minimize Public Types
**Rule:** The fewer public types you have, the smaller the number of potential dependencies.
**Rationale:** Every public type is a potential dependency. Minimizing public types minimizes the coupling surface area.

---

## CONSIDER / PREFER (Context-Dependent Advice)

### R-044 — Conway's Law: Consider Social Structure
**Rule:** Consider the best structure for a software system to be heavily influenced by the social structure of the organization that uses it.
**Rationale:** Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure.

### R-045 — Partial Boundaries: Use Facades
**Rule:** Consider using a Facade to provide a simplified interface to a complex subsystem.
**Rationale:** A Facade is a lightweight boundary. It reduces coupling without the cost of a full component boundary.

### R-046 — Partial Boundaries: Use Strategy Pattern
**Rule:** Consider using a Strategy pattern for one-dimensional boundaries.
**Rationale:** A Strategy pattern creates a one-dimensional boundary — one interface, one implementation. It is a low-cost way to invert a dependency.

### R-047 — DIP: Use Abstract Factory
**Rule:** Consider using an Abstract Factory to manage dependency on volatile concrete classes.
**Rationale:** The factory creates the concrete instances, but the client depends only on the abstract interface. The factory itself is a detail that lives in the outer circle.

### R-048 — Database: Defer Database Decision
**Rule:** Consider that the database is a detail that can be deferred.
**Rationale:** The database decision is one of the most commonly deferred decisions in software architecture. A good architecture allows the database to be chosen late in the project.

### R-049 — Web: Defer Web Decision
**Rule:** Consider that the web is a detail that can be deferred.
**Rationale:** The web decision is a delivery detail. A good architecture allows the system to be delivered via web, mobile, desktop, or API without changing the business rules.

### R-050 — Frameworks: Defer Framework Decision
**Rule:** Consider that frameworks are details that can be deferred.
**Rationale:** The framework decision is a detail. A good architecture allows the framework to be chosen late in the project, or changed mid-project.

### R-051 — Functional: Consider Event Sourcing
**Rule:** Consider using Event Sourcing to achieve immutability at the architectural level.
**Rationale:** Event Sourcing stores state as a sequence of immutable events. This eliminates the need for mutable state at the architectural level.

### R-052 — Functional: Segregate Mutability
**Rule:** Consider segregating mutability to minimize the number of mutable objects.
**Rationale:** The fewer mutable objects, the fewer race conditions, deadlocks, and concurrency bugs.

### R-053 — Services: Services Are Not Always Best
**Rule:** Consider that services are not necessarily the best way to decouple.
**Rationale:** Services decouple at the process level but may be tightly coupled at the source code level. Source code decoupling is more important than process decoupling.

### R-054 — Services: Prefer Component-Based Services
**Rule:** Consider using component-based services rather than service-oriented architectures.
**Rationale:** Component-based services have clean source code boundaries. Service-oriented architectures may have clean process boundaries but messy source code boundaries.

### R-055 — Main: Main Is the Ultimate Detail
**Rule:** Consider that the Main component is the ultimate detail.
**Rationale:** Main is the dirtiest, most concrete, most volatile component. It lives in the outermost circle. Everything else is clean.

### R-056 — Partial Boundaries: Use When Full Boundary Is Too Expensive
**Rule:** Consider using partial boundaries (skip the last step, one-dimensional boundaries, facades) when a full boundary is too expensive.
**Rationale:** Boundaries have cost. If the boundary is premature, the system may be over-engineered. Partial boundaries are a pragmatic middle ground.

### R-057 — Screaming Architecture: Architecture Should Scream Intent
**Rule:** Consider that the architecture of a system should scream its intent.
**Rationale:** When you look at the top-level directory structure, you should be able to tell what the system does — not what framework it uses.
