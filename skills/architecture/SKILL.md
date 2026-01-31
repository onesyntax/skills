---
name: architecture
description: >-
  Guide implementing features using Clean Architecture patterns (use cases, boundaries,
  dependency rule). Activates when designing new features, creating modules, planning
  system structure, working with use cases, handlers, or boundaries, or when the user
  mentions architecture, layers, dependencies, clean architecture, or module design.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature description]
---

# Architecture Workflow

Follow this workflow when designing system structure, reviewing architecture decisions, or implementing features using Clean Architecture principles.

## Workflow Steps

1. **Identify layers and boundaries** - Determine which architectural layers are involved and where boundaries exist
2. **Apply the Dependency Rule** - Ensure all dependencies point inward toward higher-level policies
3. **Define use cases and interactors** - Capture application-specific business rules
4. **Create proper boundary data structures** - Use simple DTOs to cross boundaries, never entities
5. **Apply component principles** - Follow REP, CCP, CRP, ADP, SDP, SAP for component design
6. **Apply /professional workflow** - Ensure quality standards are met

---

## Core Philosophy

### What is Architecture?

Architecture is the art of drawing lines - boundaries that separate software elements and restrict dependencies. The goal is to minimize human resources required to build and maintain systems. A good architecture allows decisions to be deferred, keeping options open as long as possible.

**The Prime Directive:** The architecture must serve the business, not the other way around. Technical decisions should be deferred, and business rules should be the center of the system.

### The Purpose of Good Architecture

1. **Minimize cost of change** - Systems should be easy to modify throughout their lifetime
2. **Keep options open** - Defer decisions about frameworks, databases, and UI until the last responsible moment
3. **Enable independent deployability** - Components should be deployable independently
4. **Support team independence** - Teams should be able to work on different components without stepping on each other
5. **Make the system testable** - Business rules should be testable without UI, database, or external systems

---

## The Dependency Rule

**The most important rule in Clean Architecture: Source code dependencies must point inward, toward higher-level policies.**

### The Concentric Circles

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

### Layer Definitions

#### 1. Entities (Enterprise Business Rules)
- The innermost circle containing enterprise-wide business rules
- Pure business objects with no knowledge of application or delivery mechanism
- Would exist even if no software system existed
- Examples: Customer, Order, Invoice with their critical business rules
- **Never change due to external concerns** - only change when business rules change

#### 2. Use Cases (Application Business Rules)
- Application-specific business rules
- Orchestrate the flow of data to and from entities
- Direct entities to use their enterprise-wide business rules
- Changes here should not affect entities
- Changes to external layers should not affect use cases

#### 3. Interface Adapters
- Convert data from the format most convenient for use cases and entities
- Contains Controllers, Presenters, and Gateways
- No business rules - only data conversion
- This is where MVC architecture lives

#### 4. Frameworks & Drivers
- The outermost layer containing frameworks and tools
- Web frameworks, databases, UI frameworks
- Generally, you don't write much code here - it's "glue code"
- This layer is where all the details go

### Crossing Boundaries

**Critical Rule:** Data that crosses boundaries should be simple data structures. Never pass Entity objects or database rows across boundaries.

```
Controller --> Use Case Input Port --> Interactor --> Use Case Output Port --> Presenter
                    (interface)                           (interface)
```

- **Input Boundary (Port):** Interface that the controller calls
- **Output Boundary (Port):** Interface that the use case calls to send results
- **Interactor:** The implementation of the use case
- **Request Model:** Data structure going into the use case
- **Response Model:** Data structure coming out of the use case

---

## Use Cases and Interactors

### What is a Use Case?

A use case is a description of how a system is used - it captures application-specific business rules. Use cases tell the story of how automated systems are used by describing the input to be provided, the output to be generated, and the processing steps involved.

### Interactor Structure

```
class CreateOrderInteractor implements CreateOrderInputPort {
    private OrderGateway orderGateway;
    private CreateOrderOutputPort presenter;

    void execute(CreateOrderRequest request) {
        // 1. Validate request
        // 2. Create/manipulate entities
        // 3. Persist through gateway
        // 4. Build response
        // 5. Pass to presenter
    }
}
```

### Use Case Principles

1. **Use cases know about entities, not the reverse**
2. **Use cases don't know about controllers, presenters, or views**
3. **Use cases define input/output boundaries (interfaces)**
4. **Request/Response models are plain data structures** - no behavior, no dependencies
5. **Each use case should have a single responsibility**

### Request and Response Models

**Request Models:**
- Simple data structures (DTOs)
- Contain only primitive types or other simple data structures
- No references to Entity objects
- Validated before reaching the interactor

**Response Models:**
- Simple data structures
- Formatted for the output port, not for any specific view
- No Entity objects - only the data needed
- May contain error information

```
// Bad - passing Entity through boundary
class OrderResponse {
    Order order;  // Entity - WRONG!
}

// Good - passing only needed data
class OrderResponse {
    String orderId;
    String customerName;
    BigDecimal total;
    String status;
}
```

---

## The SOLID Principles

### Single Responsibility Principle (SRP)

**"A module should have one, and only one, reason to change."**

More precisely: **"A module should be responsible to one, and only one, actor."**

An "actor" is a group of people who want the system to change in the same way. The SRP is about people, not about functions.

**Symptoms of SRP Violation:**
- Accidental Duplication: Different actors share code that looks the same but changes for different reasons
- Merge Conflicts: Changes for one actor collide with changes for another
- Feature Envy: A class is more interested in another class's data than its own

**Solutions:**
- Separate data from functions (Facade pattern)
- Extract classes by actor
- Create separate interfaces for different actors

**Example of Violation:**
```
class Employee {
    calculatePay()      // CFO's concern (accounting)
    reportHours()       // COO's concern (operations)
    save()              // CTO's concern (technical)
}
```

Three actors, three reasons to change - this violates SRP.

### Open-Closed Principle (OCP)

**"Software entities should be open for extension but closed for modification."**

You should be able to add new functionality without modifying existing code. This is achieved through abstraction and polymorphism.

**The Goal:** If component A should be protected from changes in component B, then B should depend on A, not vice versa.

**Implementation Strategies:**
1. Use interfaces/abstract classes at architectural boundaries
2. Apply Dependency Inversion - make volatile components depend on stable abstractions
3. Organize components into a hierarchy of protection levels

**Protected Variation:** Identify points of predicted variation and create stable interfaces around them.

```
// Closed for modification, open for extension
interface Shape {
    double area();
}

class Circle implements Shape { /* ... */ }
class Rectangle implements Shape { /* ... */ }
// Add new shapes without modifying existing code
```

### Liskov Substitution Principle (LSP)

**"Subtypes must be substitutable for their base types."**

If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

**The Rectangle/Square Problem:**
```
class Rectangle {
    void setWidth(int w) { width = w; }
    void setHeight(int h) { height = h; }
}

class Square extends Rectangle {
    void setWidth(int w) { width = w; height = w; }  // Violates LSP!
    void setHeight(int h) { width = h; height = h; }
}
```

A square IS-A rectangle mathematically, but NOT behaviorally in software. Setting width and height independently is a property users expect of Rectangle.

**Design by Contract:**
- Preconditions cannot be strengthened in a subtype
- Postconditions cannot be weakened in a subtype
- Invariants of the supertype must be preserved

**LSP in Architecture:**
- Applies to interfaces, not just inheritance
- REST APIs, microservices, plugins must follow substitutability
- Architectural violations lead to if-else chains checking types

### Interface Segregation Principle (ISP)

**"Clients should not be forced to depend on interfaces they do not use."**

Don't force a class to implement methods it doesn't need. Split large interfaces into smaller, more specific ones.

**Fat Interface Problem:**
```
interface Worker {
    void work();
    void eat();
    void sleep();
}

// Robot can work but doesn't eat or sleep!
class Robot implements Worker {
    void eat() { throw new UnsupportedOperationException(); }  // ISP violation
}
```

**Solution:**
```
interface Workable { void work(); }
interface Eatable { void eat(); }
interface Sleepable { void sleep(); }

class Human implements Workable, Eatable, Sleepable { /* ... */ }
class Robot implements Workable { /* ... */ }
```

**ISP in Architecture:**
- Statically typed languages suffer from unnecessary recompilation
- Separate interfaces mean separate deployable components
- Reduces the "fan-out" of dependencies

### Dependency Inversion Principle (DIP)

**"High-level modules should not depend on low-level modules. Both should depend on abstractions."**

**"Abstractions should not depend on details. Details should depend on abstractions."**

This is the most architecturally significant SOLID principle. It governs how boundaries are drawn and dependencies managed.

**What to Depend On:**
- Stable abstractions (interfaces, abstract classes)
- Modules that change infrequently

**What NOT to Depend On:**
- Concrete implementations
- Volatile modules (those likely to change)
- Anything in the outer circles of the architecture

**Inversion Example:**
```
// Without DIP - high-level depends on low-level
class OrderService {
    MySQLDatabase db = new MySQLDatabase();  // Direct dependency
}

// With DIP - both depend on abstraction
interface OrderRepository { /* ... */ }

class OrderService {
    OrderRepository repo;  // Depends on abstraction
}

class MySQLOrderRepository implements OrderRepository { /* ... */ }
```

**The Architectural Impact:**
- Source code dependencies oppose the flow of control
- Control flows from controllers to use cases to entities
- Dependencies point from controllers to use cases to entities
- This makes business rules independent of delivery mechanisms

---

## Component Principles

### What is a Component?

A component is the unit of deployment - the smallest entity that can be deployed as part of a system. In Java, it's a JAR file. In Ruby, a gem. In .NET, a DLL.

### Component Cohesion Principles

#### REP: Reuse/Release Equivalence Principle

**"The granule of reuse is the granule of release."**

- Classes and modules grouped into a component should be releasable together
- If you reuse one class, you implicitly reuse all classes in that component
- Components should have a version number and release documentation
- All classes in a component should share the same version

**Implication:** Don't put unrelated classes together just because they're small. Users will be forced to track releases for things they don't use.

#### CCP: Common Closure Principle

**"Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons."**

This is SRP for components. A component should not have multiple reasons to change.

**Benefits:**
- Limits the number of components that need to be redeployed
- Changes to business rules affect only business rule components
- Changes to reporting affect only reporting components

**Example:** If Order and OrderValidator always change together, put them in the same component. If they change independently, separate them.

#### CRP: Common Reuse Principle

**"Don't force users of a component to depend on things they don't need."**

This is ISP for components. When you depend on a component, you depend on the entire component - every class in it.

**Implication:** If you reuse one class from a component, you're coupled to ALL classes. If ANY class changes, your component may need to be redeployed.

**Solution:** Keep components focused. Don't mix unrelated classes.

### The Tension Triangle

```
        REP
       /    \
      /      \
    CCP ---- CRP
```

These three principles are in tension:
- **REP + CCP** = Group for reuse and closure = Components get large
- **CCP + CRP** = Group for closure and minimal coupling = Hard to reuse
- **CRP + REP** = Group for reuse and minimal coupling = Many small components, lots of releases

**Resolution:** Start with CCP (minimize changes), then relax toward CRP (minimize dependencies), then REP (better packaging). The balance shifts as the system matures.

### Component Coupling Principles

#### ADP: Acyclic Dependencies Principle

**"There must be no cycles in the component dependency graph."**

The dependency graph must be a Directed Acyclic Graph (DAG).

**The Morning After Syndrome:**
You leave code working on Friday. Monday morning, it's broken because someone changed a component you depend on, and they depended on something you changed.

**The Weekly Build Anti-Pattern:**
Everyone ignores each other for four days, then spends Friday integrating. As systems grow, integration takes longer and longer.

**Breaking Cycles:**

Method 1: Dependency Inversion
```
// Before: A -> B -> C -> A (cycle!)
// After: Extract interface, invert dependency
A -> B -> C -> InterfaceA
A implements InterfaceA
```

Method 2: Create New Component
```
// Extract the shared functionality into a new component D
A -> D
B -> D
C -> D
```

#### SDP: Stable Dependencies Principle

**"Depend in the direction of stability."**

A component with many incoming dependencies is stable - it's hard to change because many other components would be affected.

**Stability Metric (I):**
```
I = Fan-out / (Fan-in + Fan-out)

Fan-in: Incoming dependencies (classes outside that depend on classes inside)
Fan-out: Outgoing dependencies (classes inside that depend on classes outside)

I = 0: Maximally stable (only incoming, no outgoing)
I = 1: Maximally unstable (only outgoing, no incoming)
```

**Adults vs. Teenagers:**
- **Adults (I = 0):** Responsible, independent, stable. Hard to change. Many depend on them.
- **Teenagers (I = 1):** Irresponsible, dependent, unstable. Easy to change. No one depends on them.

**The Rule:** Depend on components that are MORE stable than you. Unstable components can depend on stable ones, not vice versa.

**Violation Example:**
```
Stable Component (I=0) --> Unstable Component (I=1)
```
This is wrong! The stable component will be hard to change, but it depends on something that changes frequently.

#### SAP: Stable Abstractions Principle

**"A component should be as abstract as it is stable."**

Stable components should be abstract so they can be extended. Unstable components should be concrete since they'll change anyway.

**Abstractness Metric (A):**
```
A = Na / Nc

Na: Number of abstract classes and interfaces in component
Nc: Total number of classes in component

A = 0: Component is entirely concrete
A = 1: Component is entirely abstract
```

**The Main Sequence:**

Plot components on an A vs. I graph:
```
A (Abstractness)
1 |  Zone of          .
  |  Uselessness    .
  |              .
  |           .   <-- Main Sequence
  |        .
  |     .
  |  .   Zone of Pain
0 +--------------------> I (Instability)
  0                    1
```

**Zone of Pain (0,0):** Highly stable AND highly concrete. Hard to change, and there's no way to extend it. Painful!
- Example: Database schemas, String class (but non-volatile, so acceptable)

**Zone of Uselessness (1,1):** Maximally abstract AND maximally unstable. No one depends on it, and it does nothing concrete. Useless!

**The Main Sequence:** The line from (0,1) to (1,0). Well-designed components fall near this line.

**Distance Metric (D):**
```
D = |A + I - 1|

D = 0: Component is on the Main Sequence
D = 1: Component is as far as possible from the Main Sequence
```

Track D over time. Components drifting away from the Main Sequence need attention.

---

## Design Patterns for Architecture

### The Humble Object Pattern

Separate hard-to-test code from easy-to-test code by placing them in different classes.

**The Pattern:**
- **Humble Object:** Contains all the hard-to-test code (UI, database, etc.) but has very little logic
- **Testable Object:** Contains all the business logic, receives/returns simple data structures

**Examples in Clean Architecture:**
- **Presenter (humble) / View Model (testable):** Presenter puts data into View Model strings
- **Database Gateway (humble) / Interactor (testable):** Gateway handles SQL, Interactor handles logic
- **Service Interface (humble) / Service Implementation (testable)**

```
// Humble - hard to test, minimal logic
class OrderView {
    void display(OrderViewModel vm) {
        nameLabel.setText(vm.customerName);
        totalLabel.setText(vm.formattedTotal);
    }
}

// Testable - easy to test, all logic
class OrderPresenter {
    OrderViewModel present(OrderResponse response) {
        return new OrderViewModel(
            response.customerName,
            "$" + response.total.setScale(2)
        );
    }
}
```

### Singleton Pattern

Ensures a class has only one instance and provides a global point of access.

**Classic Implementation:**
```java
class Singleton {
    private static Singleton instance;
    private static boolean initialized = false;

    private Singleton() {}

    public static Singleton getInstance() {
        if (!initialized) {
            initialized = true;
            instance = new Singleton();
        }
        return instance;
    }
}
```

**Thread-Safe Double-Checked Locking:**
```java
class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized(Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**Problems with Singleton:**
- Global state makes testing difficult
- Hidden dependencies
- Violates SRP (managing instance AND functionality)
- Hard to subclass

**Prefer Monostate for testability.**

### Monostate Pattern

All instances share the same state through static members.

```java
class Monostate {
    private static String sharedState;

    public String getState() { return sharedState; }
    public void setState(String s) { sharedState = s; }
}
```

**Advantages over Singleton:**
- Can be subclassed
- Polymorphism works
- Easier to test (can create test subclass)
- Users don't need to know it's a "singleton"

**Disadvantages:**
- Can't convert normal class to Monostate without changing internals
- Static state persists across tests (need cleanup)

### Visitor Pattern

Add operations to objects without modifying them. Implements "double dispatch."

**The 90-Degree Rotation:**
Traditional OOP: Type hierarchy on one axis, operations as methods
Visitor: Type hierarchy on one axis, operations on another axis

```java
interface Shape {
    void accept(ShapeVisitor visitor);
}

interface ShapeVisitor {
    void visit(Circle c);
    void visit(Rectangle r);
}

class AreaCalculator implements ShapeVisitor {
    void visit(Circle c) { /* calculate circle area */ }
    void visit(Rectangle r) { /* calculate rectangle area */ }
}
```

**Trade-off:**
- Easy to add new operations (new Visitor implementations)
- Hard to add new types (must modify all Visitors)

**When to Use:** When new operations are more common than new types.

### Acyclic Visitor Pattern

Breaks the dependency cycle in Visitor by using marker interfaces.

```java
interface Visitor {}  // Marker interface

interface CircleVisitor {
    void visit(Circle c);
}

interface RectangleVisitor {
    void visit(Rectangle r);
}

class Circle implements Shape {
    void accept(Visitor v) {
        if (v instanceof CircleVisitor) {
            ((CircleVisitor) v).visit(this);
        }
    }
}

class AreaCalculator implements Visitor, CircleVisitor, RectangleVisitor {
    void visit(Circle c) { /* ... */ }
    void visit(Rectangle r) { /* ... */ }
}
```

**Trade-offs:**
- No cycle in dependencies
- Can add new types without modifying existing Visitors
- Runtime type checking (performance cost, loss of type safety)
- Sparse matrix of implementations

### Proxy Pattern

Provide a surrogate or placeholder for another object to control access.

**Types:**
- **Remote Proxy:** Represents object in different address space (RPC, sockets)
- **Virtual Proxy:** Creates expensive object on demand
- **Protection Proxy:** Controls access based on permissions
- **Database Proxy:** Handles database connections and transactions

```java
interface Database {
    void store(Object o);
    Object retrieve(String id);
}

class DatabaseProxy implements Database {
    private RealDatabase realDb;

    void store(Object o) {
        connect();
        realDb.store(o);
    }

    private void connect() {
        if (realDb == null) {
            realDb = new RealDatabase();
        }
    }
}
```

**Handle-Body Pattern:** Proxy (handle) wraps the real object (body). Multiple handles can share one body.

### Observer Pattern

Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

**Pull Model:**
```java
interface Observer {
    void update();  // No data passed
}

class Subject {
    List<Observer> observers;

    void notifyObservers() {
        for (Observer o : observers) {
            o.update();  // Observer must pull data
        }
    }
}
```

**Push Model:**
```java
interface Observer {
    void update(Event e);  // Data pushed to observer
}
```

**Pull vs. Push:**
- Pull: Observer has more control, but must know about Subject
- Push: Subject has more control, Observer is more passive

**Watch for:** Multiple inheritance issues when Subject also has business type hierarchy.

### Factory Pattern

Create objects without specifying exact classes.

**Simple Factory:**
```java
class ShapeFactory {
    Shape create(String type) {
        switch(type) {
            case "circle": return new Circle();
            case "rectangle": return new Rectangle();
        }
    }
}
```

**Abstract Factory:**
```java
interface GUIFactory {
    Button createButton();
    Window createWindow();
}

class MacFactory implements GUIFactory {
    Button createButton() { return new MacButton(); }
    Window createWindow() { return new MacWindow(); }
}
```

**Factory and OCP:**
Factories allow you to add new types without modifying client code - but the factory itself must be modified. This is an acceptable trade-off; you're localizing the change to one place.

**Type Safety Trade-off:**
Using strings or enums to select types abandons compile-time type safety. Accept this at the boundary where configuration meets code.

---

## Boundaries and Boundary Crossing

### What is a Boundary?

A boundary is a line of separation between software components. Boundaries define what knows about what.

### Types of Boundaries

1. **Source-Level Boundaries:** Function calls within same codebase, separated by interfaces
2. **Deployment Boundaries:** Separate JAR files, DLLs, deployed together
3. **Service Boundaries:** Separate processes, network communication

### Rules for Boundaries

1. **Dependencies point inward** - toward higher-level policy
2. **Data structures cross boundaries** - not entities or implementations
3. **Lower-level components call higher-level interfaces** - not concrete classes
4. **The boundary is defined by the interface** - not the implementation

### Boundary Data Structures

```java
// Crossing into the use case
class CreateOrderRequest {
    String customerId;
    List<String> productIds;
    // Simple types only!
}

// Crossing out of the use case
class CreateOrderResponse {
    String orderId;
    String status;
    // Simple types only!
}
```

**Never cross boundaries with:**
- Entity objects
- Database rows
- Framework objects
- Any class from another layer

### The Dependency Inversion at Boundaries

```
┌─────────────────────────────────────────────────┐
│                   Controller                     │
│                      │                           │
│                      ▼                           │
│              <<interface>>                       │
│            InputBoundary                         │
│                      ▲                           │
│                      │                           │
│  ┌───────────────────┼───────────────────────┐  │
│  │               Interactor                   │  │
│  │                   │                        │  │
│  │                   ▼                        │  │
│  │           <<interface>>                    │  │
│  │          OutputBoundary                    │  │
│  └───────────────────┬───────────────────────┘  │
│                      │                           │
│                      ▼                           │
│                  Presenter                       │
└─────────────────────────────────────────────────┘

Dependencies: Controller --> InputBoundary <-- Interactor --> OutputBoundary <-- Presenter
```

The Interactor sits in the center. It implements the InputBoundary and uses the OutputBoundary. Control flows through Interactor, but dependencies point toward it.

---

## Database Independence

### The Database is a Detail

The database is an IO device. From the business rules' perspective, it's just a way to persist and retrieve data. The specific database (MySQL, PostgreSQL, MongoDB) should not affect business rules.

### Separating Database Concerns

```
┌─────────────────────────────────────────────────┐
│                   Use Case                       │
│                      │                           │
│                      ▼                           │
│              <<interface>>                       │
│              DataGateway                         │
│                      ▲                           │
│                      │                           │
│              DatabaseGateway                     │
│                      │                           │
│                      ▼                           │
│                  Database                        │
└─────────────────────────────────────────────────┘
```

**DataGateway Interface:** Defined by the use case layer, speaks in terms of entities and business concepts.

**DatabaseGateway Implementation:** Lives in the outer layer, knows SQL, ORM, connection pooling, etc.

### Why This Matters

1. **Testability:** Use cases can be tested with in-memory implementations
2. **Flexibility:** Can switch databases without changing business logic
3. **Clarity:** Business rules aren't polluted with SQL
4. **Performance optimization:** Database team can optimize without touching business code

---

## Framework Independence

### Frameworks are Details

Frameworks are tools, not architectures. They should serve your architecture, not dictate it.

### The Asymmetric Marriage

When you adopt a framework:
- You make a commitment to the framework
- The framework makes no commitment to you
- You follow their conventions
- They can change whenever they want

### Protecting Against Framework Changes

1. **Don't derive business entities from framework base classes**
2. **Don't let framework annotations invade business logic**
3. **Isolate framework dependencies to outer layers**
4. **Use interfaces to abstract framework capabilities**

```java
// Bad - Entity coupled to framework
@Entity
@Table(name="customers")
class Customer {
    @Id
    @GeneratedValue
    Long id;
    // Business logic mixed with persistence annotations
}

// Good - Entity is pure
class Customer {
    CustomerId id;
    // Pure business logic
}

// Framework details in outer layer
@Entity
@Table(name="customers")
class CustomerJpaEntity {
    @Id
    @GeneratedValue
    Long id;
    // Only persistence concerns
}
```

---

## Testing Architecture

### The Testing Pyramid in Clean Architecture

```
           /\
          /  \
         /E2E \
        /______\
       /        \
      /Integration\
     /______________\
    /                \
   /    Unit Tests    \
  /____________________\
```

### What Each Test Level Covers

**Unit Tests:**
- Entities and their business rules
- Interactors with mock gateways
- Presenters with test data
- Isolated, fast, no I/O

**Integration Tests:**
- Interactors with real gateways (test database)
- Controller to Presenter flows
- Component boundaries

**End-to-End Tests:**
- Full stack with real UI, database, and services
- Slow, fragile, few in number

### Testing Through the Architecture

```java
// Testing an Interactor
class CreateOrderTest {
    @Test
    void createsOrder() {
        // Arrange
        InMemoryOrderGateway gateway = new InMemoryOrderGateway();
        TestPresenter presenter = new TestPresenter();
        CreateOrderInteractor interactor =
            new CreateOrderInteractor(gateway, presenter);

        // Act
        interactor.execute(new CreateOrderRequest("cust-1", List.of("prod-1")));

        // Assert
        assertEquals("ORD-001", presenter.response.orderId);
        assertNotNull(gateway.find("ORD-001"));
    }
}
```

### The Humble Object Pattern in Testing

UI components, database access, and external services are humble objects:
- Contain minimal logic
- Difficult to unit test
- Tested through integration/E2E tests

Business logic lives in testable objects:
- Contains all decision-making
- Easy to unit test
- Covered thoroughly by unit tests

---

## Screaming Architecture

### Architecture Should Scream Its Intent

When you look at the top-level directory structure, it should tell you what the system does, not what frameworks it uses.

**Bad - Screams "Rails":**
```
/app
  /models
  /views
  /controllers
/config
/db
```

**Good - Screams "Health Clinic":**
```
/patients
/appointments
/billing
/medical_records
/prescriptions
```

### Package by Feature, Not Layer

Group code by business capability, not technical role.

**By Layer (avoid):**
```
/controllers
  OrderController
  CustomerController
/services
  OrderService
  CustomerService
/repositories
  OrderRepository
  CustomerRepository
```

**By Feature (prefer):**
```
/orders
  CreateOrderUseCase
  OrderController
  OrderRepository
/customers
  RegisterCustomerUseCase
  CustomerController
  CustomerRepository
```

---

## Common Architectural Mistakes

### 1. Database-Driven Design
Starting with the database schema and letting it drive the domain model. Instead, start with use cases and entities.

### 2. Framework-Driven Design
Letting the framework dictate your architecture. The framework should live at the edges.

### 3. Putting Business Logic in Controllers
Controllers should only:
- Parse input
- Call use case
- Format output

### 4. Passing Entities Across Boundaries
Entities should stay within their layer. Use DTOs to cross boundaries.

### 5. Circular Dependencies
If A depends on B and B depends on A, you have a design problem. Use dependency inversion.

### 6. God Classes
Single classes that do everything. Split by responsibility.

### 7. Feature Envy
A class that uses another class's data more than its own. Move the behavior.

### 8. Shotgun Surgery
A single change requires modifications across many classes. Consolidate related functionality.

---

## Memorable Quotes

> "Architecture is about intent." - The structure should communicate what the system does.

> "A good architecture maximizes the number of decisions not made." - Keep options open.

> "The database is a detail." - Don't let it drive your architecture.

> "Frameworks are details." - They serve you, not the other way around.

> "The web is a detail." - HTTP is just a delivery mechanism.

> "Good architecture makes the system easy to change." - That's the whole point.

> "The first concern of the architect is to make sure that the house is usable, it is not to ensure that the house is made of brick." - Use cases come before technology choices.

> "You can use an FP language and still make a huge OO mess. You can use an OO language and make beautiful FP code." - Paradigms are tools.

> "There are two values of software: the behavior and the structure. The structure is more important." - A system that works but can't change is worthless.

> "The goal of software architecture is to minimize the human resources required to build and maintain the required system." - It's about economics.

> "Stable components should be abstract. Unstable components should be concrete."

> "Adults are responsible and independent. Teenagers are irresponsible and dependent." - On component stability.

> "The morning after syndrome - you leave Friday with working code, Monday it's broken." - Why we need acyclic dependencies.

---

## Architecture Review Checklist

Use this checklist when reviewing architecture decisions:

### Dependency Rule
- [ ] Do all dependencies point inward toward higher-level policy?
- [ ] Are entities free of framework dependencies?
- [ ] Are use cases free of UI and database details?
- [ ] Are there any circular dependencies?

### Boundaries
- [ ] Are boundaries defined by interfaces, not implementations?
- [ ] Do data structures cross boundaries, not entities?
- [ ] Is Dependency Inversion applied at each boundary?

### Components
- [ ] Is the component graph acyclic (DAG)?
- [ ] Do stable components depend on nothing?
- [ ] Do unstable components depend on stable abstractions?
- [ ] Are components cohesive (CCP, REP, CRP balanced)?

### SOLID
- [ ] Does each class have a single responsibility?
- [ ] Can new behavior be added without modifying existing code?
- [ ] Are subtypes substitutable for their base types?
- [ ] Are interfaces segregated for different clients?
- [ ] Do high-level modules depend on abstractions?

### Testability
- [ ] Can business rules be tested without UI, database, or external services?
- [ ] Are humble objects minimal?
- [ ] Can gateways be easily mocked?

### Intent
- [ ] Does the architecture scream its business purpose?
- [ ] Are packages organized by feature, not layer?
- [ ] Can a new developer understand the domain from the structure?

---

## When to Apply These Principles

### For Small Projects
- Focus on use cases and entities first
- Keep boundaries simple (interfaces within same codebase)
- Don't over-engineer component structure

### For Growing Projects
- Introduce explicit boundaries as complexity grows
- Extract components as teams grow
- Monitor dependency metrics

### For Large Systems
- Full Clean Architecture with all layers
- Multiple deployable components
- Formal component dependency management
- Continuous architectural fitness functions

### Remember
The goal is not perfect adherence to all principles, but a system that:
1. Is easy to understand
2. Is easy to change
3. Is easy to test
4. Communicates its intent

**Start simple. Add complexity only when needed. Always ask: "Does this make the system easier to change?"**

---

## Feature to Implement

$ARGUMENTS

## Implementation Steps

1. **Define the Use Case**
   - What is the application trying to do?
   - What are the inputs (Request Model)?
   - What are the outputs (Response Model)?

2. **Identify Entities**
   - What business objects are involved?
   - What business rules do they encapsulate?

3. **Define Gateway Interfaces**
   - What external data is needed?
   - Define interfaces in the use case layer

4. **Implement the Interactor**
   - Pure business logic
   - Uses entities and gateways
   - Returns response model

5. **Create Interface Adapters**
   - Controller to handle input
   - Presenter to format output
   - Gateway implementations

6. **Wire Up Framework Layer**
   - Connect to web framework
   - Connect to database
   - Inject dependencies (pointing inward)

---

## Related Skills

- **/professional** - Apply professional standards workflow for code quality, naming conventions, formatting, and maintainability
