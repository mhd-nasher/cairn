# Cairn: New Design Workflow

> The step-by-step procedure Cairn follows when shaping a new system or service.

---

## Mode: New Design

Use this workflow when the user asks Claude to:
- Design a new system, service, or module
- Define module/layer boundaries for a greenfield project
- Choose an architecture for a new product
- Decide how to organize a new codebase
- Draw architectural boundaries for a new feature

---

## Step 1: Identify the Use Cases

**Goal:** The architecture should scream the intent of the system. The top-level structure should be organized around use cases, not technical layers.

**Actions:**
1. Ask the user: "What does this system do? List the primary use cases."
2. Name the top-level packages/directories after the use cases (e.g., `order_processing/`, `billing/`, `shipping/`).
3. **Rule check:** R-039 (Use Cases Divide the System), R-057 (Architecture Should Scream Intent).
4. **Anti-pattern check:** Framework-Centric Architecture (top-level packages named `controllers/`, `models/`, `views/`).

**Output:** A list of use cases and the proposed top-level package structure.

---

## Step 2: Separate Policy from Details

**Goal:** Identify what is policy (business rules) and what is details (IO, database, web, frameworks). Policy is the architecture; details are not.

**Actions:**
1. For each use case, identify the business rules (Entities and Use Cases).
2. Identify the delivery mechanisms (web, mobile, desktop, API).
3. Identify the data storage mechanisms (database, file system, cache).
4. Identify the frameworks (web framework, ORM, messaging, etc.).
5. **Rule check:** R-029 (IO Is Irrelevant), R-030 (Web Is an IO Device), R-031 (Database Is a Detail), R-032 (Hardware Is a Detail), R-033 (Processor Is a Detail), R-034 (OS Is a Detail), R-035 (Frameworks Are Tools).
6. **Anti-pattern check:** Database-Centric Architecture, Web-Centric Architecture, Framework-Centric Architecture.

**Output:** A list of policy (inner circles) and details (outer circles).

---

## Step 3: Draw the Boundaries

**Goal:** Draw boundaries between the inner circles (Entities, Use Cases) and the outer circles (Interface Adapters, Frameworks and Drivers). The Dependency Rule governs all crossings.

**Actions:**
1. Place Entities in the innermost circle. They are enterprise-wide critical business rules. They know nothing about the database, web, or frameworks.
2. Place Use Cases in the second circle. They are application-specific business rules. They depend on Entities but not on Interface Adapters.
3. Place Interface Adapters in the third circle. They convert data between Use Cases and external agencies. They depend on Use Cases and Entities.
4. Place Frameworks and Drivers in the outermost circle. They are the web framework, database, UI, and external tools. They depend on the inner circles.
5. **Rule check:** R-001 (Dependency Rule: Inward Only), R-002 (No Knowledge of Outer Circles), R-003 (No Names from Outer Circles), R-004 (No Outer Data Formats).
6. **Anti-pattern check:** Périphérique Anti-Pattern (infrastructure bypassing the domain).

**Output:** A boundary diagram with four concentric circles and the dependency arrows pointing inward.

---

## Step 4: Define the Interfaces (Ports)

**Goal:** The inner circles define the interfaces that the outer circles must implement. The inner circles do not know about the implementations.

**Actions:**
1. For each external dependency (database, web, messaging, external service), define an interface in the Use Cases or Entities layer.
2. The interface should be named after the business need, not the technology (e.g., `OrderRepository`, not `SqlOrderDao`).
3. The interface should use simple data structures (DTOs, structs, maps) — not framework-specific types.
4. **Rule check:** R-006 (No References to Volatile Concrete Classes), R-011 (No SQL in Use Cases), R-012 (No Frameworks in Core Code).
5. **Anti-pattern check:** Database-Centric Architecture (SQL in Entities), Framework-Centric Architecture (framework annotations in Entities).

**Output:** A list of interfaces (ports) with their signatures and the data structures they use.

---

## Step 5: Apply SOLID at the Class Level

**Goal:** The classes within each circle should follow the SOLID principles.

**Actions:**
1. **SRP:** Ensure each class is responsible to one actor. If a class is changed by multiple teams, split it.
2. **OCP:** Ensure each class is open for extension but closed for modification. Use polymorphism to add new behaviors without changing existing code.
3. **LSP:** Ensure all subtypes are substitutable for their base types. Do not expose non-substitutable hierarchies across boundaries.
4. **ISP:** Ensure no class depends on methods it does not use. Split fat interfaces into smaller, focused ones.
5. **DIP:** Ensure no class depends on volatile concrete classes. Depend on abstractions. Use factories or dependency injection.
6. **Rule check:** R-016 (SRP), R-018 (OCP), R-020 (ISP), R-006 (DIP).
7. **Anti-pattern check:** LSP Violation at the Architectural Level, Premature Elimination of Duplication.

**Output:** A class diagram for each circle, with SOLID annotations.

---

## Step 6: Apply Component Principles

**Goal:** Group classes into components (packages, modules, libraries) that are cohesive and loosely coupled.

**Actions:**
1. **REP:** Ensure the granule of reuse is the granule of release. Each component should be tracked through a release process.
2. **CCP:** Gather classes that change for the same reasons into the same component. Separate classes that change for different reasons.
3. **CRP:** Ensure no component forces its users to depend on things they don't need.
4. **ADP:** Ensure no cycles in the component dependency graph. Use a dependency analysis tool.
5. **SDP:** Ensure dependencies point in the direction of stability. Calculate I (Instability) for each component.
6. **SAP:** Ensure stable components are abstract. Calculate A (Abstractness) and D (Distance from Main Sequence) for each component.
7. **Rule check:** R-021 (REP), R-022 (CCP), R-023 (CRP), R-005 (ADP), R-024 (SDP), R-025 (SAP).
8. **Anti-pattern check:** Morning After Syndrome, Zone of Pain, Zone of Uselessness, Stable Component Depending on Volatile Component.

**Output:** A component diagram with cohesion and coupling metrics.

---

## Step 7: Design for Testability

**Goal:** The system should be testable without the GUI, database, or frameworks.

**Actions:**
1. Ensure that business rules can be tested without the GUI. Use Request and Response Models.
2. Ensure that business rules can be tested without the database. Use in-memory implementations of Gateways.
3. Ensure that business rules can be tested without the web framework. Use simple data structures, not HTTP requests.
4. Define a Testing API as a first-class architectural boundary.
5. **Rule check:** R-036 (Tests Are Parts of the System), R-037 (Design for Testability Without GUI), R-038 (Don't Depend on Volatile Things in Tests).
6. **Anti-pattern check:** App-titude Test (code that works but is untestable).

**Output:** A test plan showing which layers are tested with which dependencies.

---

## Step 8: Defer Decisions

**Goal:** A good architect maximizes the number of decisions not made. Defer the database, web, and framework decisions as long as possible.

**Actions:**
1. Do not choose a database in the first week. The database is a detail.
2. Do not choose a web framework in the first week. The web is a detail.
3. Do not choose a UI framework in the first week. The UI is a detail.
4. Shape the system so that these decisions can be deferred or changed at any time.
5. **Rule check:** R-026 (Maximize Decisions Not Made), R-027 (Leave Options Open), R-028 (Leave Decoupling Mode Open), R-048 (Defer Database Decision), R-049 (Defer Web Decision), R-050 (Defer Framework Decision).
6. **Anti-pattern check:** The Hare's Overconfidence ("we can clean it up later").

**Output:** A decision log showing which decisions are deferred and why.

---

## Step 9: Define the Main Component

**Goal:** The Main component is the ultimate detail. It wires everything together. It is the only place where the framework, database, and web are mentioned.

**Actions:**
1. Create a `Main` component (or `main()` function) in the outermost circle.
2. In Main, create the factories and set up dependency injection.
3. Wire the concrete implementations (database, web, framework) to the abstract interfaces.
4. Ensure that no other component knows about the concrete implementations.
5. **Rule check:** R-055 (Main Is the Ultimate Detail), R-047 (Use Abstract Factory).

**Output:** A wiring diagram showing how Main connects the concrete implementations to the abstract interfaces.

---

## Step 10: Review with Checklists

**Goal:** Ensure the design is complete and compliant before implementation begins.

**Actions:**
1. Run the **Design Review Checklist** (`checklists/design-review.md`).
2. For each checklist item, verify that the design satisfies the rule.
3. Mark any violations as blockers or risks.
4. Produce a design review report with findings, rule IDs, and remediation steps.

**Output:** A design review report with pass/fail status for each checklist item.

---

## Step 11: Produce the Architecture Decision Record (ADR)

**Goal:** Document the key architectural decisions for future reference.

**Actions:**
1. Use the ADR template (`templates/adr-template.md`).
2. Record the use cases, the boundary decisions, the deferred decisions, and the component structure.
3. Cite the relevant rules and principles.
4. Store the ADR in the project's documentation.

**Output:** A completed ADR document.

---

## Completion Criteria

The design is complete when:
- [ ] Use cases are identified and the top-level structure screams intent.
- [ ] Policy is separated from details.
- [ ] Boundaries are drawn and the Dependency Rule is satisfied.
- [ ] Interfaces (ports) are defined in the inner circles.
- [ ] SOLID principles are applied at the class level.
- [ ] Component principles are applied at the package level.
- [ ] The system is testable without the GUI, database, or frameworks.
- [ ] Database, web, and framework decisions are deferred.
- [ ] The Main component is defined and is the only place where concrete implementations are mentioned.
- [ ] The design review checklist is complete with no blockers.
- [ ] An ADR is produced and stored.
