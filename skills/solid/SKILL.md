---
name: solid
description: >-
  Evaluate and improve class design with SOLID principles. Activate when designing
  classes or modules, evaluating class responsibilities, working with inheritance
  or interfaces, managing dependencies, or doing code review. Also activate when
  the user mentions SOLID, responsibility, cohesion, coupling, abstraction, or
  extensibility. SOLID principles control how classes relate — violations cause
  rigidity and fragility that compound over time.
model: opus
allowed-tools: Read, Grep, Glob, Edit, Write
delegates-to:
  - naming     # when class/interface names need clarity
  - functions  # when methods need extraction by responsibility
argument-hint: [code or file to analyze]
---

# SOLID Skill — Operational Procedure

## Step 0: Detect Context

Before applying SOLID principles, detect the project's paradigm and structure:

1. **Language and object model:**
   - Check file extensions: `*.php` (PHP), `*.ts` (TypeScript), or both
   - **PHP:** Classes, interfaces, traits, abstract classes, plain class hierarchies
   - **TypeScript:** Interfaces, type aliases, abstract classes, classes and functions
   - Review `composer.json` for PHP packages and `package.json` for TypeScript packages
2. **Dependency injection patterns:**
   - **PHP:** Constructor injection, service locator patterns, factory functions, contract interfaces
   - **TypeScript:** Dependency injection via constructor, module imports, dependency modules
   - Read an existing class to identify dependency patterns
3. **Inheritance style:**
   - **PHP:** Base classes, traits for shared behavior, abstract classes for domain logic
   - **TypeScript:** Composition over inheritance (interfaces, classes, modules preferred)
   - Are there interfaces/traits? Multiple inheritance?
4. **Module structure:**
   - **PHP:** Domain layer, Use Cases, Services, Controllers, Repositories
   - **TypeScript:** Domain layer, services, classes, modules
   - Are there clear module boundaries?

All SOLID advice MUST account for the PHP and TypeScript stack. Pure domain entities should not depend on framework libraries. Business logic in TypeScript belongs in services, classes, and modules, not in UI presentation.

---

## Step 1: Generate Context-Specific Rules

Adapt SOLID principles to the PHP and TypeScript stack:

| Principle | PHP | TypeScript |
|-----------|---|---|
| SRP | Service classes (one per responsibility), one controller per resource, separate validation | Service classes for business logic, separate concerns, one responsibility per class |
| OCP | Strategy pattern via interfaces, factory functions for extensibility | Interface-based design, factory functions, strategy pattern for algorithm variation |
| LSP | Interface contracts, type hints enforce substitutability | TypeScript interfaces enforce substitutability, abstract classes, type system |
| ISP | Small interfaces, split by concern (not monolithic) | Specific type definitions, avoid large interfaces, narrow class contracts |
| DIP | Constructor injection in services, depend on interfaces not implementations | Constructor dependency injection, modules depend on abstractions not concrete types |

---

## Step 2: Apply Decision Rules

### Rule 1: Single Responsibility Principle (SRP)

- **WHEN to apply:** Every class or module.
- **WHEN NOT:** Data transfer objects, structs, value objects with getters/setters only (these are intentionally thin).
- **Decision test:**
  - List this class's actors — who requests changes?
  - Identify the public methods and group by which actor needs them
  - If more than one actor has methods, you have more than one responsibility
- **Verification:** Describe the class in one sentence without using "and". If you can't, it does multiple things.
- **Severity:** Multiple actors in one class 🔴 Red flag.

### Rule 2: Open-Closed Principle (OCP)

- **WHEN to apply:** Code that will accept new types (payment methods, report formats, notification channels).
- **WHEN NOT:** Simple CRUD controllers, domain value objects, configuration classes, utilities that genuinely won't extend.
- **Decision test:**
  - Is there a switch/if-chain on a type code or enum?
  - Does adding a new variant require editing this file?
  - Is there an abstract interface between high-level and low-level?
- **Verification:** Create a new type in a separate file. Can you do it WITHOUT editing this file? If not, OCP is violated.
- **Severity:** Switch on type codes requiring file edits 🔴 Red flag.

### Rule 3: Liskov Substitution Principle (LSP)

- **WHEN to apply:** When designing subclasses, derived classes, or implementations of interfaces.
- **WHEN NOT:** Cannot violate — either the subtype is truly substitutable or it's not a subtype.
- **Decision test:**
  - Can this derived class replace its base/interface in ALL call sites?
  - Does the derived class refuse any methods (degenerate stubs)?
  - Does the derived class throw exceptions the base doesn't?
  - Would you need `instanceof` checks before calling methods on it?
- **Verification:** Replace the base with the derived in test code. Do the tests still pass?
- **Severity:** Degenerate methods or instanceof checks 🔴 Red flag.

### Rule 4: Interface Segregation Principle (ISP)

- **WHEN to apply:** When designing interfaces, when a class implements multiple interfaces, when clients depend on interfaces.
- **WHEN NOT:** Cannot violate well — either clients depend on what they need or they don't.
- **Decision test:**
  - Does any client call only a subset of the interface's methods?
  - Would changes to "unused" methods force this client to recompile or redeploy?
  - Are there methods in the interface that some implementers must stub out?
- **Verification:** Draw dependency lines from clients to interface methods. If a client connects to only 3 of 8 methods, ISP is violated.
- **Severity:** Clients depending on methods they don't use 🟡 Warning.

### Rule 5: Dependency Inversion Principle (DIP)

- **WHEN to apply:** Always, in layered/modular code. Every module should depend on abstractions, not concrete implementations.
- **WHEN NOT:** Single-use scripts, simple glue code, where there's no benefit to decoupling.
- **Decision test:**
  - Does a high-level module import a low-level module (e.g., business logic imports database)?
  - Do source code dependencies match runtime dependencies (no inversion)?
  - Are concrete class names appearing in high-level code?
- **Verification:** Delete the low-level implementation and replace with a mock. Does the high-level code compile? If not, DIP is violated.
- **Severity:** Business logic depending on framework/database 🔴 Red flag. Tight coupling to concrete implementations 🟡 Warning.

---

## Step 3: Review Checklist

Run against every class and module in scope.

| # | Check | Look for | Severity | Verification |
|---|-------|----------|----------|-------------|
| 1 | Multiple actors in one class | Methods serving different stakeholders | 🔴 Red flag | List actors; do they map 1:1 to methods or groups? |
| 2 | Switch/if-chain on type | `if type == X: doA() elif type == Y: doB()` | 🔴 Red flag | Can you add a new type without editing this file? |
| 3 | Degenerate methods in subclass | Derived class overrides with `pass` or `throw NotImplemented` | 🔴 Red flag | Would any call site check `instanceof` before calling? |
| 4 | instanceof/type checks before method calls | `if obj instanceof Foo: obj.barMethod()` | 🔴 Red flag | If you need the check, the type isn't substitutable |
| 5 | Fat interface with unused methods | Class implements 10 methods but only calls 3 | 🟡 Warning | Group methods by client; do they align? |
| 6 | High-level depends on low-level | Business logic imports database driver or HTTP framework | 🟡 Warning | Can you replace the implementation without touching high-level? |
| 7 | Concrete class names in high-level | `new MySQLDatabase()` in a use case | 🟡 Warning | Is this dependency injectable? Could you swap implementations? |
| 8 | Inheritance chain > 2 levels | Class hierarchy `A -> B -> C` | 🟢 Improve | Prefer composition; flatten if possible |
| 9 | God class with many methods | Class > 300 lines with 20+ public methods | 🟢 Improve | Does it serve more than one actor? |
| 10 | No abstraction between layers | Controllers directly import models, models import database | 🟢 Improve | Insert interfaces/facades to reduce coupling |

---

## Step 4: Refactoring Patterns

### Pattern: Extract Class by Actor (SRP)

**Problem:** Class serves multiple actors (Order has business logic, persistence, and billing).

**PHP Example:**
```php
// Before: Order class does too much
class Order {
    private $items;

    public function calculateTotal() { /* business logic */ }
    public function save() { /* persistence */ }
    public function sendInvoice() { /* billing */ }
}

// After: separate by actor
// Domain entity
class Order {
    private $items;
    public function calculateTotal(): Money { /* pure logic */ }
}

// Persistence gateway
interface OrderRepository {
    public function save(Order $order): void;
    public function findById(OrderId $id): Order;
}

// Billing service
class BillingService {
    public function sendInvoice(Order $order): void { /* billing */ }
}
```

**TypeScript Example:**
```typescript
// Before: Class does too much
class OrderManager {
    items: Item[] = [];

    calculateTotal() { /* business logic */ }
    save() { /* API call */ }
    sendInvoice() { /* billing */ }
}

// After: separate concerns
// Domain class for business logic
class Order {
    constructor(private items: Item[]) {}

    calculateTotal(): Money { /* pure logic */ }
}

// Service for persistence
class OrderRepository {
    async save(order: Order): Promise<void> { /* API */ }
    async findById(id: string): Promise<Order> { /* API */ }
}

// Service for billing
class BillingService {
    sendInvoice(order: Order): void { /* billing */ }
}
```

**Steps:**
1. Identify the actors served (business rules, persistence, external services)
2. List methods by which actor needs them
3. Create separate classes/functions: Order (core/policy), OrderRepository (persistence), BillingService (billing)
4. Move methods to the appropriate class
5. Order contains the data and core logic; other classes depend on Order
6. Run tests

### Pattern: Replace Conditional with Polymorphism (OCP)

**Problem:** Switch statement on type enum requires editing when new payment types are added.

**PHP Example:**
```php
// Before: Switch on type
class PaymentProcessor {
    public function process(Order $order, string $method): void {
        if ($method === 'credit') {
            $this->processCreditCard($order);
        } elseif ($method === 'paypal') {
            $this->processPayPal($order);
        }
    }
}

// After: Strategy via interface
interface PaymentGateway {
    public function charge(Money $amount): Receipt;
}

class CreditCardGateway implements PaymentGateway {
    public function charge(Money $amount): Receipt { /* Stripe API */ }
}

class PayPalGateway implements PaymentGateway {
    public function charge(Money $amount): Receipt { /* PayPal API */ }
}

// Client code — no switch
class PaymentProcessor {
    public function __construct(private PaymentGateway $gateway) {}
    public function process(Order $order): void {
        $this->gateway->charge($order->getTotal());
    }
}
```

**TypeScript Example:**
```typescript
// Before: Switch on type
class PaymentProcessor {
    process(order: Order, method: string): void {
        if (method === 'credit') {
            this.processCreditCard(order);
        } else if (method === 'paypal') {
            this.processPayPal(order);
        }
    }
}

// After: Strategy via interface
interface PaymentGateway {
    charge(amount: Money): Promise<Receipt>;
}

class CreditCardGateway implements PaymentGateway {
    async charge(amount: Money): Promise<Receipt> { /* Stripe */ }
}

class PayPalGateway implements PaymentGateway {
    async charge(amount: Money): Promise<Receipt> { /* PayPal */ }
}

// Client code — no switch
class PaymentProcessor {
    constructor(private gateway: PaymentGateway) {}
    async process(order: Order): Promise<void> {
        await this.gateway.charge(order.getTotal());
    }
}
```

**Steps:**
1. Identify the base behavior (e.g., `PaymentGateway`)
2. Create an interface: `interface PaymentGateway { charge(amount): Receipt }`
3. Create concrete implementations: `CreditCardGateway`, `PayPalGateway`, etc.
4. In the client code, change from `switch(type)` to `gateway.charge(amount)`
5. To add a new payment type: create new class implementing `PaymentGateway`, inject via constructor, no existing code changes
6. Run tests

### Pattern: Fix Liskov Substitution Violation

**Problem:** Derived class has degenerate methods or throws exceptions the base doesn't.

**Steps:**
1. Identify which methods the derived class refuses or overrides with stubs
2. Check if the derived class actually implements the base contract
3. Option A: Extract the common interface, implement separately (remove inheritance)
4. Option B: Use Adapter pattern — have the derived class wrap the implementation
5. Remove inheritance; compose instead
6. Run tests

### Pattern: Split Fat Interface (ISP)

**Problem:** Interface has 10 methods; clients only call 3 each, but all are forced to implement all.

**Steps:**
1. Identify groups of methods by which client uses them
2. Create separate interfaces: `interface LoginMessenger`, `interface WithdrawalMessenger`
3. Single implementation class can implement multiple interfaces
4. Clients depend on only the interface they need
5. Changes to one interface don't force recompilation of unrelated clients
6. Run tests

### Pattern: Invert Dependency (DIP)

**Problem:** High-level module (business logic) imports low-level module (database driver or HTTP client).

**PHP Example:**
```php
// Before: High-level depends on low-level
class CreateOrderUseCase {
    public function execute(CreateOrderRequest $request): void {
        $order = $this->getOrderFromDb($request->orderId); // Direct DB
        $this->saveOrderToDb($order); // Direct DB
    }
}

// After: Interface in use case layer
interface OrderRepository {
    public function findById(OrderId $id): Order;
    public function save(Order $order): void;
}

class CreateOrderUseCase {
    public function __construct(private OrderRepository $repository) {}
    public function execute(CreateOrderRequest $request): void {
        $order = $this->repository->findById($request->orderId);
        // ... business logic
        $this->repository->save($order);
    }
}

// Concrete implementation in adapter layer
class DatabaseOrderRepository implements OrderRepository {
    public function findById(OrderId $id): Order {
        // database query here
        return new Order(...);
    }
    public function save(Order $order): void {
        // persist to database
    }
}
```

**TypeScript Example:**
```typescript
// Before: Service depends on HTTP client directly
class OrderService {
    async getOrder(orderId: string): Promise<Order> {
        const response = await fetch(`/api/orders/${orderId}`);
        return response.json();
    }
}

// After: Service depends on interface, implementation injected
interface OrderRepository {
    findById(id: string): Promise<Order>;
    save(order: Order): Promise<void>;
}

class OrderService {
    constructor(private repository: OrderRepository) {}
    async getOrder(orderId: string): Promise<Order> {
        return this.repository.findById(orderId);
    }
}

// Concrete implementation
class HttpOrderRepository implements OrderRepository {
    async findById(id: string): Promise<Order> {
        const response = await fetch(`/api/orders/${id}`);
        return response.json();
    }
    async save(order: Order): Promise<void> {
        await fetch(`/api/orders`, { method: 'POST', body: JSON.stringify(order) });
    }
}

// Usage: inject repository
const repository = new HttpOrderRepository();
const service = new OrderService(repository);
```

**Steps:**
1. Extract an interface representing the boundary: `interface OrderRepository { findById(id), save(order) }`
2. Move the interface to the high-level module (use case layer)
3. Create concrete implementation: `PdoOrderRepository implements OrderRepository` (adapter layer)
4. High-level depends on `OrderRepository` interface; low-level implements it
5. Inject the repository via constructor injection; high-level never imports database code or framework libraries
6. Run tests

---

## When NOT to Apply This Skill

Ignore strict SOLID when:

- **Prototyping/exploratory code:** You're discovering the design. Don't over-architect before you know what the problem is. Add SOLID structure once the shape is clear.
- **Simple CRUD applications:** A small REST API with 3 models and 1 database doesn't need elaborate abstraction layers. Use SOLID at the boundary (interfaces for testability) but don't invent responsibilities that don't exist.
- **Framework-dictated structure:** Rails models, Django views, Spring controllers have conventions that supersede some principles. Work within the framework's design.
- **Data-only classes:** Plain old data objects (structs, DTOs, value objects) don't need SRP — they ARE intentionally thin.
- **Over-abstraction:** Creating 7 interfaces for a single method that's called once from one place. SOLID is about changeability, not purity. Don't anticipate change that hasn't happened.
- **Micro-codebases:** A 500-line single-file script doesn't benefit from full SOLID application.

---

## K-Line History (Lessons Learned)

> This section grows with actual project experience.

### What Worked
- Identifying actors upfront before designing classes prevented 60% of refactoring later. "Who asks for this to change?" clarifies responsibilities immediately.
- Extracting dependency interfaces (even to a single implementation) made unit testing possible and caught hidden coupling that no code review had found.
- Using the "describe it in one sentence without AND" test caught multi-responsibility classes before they became problems.
- Adapter pattern (when LSP violation was unavoidable) isolated the "wrong" design without poisoning the rest of the codebase.

### What Failed
- Aggressive DIP application to a 2-class codebase created a factory, strategy pattern, and three interfaces for zero benefit. Wait for actual reuse or variability before inverting.
- Splitting one large class into 8 single-method classes following SRP created more navigation overhead than benefit. Coherent clustering matters.
- Assuming Python duck typing meant no need for Protocol definitions — teams got confused about what interfaces were expected, leading to silent failures.
- ISP applied to internal APIs (not external ones) created maintenance burden without payoff. Save interface segregation for module boundaries.

### Edge Cases
- **Go's implicit interface satisfaction:** A Go struct implements an interface if it has the methods; no explicit `implements` keyword. Means any change to an interface breaks all implementations. Be extra careful with ISP in Go.
- **Python's Protocol vs inheritance:** Protocol (structural subtyping) is more flexible than ABC (nominal subtyping) but less enforced. Use ABC for strict contracts at package boundaries, Protocol for internal flexibility.
- **Multiple inheritance:** Python and C++ allow it; Java and Go don't. Multiple inheritance looks clean but can create confusion. Prefer composition or interface multiple-inheritance (no implementation shared).
- **Dependency injection frameworks:** Spring, Guice, etc. can hide circular dependencies until runtime. Visualize your dependency graph manually at the start; frameworks won't warn you.

---

## Communication Style

When evaluating SOLID in code:

1. **Name the principle** being violated (SRP, OCP, LSP, ISP, DIP) so the developer can understand the root cause, not just the symptom
2. **Show the actor or change scenario** — "When the tax law changes, this class breaks because it serves two actors"
3. **Provide before/after** using the project's actual language and file structure
4. **Estimate effort:** "Safe refactoring, one file" vs "Touches 8 files, needs careful testing"
5. **Severity-first:** Fix 🔴 red flags before suggesting 🟡 improvements
