# Code Review Checklist

> Use this checklist when reviewing existing code for architectural soundness. Each item references a rule ID for traceability.

---

## 1. Dependency Rule Violations

- [ ] **V-DR-001** No inner-circle code imports or references outer-circle code.  
  *Rule:* R-001, R-002, R-003  
  *Check:* Search for framework, database, web, or UI imports in Entities and Use Cases.

- [ ] **V-DR-002** No SQL in the Use Cases or Entities layers.  
  *Rule:* R-011  
  *Check:* Search for SQL strings, query builders, or ORM imports in Use Cases and Entities.

- [ ] **V-DR-003** No HTTP request/response objects in the Use Cases layer.  
  *Rule:* R-030, R-004  
  *Check:* Search for `HttpServletRequest`, `Request`, `Response`, or similar in Use Cases.

- [ ] **V-DR-004** No framework annotations in business objects.  
  *Rule:* R-012, R-013  
  *Check:* Search for `@Entity`, `@Controller`, `@Service`, `@Table`, etc. in Entities and Use Cases.

- [ ] **V-DR-005** Data formats from outer circles are not used in inner circles.  
  *Rule:* R-004  
  *Check:* Search for JSON, XML, protobuf, or SQL result sets in Entities and Use Cases.

---

## 2. SOLID Violations

- [ ] **V-SOL-001** No class serves multiple actors.  
  *Rule:* R-016, R-017  
  *Check:* Does the class have methods that are changed by different teams for different reasons?

- [ ] **V-SOL-002** No class is modified when new features are added.  
  *Rule:* R-018, R-019  
  *Check:* When a new feature is added, does an existing class change? If so, apply OCP.

- [ ] **V-SOL-003** No subtype violates substitutability.  
  *Rule:* R-019 (LSP)  
  *Check:* Are there `instanceof` checks, downcasts, or overridden methods that break the base contract?

- [ ] **V-SOL-004** No client depends on a fat interface.  
  *Rule:* R-020  
  *Check:* Does any client implement an interface and leave methods empty or throw `NotImplemented`?

- [ ] **V-SOL-005** No class directly instantiates volatile concrete classes.  
  *Rule:* R-006, R-007, R-008, R-009  
  *Check:* Search for `new DatabaseConnection()`, `new HttpClient()`, `new FrameworkWidget()` in business logic.

---

## 3. Component Coupling Violations

- [ ] **V-COMP-001** No cycles in the component dependency graph.  
  *Rule:* R-005  
  *Check:* Run a dependency analysis tool (e.g., `mvn dependency:analyze`, `gradle dependencies`, or a custom script).

- [ ] **V-COMP-002** No stable component depends on a volatile component.  
  *Rule:* R-024  
  *Check:* Calculate I (Instability) for each component. Are there arrows from low-I to high-I?

- [ ] **V-COMP-003** No stable component is entirely concrete.  
  *Rule:* R-025  
  *Check:* Calculate A (Abstractness) and D (Distance) for each component. Is any component in the Zone of Pain?

- [ ] **V-COMP-004** No abstract component is entirely unused.  
  *Rule:* R-025  
  *Check:* Is any component full of interfaces but with no dependents (Zone of Uselessness)?

- [ ] **V-COMP-005** No component forces users to depend on unused classes.  
  *Rule:* R-023  
  *Check:* Does any client of a component use only a small fraction of its classes?

---

## 4. Testability Violations

- [ ] **V-TEST-001** Business rules can be unit-tested without the GUI.  
  *Rule:* R-037  
  *Check:* Try to write a unit test for a Use Case. Does it require a browser or UI framework?

- [ ] **V-TEST-002** Business rules can be unit-tested without the database.  
  *Rule:* R-011, R-031  
  *Check:* Try to write a unit test for a Use Case. Does it require a real database connection?

- [ ] **V-TEST-003** Business rules can be unit-tested without the web framework.  
  *Rule:* R-030  
  *Check:* Try to write a unit test for a Use Case. Does it require a web server?

- [ ] **V-TEST-004** Tests are not tightly coupled to volatile components.  
  *Rule:* R-038  
  *Check:* Do tests break when the database schema or framework version changes?

---

## 5. Boundary Quality Violations

- [ ] **V-BOUND-001** Boundaries are not drawn along technical layers.  
  *Rule:* R-057, R-039  
  *Check:* Are the top-level packages named after business functions, not technical layers?

- [ ] **V-BOUND-002** No infrastructure code bypasses the domain.  
  *Rule:* R-001, R-002  
  *Check:* Does any database or web code directly access business logic without going through the Use Cases?

- [ ] **V-BOUND-003** No full boundary exists where a partial boundary would suffice.  
  *Rule:* R-056  
  *Check:* Are there separate deployment units for components that always change together?

- [ ] **V-BOUND-004** No partial boundary exists where a full boundary is needed.  
  *Rule:* R-027, R-028  
  *Check:* Are there leaky abstractions where a volatile detail bleeds into the core?

---

## 6. Detail Deferral Violations

- [ ] **V-DET-001** The database is not the center of the architecture.  
  *Rule:* R-031, R-048  
  *Check:* Is the database schema designed before the use cases? Is business logic in stored procedures?

- [ ] **V-DET-002** The web is not the center of the architecture.  
  *Rule:* R-030, R-049  
  *Check:* Is the system impossible to deliver via mobile or desktop? Are HTTP concepts in the business logic?

- [ ] **V-DET-003** The framework is not the center of the architecture.  
  *Rule:* R-035, R-050  
  *Check:* Is the system impossible to test without the framework? Are framework annotations in business objects?

- [ ] **V-DET-004** The deployment mode is not forced by the architecture.  
  *Rule:* R-028  
  *Check:* Can the system be deployed as a monolith or as services without changing the business rules?

---

## 7. Duplication Violations

- [ ] **V-DUP-001** Duplication is not eliminated prematurely.  
  *Rule:* R-040  
  *Check:* Are two pieces of code merged even though they change for different reasons?

- [ ] **V-DUP-002** Real duplication is eliminated.  
  *Rule:* R-022  
  *Check:* Are two pieces of code that change for the same reasons kept separate?

---

## 8. Embedded Systems Violations (if applicable)

- [ ] **V-EMB-001** No hardware details in business logic.  
  *Rule:* R-014, R-032  
  *Check:* Search for register reads, interrupt handlers, or hardware headers in business logic.

- [ ] **V-EMB-002** No processor-specific code in business logic.  
  *Rule:* R-033  
  *Check:* Search for assembly, intrinsics, or processor-specific APIs in business logic.

- [ ] **V-EMB-003** No OS-specific code in business logic.  
  *Rule:* R-034  
  *Check:* Search for OS-specific APIs (e.g., `pthread`, `Win32`, `sys/socket`) in business logic.

- [ ] **V-EMB-004** Conditional compilation is DRY.  
  *Rule:* R-041 (DRY)  
  *Check:* Are `#ifdef` directives scattered throughout the code? Are they centralized?

---

## 9. Framework-Specific Violations

- [ ] **V-FW-001** No framework base classes in business objects.  
  *Rule:* R-012  
  *Check:* Do Entities or Use Cases extend a framework base class?

- [ ] **V-FW-002** No framework configuration in business logic.  
  *Rule:* R-012, R-013  
  *Check:* Are framework configuration files (e.g., `application.yml`, `web.xml`) the primary source of truth?

- [ ] **V-FW-003** No framework-specific dependency injection in business logic.  
  *Rule:* R-012  
  *Check:* Are framework annotations (`@Autowired`, `@Inject`) used in Entities or Use Cases?

---

## 10. Service-Specific Violations (if applicable)

- [ ] **V-SVC-001** Services are not used to hide source code coupling.  
  *Rule:* R-053, R-054  
  *Check:* Do services share a database schema or library? Are they independently deployable?

- [ ] **V-SVC-002** The architecture does not force a service boundary.  
  *Rule:* R-028  
  *Check:* Can the system be deployed as a monolith without changing the business rules?

---

## Sign-Off

- [ ] All Blocker violations are fixed or have a remediation plan.
- [ ] All High violations are tracked in the issue tracker.
- [ ] The audit report is updated with findings and rule IDs.
- [ ] The team has reviewed and agreed to the checklist.
