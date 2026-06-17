# Glossary

> This file defines the Cairn canon's key terms in its own framing. No generic industry definitions are substituted.

---

## A

**Abstractness (A)** — A metric measuring the abstractness of a component. `A = Na / Nc`, where `Na` is the number of abstract classes and interfaces, and `Nc` is the total number of classes in the component. A component with `A = 0` is entirely concrete; `A = 1` is entirely abstract. See also: SAP, Main Sequence, Zone of Pain, Zone of Uselessness.

**Actor** — A group of one or more stakeholders who require a change in the system for the same reason. The Single Responsibility Principle states that a module should be responsible to one, and only one, actor. See also: SRP.

**ADP (Acyclic Dependencies Principle)** — Allow no cycles in the component dependency graph. Cycles force all components in the cycle to be released together, defeating independent testability, releasability, and understandability. See also: Component Coupling, Morning After Syndrome.

**Architecture** — The shape of the system, the outward appearance, the layout of the spaces and rooms, and all the low-level details that support the high-level decisions. There is no difference between design and architecture; they form a continuous fabric. See also: The Goal of Software Architecture.

**Axis of Change** — The line along which a system is likely to change. Boundaries should be drawn along axes of change. See also: Boundaries.

## B

**Behavior** — The first value of software: what the system does. Behavior is urgent but not always important. See also: The Two Values of Software, Eisenhower's Matrix.

**Big Ball of Mud** — An architecture without clear structure. No boundaries, no layers, no components. Everything is interconnected. See also: Anti-Patterns.

**Boundary** — A separation between software elements. Boundaries are drawn to separate things that are important from things that are not. The IO is irrelevant; the web is an IO device; the database is an IO device. See also: Boundaries: Drawing Lines, Boundary Anatomy.

**Boundary Crossing** — The act of passing control or data across a boundary. At the architectural level, we use polymorphism to cross boundaries. See also: Dependency Rule, Plugin Architecture.

## C

**CCP (Common Closure Principle)** — Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons. The component-level analog of SRP. See also: Component Cohesion.

**Cairn Architecture** — An architecture with four concentric circles: Entities, Use Cases, Interface Adapters, Frameworks and Drivers. Source code dependencies point only inward. See also: The Dependency Rule.

**Component** — A unit of deployment. A collection of classes and modules that are released together. See also: Component Principles, Component Cohesion, Component Coupling.

**Component Cohesion** — The principles that govern how classes are grouped into components: REP, CCP, CRP. See also: Component Principles.

**Component Coupling** — The principles that govern how components depend on each other: ADP, SDP, SAP. See also: Component Principles.

**Conway's Law** — Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure. See also: SRP, Independence.

**CRP (Common Reuse Principle)** — Don't force users of a component to depend on things they don't need. The component-level analog of ISP. See also: Component Cohesion.

## D

**D (Distance from Main Sequence)** — A metric measuring how far a component is from the Main Sequence. `D = |A + I - 1|`. A component with `D = 0` is on the Main Sequence; `D = 1` is in the Zone of Pain or Zone of Uselessness. See also: Main Sequence, SAP, SDP.

**Data Mapper** — An ORM system that maps between database tables and in-memory objects. The Data Mapper is a Humble Object — tied to the database schema and hard to test. The Entity is testable. See also: Humble Object Pattern, Presenters and Humble Objects.

**Database Gateway** — A polymorphic interface between use cases and the database. The Gateway is an interface defined in the use cases layer; the implementation is in the Interface Adapters layer. See also: Humble Object Pattern, The Database Is a Detail.

**Dependency Inversion** — The true power of object-oriented programming. High-level modules should not depend on low-level modules; both should depend on abstractions. See also: DIP, OCP, Plugin Architecture.

**Dependency Rule** — Source code dependencies must point only inward, toward higher-level policies. Nothing in an inner circle can know anything at all about something in an outer circle. See also: Cairn Architecture, Policy and Level.

**Detail** — Something that is not the architecture. The database is a detail. The web is a detail. Frameworks are details. The hardware is a detail. Details are volatile and should be deferred. See also: Policy and Level.

**DIP (Dependency Inversion Principle)** — Depend on abstractions, not concretions. Don't refer to volatile concrete classes; don't derive from them; don't override concrete functions; never mention the name of anything concrete and volatile. See also: SOLID, Stable Abstractions.

## E

**Eisenhower's Matrix** — A matrix of importance versus urgency. Architecture is important but not urgent; behavior is urgent but not always important. Developers must fight for architecture over the urgency of features. See also: The Two Values of Software.

**Entities** — Enterprise-wide Critical Business Rules. The innermost circle of the Cairn architecture. Entities are the most stable, highest-level policy. They know nothing about the database, web, or frameworks. See also: Business Rules, Cairn Architecture.

**Event Sourcing** — Storing state as a sequence of immutable events. The current state is derived by replaying the events. This eliminates the need for mutable state at the architectural level. See also: Functional Programming, Immutability.

## F

**Facade** — A simplified interface to a complex subsystem. A lightweight boundary that reduces coupling without the cost of a full component boundary. See also: Partial Boundaries, SRP.

**Fan-in** — The number of classes outside a component that depend on classes inside the component. A measure of a component's responsibility. See also: Stability Metrics.

**Fan-out** — The number of classes inside a component that depend on classes outside the component. A measure of a component's independence. See also: Stability Metrics.

**Framework** — A tool, not a way of life. Frameworks are details. Don't let frameworks into your core code. Don't marry the framework! See also: Frameworks Are Details, Screaming Architecture.

**Frameworks and Drivers** — The outermost circle of the Cairn architecture. Contains the web framework, the database, the UI, and other external tools. See also: Cairn Architecture.

**Functional Programming** — A paradigm that imposes discipline on assignment. Removes unconstrained mutable state. Replaced with immutability. At the architectural level, this means segregating mutability and considering event sourcing. See also: Programming Paradigms, Immutability.

## G

**Goal of Software Architecture** — To minimize the human resources required to build and maintain the required system. The measure of design quality is the measure of effort required to meet customer needs. See also: What Is Design and Architecture?

## H

**HAL (Hardware Abstraction Layer)** — An interface that hides the details of the hardware from the business rules. The hardware is a detail. See also: Clean Embedded Architecture.

**Humble Object Pattern** — Split behaviors into two modules: one that is humble (hard to test, tightly coupled to a framework or device) and one that is testable (contains all the business logic). The humble module delegates to the testable module. See also: Presenters and Humble Objects, Database Gateway, Data Mapper, Presenter/View.

## I

**I (Instability)** — A metric measuring the instability of a component. `I = Fan-out / (Fan-in + Fan-out)`. A component with `I = 0` is maximally stable; `I = 1` is maximally unstable. See also: SDP, Stability Metrics.

**Immutability** — The notion that the values of symbols do not change. A foundational notion of functional programming. At the architectural level, this means segregating mutability and considering event sourcing. See also: Functional Programming, Event Sourcing.

**Independence** — A good architecture makes the system easy to change in all the ways it must change, by leaving options open. The architecture should leave the decoupling mode open as an option (monolith, components, services, threads, processes). See also: Independence, Use Cases.

**Interface Adapters** — The third circle of the Cairn architecture. Converts data between the use cases and the external agencies (database, web, UI, external services). See also: Cairn Architecture, Presenters and Humble Objects.

**ISP (Interface Segregation Principle)** — Don't depend on things you don't use. Depending on something that carries baggage that you don't need can cause you troubles you didn't expect. See also: SOLID.

## L

**Level** — The distance from inputs and outputs in the policy hierarchy. High-level policy is the business logic farthest from the IO. Low-level policy is the code that deals with the IO directly. See also: Policy and Level, Dependency Rule.

**LSP (Liskov Substitution Principle)** — Subtypes must be substitutable for their base types. Violations of LSP at the class level become architectural time bombs when the types are used across component boundaries. See also: SOLID, Polymorphism.

## M

**Main Component** — The ultimate detail. The entry point of the system. Creates the factories, sets up the dependency injection, and wires everything together. The dirtiest, most concrete, most volatile component. Lives in the outermost circle. See also: The Main Component.

**Main Sequence** — The locus of points on the A/I graph that are maximally distant from the Zone of Pain and Zone of Uselessness. The ideal relationship is `A + I = 1`. See also: SAP, SDP, D Metric.

**Making Messes Is Always Slower Than Staying Clean** — The refutation of the "quick and dirty" myth. No matter the time scale, writing clean code is faster than writing messy code. See also: What Is Design and Architecture?

**Morning After Syndrome** — The build breaks because someone changed a dependency overnight. A direct consequence of cycles in the component dependency graph. See also: ADP, Anti-Patterns.

## O

**OCP (Open-Closed Principle)** — A software artifact should be open for extension but closed for modification. If component A should be protected from changes in component B, then component B should depend on component A. See also: SOLID, Directional Control.

**OSAL (Operating System Abstraction Layer)** — An interface that hides the details of the operating system from the business rules. The operating system is a detail. See also: Clean Embedded Architecture.

## P

**PAL (Processor Abstraction Layer)** — An interface that hides the details of the processor from the business rules. The processor is a detail. See also: Clean Embedded Architecture.

**Partial Boundaries** — When a full boundary is too expensive, use a partial boundary: skip the last step, one-dimensional boundaries, or facades. See also: Partial Boundaries, Facade, Strategy Pattern.

**Policy** — The business rules. The high-level decisions. The code that is farthest from the IO. Policy is the architecture; details are not. See also: Policy and Level, Dependency Rule.

**Polymorphism** — The mechanism we use to cross architectural boundaries. The true power of object-oriented programming. See also: OOP, Dependency Inversion, Plugin Architecture.

**Presenter** — The testable half of the Presenter/View Humble Object pair. Contains all the presentation logic. Formats the data from the use case into a form that the View can display. See also: Humble Object Pattern, Presenters and Humble Objects.

**Plugin Architecture** — The core business rules are the stable center. The peripheral components (UI, database, web, frameworks) are plugins. The core does not know about the plugins. The plugins depend on the core. See also: Boundaries: Drawing Lines, Dependency Rule.

## R

**REP (Reuse/Release Equivalence Principle)** — The granule of reuse is the granule of release. What is reused must also be released and tracked. See also: Component Cohesion.

**Request and Response Models** — Simple data structures (DTOs) that cross the boundary between the Interface Adapters and the Use Cases. They contain no framework-specific code. See also: Business Rules, Cairn Architecture.

## S

**SAP (Stable Abstractions Principle)** — A component should be as abstract as it is stable. Stable components are hard to change; to make them easy to extend without changing them, they should be abstract. See also: Component Coupling, Main Sequence, Zone of Pain, Zone of Uselessness.

**Screaming Architecture** — The architecture of a system should scream its intent. When you look at the top-level directory structure, you should be able to tell what the system does — not what framework it uses. See also: Screaming Architecture, Package by Component.

**SDP (Stable Dependencies Principle)** — Depend in the direction of stability. A component should depend on components that are more stable than it is. See also: Component Coupling, Stability Metrics.

**Service Listener** — The humble half of the Service Listener/Use Case Humble Object pair. Tied to the message queue. Delegates to the testable Use Case. See also: Humble Object Pattern, Presenters and Humble Objects.

**Services** — A deployment mode, not an architectural principle. Services are not necessarily the best way to decouple. Source code decoupling is more important than process decoupling. See also: Services: Great and Small, Independence.

**Shotgun Surgery** — A single change requires touching many components. The symptom of a stable component that is also concrete — the Zone of Pain. See also: Zone of Pain, Anti-Patterns.

**SOLID** — The five class-level design principles: SRP, OCP, LSP, ISP, DIP. See also: Design Principles.

**SRP (Single Responsibility Principle)** — A module should be responsible to one, and only one, actor. The best structure is influenced by the social structure of the organization (Conway's Law). See also: SOLID, Actor.

**Stable Abstractions** — The principle that stable components should be abstract. See also: SAP, DIP.

**Stability** — The resistance to change. A stable component is heavily depended upon and does not depend on much. Measured by `I = Fan-out / (Fan-in + Fan-out)`. See also: SDP, Stability Metrics.

**Strategy Pattern** — A one-dimensional boundary using an interface and an implementation. The client depends on the interface; the implementation is a plugin. See also: Partial Boundaries, DIP.

**Structured Programming** — A paradigm that imposes discipline on direct transfer of control. Removes unrestrained `goto`. Replaced with sequence, selection, and iteration. See also: Programming Paradigms.

## T

**Test Boundary** — The boundary between the system and its tests. Tests are not outside the system; they are parts of the system. The Testing API should be a first-class architectural boundary. See also: The Test Boundary, Design for Testability.

**Testing API** — An API designed specifically for testing. It should be stable and not depend on volatile things. See also: The Test Boundary, Tests as System Components.

**The Only Way to Go Fast Is to Go Well** — The core thesis on productivity. Writing clean, well-designed code is faster than writing messy code, no matter the time scale. See also: What Is Design and Architecture?

**Two Values of Software** — Behavior (what the system does) and Architecture (how easy the system is to change). Behavior is urgent but not always important; Architecture is important but never urgent. See also: A Tale of Two Values, Eisenhower's Matrix.

## U

**Use Cases** — Application-specific business rules. The second circle of the Cairn architecture. Use cases are a natural way to divide the system. See also: Business Rules, Cairn Architecture, Independence.

## V

**View** — The humble half of the Presenter/View Humble Object pair. Tied to the UI framework. Only renders. Delegates all presentation logic to the Presenter. See also: Humble Object Pattern, Presenters and Humble Objects.

**Volatile** — Likely to change. Volatile components should not be depended upon by stable components. See also: DIP, SDP, Stable Abstractions.

## W

**Web** — An IO device. The architecture of a system should treat the web as an IO device. The system should be as ignorant as possible about how it will be delivered. See also: The Web Is a Detail, Screaming Architecture.

**Zone of Pain** — Highly stable and concrete components (I ≈ 0, A ≈ 0). Undesirable. Hard to change and heavily depended upon. See also: SAP, Main Sequence, D Metric.

**Zone of Uselessness** — Highly abstract but unused components (I ≈ 1, A ≈ 1). Undesirable. Full of interfaces but no one depends on them. See also: SAP, Main Sequence, D Metric.
