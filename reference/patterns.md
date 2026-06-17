# Patterns

> This file catalogs every named pattern in the Cairn canon, with when to use it, how it works, and which rules it supports.

---

## Humble Object Pattern

**Presenters and Humble Objects**

**What it is:** Split behaviors into two modules: one that is **humble** (hard to test, tightly coupled to a framework or device) and one that is **testable** (contains all the business logic). The humble module delegates to the testable module.

**When to use it:**
- A piece of code is hard to unit test because it depends on a framework, database, or UI.
- You want to test the business rules without the framework, database, or UI.
- You need to keep the untestable code thin and delegate all decisions to testable code.

**How it works:**
1. Identify the behavior that is hard to test (e.g., a UI view, a database ORM, a framework callback).
2. Extract all the logic into a testable module (e.g., a Presenter, a Gateway, a Mapper).
3. The humble module becomes a thin wrapper that delegates to the testable module.

**Examples:**
- **Presenter / View**: The View is humble (tied to the UI framework). The Presenter is testable (contains all the presentation logic).
- **Database Gateway / ORM**: The ORM is humble (tied to the database). The Gateway is testable (contains all the data access logic).
- **Data Mapper / Entity**: The Mapper is humble (tied to the database schema). The Entity is testable (contains all the business rules).
- **Service Listener / Use Case**: The Listener is humble (tied to the message queue). The Use Case is testable (contains all the business logic).

**Rules supported:** R-036, R-037, R-038 (Tests as System Components)

---

## Plugin Architecture

**Boundaries: Drawing Lines**

**What it is:** The core business rules are the stable center. The peripheral components (UI, database, web, frameworks) are plugins. The core does not know about the plugins. The plugins depend on the core.

**When to use it:**
- You want the system to be deployable in multiple configurations (with or without a web UI, with or without a database, with or without a particular framework).
- You want to defer decisions about UI, database, and framework.
- You want to test the core business rules without any of the peripherals.

**How it works:**
1. Define the core business rules in the innermost circle (Entities, Use Cases).
2. Define interfaces for the peripherals in the Interface Adapters layer.
3. Implement the peripherals in the Frameworks and Drivers layer.
4. The core depends on the interfaces, not the implementations.

**Rules supported:** R-001, R-002, R-003, R-004 (Dependency Rule); R-029 (IO Is Irrelevant); R-027 (Leave Options Open)

---

## Facade Pattern

**Single Responsibility and Partial Boundaries**

**What it is:** Provide a simplified interface to a complex subsystem. The Facade is a lightweight boundary that reduces coupling without the cost of a full component boundary.

**When to use it:**
- A subsystem is complex and has many public types.
- You want to reduce the coupling surface area without creating a full boundary.
- You want to provide a simplified interface for common operations.

**How it works:**
1. Identify the complex subsystem.
2. Create a Facade class that exposes only the operations that clients need.
3. The Facade delegates to the subsystem's internal classes.
4. Clients depend only on the Facade, not on the subsystem's internal classes.

**Rules supported:** R-045 (Use Facades); R-043 (Minimize Public Types)

---

## Strategy Pattern

**Partial Boundaries**

**What it is:** A one-dimensional boundary using an interface and an implementation. The client depends on the interface; the implementation is a plugin.

**When to use it:**
- You want to invert a dependency but a full boundary is too expensive.
- You have a single volatile behavior that needs to be abstracted.
- You want to allow multiple implementations of the same behavior.

**How it works:**
1. Define an interface (Strategy) that captures the behavior.
2. Create one or more implementations of the interface.
3. The client depends on the interface, not the implementation.
4. The implementation is injected into the client at runtime.

**Rules supported:** R-046 (Use Strategy Pattern); R-006 (No References to Volatile Concrete Classes)

---

## Abstract Factory

**DIP: The Dependency Inversion Principle**

**What it is:** A factory that creates instances of concrete classes, but the client depends only on the abstract interface. The factory itself is a detail that lives in the outer circle.

**When to use it:**
- A client needs to create instances of a volatile concrete class.
- You want to invert the dependency so that the client depends on an abstract interface, not the concrete class.
- You want to centralize the creation logic for a family of related objects.

**How it works:**
1. Define an abstract interface for the product.
2. Define an abstract interface for the factory.
3. Create concrete implementations of the factory that create concrete products.
4. The client depends on the abstract factory and abstract product.
5. The concrete factory and product are injected at runtime.

**Rules supported:** R-047 (Use Abstract Factory); R-006, R-007, R-008, R-009 (DIP)

---

## Database Gateway

**Presenters and Humble Objects**

**What it is:** A polymorphic interface between use cases and the database. The Gateway is an interface defined in the use cases layer. The implementation is in the Interface Adapters layer.

**When to use it:**
- You want to decouple the use cases from the database.
- You want to test the use cases without a real database.
- You want to defer the database decision.

**How it works:**
1. Define a Gateway interface in the use cases layer.
2. The use cases depend on the Gateway interface, not the database.
3. Create an implementation of the Gateway in the Interface Adapters layer.
4. The implementation uses the database (SQL, ORM, etc.).
5. The Main component wires the Gateway implementation to the use cases.

**Rules supported:** R-011 (No SQL in Use Cases); R-031 (Database Is a Detail); R-036, R-037, R-038 (Tests)

---

## Data Mapper

**Presenters and Humble Objects**

**What it is:** An ORM system that maps between database tables and in-memory objects. The Data Mapper is a Humble Object — it is tied to the database schema and is hard to test. The Entity is testable.

**When to use it:**
- You need to persist entities to a relational database.
- You want to keep the entities clean of database annotations and SQL.
- You want to test the entities without the database.

**How it works:**
1. Define the Entity in the inner circle (pure business rules, no database knowledge).
2. Define the Data Mapper in the Interface Adapters layer (knows about the database schema).
3. The Data Mapper converts between the database representation and the Entity.
4. The Entity knows nothing about the Data Mapper.

**Rules supported:** R-011 (No SQL in Use Cases); R-031 (Database Is a Detail)

---

## Presenter / View

**Presenters and Humble Objects**

**What it is:** The View is the Humble Object (tied to the UI framework). The Presenter is testable (contains all the presentation logic). The Presenter formats the data from the use case into a form that the View can display.

**When to use it:**
- You want to test the presentation logic without the UI framework.
- You want to keep the UI framework out of the use cases.
- You want to support multiple UI technologies (web, mobile, desktop) with the same presentation logic.

**How it works:**
1. The Use Case produces a Response Model (simple data structure).
2. The Presenter takes the Response Model and formats it into a View Model.
3. The View takes the View Model and renders it.
4. The View is humble — it only renders. The Presenter is testable — it contains all the logic.

**Rules supported:** R-030 (Web Is an IO Device); R-035 (Frameworks Are Tools); R-036, R-037 (Tests)

---

## Event Sourcing

**Functional Programming**

**What it is:** Store state as a sequence of immutable events. The current state is derived by replaying the events. This eliminates the need for mutable state at the architectural level.

**When to use it:**
- You want to achieve immutability at the architectural level.
- You need a complete audit trail of all changes.
- You want to support temporal queries ("what was the state at time T?").
- You want to avoid the complexity of mutable state in a distributed system.

**How it works:**
1. Every change to the system is recorded as an immutable event.
2. Events are appended to an event log.
3. The current state is derived by replaying the events.
4. Events are never modified or deleted.

**Rules supported:** R-051 (Consider Event Sourcing); R-052 (Segregate Mutability)

---

## HAL / PAL / OSAL

**Embedded Architecture**

**What it is:** Hardware Abstraction Layer, Processor Abstraction Layer, and Operating System Abstraction Layer. These are interfaces that hide the details of the hardware, processor, and OS from the business rules.

**When to use it:**
- You are writing embedded or hardware-adjacent software.
- You want to test the business logic on a development machine, not the target hardware.
- You want to support multiple hardware platforms, processors, or OS versions.

**How it works:**
1. Define the HAL interface in the inner circle (business rules).
2. Create a HAL implementation in the outer circle (hardware-specific).
3. The business rules depend on the HAL interface, not the hardware.
4. The Main component wires the HAL implementation to the business rules.
5. Repeat for PAL and OSAL.

**Rules supported:** R-032 (Hardware Is a Detail); R-033 (Processor Is a Detail); R-034 (OS Is a Detail); R-014 (No Hardware Details in HAL Users)

---

## Skip the Last Step (Partial Boundary)

**Partial Boundaries**

**What it is:** Create the interface and the implementation, but keep them in the same component. This is a partial boundary — the code is separated but not deployed separately.

**When to use it:**
- A full boundary (separate component, separate deployment) feels like overkill.
- You want to keep the option to extract the boundary later.
- You want to reduce coupling without the cost of a full boundary.

**How it works:**
1. Define the interface in a separate file/package within the same component.
2. Implement the interface in another file/package within the same component.
3. Clients depend on the interface, not the implementation.
4. Later, if needed, the interface and implementation can be moved to separate components.

**Rules supported:** R-056 (Use Partial Boundaries When Too Expensive)

---

## One-Dimensional Boundary (Strategy Pattern)

**Partial Boundaries**

**What it is:** A partial boundary using the Strategy pattern — one interface, one implementation. This is the simplest form of boundary.

**When to use it:**
- You have a single volatile behavior that needs to be abstracted.
- A full boundary is too expensive.
- You want to invert a dependency with minimal ceremony.

**How it works:**
1. Define an interface that captures the single behavior.
2. Create an implementation of the interface.
3. The client depends on the interface, not the implementation.
4. The implementation is injected into the client.

**Rules supported:** R-046 (Use Strategy Pattern); R-056 (Use Partial Boundaries)

---

## Package by Component

**Implementation Strategy**

**What it is:** Organize code into top-level packages that reflect business components (e.g., `order_processing/`, `billing/`, `shipping/`), not technical layers (e.g., `controllers/`, `models/`, `views/`). Each package contains all the code for that component — entities, use cases, interface adapters, and framework-specific code.

**When to use it:**
- You want the architecture to scream its intent.
- You want to minimize the number of public types.
- You want to align the code structure with the business structure.

**How it works:**
1. Identify the business components (use cases).
2. Create a top-level package for each component.
3. Place all the code for that component inside the package.
4. Keep the package's public API small and stable.
5. Hide implementation details inside the package.

**Rules supported:** R-057 (Architecture Should Scream Intent); R-043 (Minimize Public Types); R-039 (Use Cases Divide the System)

---

## Ports and Adapters (Hexagonal Architecture)

**Implementation Strategy**

**What it is:** An architecture where the domain is at the center, and all external interactions go through ports (interfaces) and adapters (implementations). The domain defines the ports; the adapters implement them.

**When to use it:**
- You want to decouple the domain from all external technologies (UI, database, web, messaging).
- You want to test the domain without any external dependencies.
- You want to support multiple UIs, databases, or delivery mechanisms.

**How it works:**
1. Define the domain in the center (Entities, Use Cases).
2. Define ports (interfaces) for each external interaction.
3. Create adapters (implementations) for each external technology.
4. The domain depends on the ports, not the adapters.
5. The adapters depend on the domain and the ports.

**Rules supported:** R-001, R-002, R-003, R-004 (Dependency Rule); R-027 (Leave Options Open); R-029 (IO Is Irrelevant)
