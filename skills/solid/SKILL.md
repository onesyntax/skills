---
name: solid
description: >-
  Apply SOLID principles to class and module design. Activate whenever designing
  new classes, reviewing class responsibilities, working with interfaces or
  abstractions, refactoring, or doing code review. Also activate when the user
  mentions SOLID, single responsibility, open-closed, dependency inversion,
  interface segregation, Liskov substitution, or dependency management. SOLID
  governs how classes relate to each other — get it wrong and the system rots.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# SOLID Skill

The SOLID principles are five dependency management principles that control relationships between classes. The essential quality of object-oriented design is the ability to **invert key dependencies**, protecting high-level policies from low-level details. When dependencies oppose the flow of control, the system doesn't rot.

**Important:** No design should be fully SOLID compliant — that's an oxymoron. The principles illuminate design issues and recommend solutions. Use them to make trade-offs, not as rigid dogma.

For detailed SOLID walkthroughs with before/after examples, read `references/extended-examples.md`.

### The Two Values of Software

Software has exactly two values: **behavior** (what it does now) and **structure** (the ability to change it). Structure is more important — a system that works but can't change becomes worthless as requirements evolve. Your primary job is to give software a shape that makes it easy to change. SOLID principles serve this primary value.

### Design Smells That SOLID Prevents

- **Rigidity**: Small changes force large rebuilds due to coupled modules
- **Fragility**: Changes to one module cause unrelated modules to misbehave
- **Immobility**: Internal components cannot be easily extracted and reused
- **Viscosity**: Necessary operations like building and testing are difficult to perform
- **Needless Complexity**: Anticipatory design adds weight without current benefit

When you detect these smells, one or more SOLID principles are being violated.

---

## Before Applying Any Principle: Identify Actors

An **actor** is a role (not a person) that uses the system and can request changes. Users wear multiple hats — responsibilities are tied to actors, not individuals.

Ask:
- Who are the actors served by this module?
- What families of functions serve each actor?
- Are multiple actors served by the same module?

The actor for a responsibility is the single source of change for that responsibility. This understanding drives everything that follows.

---

## SRP: Single Responsibility Principle

**A module should have one, and only one, reason to change.**

Another way: gather together things that change for the same reasons, separate things that change for different reasons.

A "responsibility" is NOT just "what a class does." It's tied to an **actor** — a group of users who will request changes. If two different actors depend on the same module, their changes will collide.

```
// Bad — three actors, three reasons to change
class Employee:
    calculatePay()       // Policy actor (accountants)
    save()               // Architecture actor (DBAs)
    describeEmployee()   // Operations actor (report consumers)

// Good — separated by actor
class Employee:          // data and policy rules
class EmployeeGateway:   // database operations
class EmployeeReporter:  // reporting functions
```

### SRP Violation Examples

```
// Violation: direction logic mixed with display formatting
move():
    directions = getAvailableDirections()
    message = "You can go: " + join(directions, ", ")
    display(message)
// Two responsibilities: determining directions AND formatting output

// Violation: game mechanics mixed with game policy
shootArrow():
    followArrowPath()
    if hitTarget:
        terminateGame()  // Policy decision buried in mechanics!

// Violation: logging intertwined with business logic
execute():
    if verbose: log("Starting execution")
    doSomething()
    if verbose: log("Step completed")
    doSomethingElse()
    if verbose: log("Execution finished")
// Fix: extract logging into a decorator/wrapper
```

### Detecting SRP Violations

- Multiple actors affected by one module
- Accidental coupling: shared code that changes for different reasons
- Mixed concerns: business rules next to UI formatting, persistence next to domain logic
- Changes for one purpose break another

### Refactoring Techniques

1. **Split into separate classes** — one per actor
2. **Facade pattern** — single entry point delegating to separate implementations
3. **Interface segregation** — one interface per actor, single class implements all
4. **Extract and compose** — decorator/wrapper for cross-cutting concerns like logging

---

## OCP: Open-Closed Principle

**Software entities should be open for extension, but closed for modification.**

You should be able to add new functionality by adding new code, not changing old code. Old code that doesn't change can't rot.

The mechanism: insert an abstract interface between high-level policy and low-level details. Invert the dependencies so they oppose the flow of control.

```
// Bad — adding a new payment type requires modifying this function
checkout():
    switch paymentType:
        CASH: handleCash()
        CREDIT: handleCredit()
        // must add new cases here

// Good — new payment types extend, nothing changes
interface PaymentMethod:
    getPayment()

checkout(method: PaymentMethod):
    payment = method.getPayment()
    receipt.addPayment(payment)
// Add CryptoPayment without touching checkout
```

### The Crystal Ball Problem

OCP only protects you from changes you predicted. Two approaches:

**BDUF:** Anticipate everything upfront. Results in heavy, over-abstracted designs.

**Agile Design:** Do the simplest thing. When actual changes come, add abstractions to protect from *that kind* of change going forward. Past change is the best predictor of future change.

### The Expense Report Example

```
// Bad — adding lunch requires changing enum AND hunting every switch
printExpense(expense):
    switch expense.type:
        DINNER: name = "Dinner"
        BREAKFAST: name = "Breakfast"
        CAR_RENTAL: name = "Car Rental"
    // More switch statements for overage checking, meal flags, etc.

// Good — adding lunch means adding one new class, no existing code changes
abstract class Expense:
    getName()
    isMeal()
    isOverage()

class DinnerExpense extends Expense:
    getName(): return "Dinner"
    isMeal(): return true
    isOverage(): return amount > 5000

// class LunchExpense extends Expense: ...  ← just add this
```

### Detecting OCP Violations

- Switch statements on type codes
- Adding a new type requires changing multiple existing files
- Rigid: small design changes cascade through the system

---

## LSP: Liskov Substitution Principle

**Subtypes must be substitutable for their base types.**

If S is a subtype of T, objects of type S can replace objects of type T without breaking the program. A subtype can do MORE but never LESS than its parent.

### The Square/Rectangle Problem

```
class Rectangle:
    setHeight(h): height = h
    setWidth(w): width = w
    area(): return height * width

class Square extends Rectangle:
    setHeight(h): height = h; width = h   // violates LSP!
    setWidth(w): height = w; width = w
```

A user of Rectangle expects setting width doesn't change height. Square breaks this expectation. Geometrically a square IS a rectangle — but in code, the representative of Square is NOT a subtype of the representative of Rectangle.

**The Principle of Representatives:** Representatives do not share the relationships of the things they represent.

### Detecting LSP Violations

1. **Degenerate methods** — derived class methods that do nothing
2. **Unconditional exceptions** — derived methods throw exceptions the base doesn't
3. **If-instanceof / type checks** — checking type before acting means substitutability is broken
4. **Refused bequests** — derived class inherits methods it can't meaningfully support

### The Modem Case Study

File Movers use the Modem interface (`dial`, `hangup`, `send`, `receive`). Dead Users only need `send` and `receive`.

**Bad:** DedicatedModem extends Modem with degenerate `dial`/`hangup` that do nothing. Creates refused bequest, subtle bugs, forces Dead Users to call methods that make no sense.

**Good:** Use Adapter pattern. `DedicatedModemAdapter` extends Modem, delegates `send`/`receive` to `DedicatedModem`. The adapter contains the fix; `DedicatedModem` stays clean. Dependencies point away from the hack.

### Design by Contract

- Preconditions cannot be strengthened in a subtype
- Postconditions cannot be weakened in a subtype
- Invariants of the supertype must be preserved

### Generics and LSP

If S is a subtype of T, `List<S>` is NOT automatically a subtype of `List<T>`:

```
g():
    circles: List<Circle> = new List()
    f(circles)  // ERROR — not safe!

f(shapes: List<Shape>):
    shapes.add(new Square())  // Would put Square in a Circle list!
```

A `List<Circle>` cannot substitute for `List<Shape>` because the consumer could insert a non-Circle. This is why many languages distinguish covariant from invariant generics.

### Every LSP Violation is a Latent OCP Violation

When you violate LSP, you'll eventually need if-instanceof checks, which hang dependencies on subtypes, which violates OCP.

---

## ISP: Interface Segregation Principle

**Don't depend on things you don't need.**

Clients should not be forced to depend on methods they don't use. When they do, changes to methods they don't call can still force them to recompile, redeploy, or break.

```
// Bad — LoginHandler depends on withdrawal methods it never calls
interface Messenger:
    askForCard()
    askForPin()
    showBalance()
    askForAmount()
    confirmWithdrawal()

// Good — each client gets only what it needs
interface LoginMessenger:
    askForCard()
    askForPin()

interface WithdrawMessenger:
    askForAmount()
    confirmWithdrawal()

class Messenger implements LoginMessenger, WithdrawMessenger:
    // implements all methods
```

### Interface Naming

Interfaces belong to their USERS, not their implementers. Name them after what users do with them, not after what implements them.

Bad: `AbstractLight` (named after implementer)
Good: `Switchable` (named after user's perspective)

### ISP Beyond Compile-Time

Even without static type systems, ISP applies:
- Have you had to create objects and pass constructor arguments you don't use?
- Have you had to fire up a web server just to test a business rule?
- Have you had to load a library for some unused feature?

All ISP violations.

### The Photocopier Origin Story

ISP was born from a 1990s C++ copier application. A single `Job` class was used by every subsystem — stapler, imager, inverter — each calling different methods. ANY change to `Job` forced an hour-long rebuild of the entire system. The fix: create separate interfaces for each subsystem's needs. `Job` multiply inherits from all interfaces. Changes now only affect subsystems that use the changed methods. Build times shrank dramatically.

### Detecting ISP Violations

- Fat interfaces with many methods serving different clients
- Changes to one client's methods force recompilation of unrelated clients
- Clients importing/depending on code they never call

---

## DIP: Dependency Inversion Principle

**High-level policy should not depend on low-level detail. Both should depend on abstractions.**

This is the principle at the core of object-oriented design and the mechanism that makes Clean Architecture possible.

### Two Kinds of Dependencies

**Runtime dependencies:** Flow of control — when one module calls another.
**Source code dependencies:** When a name defined in one module appears in another.

Key insight: these do NOT have to be aligned. You can invert source code dependencies so they oppose the flow of control.

```
Before:  A ---(calls)---> B
         A ---(depends)---> B

After:   A ---(calls)---> [Interface] <---(implements)--- B
         A ---(depends)---> [Interface] <---(depends)--- B
```

### The Thermostat Example

```
// Bad — high-level algorithm locked to low-level I/O hardware
regulate():
    while true:
        current = readFromAddress(0x01)   // hard-coded I/O port
        desired = readFromAddress(0x02)
        if current > desired:
            writeToAddress(0x04, true)    // cooler
        else if current < desired:
            writeToAddress(0x03, true)    // heater
        sleep(60000)

// Good — high-level algorithm is independent of hardware
interface HVAC:
    getCurrentTemperature()
    getDesiredTemperature()
    setHeater(on)
    setCooler(on)

regulate(hvac: HVAC):
    while true:
        current = hvac.getCurrentTemperature()
        desired = hvac.getDesiredTemperature()
        if current > desired:
            hvac.setCooler(true)
        else if current < desired:
            hvac.setHeater(true)
        sleep(60000)
```

The control algorithm is now testable, reusable, and independent of any specific hardware.

### Plug-in Architecture

The goal of DIP: make everything a plug-in to the application. The application is the socket; UI, database, frameworks, and devices are plugs. All plug-in dependencies point toward the thing being plugged into.

```
// Bad — high-level depends on low-level
class OrderService:
    db = new MySQLDatabase()  // hard-coded dependency

// Good — both depend on abstraction
interface OrderRepository: ...

class OrderService:
    repo: OrderRepository     // depends on abstraction

class MySQLOrderRepository implements OrderRepository: ...
```

### What Should Be Plug-ins?

- **Main:** Always a plug-in to the application
- **UI:** Plug-in to use cases
- **Database:** Plug-in to the application
- **Frameworks:** Plug-ins, not the center of architecture

### The 1978 ROM Chip Story

32 ROM chips containing embedded software. Any change required shipping all 32 chips worldwide. Solution: reserve first 32 bytes of each ROM for vectors to subroutines. On boot, copy vectors to RAM. All calls go through RAM vectors. Now you can ship just the changed chip. This was dependency inversion before OO languages existed — the source code dependencies were made to oppose the flow of control.

### Structured Design vs. OO Design

**Structured Design:** Top-down decomposition. Source code dependencies mirror runtime dependencies. High-level calls low-level, high-level depends on low-level. Changes ripple downward.

**OO Design:** Source code dependencies can oppose runtime dependencies. High-level calls low-level at runtime, but low-level depends on high-level at compile time (through interfaces). This is the essential difference that makes OO useful.

### The Reusable Framework Lesson (1992)

18 C++ applications needed a shared framework. First attempt: built a 70,000-line framework alongside one application. Failed — the framework was tuned to that application and couldn't be reused. Second attempt: rebuilt the framework in parallel with three applications. Nothing got in unless reused by all three. Subsequent applications took 4 man-months each. The framework had no dependencies on any application — pure dependency inversion.

### Detecting DIP Violations

- High-level policy modules importing low-level detail modules
- Source code dependencies mirroring runtime dependencies (no inversion)
- No interfaces separating policy from detail
- Concrete class names appearing in high-level modules

---

## Case Study: The Payroll System

A comprehensive example applying all five principles together.

**Actors:** Operations (runs the system, adds employees), Policy (sets pay rules), Union (handles dues, service charges, membership).

**SRP applied:** Requirements broken into use cases, partitioned by actor. `AddEmployee` is abstract; `AddHourlyEmployee`, `AddCommissionedEmployee`, `AddSalariedEmployee` are specifics. `SetUnionMembership` extracted to separate union concerns from policy.

**The AddTimeCard Dilemma (OCP + LSP):** How does `AddTimeCard` add a time card to `HourlyEmployee`? Putting `addTimeCard` in `Employee` violates OCP (Employee knows about TimeCard). Putting it in `PayType` interface violates LSP (not all pay types have time cards). Solution: get `PayType`, downcast to `HourlyPayType`, call `addTimeCard`. When a cast tells the truth, it's a fine cast.

**The Null Object Pattern (LSP):** `UnionMembership` interface with `Member` and `NonMember` derivatives. `NonMember` does nothing in every method. This is NOT an LSP violation — when ALL methods do nothing, it's a valid Null Object, not a refused bequest.

**ISP trade-off:** `RequestBuilder` and `UseCaseFactory` have methods for all requests. Each controller depends on methods it doesn't call. Solutions: (1) dynamic interface with single `make(name)` method (loses type safety), or (2) segregated interfaces per controller (many interfaces). The choice depends on trust in unit tests vs. need for static typing.

**The Beautiful Payroll Algorithm (DIP):**

```
for employee in employees:
    if employee.isPayDay(today):
        pay = employee.calculatePay()
        deductions = employee.calculateDeductions()
        employee.sendPay(pay.minus(deductions))
```

This algorithm is completely true and completely independent of all the low-level details that complicate the payroll application. That independence is the result of dependency inversion.

---

## When Reviewing Code

### Process

1. Identify classes and their actors (who requests changes?)
2. Check each principle systematically:
   - **SRP:** More than one actor per class?
   - **OCP:** Adding new behavior requires modifying existing code?
   - **LSP:** Degenerate methods, instanceof checks, refused bequests?
   - **ISP:** Clients depending on methods they don't call?
   - **DIP:** High-level depending on low-level concretions?
3. Assess impact: rigidity, fragility, immobility, development friction
4. Suggest specific refactorings with before/after

### Severity Levels

| Severity | Type | Example |
|----------|------|---------|
| Critical | DIP violation — business rules depend on framework/database | Entity class imports ORM annotations |
| High | SRP violation — multiple actors in one class | Employee has pay, save, and report in one class |
| Medium | OCP violation — switch on type codes, LSP — instanceof checks | Adding a type requires editing 5 files |
| Low | ISP — slightly fat interface, minor coupling | Interface has 2 extra methods one client doesn't need |

### Output Format

```
**Principle:** [S/O/L/I/D]
**Location:** file:line
**Class/Module:** `ClassName`
**Violation:** [what's wrong]
**Impact:** [rigidity/fragility/immobility]
**Refactoring:** [specific fix with reasoning]
```

---

## When Writing Classes

Run this checklist before committing:

1. **SRP** — Does this class serve only ONE actor? Can I describe its purpose without "and"?
2. **OCP** — Can new behavior be added without modifying this class?
3. **LSP** — If this class has subtypes, are they fully substitutable? No degenerate methods?
4. **ISP** — Do clients depend only on methods they actually call?
5. **DIP** — Does this class depend on abstractions, not concretions?

---

## Related Skills

- `/naming` — class and interface names must reveal intent
- `/functions` — methods within classes follow function principles
- `/architecture` — SOLID at the architectural level (boundaries, layers, plug-ins)
- `/components` — SOLID for components (REP, CCP, CRP are SRP/ISP for components)
- `/clean-code-review` — comprehensive review including SOLID checks
