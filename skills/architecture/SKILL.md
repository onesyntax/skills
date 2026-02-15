---
name: architecture
description: >-
  Design and review software architecture using Clean Architecture principles.
  Activate whenever designing system structure, defining boundaries, creating
  use cases, planning modules, reviewing dependency direction, or discussing
  layers, deployment, or framework/database independence. Architecture touches
  everything — if dependencies point the wrong way, no amount of clean code at
  the function level will save the system.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature description or code to analyze]
---

# Architecture Skill

Architecture is the art of drawing lines — boundaries that separate software elements and restrict dependencies. The goal is to minimize the human resources required to build and maintain the system. A good architecture keeps options open, defers decisions, and makes the system easy to change.

For SOLID principles at the class level, see `/solid`. For component cohesion and coupling metrics, see `/components`. For design patterns, see `/patterns`.

For detailed architecture walkthroughs with full system examples, read `references/extended-examples.md`.

---

## The Two Values of Software

Software has exactly two values: **behavior** (what it does now) and **structure** (the ability to change it). Structure is more important — a system that works but can't change is worthless, because requirements will change. A system that doesn't work but can change is valuable, because you can make it work.

Most managers prioritize behavior (urgent) over structure (important). Architects must fight for structure, or the system drowns in its own mess.

---

## The Dependency Rule

**The most important rule in Clean Architecture: source code dependencies must point inward, toward higher-level policies.**

```
┌─────────────────────────────────────────────────────────────┐
│                    Frameworks & Drivers                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Interface Adapters                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │           Application Business Rules         │    │    │
│  │  │  ┌─────────────────────────────────────┐    │    │    │
│  │  │  │    Enterprise Business Rules        │    │    │    │
│  │  │  │         (Entities)                  │    │    │    │
│  │  │  └─────────────────────────────────────┘    │    │    │
│  │  │           (Use Cases)                        │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │    (Controllers, Gateways, Presenters)              │    │
│  └─────────────────────────────────────────────────────┘    │
│      (Web, UI, DB, Devices, External Interfaces)            │
└─────────────────────────────────────────────────────────────┘
```

### The Four Layers

**1. Entities (Enterprise Business Rules)** — Pure business objects with no knowledge of application or delivery mechanism. Would exist even if no software existed. Only change when business rules change.

**2. Use Cases (Application Business Rules)** — Application-specific rules. Orchestrate data flow to/from entities. Don't know about controllers, presenters, or views.

**3. Interface Adapters** — Convert data between formats convenient for use cases and formats convenient for external tools. Controllers, Presenters, Gateways. No business rules — only data conversion. MVC lives here.

**4. Frameworks & Drivers** — The outermost layer. Web frameworks, databases, UI frameworks. Mostly glue code. All the details go here.

---

## Crossing Boundaries

**Data that crosses boundaries must be simple data structures. Never pass Entity objects or database rows across boundaries.**

```
Controller --> InputBoundary(interface) --> Interactor --> OutputBoundary(interface) --> Presenter
```

- **Input Boundary (Port):** Interface the controller calls
- **Output Boundary (Port):** Interface the use case calls to send results
- **Interactor:** The use case implementation
- **Request/Response Models:** Plain DTOs with primitive types only — no entities, no framework objects

```
// Bad — passing Entity through boundary
OrderResponse { order: Order }  // Entity leaking out!

// Good — only the data needed
OrderResponse {
    orderId
    customerName
    total
}
```

The Interactor sits at the center. Control flows through it, but dependencies point toward it — this is Dependency Inversion at the architectural level.

---

## Use Cases and Interactors

A use case captures application-specific business rules — input, output, and processing steps.

```
CreateOrderInteractor implements CreateOrderInputPort:
    orderGateway: OrderGateway
    presenter: CreateOrderOutputPort

    execute(request: CreateOrderRequest):
        // 1. Validate request
        // 2. Create/manipulate entities
        // 3. Persist through gateway
        // 4. Build response
        // 5. Pass to presenter
```

**Principles:** Use cases know about entities, not the reverse. Each use case has a single responsibility. Request/Response models are plain data structures with no behavior.

---

## The Humble Object Pattern

Separate hard-to-test code from easy-to-test code:

- **Humble Object:** Hard-to-test code (UI, database), minimal logic
- **Testable Object:** All business logic, receives/returns simple data

**Examples:** Presenter (humble) / ViewModel (testable). Database Gateway (humble) / Interactor (testable).

---

## Database and Framework Independence

### The Database is a Detail

The database is an I/O device. Business rules shouldn't know which database they use. Define a `DataGateway` interface in the use case layer; implement it in the outer layer with SQL/ORM/connection pooling.

### Frameworks are Details

Frameworks are tools, not architectures. The framework makes no commitment to you — you make a commitment to it.

```
// Bad — Entity coupled to framework
class Customer:
    [persistence annotations]
    id
    // business logic mixed with persistence concerns

// Good — Entity is pure
class Customer:
    id: CustomerId
    // pure business logic only

// Framework details in outer layer
class CustomerPersistenceModel:
    [persistence annotations]
    id
    // only persistence concerns
```

Never derive business entities from framework base classes. Isolate framework dependencies to outer layers.

---

## Screaming Architecture

The top-level directory structure should tell you what the system **does**, not what frameworks it uses.

```
// Bad — screams "Rails"          // Good — screams "Health Clinic"
/app                               /patients
  /models                          /appointments
  /views                           /billing
  /controllers                     /medical_records
```

**Package by feature, not layer.** Group code by business capability: `/orders` contains CreateOrderUseCase, OrderController, OrderRepository together.

---

## The Three Paradigms as Foundations

**Structured Programming (concrete blocks):** Sequence, selection, iteration — sufficient for any computation.

**OO Programming (girders and beams):** The real power is safe polymorphism — inverting source code dependencies against the flow of control. Without this, Clean Architecture would be impossible.

**Functional Programming (plumbing):** Immutability eliminates race conditions, deadlocks, concurrent update problems. Event Sourcing is FP's architectural manifestation.

Each paradigm removes something: structured removes goto, OO removes function pointers (replaces with safe polymorphism), FP removes assignment.

---

## Event Sourcing

Store transactions (events) rather than state. CRUD becomes CR — no updates, no deletes, only new events. Current state is computed by replaying events.

Git is event sourcing for source code. No mutable state means no race conditions, no concurrent update problems, no need for traditional locks.

---

## The Decoupling Modes Spectrum

From tightest to loosest: Static Monolith → Dynamic Linking → Threads → Processes → Services/Microservices.

**Architecture should be independent of decoupling mode.** The same source code boundaries should work whether deployed as monolith or microservices. Microservices are a deployment strategy, not an architectural strategy.

---

## The Main Module

Main is the dirtiest, lowest-level module — where all SOLID principles are violated, and that's acceptable. It creates concrete instances, wires dependencies, and knows about everything. All dependencies point away from Main.

You can have multiple Main modules: one for production, one for testing, one for development — each wiring different concrete implementations. Tests are even lower than Main — they depend on everything, nothing depends on them.

---

## Types of Boundaries

Not all boundaries are the same. Choose based on the system's needs:

1. **Source-Level Boundaries** — Function calls within the same codebase, separated by interfaces. Cheapest to create, easiest to change. Start here.
2. **Deployment Boundaries** — Separate JARs, DLLs, gems deployed together but compiled independently. Changes to one don't force recompilation of others.
3. **Service Boundaries** — Separate processes communicating over the network. Most expensive, most independent. Only use when deployment independence is essential.

**Strategy:** Start with source-level boundaries. Promote to deployment or service boundaries only when the cost of coupling exceeds the cost of separation. Components define the fracture lines — draw architectural boundaries along them later, when you know more.

---

## Testing Architecture

Clean Architecture makes testing natural — business rules live in the center, free of frameworks and I/O.

**Unit tests** cover entities and interactors with mock gateways. Fast, isolated, no I/O. The bulk of your tests live here.

**Integration tests** cover interactors with real gateways (test database), controller-to-presenter flows, and component boundaries.

**End-to-end tests** cover the full stack. Slow, fragile, few in number. Verify wiring, not logic.

The Humble Object pattern is the key: UI, database, and external services are humble (minimal logic, hard to test). Business logic is testable (all decisions, easy to unit test). If you can't test business rules without starting a web server or connecting to a database, the architecture has failed.

---

## Common Architectural Mistakes

1. **Database-Driven Design** — Starting with the schema instead of use cases and entities
2. **Framework-Driven Design** — Letting the framework dictate architecture instead of living at the edges
3. **Business Logic in Controllers** — Controllers should only parse input, call use case, format output
4. **Entities Crossing Boundaries** — Use DTOs; entities stay in their layer
5. **Circular Dependencies** — Use dependency inversion to break cycles
6. **Ignoring Structure for Behavior** — Prioritizing "make it work" over "make it changeable"

---

## When Writing Architecture

### Implementation Steps

1. **Define the Use Case** — What is the application doing? What are inputs (Request Model) and outputs (Response Model)?
2. **Identify Entities** — What business objects are involved? What rules do they encapsulate?
3. **Define Gateway Interfaces** — What external data is needed? Define interfaces in the use case layer
4. **Implement the Interactor** — Pure business logic using entities and gateways
5. **Create Interface Adapters** — Controller, Presenter, Gateway implementations
6. **Wire Up Framework Layer** — Connect to web/database, inject dependencies pointing inward

### Scale Guidance

**Small projects:** Focus on use cases and entities. Keep boundaries simple. Don't over-engineer.

**Growing projects:** Introduce explicit boundaries as complexity grows. Extract components as teams grow.

**Large systems:** Full Clean Architecture with all layers. Multiple deployable components. Monitor dependency metrics (see `/components` for I, A, D metrics).

---

## When Reviewing Architecture

### Checklist

**Dependency Rule:**
- Do all dependencies point inward?
- Are entities free of framework dependencies?
- Are use cases free of UI and database details?
- Any circular dependencies?

**Boundaries:**
- Defined by interfaces, not implementations?
- Data structures (not entities) crossing boundaries?
- Dependency Inversion at each boundary?

**Testability:**
- Can business rules be tested without UI/database/external services?
- Are humble objects minimal?
- Can gateways be easily mocked?

**Intent:**
- Does the architecture scream its business purpose?
- Packages organized by feature, not layer?

### Severity Levels

| Severity | Type | Example |
|----------|------|---------|
| Critical | Dependency Rule violation — inner layer depends on outer | Entity imports Spring annotations |
| High | Entities crossing boundaries, circular dependencies | Use case returns JPA entity |
| Medium | Business logic in controllers, framework-driven structure | Validation rules in REST handler |
| Low | Package-by-layer instead of package-by-feature | `/controllers` + `/services` instead of `/orders` |

---

## Related Skills

- `/solid` — SOLID principles for class-level design within architectural boundaries
- `/components` — Component cohesion and coupling (REP, CCP, CRP, ADP, SDP, SAP) with stability metrics
- `/patterns` — Design patterns that implement architectural concepts (Factory, Observer, Visitor, Proxy)
- `/tdd` — TDD enables fearless refactoring and the tortoise's advantage
- `/functional-programming` — FP provides immutability foundations for event sourcing
- `/professional` — Professional standards for architectural decisions
