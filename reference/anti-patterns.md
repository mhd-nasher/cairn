# Anti-Patterns

> This file catalogs every named anti-pattern, smell, and violation in the Cairn canon. For each: the name, what it is, the rules it breaks, and how to remediate.

---

## Big Ball of Mud

**Implementation Strategy**

**What it is:** An architecture without clear structure. No boundaries, no layers, no components. Everything is interconnected. The code is a tangled mess of dependencies.

**Rules broken:** R-001 (Dependency Rule), R-005 (ADP), R-016 (SRP), R-022 (CCP), R-024 (SDP), R-025 (SAP), R-027 (Leave Options Open)

**How to detect it:**
- The directory structure is organized by technical layer (`controllers/`, `models/`, `views/`) rather than by business function.
- There are no clear boundaries between business rules and technical details.
- The database schema is known throughout the codebase.
- Framework annotations appear in business objects.
- Circular dependencies exist between packages or modules.

**How to remediate:**
1. Identify the use cases (business functions).
2. Draw boundaries around each use case.
3. Move business rules to the inner circles.
4. Move technical details to the outer circles.
5. Apply the Dependency Rule: dependencies point inward only.
6. Break circular dependencies using the Acyclic Dependencies Principle (ADP).

---

## Morning After Syndrome

**Component Coupling**

**What it is:** The build breaks because someone changed a dependency overnight. A team checks in code that compiles locally but breaks the build because another team changed a dependency that the first team did not know about.

**Rules broken:** R-005 (ADP — cycles in the dependency graph)

**How to detect it:**
- Builds break frequently after overnight check-ins.
- Teams are afraid to update their dependencies.
- Integration is a painful, scheduled event.
- The "weekly build" is a source of dread.

**How to remediate:**
1. Detect cycles in the component dependency graph.
2. Break the cycle by applying one of these techniques:
   - Apply the Dependency Inversion Principle (create an interface in the component that is depended upon).
   - Create a new component that both components depend on.
   - Use a Facade to break the cycle.
3. Ensure that all dependencies point in the direction of stability (SDP).

---

## Périphérique Anti-Pattern

**Implementation Strategy**

**What it is:** Infrastructure code bypasses the domain in a Ports & Adapters architecture. Instead of going through the ports, infrastructure code directly accesses the database or external services, bypassing the domain logic.

**Rules broken:** R-001 (Dependency Rule), R-002 (No Knowledge of Outer Circles), R-011 (No SQL in Use Cases), R-031 (Database Is a Detail)

**How to detect it:**
- Infrastructure code directly queries the database.
- The domain is bypassed for "performance" or "convenience."
- Business rules are duplicated in the infrastructure layer.
- The "adapter" is not really an adapter — it contains business logic.

**How to remediate:**
1. Ensure that all external access goes through the domain's ports.
2. Move business logic from the infrastructure to the domain.
3. Ensure that the adapters are thin — they only translate between the external format and the domain format.
4. Apply the Humble Object pattern: the adapter is humble, the domain is testable.

---

## App-titude Test

**Embedded Architecture**

**What it is:** Code that merely "works" but has no sound structure. It passes the functional tests but is untestable, unmaintainable, and tightly coupled to the hardware.

**Rules broken:** R-032 (Hardware Is a Detail), R-033 (Processor Is a Detail), R-034 (OS Is a Detail), R-014 (No Hardware Details in HAL Users), R-036 (Tests Are Parts of the System), R-037 (Design for Testability)

**How to detect it:**
- The code cannot be tested on a development machine.
- Hardware registers are accessed directly from business logic.
- Conditional compilation directives are scattered throughout the code.
- The code "works" but no one dares to change it.

**How to remediate:**
1. Introduce a Hardware Abstraction Layer (HAL).
2. Move all hardware-specific code to the HAL implementation.
3. Move all processor-specific code to the PAL implementation.
4. Move all OS-specific code to the OSAL implementation.
5. Test the business logic on the development machine using mock HAL/PAL/OSAL implementations.

---

## Software/Firmware Intermingling

**Embedded Architecture**

**What it is:** Hardware dependencies pollute all code. Business logic is mixed with register reads, interrupt handlers, and device-specific protocols. The code is "firmware" in the sense that it is inseparable from the hardware.

**Rules broken:** R-032 (Hardware Is a Detail), R-014 (No Hardware Details in HAL Users), R-015 (No Clutter in Interface Headers)

**How to detect it:**
- Business logic files contain `#include <hardware_register.h>`.
- Functions in the "business logic" layer call `read_register()` or `write_register()`.
- The build system has conditional compilation for different hardware variants.
- The code cannot be compiled or tested without the target hardware toolchain.

**How to remediate:**
1. Define a HAL interface in the business logic layer.
2. Move all hardware-specific code to a separate implementation layer.
3. Ensure that no business logic file includes a hardware header.
4. Use dependency injection to wire the HAL implementation at runtime (or compile time, but in a single, clean location).
5. Apply DRY to conditional compilation directives — centralize them.

---

## Framework-Centric Architecture

**Screaming Architecture; Frameworks Are Details**

**What it is:** The architecture is organized around the framework, not the use cases. The top-level directory structure screams "Spring!" or "Rails!" or "Django!" instead of "Order Processing!" or "Billing!"

**Rules broken:** R-012 (No Frameworks in Core Code), R-013 (Don't Marry the Framework), R-035 (Frameworks Are Tools), R-057 (Architecture Should Scream Intent)

**How to detect it:**
- The top-level packages are `controllers/`, `models/`, `views/`, `services/`, `repositories/`.
- Framework annotations (`@Entity`, `@Controller`, `@Service`) appear in business objects.
- The system cannot be tested without the framework running.
- The framework's configuration files are the primary source of architectural truth.

**How to remediate:**
1. Identify the use cases (business functions).
2. Create top-level packages named after the use cases (e.g., `order_processing/`, `billing/`).
3. Move framework-specific code to the outermost circle.
4. Ensure that business objects have no framework imports or annotations.
5. Use the framework as a plugin — the framework depends on the business rules, not the other way around.

---

## Database-Centric Architecture

**The Database Is a Detail**

**What it is:** The architecture is organized around the database schema. The database is the center of the system. Business rules are implemented as stored procedures, triggers, or ORM mappings. The system cannot function without the database.

**Rules broken:** R-011 (No SQL in Use Cases), R-031 (Database Is a Detail), R-001 (Dependency Rule), R-027 (Leave Options Open)

**How to detect it:**
- The database schema is designed before the use cases.
- Business logic is in stored procedures or triggers.
- Entities are annotated with ORM mappings (`@Entity`, `@Table`).
- The system cannot be tested without a real database.
- SQL is scattered throughout the use cases.

**How to remediate:**
1. Move business rules out of stored procedures and into the use cases layer.
2. Remove ORM annotations from entities. Use Data Mappers instead.
3. Define Gateway interfaces in the use cases layer.
4. Move all SQL to the Interface Adapters layer.
5. Test the use cases with in-memory Gateway implementations.

---

## Web-Centric Architecture

**The Web Is a Detail**

**What it is:** The architecture is organized around the web delivery mechanism. HTTP concepts (request, response, session, cookie, URL) leak into the business rules. The system cannot be delivered via any other mechanism.

**Rules broken:** R-030 (Web Is an IO Device), R-041 (System Ignorant of Delivery), R-001 (Dependency Rule)

**How to detect it:**
- Use cases accept HTTP request objects as parameters.
- Business logic checks `request.getSession()` or `request.getCookie()`.
- The system cannot be tested without a web server.
- JSON or XML parsing happens in the use cases layer.
- URL routing is the primary source of architectural truth.

**How to remediate:**
1. Define Request and Response Models as simple data structures (DTOs) in the use cases layer.
2. The web controller (Interface Adapter) converts HTTP requests to Request Models and Response Models to HTTP responses.
3. Ensure that no use case imports an HTTP library or web framework.
4. Test the use cases with simple data structures, not HTTP requests.

---

## Service-Oriented Architecture Without Source Code Decoupling

**Services: Great and Small**

**What it is:** The system is split into services at the deployment level, but the source code is still tightly coupled. Services share a data model, a library, or a database schema. The services are not independently deployable or developable.

**Rules broken:** R-053 (Services Are Not Always Best), R-054 (Prefer Component-Based Services), R-027 (Leave Options Open), R-028 (Leave Decoupling Mode Open)

**How to detect it:**
- Services share a database schema.
- Services share a library that is not versioned.
- A change to one service requires a coordinated deployment of multiple services.
- Services are tightly coupled at the source code level, even though they run in separate processes.

**How to remediate:**
1. Ensure that source code boundaries are clean before splitting into services.
2. Each service should own its data model and database schema.
3. Services should communicate through well-defined interfaces (ports and adapters).
4. Consider whether the system should be a monolith with clean internal boundaries, rather than prematurely distributed.

---

## Premature Elimination of Duplication

**Independence**

**What it is:** Two pieces of code that look the same are merged into a single module, even though they change for different reasons. This creates coupling between unrelated features.

**Rules broken:** R-040 (Verify Duplication Is Real), R-016 (SRP), R-022 (CCP)

**How to detect it:**
- A utility function is used by two different actors.
- A change to the utility function breaks one of the callers.
- The duplication was eliminated "to keep the code DRY" without considering the reasons for change.

**How to remediate:**
1. Ask: "Do these two pieces of code change for the same reasons?"
2. If not, allow the duplication to exist.
3. If they do change for the same reasons, extract the common code into a shared module that is owned by both actors.
4. Ensure that the shared module has a single responsibility (one actor).

---

## Stable Component Depending on Volatile Component

**Component Coupling**

**What it is:** A component that is heavily depended upon (stable, low I) depends on a component that changes frequently (volatile, high I). Every change to the volatile component forces the stable component to change.

**Rules broken:** R-024 (SDP — Depend in Direction of Stability)

**How to detect it:**
- A utility library is depended upon by many components.
- The utility library depends on a framework or database driver.
- When the framework or driver is updated, the utility library must change, forcing all its dependents to recompile/redeploy.

**How to remediate:**
1. Calculate the I (Instability) metric for both components.
2. The dependency arrow should point from the unstable component to the stable component.
3. Apply the Dependency Inversion Principle: create an interface in the stable component, and have the unstable component implement it.
4. Alternatively, create a new abstract component that both components depend on.

---

## Zone of Pain

**Component Coupling**

**What it is:** A component that is highly stable (I ≈ 0) and highly concrete (A ≈ 0). It is heavily depended upon and hard to change. Any change to it causes a cascade of recompilation and redeployment.

**Rules broken:** R-025 (SAP — Abstractness Proportional to Stability)

**How to detect it:**
- The component has high fan-in and low fan-out.
- The component has few or no abstract classes/interfaces.
- The component is changed frequently, causing widespread breakage.
- The D metric (distance from Main Sequence) is high.

**How to remediate:**
1. Introduce abstract interfaces into the component.
2. Make the component depend on abstractions, not concretions.
3. Move concrete implementations to less stable components.
4. The goal is to move the component toward the Main Sequence (A + I ≈ 1).

---

## Zone of Uselessness

**Component Coupling**

**What it is:** A component that is highly abstract (A ≈ 1) and highly unstable (I ≈ 1). It is full of interfaces but no one depends on it. It is dead code.

**Rules broken:** R-025 (SAP — Abstractness Proportional to Stability)

**How to detect it:**
- The component has many abstract classes/interfaces but few or no implementations.
- The component has low fan-in and high fan-out.
- No other component depends on it.
- The D metric (distance from Main Sequence) is high.

**How to remediate:**
1. Merge the component with a more stable component that needs its abstractions.
2. Or, make the component more stable by having other components depend on it.
3. Or, delete the component if it is truly unused.
4. The goal is to move the component toward the Main Sequence (A + I ≈ 1).

---

## LSP Violation at the Architectural Level

**LSP: The Liskov Substitution Principle**

**What it is:** A subtype is not substitutable for its base type in a cross-component context. The violation is harmless within a single component but becomes a time bomb when the types are used across a boundary.

**Rules broken:** R-018 (OCP), R-001 (Dependency Rule)

**How to detect it:**
- A component exposes a type hierarchy that is not truly substitutable.
- A client component breaks when it receives a subtype that behaves differently from the base type.
- The violation was "acceptable" within the team but breaks when the component is consumed by another team.

**How to remediate:**
1. Ensure that all subtypes are fully substitutable for their base types.
2. Use composition over inheritance where substitutability is unclear.
3. If the hierarchy is not substitutable, do not expose it across component boundaries.
4. Define a separate interface for cross-component use that captures only the substitutable behaviors.

---

## Shotgun Surgery

**Component Coupling (implied by Zone of Pain)**

**What it is:** A single change requires touching many components. This is the symptom of a stable component that is also concrete — the Zone of Pain.

**Rules broken:** R-025 (SAP), R-022 (CCP), R-016 (SRP)

**How to detect it:**
- A simple feature request requires changes to 10+ files across 5+ packages.
- Developers avoid making changes because the ripple effect is too large.
- The code review for a small change is enormous.

**How to remediate:**
1. Identify the stable component that is causing the cascade.
2. Introduce abstractions into the stable component.
3. Move concrete implementations to less stable components.
4. Ensure that the stable component is closed for modification and open for extension (OCP).

---

## The Hare's Overconfidence

**What Is Design and Architecture?**

**What it is:** The belief that "we can clean it up later; we just have to get to market first!" The belief that making messes is faster in the short term. The belief that a redesign from scratch will be better.

**Rules broken:** R-026 (Maximize Decisions Not Made), R-027 (Leave Options Open), R-001 (Dependency Rule)

**How to detect it:**
- The team is shipping features but the codebase is deteriorating.
- Developers are working overtime but productivity is declining.
- Management is pushing for speed over quality.
- The team is planning a "grand rewrite" to fix everything.

**How to remediate:**
1. Show the data: productivity is declining, cost per line of code is rising.
2. Emphasize: "The only way to go fast, is to go well."
3. Start applying the Dependency Rule and SOLID principles incrementally.
4. Do not allow a grand rewrite — the same overconfidence will drive the redesign into the same mess.
