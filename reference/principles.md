# Cairn Principles

> This file is the principle layer of the Cairn architecture engine. Each entry names a principle, states Cairn's definition, explains why it matters, and adds a concrete "applies when..." note. These principles are the canon Cairn applies when it reasons about any system design.

---

## The Goal of Software Architecture

**Section — What Is Design and Architecture?**

> *The goal of software architecture is to minimize the human resources required to build and maintain the required system.*

**Why it matters:** The measure of design quality is the measure of effort required to meet customer needs. If effort is low and stays low, the design is good. If effort grows with each release, the design is bad. Messy systems asymptotically approach zero productivity over time.

**Applies when...** Evaluating any architectural decision, trade-off, or refactoring proposal. Ask: "Does this reduce the long-term human effort required to build and maintain the system?"

---

## The Two Values of Software

**Section — A Tale of Two Values**

Every software system provides two values to stakeholders:
1. **Behavior** — what the system does (urgent but not always important)
2. **Architecture** — how easy the system is to change (important but never urgent)

**Why it matters:** Software was invented to be "soft" — easy to change. A system that works perfectly but is impossible to change becomes useless when requirements change. A system that does not work but is easy to change can be made to work and kept working. Cairn holds that you must fight for architecture over the urgency of features.

**Applies when...** Prioritizing work, negotiating with stakeholders, or deciding whether to take on technical debt. Use Eisenhower's Matrix: architecture is important; behavior is urgent.

---

## The Three Programming Paradigms

**Section — Programming Paradigms**

Cairn recognizes three paradigms, each of which *removes* a capability from the programmer:

1. **Structured Programming**: Imposes discipline on direct transfer of control. Removes unrestrained `goto`. Replaced with sequence, selection, and iteration. Enables functional decomposition and testable (falsifiable) units.
2. **Object-Oriented Programming**: Imposes discipline on indirect transfer of control. Removes unconstrained function pointers. Replaced with polymorphism. The true power of OO is dependency inversion through polymorphism.
3. **Functional Programming**: Imposes discipline on assignment. Removes unconstrained mutable state. Replaced with immutability. At the architectural level, this means segregating mutability and considering event sourcing.

**Why it matters:** At the architectural level, we use polymorphism to cross architectural boundaries, functional programming to impose discipline on data location and access, and structured programming as the algorithmic foundation of modules.

**Applies when...** Choosing languages, designing modules, or deciding how to manage state across boundaries.

---

## SOLID Principles (Class-Level Design Principles)

### SRP — The Single Responsibility Principle

> *A module should be responsible to one, and only one, actor.*

Cairn defines SRP not as "a module should do one thing" but in terms of **actors** — the users or stakeholders who drive change. A module that serves multiple actors will suffer from:
- Accidental duplication (different actors need the same data for different reasons)
- Merge conflicts (different actors' teams changing the same file)

**Why it matters:** The best structure for a software system is heavily influenced by the social structure of the organization that uses it (Conway's Law). Separate the code that different actors depend on.

**Applies when...** A class or module is being changed by multiple teams, or a single change affects unrelated features.

---

### OCP — The Open-Closed Principle

> *A software artifact should be open for extension but closed for modification.*

Cairn frames OCP as a directional control principle: if component A should be protected from changes in component B, then component B should depend on component A. The interface between them should be owned by A. New features are added by extending B, not by modifying A.

**Why it matters:** The most important reason to change a system is to add new features. If adding a feature requires touching existing, working code, the risk of breakage is high.

**Applies when...** Adding a new feature that touches an existing component. Ask: "Can I extend this without modifying it?"

---

### LSP — The Liskov Substitution Principle

> *Subtypes must be substitutable for their base types.*

Cairn emphasizes that LSP is not just about inheritance — it is about **substitutability** in any context where a type is expected. Violations of LSP at the class level become architectural time bombs when the types are used across component boundaries.

**Why it matters:** Violations of LSP break polymorphism, which is the mechanism we use to cross architectural boundaries. If a subtype cannot substitute for its base type, the dependency inversion that the architecture relies on collapses.

**Applies when...** Using inheritance, implementing interfaces, or designing any type hierarchy that will be used across a boundary.

---

### ISP — The Interface Segregation Principle

> *Don't depend on things you don't use.*

Depending on something that carries baggage you don't need can cause troubles you didn't expect. ISP is in part a language issue: statically typed languages force recompilation when unused dependencies change. Dynamically typed languages avoid this, but the principle still matters at the architectural level.

**Why it matters:** At the architectural level, depending on a module that contains more than you need can cause unnecessary redeployment and recompilation cascades.

**Applies when...** A client is forced to depend on a fat interface or module that includes functionality it does not use.

---

### DIP — The Dependency Inversion Principle

> *Depend on abstractions, not concretions.*

Cairn states DIP as a set of concrete prohibitions:
- Don't refer to volatile concrete classes; refer to abstract interfaces instead.
- Don't derive from volatile concrete classes.
- Don't override concrete functions.
- Never mention the name of anything concrete and volatile.

**Why it matters:** Stable, high-level policies should not depend on volatile, low-level details. The direction of dependency should be inverted so that details depend on abstractions.

**Applies when...** A high-level module directly imports or instantiates a low-level, volatile module (e.g., a database driver, a web framework class, a UI component).

---

## Component Cohesion Principles

### REP — The Reuse/Release Equivalence Principle

> *The granule of reuse is the granule of release.*

What is reused must also be released and tracked. A component cannot be reused unless it is tracked through a release process. The classes and modules grouped together in a component must be releasable together.

**Why it matters:** Reuse requires trust. Trust requires tracking. Tracking requires releases. Therefore, the unit of reuse is the unit of release.

**Applies when...** Grouping classes into a library, package, or component that will be consumed by other teams or systems.

---

### CCP — The Common Closure Principle

> *Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons.*

This is the component-level analog of SRP. A component should not have multiple reasons to change.

**Why it matters:** If a component contains classes that change for different reasons, the component will be released more often than necessary, causing cascading work for dependent teams.

**Applies when...** Organizing code into packages, modules, or components. Ask: "Do these classes change together?"

---

### CRP — The Common Reuse Principle

> *Don't force users of a component to depend on things they don't need.*

This is the component-level analog of ISP. If a component depends on another component, it should depend on every class in that component — otherwise, the dependency is too broad.

**Why it matters:** Unnecessary dependencies cause unnecessary recompilation, redeployment, and fragility.

**Applies when...** A component depends on another component but only uses a small fraction of its classes.

---

## Component Coupling Principles

### ADP — The Acyclic Dependencies Principle

> *Allow no cycles in the component dependency graph.*

If a cycle exists in the dependency graph, the components in the cycle cannot be tested, released, or understood independently. The "Morning After Syndrome" — build breaks because someone changed a dependency overnight — is a direct consequence of cycles.

**Why it matters:** Cycles force all components in the cycle to be released together, defeating the purpose of componentization.

**Applies when...** Any time components depend on each other. Use dependency analysis tools to detect and break cycles.

---

### SDP — The Stable Dependencies Principle

> *Depend in the direction of stability.*

A component should depend on components that are more stable than it is. Stability is measured by `I = Fan-out / (Fan-in + Fan-out)`. A component with `I = 0` is maximally stable; `I = 1` is maximally unstable.

**Why it matters:** Volatile components should not be depended upon by stable components. If a stable component depends on a volatile one, every change to the volatile component forces the stable component to change.

**Applies when...** Evaluating whether a dependency arrow points in the right direction. The arrow should point toward more stable components.

---

### SAP — The Stable Abstractions Principle

> *A component should be as abstract as it is stable.*

Stable components are hard to change. To make them easy to extend without changing them, they should be abstract. Abstractness is measured by `A = Na / Nc` (number of abstract classes / total classes). The ideal relationship is `A + I = 1` (the Main Sequence). The Zone of Pain is `(A ≈ 0, I ≈ 0)` — stable and concrete. The Zone of Uselessness is `(A ≈ 1, I ≈ 1)` — abstract and unused.

**Why it matters:** A stable component that is also concrete is a target for the Shotgun Surgery anti-pattern. An abstract component that no one uses is dead code.

**Applies when...** A component is both heavily depended upon and frequently changed, or a component is full of interfaces but has no implementations.

---

## The Dependency Rule

**Section — Sound Architecture**

> *Source code dependencies must point only inward, toward higher-level policies.*

Nothing in an inner circle can know anything at all about something in an outer circle. The name of something declared in an outer circle must not be mentioned by the code in an inner circle. Data formats declared in an outer circle should not be used by an inner circle.

**Why it matters:** The inner circles contain the highest-level, most stable business rules. The outer circles contain volatile details (UI, database, web, frameworks). If inner circles depend on outer circles, a change to a detail forces a change to the business rules.

**Applies when...** Every import statement, every constructor call, every data structure crossing a boundary. Ask: "Does this dependency point inward?"

---

## Policy and Level

**Section — Policy and Level**

**Level** is the distance from inputs and outputs. High-level policy is the business logic that is farthest from the IO. Low-level policy is the code that deals with the IO directly. The Dependency Rule says that low-level policy depends on high-level policy, not the other way around.

**Why it matters:** The web is an IO device. The database is an IO device. Frameworks are IO devices. They are all low-level details. The business rules are high-level policy. The architecture must protect the high-level policy from the low-level details.

**Applies when...** Deciding where a new piece of code belongs, or whether a dependency arrow points in the right direction.

---

## The Database Is a Detail

> *The database is a detail.*

Relational databases are a technology for moving data across a boundary. They are not the architecture. The data model is not the architecture. No code inward of the Interface Adapters layer should know anything about the database. If the database is SQL, all SQL should be restricted to the Interface Adapters layer.

**Why it matters:** The database is a volatile detail. It may change from relational to NoSQL to in-memory. The business rules should not care.

**Applies when...** A use case or entity directly imports an ORM, a SQL library, or a database-specific data structure.

---

## The Web Is a Detail

> *The web is an IO device.*

The web is a delivery mechanism. The architecture of the system should treat the web as an IO device. The system should be as ignorant as possible about how it will be delivered.

**Why it matters:** The delivery mechanism changes (desktop → web → mobile → API). The business rules should not change with it.

**Applies when...** A use case or entity knows about HTTP, REST, JSON, or web-specific frameworks.

---

## Frameworks Are Details

> *Don't marry the framework!*

Frameworks are tools, not ways of life. Architectures should not be supplied by frameworks. Your business objects should not know about Spring, Rails, Django, or React. Don't let frameworks into your core code. Use the framework, but don't let it use you.

**Why it matters:** Frameworks are volatile. They evolve rapidly. They may become obsolete. If your business rules depend on a framework, your business rules are volatile too.

**Applies when...** A framework annotation, base class, or import appears in an entity or use case.

---

## Screaming Architecture

> *The architecture of a system should scream its intent.*

When you look at the top-level directory structure and the top-level source files, you should be able to tell what the system does — not what framework it uses, not what database it uses, not what web server it uses. The architecture should be about the use cases.

**Why it matters:** A framework-centric architecture (e.g., `controllers/`, `models/`, `views/`) tells you nothing about the system's purpose. A use-case-centric architecture (e.g., `order_processing/`, `billing/`, `shipping/`) tells you everything.

**Applies when...** Naming top-level packages, directories, or modules. Ask: "Does this name describe a business function or a technical detail?"

---

## The Humble Object Pattern

**Section — Presenters and Humble Objects**

Split behaviors into two modules: one that is **humble** (hard to test, tightly coupled to a framework or device) and one that is **testable** (contains all the business logic). The humble module delegates to the testable module. Examples: Presenter/View, Database Gateway/ORM, Data Mapper/Entity, Service Listener/Use Case.

**Why it matters:** We want to test the business rules without the framework, database, or UI. The Humble Object pattern keeps the untestable code thin and delegates all decisions to testable code.

**Applies when...** A piece of code is hard to unit test because it depends on a framework, database, or UI. Extract the logic into a testable module and leave a thin humble wrapper.

---

## Plugin Architecture

**Section — Boundaries: Drawing Lines**

The core business rules are the stable center. The peripheral components (UI, database, web, frameworks) are plugins. The core does not know about the plugins. The plugins depend on the core. This is the architectural analog of the Dependency Rule.

**Why it matters:** Plugin architecture allows the system to be deployed in multiple configurations (with or without a web UI, with or without a database, with or without a particular framework).

**Applies when...** Deciding how to integrate a UI, database, or external service. The core should define interfaces; the peripherals should implement them.

---

## Independence

**Section — Independence**

A good architecture makes the system easy to change in all the ways it must change, by leaving options open. The architecture should leave the decoupling mode open as an option (monolith, components, services, threads, processes). Use cases are a natural way to divide the system. Resist the temptation to eliminate duplication prematurely — make sure the duplication is real.

**Why it matters:** The best architecture is the one that allows the system to be deployed as a monolith today and as microservices tomorrow, without changing the business rules.

**Applies when...** Deciding whether to use services, monoliths, or components. The architecture should not force the decision.

---

## Tests as System Components

**Section — The Test Boundary**

Tests are not outside the system; they are parts of the system. Design the system so that business rules can be tested without using the GUI. Don't depend on volatile things in tests. The Testing API should be a first-class architectural boundary.

**Why it matters:** If tests are tightly coupled to the UI or database, they become brittle and slow. If the system is designed for testability, the tests become a stable, fast feedback loop.

**Applies when...** Writing tests, designing the Testing API, or deciding whether a test should touch the database or UI.

---

## Embedded Architecture

**Section — Embedded Architecture**

The hardware is a detail. The processor is a detail. The operating system is a detail. Use HAL, PAL, and OSAL to abstract them. Don't reveal hardware details to the user of the HAL. Programming to interfaces and substitutability applies even at the firmware level. DRY conditional compilation directives.

**Why it matters:** Embedded systems often suffer from software/firmware intermingling, making them untestable off-target. A sound embedded architecture makes firmware testable on a development machine.

**Applies when...** Designing embedded or hardware-adjacent software. Ask: "Can I test this logic without the target hardware?"

---

## Partial Boundaries

**Section — Partial Boundaries**

When a full boundary is too expensive, use a partial boundary:
- **Skip the last step**: Create the interface and the implementation, but keep them in the same component.
- **One-dimensional boundaries**: Use a Strategy pattern — one interface, one implementation.
- **Facades**: Provide a simplified interface to a complex subsystem.

**Why it matters:** Boundaries have cost. If the boundary is premature, the system may be over-engineered. If the boundary is missing, the system may be under-engineered. Partial boundaries are a pragmatic middle ground.

**Applies when...** A full boundary (separate component, separate deployment) feels like overkill, but some separation is still needed.

---

## The Main Component

**Section — The Main Component**

The Main component is the ultimate detail. It is the entry point of the system. It creates the factories, sets up the dependency injection, and wires everything together. It is the dirtiest, most concrete, most volatile component. It lives in the outermost circle.

**Why it matters:** The Main component is the only place where the framework, database, and web are mentioned. Everything else is clean.

**Applies when...** Writing the `main()` function, the application entry point, or the dependency injection configuration.

---

## Services: Great and Small

**Section — Services: Great and Small**

Services are not necessarily the best way to decouple. The decoupling fallacy: services decouple at the process level but may be tightly coupled at the source code level. The fallacy of independent development and deployment: services often share a data model or library, making them not independent. Objects and component-based services are often better than service-oriented architectures.

**Why it matters:** Microservices are a deployment detail, not an architectural principle. The architecture should be decoupled at the source code level first; the deployment mode should be a secondary decision.

**Applies when...** Deciding whether to split a system into services. Ask: "Are the source code boundaries already clean? If not, services will not help."
