# Cairn: Audit Existing Code

> The step-by-step procedure Cairn follows when auditing or refactoring existing code against the Cairn canon.

---

## Mode: Audit / Refactor

Use this workflow when the user asks Claude to:
- Review existing code for architectural soundness
- Refactor a codebase to comply with the Cairn canon
- Identify violations of SOLID, component principles, or the Dependency Rule
- Audit a system for testability, decoupling, or boundary violations
- Assess whether a database/web/framework is properly treated as a detail

---

## Step 1: Map the Current Structure

**Goal:** Understand the current architecture before judging it.

**Actions:**
1. List the top-level directories/packages. Do they scream intent (use cases) or technology (controllers, models, views)?
2. Draw a rough dependency graph of the major components. Which components depend on which?
3. Identify the framework, database, web, and UI technologies in use.
4. Identify the build and deployment structure (monolith, components, services).
5. **Rule check:** R-057 (Architecture Should Scream Intent), R-039 (Use Cases Divide the System).
6. **Anti-pattern check:** Big Ball of Mud, Framework-Centric Architecture, Database-Centric Architecture, Web-Centric Architecture.

**Output:** A current-state diagram and a list of technologies and dependencies.

---

## Step 2: Detect Dependency Rule Violations

**Goal:** Find every place where an inner circle depends on an outer circle.

**Actions:**
1. Search for imports of framework packages in business logic (Entities, Use Cases).
2. Search for imports of database packages in business logic.
3. Search for imports of web packages in business logic.
4. Search for SQL in the Use Cases or Entities layer.
5. Search for HTTP request/response objects in the Use Cases layer.
6. Search for framework annotations (`@Entity`, `@Controller`, `@Service`) in business objects.
7. **Rule check:** R-001 (Dependency Rule: Inward Only), R-002 (No Knowledge of Outer Circles), R-003 (No Names from Outer Circles), R-004 (No Outer Data Formats), R-011 (No SQL in Use Cases), R-012 (No Frameworks in Core Code), R-030 (Web Is an IO Device).
8. **Anti-pattern check:** Périphérique Anti-Pattern, Database-Centric Architecture, Web-Centric Architecture, Framework-Centric Architecture.

**Output:** A list of Dependency Rule violations with file paths and line numbers.

---

## Step 3: Detect SOLID Violations

**Goal:** Find class-level violations of SRP, OCP, LSP, ISP, and DIP.

**Actions:**
1. **SRP:** Find classes that are changed by multiple teams or contain methods for multiple actors. Look for classes with many unrelated methods.
2. **OCP:** Find classes that are modified frequently when new features are added. Look for `switch` statements or `if-else` chains that grow over time.
3. **LSP:** Find inheritance hierarchies where subtypes are not substitutable. Look for `instanceof` checks or downcasts.
4. **ISP:** Find interfaces with many methods where clients only use a few. Look for "fat" interfaces.
5. **DIP:** Find classes that directly instantiate volatile concrete classes. Look for `new DatabaseConnection()`, `new HttpClient()`, `new FrameworkWidget()`.
6. **Rule check:** R-016 (SRP), R-018 (OCP), R-020 (ISP), R-006 (DIP).
7. **Anti-pattern check:** LSP Violation at the Architectural Level, Premature Elimination of Duplication, Stable Component Depending on Volatile Component.

**Output:** A list of SOLID violations with file paths, rule IDs, and remediation suggestions.

---

## Step 4: Detect Component Coupling Violations

**Goal:** Find cycles, unstable dependencies, and zones of pain/uselessness.

**Actions:**
1. Run a dependency analysis tool to detect cycles in the component graph. **Rule:** R-005 (ADP).
2. Calculate Fan-in and Fan-out for each component. Compute I (Instability). **Rule:** R-024 (SDP).
3. Calculate Na and Nc for each component. Compute A (Abstractness). **Rule:** R-025 (SAP).
4. Compute D (Distance from Main Sequence) for each component. Identify components in the Zone of Pain (D ≈ 1, A ≈ 0, I ≈ 0) or Zone of Uselessness (D ≈ 1, A ≈ 1, I ≈ 1).
5. **Anti-pattern check:** Morning After Syndrome, Zone of Pain, Zone of Uselessness, Shotgun Surgery.

**Output:** A component coupling report with metrics and flagged components.

---

## Step 5: Assess Testability

**Goal:** Determine whether the system can be tested without the GUI, database, or frameworks.

**Actions:**
1. Try to write a unit test for a Use Case without the GUI. Does it require a web framework?
2. Try to write a unit test for a Use Case without the database. Does it require a real database connection?
3. Try to write a unit test for an Entity without the ORM. Does it require ORM annotations?
4. Check if the Testing API is a first-class architectural boundary or an afterthought.
5. **Rule check:** R-036 (Tests Are Parts of the System), R-037 (Design for Testability Without GUI), R-038 (Don't Depend on Volatile Things in Tests).
6. **Anti-pattern check:** App-titude Test (code that works but is untestable).

**Output:** A testability report with pass/fail for each layer and a list of blockers.

---

## Step 6: Assess Boundary Quality

**Goal:** Determine whether boundaries are drawn in the right places and whether they are too expensive or too cheap.

**Actions:**
1. Identify the axes of change. Are boundaries drawn along these axes? **Rule:** R-029 (IO Is Irrelevant).
2. Check if full boundaries exist where partial boundaries would suffice. **Rule:** R-056 (Use Partial Boundaries When Too Expensive).
3. Check if partial boundaries exist where full boundaries are needed. Look for leaky abstractions.
4. Check if the Main component is the only place where concrete implementations are wired. **Rule:** R-055 (Main Is the Ultimate Detail).
5. Check if the system can be deployed as a monolith or as services without changing the business rules. **Rule:** R-028 (Leave Decoupling Mode Open).
6. **Anti-pattern check:** Service-Oriented Architecture Without Source Code Decoupling.

**Output:** A boundary assessment report with recommendations for full, partial, or no boundaries.

---

## Step 7: Assess Detail Deferral

**Goal:** Determine whether the system has prematurely committed to details.

**Actions:**
1. Is the database decision reversible? Can the system switch from relational to NoSQL without changing the business rules? **Rule:** R-031 (Database Is a Detail), R-048 (Defer Database Decision).
2. Is the web decision reversible? Can the system switch from web to mobile without changing the business rules? **Rule:** R-030 (Web Is an IO Device), R-049 (Defer Web Decision).
3. Is the framework decision reversible? Can the system switch from Spring to Django without changing the business rules? **Rule:** R-035 (Frameworks Are Tools), R-050 (Defer Framework Decision).
4. Are there hardcoded URIs, connection strings, or framework-specific configurations in the business logic? **Rule:** R-010 (No Physical Knowledge of Lower-Level Services).
5. **Anti-pattern check:** The Hare's Overconfidence ("we can clean it up later").

**Output:** A detail deferral report with reversibility ratings for each technology.

---

## Step 8: Produce the Audit Report

**Goal:** Summarize all findings in a structured, actionable report.

**Actions:**
1. Categorize findings by severity: Blocker, High, Medium, Low.
2. For each finding, cite the rule ID (e.g., "violates R-011").
3. For each finding, provide a concrete remediation step.
4. For each finding, estimate the effort to fix.
5. Prioritize findings by impact on the Goal of Software Architecture (minimizing human resources).
6. **Rule check:** All findings must map to a Cairn rule ID or principle.

**Output:** An audit report with findings, rule IDs, remediation steps, and effort estimates.

---

## Step 9: Produce the Refactoring Plan

**Goal:** Turn the audit report into a concrete, phased refactoring plan.

**Actions:**
1. Phase 1: Break the worst cycles (ADP). Start with the cycles that cause the most Morning After Syndrome.
2. Phase 2: Invert the worst dependencies (DIP). Start with the dependencies that cause the most framework/database/web leakage.
3. Phase 3: Extract the core business rules (Entities and Use Cases). Move them to the innermost circles.
4. Phase 4: Introduce Gateways and Presenters (Humble Object pattern). Decouple the business rules from the database and UI.
5. Phase 5: Apply SOLID at the class level. Split fat classes, introduce interfaces, fix LSP violations.
6. Phase 6: Apply component principles. Reorganize packages by component (Package by Component).
7. Phase 7: Improve testability. Add in-memory implementations, mock Gateways, Testing API.
8. For each phase, define the success criteria and the checkpoint.

**Output:** A phased refactoring plan with milestones and success criteria.

---

## Step 10: Review with Checklists

**Goal:** Ensure the audit and refactoring plan are complete and compliant.

**Actions:**
1. Run the **Code Review Checklist** (`checklists/code-review.md`).
2. For each checklist item, verify that the audit covers it.
3. Mark any gaps as risks.
4. Produce a final review report.

**Output:** A code review checklist with pass/fail status for each item.

---

## Completion Criteria

The audit is complete when:
- [ ] The current structure is mapped and understood.
- [ ] Dependency Rule violations are identified with file paths and line numbers.
- [ ] SOLID violations are identified with rule IDs and remediation steps.
- [ ] Component coupling violations are identified with metrics (I, A, D).
- [ ] Testability is assessed with pass/fail for each layer.
- [ ] Boundary quality is assessed with recommendations.
- [ ] Detail deferral is assessed with reversibility ratings.
- [ ] An audit report is produced with severity, rule IDs, and remediation steps.
- [ ] A phased refactoring plan is produced with milestones and success criteria.
- [ ] The code review checklist is complete with no gaps.
