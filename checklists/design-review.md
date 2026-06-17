# Design Review Checklist

> Use this checklist before building a new system, service, or major feature. Each item references a rule ID for traceability.

---

## 1. Use Case Alignment

- [ ] **UC-001** The top-level directory structure is organized by use case (business function), not by technical layer.  
  *Rule:* R-039 (Use Cases Divide the System), R-057 (Architecture Should Scream Intent)  
  *Test:* Can you tell what the system does by looking at the top-level folders?

- [ ] **UC-002** Each use case is independently identifiable and has a clear boundary.  
  *Rule:* R-039  
  *Test:* Can you describe a use case without mentioning the database, web, or framework?

---

## 2. Policy vs. Details

- [ ] **PD-001** The database is treated as a detail. No database-specific code exists in the Entities or Use Cases layers.  
  *Rule:* R-031 (Database Is a Detail), R-011 (No SQL in Use Cases)  
  *Test:* Can the Entities and Use Cases be compiled without a database library?

- [ ] **PD-002** The web is treated as a detail. No HTTP-specific code exists in the Entities or Use Cases layers.  
  *Rule:* R-030 (Web Is an IO Device)  
  *Test:* Can the Use Cases be tested without a web server or HTTP client?

- [ ] **PD-003** Frameworks are treated as details. No framework imports or annotations exist in the Entities or Use Cases layers.  
  *Rule:* R-035 (Frameworks Are Tools), R-012 (No Frameworks in Core Code)  
  *Test:* Can the Entities and Use Cases be compiled without the framework?

- [ ] **PD-004** The hardware/OS/processor are treated as details (for embedded systems).  
  *Rule:* R-032 (Hardware Is a Detail), R-033 (Processor Is a Detail), R-034 (OS Is a Detail)  
  *Test:* Can the business logic be tested on a development machine without the target hardware?

---

## 3. Dependency Rule

- [ ] **DR-001** All source code dependencies point inward, toward higher-level policies.  
  *Rule:* R-001 (Dependency Rule: Inward Only)  
  *Test:* Draw the dependency graph. Do any arrows point outward?

- [ ] **DR-002** No inner circle mentions the name of anything declared in an outer circle.  
  *Rule:* R-003 (No Names from Outer Circles)  
  *Test:* Search for imports of framework, database, or web packages in the Entities and Use Cases layers.

- [ ] **DR-003** No inner circle uses data formats declared in an outer circle.  
  *Rule:* R-004 (No Outer Data Formats)  
  *Test:* Are JSON, XML, SQL result sets, or HTTP request objects used in the Entities or Use Cases layers?

- [ ] **DR-004** The Main component is the only place where concrete implementations are wired.  
  *Rule:* R-055 (Main Is the Ultimate Detail)  
  *Test:* Is there any other place where `new DatabaseConnection()` or `new HttpServer()` appears?

---

## 4. SOLID Principles

- [ ] **SOL-001** Each class is responsible to one, and only one, actor.  
  *Rule:* R-016 (SRP: One Actor per Module)  
  *Test:* List the actors who might request a change to this class. Is there more than one?

- [ ] **SOL-002** Classes are open for extension but closed for modification.  
  *Rule:* R-018 (OCP)  
  *Test:* Can a new feature be added without changing existing, working classes?

- [ ] **SOL-003** All subtypes are substitutable for their base types.  
  *Rule:* R-019 (LSP)  
  *Test:* Can a client use a subtype without knowing it is a subtype?

- [ ] **SOL-004** No client depends on methods it does not use.  
  *Rule:* R-020 (ISP)  
  *Test:* Does any client implement an interface and leave methods empty or throw `NotImplemented`?

- [ ] **SOL-005** No class depends on volatile concrete classes.  
  *Rule:* R-006 (DIP: No References to Volatile Concrete Classes)  
  *Test:* Does any class instantiate a database driver, HTTP client, or framework widget directly?

---

## 5. Component Principles

- [ ] **COMP-001** No cycles exist in the component dependency graph.  
  *Rule:* R-005 (ADP)  
  *Test:* Run a dependency analysis tool. Are there any cycles?

- [ ] **COMP-002** Dependencies point in the direction of stability.  
  *Rule:* R-024 (SDP)  
  *Test:* Calculate I (Instability) for each component. Do arrows point from high-I to low-I?

- [ ] **COMP-003** Stable components are abstract.  
  *Rule:* R-025 (SAP)  
  *Test:* Calculate A (Abstractness) and D (Distance) for each component. Are stable components near the Main Sequence?

- [ ] **COMP-004** Components gather classes that change for the same reasons.  
  *Rule:* R-022 (CCP)  
  *Test:* If one class in the component changes, do the others typically change too?

- [ ] **COMP-005** Components do not force users to depend on things they don't need.  
  *Rule:* R-023 (CRP)  
  *Test:* Does a client of this component use all the classes in it?

---

## 6. Testability

- [ ] **TEST-001** Business rules can be tested without the GUI.  
  *Rule:* R-037 (Design for Testability Without GUI)  
  *Test:* Write a unit test for a Use Case. Does it require a browser or UI framework?

- [ ] **TEST-002** Business rules can be tested without the database.  
  *Rule:* R-011 (No SQL in Use Cases), R-031 (Database Is a Detail)  
  *Test:* Write a unit test for a Use Case. Does it require a real database connection?

- [ ] **TEST-003** Business rules can be tested without the web framework.  
  *Rule:* R-030 (Web Is an IO Device)  
  *Test:* Write a unit test for a Use Case. Does it require a web server?

- [ ] **TEST-004** The Testing API is a first-class architectural boundary.  
  *Rule:* R-036 (Tests Are Parts of the System)  
  *Test:* Is the Testing API stable, documented, and treated as part of the system?

---

## 7. Deferral of Decisions

- [ ] **DEF-001** The database decision can be deferred or reversed.  
  *Rule:* R-048 (Defer Database Decision)  
  *Test:* Can the system switch from PostgreSQL to MongoDB without changing the Entities or Use Cases?

- [ ] **DEF-002** The web decision can be deferred or reversed.  
  *Rule:* R-049 (Defer Web Decision)  
  *Test:* Can the system switch from REST to gRPC without changing the Use Cases?

- [ ] **DEF-003** The framework decision can be deferred or reversed.  
  *Rule:* R-050 (Defer Framework Decision)  
  *Test:* Can the system switch from Spring to Quarkus without changing the Entities or Use Cases?

- [ ] **DEF-004** The decoupling mode (monolith vs. services) is left open.  
  *Rule:* R-028 (Leave Decoupling Mode Open)  
  *Test:* Can the system be deployed as a monolith today and as microservices tomorrow without changing the business rules?

---

## 8. Boundary Quality

- [ ] **BOUND-001** Boundaries are drawn along axes of change.  
  *Rule:* R-029 (IO Is Irrelevant)  
  *Test:* If the database changes, does only one component change? If the web framework changes, does only one component change?

- [ ] **BOUND-002** Full boundaries are used where needed; partial boundaries are used where full boundaries are too expensive.  
  *Rule:* R-056 (Use Partial Boundaries When Too Expensive)  
  *Test:* Is there a boundary between every volatile detail and the stable core? Are any boundaries over-engineered?

- [ ] **BOUND-003** The Humble Object pattern is applied to UI, database, and external services.  
  *Rule:* R-037 (Design for Testability Without GUI)  
  *Test:* Is the UI layer thin and humble? Is the database layer thin and humble?

---

## 9. Duplication

- [ ] **DUP-001** Duplication is real before it is eliminated.  
  *Rule:* R-040 (Verify Duplication Is Real)  
  *Test:* Do the two pieces of code change for the same reasons? If not, leave them separate.

---

## 10. Embedded Systems (if applicable)

- [ ] **EMB-001** Hardware details are hidden behind a HAL.  
  *Rule:* R-014 (No Hardware Details in HAL Users)  
  *Test:* Does any business logic file include a hardware register header?

- [ ] **EMB-002** The processor is hidden behind a PAL.  
  *Rule:* R-033 (Processor Is a Detail)  
  *Test:* Does any business logic file contain processor-specific assembly or intrinsics?

- [ ] **EMB-003** The OS is hidden behind an OSAL.  
  *Rule:* R-034 (OS Is a Detail)  
  *Test:* Does any business logic file call OS-specific APIs directly?

---

## Sign-Off

- [ ] All Blocker items are resolved.
- [ ] All High items have a remediation plan.
- [ ] The ADR is updated with any changes.
- [ ] The team has reviewed and agreed to the checklist.
