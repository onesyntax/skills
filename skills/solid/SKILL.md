---
name: solid
description: >-
  Guide applying SOLID principles to class and module design. Activates when
  designing new classes, reviewing class responsibilities, working with
  interfaces or abstractions, or when the user mentions SOLID, single responsibility,
  open-closed, dependency inversion, interface segregation, or Liskov substitution.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# SOLID Workflow

Apply Uncle Bob's SOLID principles to analyze code architecture, identify violations, and suggest refactoring improvements. Follow these workflow steps when designing classes or reviewing module boundaries.

## Workflow Steps

1. **Identify Actors and Responsibilities** - Determine who the module serves
2. **Single Responsibility (SRP)** - One reason to change per module
3. **Open-Closed (OCP)** - Open for extension, closed for modification
4. **Liskov Substitution (LSP)** - Subtypes must be substitutable
5. **Interface Segregation (ISP)** - Don't depend on unused methods
6. **Dependency Inversion (DIP)** - Depend on abstractions
7. **Apply /professional workflow** - Follow professional quality standards

---

## Overview of SOLID

The SOLID principles are five dependency management principles that control relationships and operations between classes in object-oriented design. They form a regime of dependency management describing how to use OO to build applications with high cohesion and low coupling.

### The Essence of Object-Oriented Design

Object-oriented design is fundamentally about **dependency management**. The essential quality of OO is the ability to **invert key dependencies**, protecting high-level policies from low-level details.

> "The essential quality of OO, the thing that makes it different from other paradigms, and the thing that makes it useful, is the ability to invert key dependencies, protecting high-level policies from low-level details."

### Why Dependencies Matter

- **Rigidity**: When small changes force large rebuilds due to coupled modules
- **Fragility**: When changes to one module cause unrelated modules to misbehave
- **Immobility**: When internal components cannot be easily extracted and reused
- **Viscosity**: When necessary operations like building and testing are difficult to perform
- **Needless Complexity**: When anticipatory design adds weight without current benefit

### The Copy Program Parable

The foundational example: A program that copies from keyboard to printer. When requirements change (add paper tape reader, paper tape punch), the naive approach adds booleans and conditionals, causing the module to rot.

The solution: Use abstraction (`getchar`/`putchar`) pointing to a `File` abstraction. New devices implement this abstraction. The dependencies are **inverted** - they oppose the flow of control.

> "When the dependencies oppose the flow of control, the system doesn't rot."

---

## Step 1: Identify Actors and Responsibilities

Before applying any principle, identify:

- **Who are the actors** served by this module?
- **What families of functions** serve each actor?
- **Are multiple actors** served by the same module?

### Actors vs. Users

- **Users** are individual people who may wear multiple hats
- **Actors** are roles that users play (e.g., Policy, Architecture, Operations)
- Responsibilities are tied to actors, not individuals
- When the needs of an actor change, the family of functions serving that actor must change
- The actor for a responsibility is the single source of change for that responsibility

---

## Step 2: Single Responsibility Principle (SRP)

### Definition

**A module should have one, and only one, reason to change.**

Another way to say this: Gather together the things that change for the same reasons, and separate the things that change for different reasons.

### Understanding "Responsibility"

A responsibility is NOT just "what a class does." A responsibility is tied to an **actor** - a group of users who will request changes to the software.

> "The responsibilities that the single responsibility principle is talking about are the responsibilities that your software has to all the different groups of people that it serves."

### The Employee Class Example

```java
class Employee {
    void calculatePay()      // Policy actor (accountants, managers)
    void save()              // Architecture actor (DBAs, architects)
    void describeEmployee()  // Operations actor (report consumers)
}
```

This class has THREE responsibilities because it serves THREE actors. Problems include:
- Bob (business rules) and Bill (database) must change the same module
- Merge conflicts and interference
- Huge fan-out of dependencies
- Accidental coupling between responsibilities

### The Two Values of Software

**Primary Value**: The ability to change (software is "soft")
- Sustainable profitability is tied to flexibility
- If software is easy to change, it's good for business
- Your PRIMARY job is to give software structure that makes it easy to change

**Secondary Value**: Current behavior that meets user needs
- High secondary value but low primary value leads to decreasing profitability
- Systems that work but are hard to change become unprofitable

> "Perhaps you thought your job was to get the software to work, and of course it is. But that's just your secondary job. Your primary job is to give the software a shape and structure that makes it easy to change."

### Detecting SRP Violations

1. **Multiple actors affected by one module**: Policy, Architecture, and Operations all depend on the same Employee class
2. **Accidental coupling**: Resources shared between responsibilities that change at different times
3. **Mixed concerns in one function**: Business rules mixed with UI formatting, SQL with HTML
4. **Changes for one purpose affect another**: Changing a report breaks business rules

### Examples of SRP Violations

**Violation: Mixed directions and messages**
```java
void move() {
    List<String> directions = getAvailableDirections();
    String message = "You can go: " + String.join(", ", directions);
    display(message);
}
```
Two responsibilities: determining available directions AND formatting messages for display.

**Violation: Mechanics mixed with policy**
```java
void shootArrow() {
    followArrowPath();
    if (hitTarget) {
        terminateGame();  // Policy mixed with mechanics!
    }
}
```

**Violation: Logging intertwined with business logic**
```java
void execute() {
    if (verbose) log("Starting execution");
    doSomething();
    if (verbose) log("Step completed");
    doSomethingElse();
    if (verbose) log("Execution finished");
}
```

### Refactoring Techniques for SRP

**1. Extract Interface and Implementation**
```java
interface Employee { ... }
class EmployeeImpl implements Employee { ... }
```
Decouples actors from implementation but not from each other.

**2. Split into Separate Classes**
```java
class Employee { /* data and policy */ }
class EmployeeGateway { /* database operations */ }
class EmployeeReporter { /* reporting functions */ }
```
Strong separation but introduces hunting problem.

**3. Facade Pattern**
```java
class EmployeeFacade {
    private Employee employee;
    private EmployeeGateway gateway;
    private EmployeeReporter reporter;
    // Delegates to appropriate implementation
}
```
Easy to find functions but actors remain coupled.

**4. Interface Segregation**
```java
interface PayCalculator { void calculatePay(); }
interface EmployeePersistence { void save(); }
interface EmployeeDescriber { void describe(); }
class EmployeeImpl implements PayCalculator, EmployeePersistence, EmployeeDescriber { ... }
```
Actors fully decoupled but implementations still coupled.

**5. Extract and Compose (for logging)**
```java
class Executive {
    void execute() { ... }
}
class LoggingExecutive extends Executive {
    void execute() {
        log("Starting");
        super.execute();
        log("Finished");
    }
}
```

### The Mastermind Case Study

Three actors identified:
- **Game Designer**: responsible for messages, formatting, language
- **Strategist**: responsible for the guessing algorithm
- **Customer**: responsible for game flow, rules, variations

Architecture solution:
- `gameplay` package serves Customer (center of architecture)
- `game_interface` package serves Game Designer
- `strategy` package serves Strategist
- All dependencies point toward the gameplay package

### SRP Wisdom

> "We do not mix SQL and HTML in the same module. We do not put business rules into JSPs. We do not implement business rules in stored procedures."

> "When modules contain more than one responsibility, the system tends to become fragile due to unintended interactions between those responsibilities."

> "Unit tests, as it turns out, tend to align with actors. The kinds of things that actors keep separate are the very things that unit tests tend to keep separate."

---

## Step 3: Open-Closed Principle (OCP)

### Definition

**A software module should be open for extension, but closed for modification.**

Coined by Bertrand Meyer in "Object Oriented Software Construction" (1988).

> "This principle is at the moral center of software architecture."

### What "Open" and "Closed" Mean

- **Open for Extension**: It should be simple to change the behavior of the module
- **Closed for Modification**: The source code shouldn't change

The apparent paradox: How can you change behavior without modifying source code?

### The Answer: Abstraction and Inversion

Insert an abstract interface between the high-level policy and the low-level details. Invert the dependencies so they oppose the flow of control.

```java
// Before (violates OCP)
void checkout() {
    for (Item item : items) {
        receipt.add(item.getPrice());
    }
    double payment = getCashPayment();  // Hard-coded to cash!
    receipt.addPayment(payment);
}

// After (conforms to OCP)
interface PaymentMethod {
    double getPayment();
}

void checkout(PaymentMethod method) {
    for (Item item : items) {
        receipt.add(item.getPrice());
    }
    double payment = method.getPayment();
    receipt.addPayment(payment);
}
```

Now new payment methods (credit card, crypto, etc.) can be added without modifying the checkout algorithm.

### The Promise and the Lie

The promise: If you design systems conforming to OCP, you can add new features by adding new code, not changing old code. Old code doesn't rot.

**The Lie**: This only works if you can predict the future. You must know what kinds of changes will be requested to create the right abstractions.

> "The open-closed principle only protects you from change if you can predict the future."

### The Crystal Ball Problem

Perfect conformance to OCP requires perfect foresight. Customers have an uncanny ability to change the one thing you forgot to protect yourself from.

### Two Approaches to the Crystal Ball Problem

**Big Design Up Front (BDUF)**:
- Think really hard about every possible change
- Create abstractions for everything
- Results in large, top-heavy, complex designs
- Abstractions that aren't needed are expensive to maintain

**Agile Design**:
- Do the simplest thing possible
- Get it in front of customers quickly
- When customers make changes, add abstractions to protect from that kind of change in the future
- Refactor based on actual change requests

> "One of the best predictors of change is past change."

### The Expense Report Case Study

**Bad Design (violates OCP)**:
```java
void printExpense(Expense e) {
    String name;
    switch(e.type) {
        case DINNER: name = "Dinner"; break;
        case BREAKFAST: name = "Breakfast"; break;
        case CAR_RENTAL: name = "Car Rental"; break;
    }
    // More switch statements for overage checking, etc.
}
```

Problems:
- Adding lunch requires changing the enum (affects all dependent modules)
- Must hunt for all switch statements throughout the system
- Leads to rigidity, fragility, and immobility

**Good Design (conforms to OCP)**:
```java
abstract class Expense {
    abstract String getName();
    abstract boolean isMeal();
    abstract boolean isOverage();
}

class DinnerExpense extends Expense {
    String getName() { return "Dinner"; }
    boolean isMeal() { return true; }
    boolean isOverage() { return amount > 5000; }
}
```

Adding lunch: Just create `LunchExpense` class. No existing code changes.

### Design Smells from OCP Violations

- **Rigidity**: Small design change has huge impact (changing enum forces recompile of everything)
- **Fragility**: Adding lunch breaks taxation calculations
- **Immobility**: Cannot deploy features as separate plugins

### The Practical Process

1. Spend 1-2 weeks on initial requirements and simple architecture (Iteration Zero)
2. Work in 1-2 week iterations, getting executable software in front of users
3. When users request changes, refactor to add abstractions protecting from that kind of change
4. Each iteration should see growing conformance to OCP

### The Main Problem

Main cannot conform to OCP because it's responsible for loading resources, strategies, factories. Changes to those require changes to main.

Solution: Separate main from the application by a boundary. All dependencies cross pointing away from main.

### OCP Wisdom

> "To the extent that a system is not open for extension and closed for modification, that system is immoral."

> "The open-closed principle is the moral center of system architecture."

> "When you modify them, you can do so by adding new code, not by changing any old code. That's quite a thought. If the old code doesn't ever have to get modified, then it can't rot."

---

## Step 4: Liskov Substitution Principle (LSP)

### Definition

**If S is a subtype of T, then objects of type S may be substituted for objects of type T without altering any of the desirable properties of that program.**

From Barbara Liskov's 1988 ACM paper, named "Liskov Substitution Principle" by James Coplien.

> "Subtypes can be used as their parent types. If you have users U that use type T, and S is a subtype of T, then U should be able to use S without knowing it."

### Understanding Types

A type is a "bag of operations." From the outside, a type is nothing but a bunch of methods. The data within is hidden behind those operations.

```c
// This is NOT a type - just a data structure
struct Point { int x; int y; };

// This IS a type - operations define it
Point* createPoint(int x, int y);
double distance(Point* p1, Point* p2);
void translate(Point* p, int dx, int dy);
void rotate(Point* p, double angle);
```

### Subtypes and Substitutability

A subtype has the same methods as its parent type (possibly with different implementations). The subtype must be substitutable for its parent - it can do MORE but never LESS.

In static languages: Achieved through inheritance
In dynamic languages: Achieved through duck typing

> "When I see a bird that walks like a duck and quacks like a duck and swims like a duck, I call that bird a duck."

### The Square/Rectangle Problem

The definitive case for LSP.

```java
class Rectangle {
    int height, width;
    void setHeight(int h) { height = h; }
    void setWidth(int w) { width = w; }
    int area() { return height * width; }
}

class Square extends Rectangle {
    void setHeight(int h) { height = h; width = h; }
    void setWidth(int w) { height = w; width = w; }
}
```

**The Problem**: A user of Rectangle expects that setting width doesn't change height. But with Square, it does!

```java
void testRectangle(Rectangle r) {
    r.setWidth(5);
    r.setHeight(4);
    assert(r.area() == 20);  // FAILS for Square!
}
```

**Why It Fails**: The Square violates the expectations of Rectangle users. This is a **refused bequest**.

### The Principle of Representatives

**Representatives do not share the relationships of the things they represent.**

- Two divorcing people have lawyers representing them
- The lawyers are not divorcing each other
- Similarly, a Square IS-A Rectangle geometrically
- But the code representing Square is NOT a subtype of the code representing Rectangle

> "While geometrically a square is a rectangle, the software representatives of those concepts don't share the subtype relationship."

### Solutions to Square/Rectangle

1. **Immutability**: Remove setters (much of the problem goes away)
2. **Separate types**: Treat Square and Rectangle as unrelated types
3. **Inverted inheritance**: Rectangle extends Square (solves memory but creates new LSP violation)

### The Integers/Reals/Complex Problem

- Integer IS-A Real number
- Real IS-A Complex number
- Complex contains two Reals (real and imaginary parts)

In UML this looks fine. In code, it creates recursive definitions like Russell's paradox!

### Generics and LSP

If S is a subtype of T, `List<S>` is NOT automatically a subtype of `List<T>`.

```java
void g() {
    List<Circle> circles = new ArrayList<>();
    f(circles);  // ERROR in Java!
}

void f(List<Shape> shapes) {
    shapes.add(new Square());  // Would put Square in Circle list!
}
```

### Detecting LSP Violations

**1. Degenerate Functions**
Methods that do nothing in derived classes (especially if they did something in base):
```java
class DedicatedModem extends Modem {
    void dial(String number) { /* does nothing */ }
    void hangup() { /* does nothing */ }
}
```

**2. Unconditional Exceptions**
Derived methods that throw exceptions the base doesn't:
```java
class ReadOnlyList extends List {
    void add(Object o) { throw new UnsupportedOperationException(); }
}
```

**3. If-InstanceOf / Type Cases**
When you have to check the type, you're working around a substitutability problem:
```java
if (rectangle instanceof Square) {
    // Special handling - LSP violation indicator!
}
```

**4. Type cases** (chains of if-instanceof) should be replaced with polymorphic dispatch.

### When InstanceOf Is Acceptable

When you ALREADY KNOW the type and the compiler has forgotten it:
```java
Employee emp = employeeGateway.find(hourlyEmployeeId);
if (emp instanceof HourlyEmployee) {  // Asserting what we know
    HourlyEmployee hourly = (HourlyEmployee) emp;
    hourly.addTimeCard(timeCard);
}
```

### The Modem Case Study

File Movers use Modem interface (dial, hangup, send, receive).
Dead Users use DedicatedModem interface (send, receive only).

Bad solution: DedicatedModem extends Modem with degenerate dial/hangup.
- Creates refused bequest
- Subtle bugs (race conditions)
- Forces Dead Users to call dial/hangup (makes no sense)
- 2 AM prank phone calls from angry programmers

Good solution: Use Adapter pattern
- Create DedicatedModemAdapter that extends Modem
- Adapter delegates send/receive to DedicatedModem
- Adapter contains fix for race condition
- DedicatedModem unchanged
- Dependencies point away from the hack

### Every LSP Violation is a Latent OCP Violation

When you violate LSP, you'll eventually need if-instanceof statements, which hang dependencies on subtypes, violating OCP.

> "Every refused bequest, every violation of the Liskov substitution principle, is a latent violation of the open-closed principle."

### Inheritance and Rigidity

In static languages, inheritance is the strongest relationship between types. When you inherit, you drag along all the baggage. The relationship that gives flexibility also creates rigidity.

Dynamic languages (Ruby, Python) don't rely on inheritance for subtyping, avoiding this trap.

### LSP Wisdom

> "A subtype can do more than its parent type, but it can never do less."

> "Undefined behavior means it's going to work perfectly on your laptop and in your development environment. But as soon as you ship it to the customer, it's going to crash horribly and delete all the master files."

> "The representatives of things do not share the relationships of the things they represent."

---

## Step 5: Interface Segregation Principle (ISP)

### Definition

**Don't depend on things you don't need.**

More specifically: Clients should not be forced to depend on methods they do not use.

> "Loose lips sink ships, and leaky abstractions create distractions."

### The Origin Story: The Photocopier

A 1990s C++ copier application with a `Job` class. Every subsystem (stapler, imager, inverter) depended on Job for different reasons, calling different methods.

Problem: ANY change to Job forced an hour-long rebuild of the entire system.

Solution: Create separate interfaces for each subsystem's needs. Job multiply inherits from all interfaces. Changes only affect subsystems that use the changed methods.

> "The build time shrank considerably. We stopped worrying about hour-long builds and started changing the job class whenever we felt like it."

### Fat Classes

Classes with lots of methods serving many different clients. Even if you can't split the class (data must be managed in one place), you can split the INTERFACE.

### The ATM Example

```java
interface Messenger {
    void askForCard();
    void askForPin();
    void showBalance();
    void askForAmount();
    void confirmWithdrawal();
    void requestApprovalOfFee();  // NEW for withdrawal
    // ... many more methods
}
```

**The Strange Backwards Dependency**:
- LoginInteractor depends on askForCard, askForPin
- WithdrawInteractor depends on askForAmount, confirmWithdrawal
- But BOTH depend on Messenger interface
- When withdrawal adds requestApprovalOfFee, LoginInteractor must recompile!

**The Problem**: Each interactor depends on methods it doesn't call. They know too much.

### The Solution: Segregate Interfaces

```java
interface LoginMessenger {
    void askForCard();
    void askForPin();
}

interface WithdrawMessenger {
    void askForAmount();
    void confirmWithdrawal();
    void requestApprovalOfFee();
}

interface DepositMessenger { ... }

// Implementation multiplies inherits all interfaces
class Messenger implements LoginMessenger, WithdrawMessenger, DepositMessenger {
    // Implements all methods
}
```

Now:
- LoginInteractor depends only on LoginMessenger
- Changes to WithdrawMessenger don't affect LoginInteractor
- No strange backwards coupling

### Why Interfaces Exist (The Sad Truth)

Interfaces in Java/C# exist because language designers were "too lazy to figure out a reasonable solution for multiple inheritance." They punted on the Deadly Diamond of Death.

In C++, you can multiply inherit classes. In Java/C#, you can only multiply inherit interfaces.

### Interface Naming

Interfaces belong to their USERS, not their implementers.

Bad: `AbstractLight` (named after implementer)
Good: `Switchable` (named after what users do with it)

> "Interfaces have more to do with the classes that use them than with the classes that implement them."

### Physical Structure Considerations

If all interactors use the same Messenger instance, how do you avoid leaking that knowledge?

Options:
1. **Main creates everything**: Main creates Messenger, creates all interactors with appropriate interface types, passes across boundary
2. **Builder pattern**: Application creates interactors, passes to Main via Builder interface, Main sets the messenger interfaces
3. **Factory with getters** (problematic): Factory becomes dependency magnet, recreates the problem
4. **Static variable with cast** (problematic): Cast implies object implements more than needed
5. **Dependency injection** (be careful): Don't let DI annotations litter application code; keep DI knowledge in Main

### Beyond Compile-Time Dependencies

ISP applies even in dynamic languages where the strange coupling doesn't exist:

- Have you had to create objects and pass constructor arguments you don't use?
- Have you had to fire up a web server just to test a business rule?
- Have you had to load a library to satisfy some unused feature?
- Have you had to walk through login to test a business rule?

All ISP violations!

### ISP Wisdom

> "The interface segregation principle is all about the need to know. Loose lips sink ships, and leaky abstractions create distractions."

> "Don't force your users to depend on things they don't need. Whether those users are modules, people, or tests."

> "Keep your abstractions private. Dispense knowledge only to those with a need to know."

> "It is the ultimate arrogance of library designers that they force you to use strong physical couplings like inheritance."

---

## Step 6: Dependency Inversion Principle (DIP)

### Definition

**High-level policy should not depend on low-level detail. Low-level detail should depend on high-level policy.**

In other words: Depend on abstractions, not concretions.

> "This is the principle that is at the core of object-oriented design."

### Two Kinds of Dependencies

**Runtime Dependencies**: When flow of control leaves one module and enters another, or when one module accesses variables in another.

**Compile-time/Source Code Dependencies**: When a name is defined in one module but appears in another module.

Key insight: These DO NOT have to be aligned!

### The 1978 ROM Chip Story

32 ROM chips containing embedded software. Any change required shipping all 32 chips worldwide.

Solution:
- Reserve first 32 bytes of each ROM for vectors to subroutines
- On boot, copy vectors to RAM
- All calls go through RAM vectors
- Now you can ship just the changed chip

> "We inverted the direction of the source code dependencies. We got the source code dependencies to oppose the flow of control."

This was essentially object-oriented design before OO languages existed.

### How to Invert Dependencies

Insert an interface between caller and callee. The caller uses the interface, the callee implements it.

```
Before:  A ---(calls)---> B
         A ---(depends)---> B

After:   A ---(calls)---> [Interface] <---(implements)--- B
         A ---(depends)---> [Interface] <---(depends)--- B
```

The source code dependency of B on the interface **opposes** the runtime dependency of A on B.

### Plug-in Architecture

Inverting dependencies is how you create **boundaries** and **plug-ins**.

- A plug-in is a module anonymously called by another module
- The caller has no idea who or what it's calling
- All plug-in dependencies point toward the thing being plugged into
- The application is the socket; devices/UI/database are plugs

> "A good application architecture is a plug-in architecture. And a plug-in architecture is achieved through careful and judicious use of the dependency inversion principle."

### Device Independence in Operating Systems

OS provides device independence through DIP:
- Every I/O driver implements the I/O driver interface (open, close, read, write, seek)
- Drivers load function pointers into vector tables
- getchar/putchar call through these vectors
- OS has no source code dependencies on any specific driver

> "I.O. drivers are just plug-ins to the operating system."

### The Thermostat Example

**Bad (violates DIP)**:
```java
void regulate() {
    while (true) {
        int current = in(0x01);   // Hard-coded I/O address!
        int desired = in(0x02);   // Hard-coded I/O address!
        if (current > desired)
            out(0x04, true);      // Hard-coded!
        else if (current < desired)
            out(0x03, true);      // Hard-coded!
        sleep(60000);
    }
}
```

**Good (conforms to DIP)**:
```java
interface HVAC {
    int getCurrentTemperature();
    int getDesiredTemperature();
    void setHeater(boolean on);
    void setCooler(boolean on);
}

void regulate(HVAC hvac) {
    while (true) {
        int current = hvac.getCurrentTemperature();
        int desired = hvac.getDesiredTemperature();
        if (current > desired)
            hvac.setCooler(true);
        else if (current < desired)
            hvac.setHeater(true);
        sleep(60000);
    }
}
```

The high-level control algorithm is now independent of the low-level I/O details.

### The Reusable Framework Story (1992)

18 C++ applications for architects. Built 70,000 line "reusable" framework alongside first 10,000 line application.

**Failed**: Framework was tuned to first application, couldn't be reused by next three.

**Succeeded**: Rebuilt framework in parallel with three applications. Nothing got in unless reused by all three. Next applications done in 4 man-months each.

Key insight: The framework (high-level policy) had no dependencies on applications (low-level details). This was dependency inversion.

### What Should Be Plug-ins?

- **Main**: Always a plug-in to the application
- **UI**: Plug-in to use cases
- **Database**: Plug-in to the application
- **Frameworks**: Plug-ins, not the center of architecture

### Structured Design vs. OO Design

**Structured Design**: Top-down, source code dependencies mirror runtime dependencies. High-level calls low-level, high-level depends on low-level.

**OO Design**: Source code dependencies can oppose runtime dependencies. High-level calls low-level, but low-level depends on high-level (through interfaces).

### DIP Wisdom

> "Inverting dependencies is the means by which we create boundaries between software modules."

> "The way you create an independently deployable and independently developable application architecture is to compose it out of plug-ins."

> "If you don't build it in parallel with more than one application that reuses it, you will almost certainly fail."

---

## Case Study Lessons (Payroll System)

### Identifying Actors First

For the payroll system:
- **Operations**: Runs the system, adds employees, time cards, etc.
- **Policy**: Sets rules for how employees get paid
- **Union**: Handles union dues, service charges, membership

### Use Case Driven Architecture

Break requirements into use cases, then partition use cases by actor responsibility.

Example: Add Employee use case
- Abstract AddEmployee (shared data)
- AddHourlyEmployee, AddCommissionedEmployee, AddSalariedEmployee (specific data)
- SetUnionMembership (extracted to separate union concerns from policy concerns)

### Data Dictionary Building

Listen to customer, capture data implied by their words. Build data entities iteratively.

### Diagrams Are Communication Tools

> "I wouldn't really have been drawing all these formal diagrams. What I would have been doing instead is maybe scratching some diagrams on a whiteboard and then writing quite a bit of code."

Elaborate diagrams are useful for:
- Communicating thought process to others
- Teaching/training

NOT useful for:
- Historical records (they rot quickly)
- New team member onboarding (unless maintained)

### The AddTimeCard Dilemma

How does AddTimeCard use case add a time card to HourlyEmployee?

**Bad**: Put addTimeCard in Employee (violates OCP - Employee knows about TimeCard)
**Bad**: Put addTimeCard in PayType interface (violates LSP - not all pay types have time cards)
**Good**: Get PayType, downcast to HourlyPayType, call addTimeCard

> "When a cast tells the truth, that's a fine cast indeed."

### The Null Object Pattern

UnionMembership interface with Member and NonMember derivatives.
NonMember does nothing in every method - this is NOT an LSP violation when ALL methods do nothing (Null Object pattern).

### ISP in the Payroll System

RequestBuilder and UseCaseFactory have methods for all requests/use cases.
Each controller depends on methods it doesn't call.

Solutions:
1. **Dynamic interface**: Single `make(String name)` method (loses type safety)
2. **Segregated interfaces**: One interface per controller's needs (many interfaces)

Choice depends on trust in unit tests vs. need for static typing.

### The Beautiful Payroll Algorithm

```java
for (Employee e : employees) {
    if (e.isPayDay(today)) {
        Money pay = e.calculatePay();
        Money deductions = e.calculateDeductions();
        e.sendPay(pay.minus(deductions));
    }
}
```

> "This algorithm is true. It's the utter truth. And yet, it's completely independent of all the low-level details that complicate the payroll application."

### Don't Be a Slave to Principles

> "No design is fully SOLID compliant. No design should be fully SOLID compliant. In fact, full SOLID compliance is an oxymoron."

The principles illuminate design issues and recommend solutions. They don't prescribe behavior. Use them to make trade-offs and compromises.

---

## Review Process

When reviewing code for SOLID compliance:

### 1. Identify Classes and Their Responsibilities

- Who are the actors served by this module?
- What families of functions serve each actor?
- Are multiple actors served by the same module? (SRP violation)

### 2. Check Each SOLID Principle Systematically

**SRP Check**:
- Does this class have more than one reason to change?
- Are there multiple actors with interest in this class?
- Is business logic mixed with UI/database/formatting?

**OCP Check**:
- To add a new type/behavior, do you modify existing code or add new code?
- Are there switch statements on type codes?
- Are abstractions in place to allow extension without modification?

**LSP Check**:
- Do derived classes do less than their base classes?
- Are there degenerate methods (do nothing or throw exceptions)?
- Are there if-instanceof checks that add special handling?
- Would users of the base class be surprised by subclass behavior?

**ISP Check**:
- Do clients depend on methods they don't call?
- Are there fat interfaces that force unnecessary dependencies?
- Would changes to one client's methods force recompilation of unrelated clients?

**DIP Check**:
- Do high-level policy modules depend on low-level detail modules?
- Do source code dependencies mirror or oppose runtime dependencies?
- Are there interfaces separating policy from detail?
- Is main separated from the application by a boundary?

### 3. Note Violations with Specific Line Numbers

Document:
- File path and line number
- Which principle is violated
- The specific code construct causing the violation
- The actors or responsibilities involved

### 4. Explain Impact of Each Violation

- **Rigidity**: What will need to change when this module changes?
- **Fragility**: What might break when this module changes?
- **Immobility**: Can this be extracted and reused? Why not?
- **Development friction**: How does this affect team collaboration?

### 5. Suggest Refactoring with Code Examples

For each violation, provide:
- The principle being applied
- Before and after code snippets
- Explanation of why the refactoring improves the design
- Any trade-offs introduced by the refactoring

Remember: Perfect SOLID compliance is not the goal. The goal is a balanced design that minimizes pain and maximizes flexibility where it matters most.

---

## Code to Analyze

$ARGUMENTS

---

## Output Format

For each SOLID violation:
```
**Principle:** [S/O/L/I/D]
**Location:** file:line
**Class/Module:** `ClassName`
**Violation:** [Description of the violation]
**Impact:** [Why this is problematic]
**Refactoring:** [How to fix it]
```

---

## Self-Review (Back Pressure)

After designing or refactoring classes, ALWAYS perform this self-review before presenting code as done:

### Self-Review Steps
1. **SRP Check**: Does each class have only ONE reason to change? ONE actor?
2. **OCP Check**: Can I add new behavior without modifying existing code?
3. **LSP Check**: Are all subtypes substitutable for their base types?
4. **ISP Check**: Are clients forced to depend on methods they don't use?
5. **DIP Check**: Do high-level modules depend on abstractions (not concretions)?

### If Violations Found
- Fix the violations immediately
- Re-run self-review
- Only present as "done" when self-review passes

### Mandatory Quality Gate
Classes are NOT complete until:
- [ ] Each class serves ONE actor (SRP)
- [ ] New features can be added by adding code, not modifying it (OCP)
- [ ] No degenerate methods or instanceof checks (LSP)
- [ ] No fat interfaces (ISP)
- [ ] Dependencies point toward abstractions (DIP)

## Related Skills

- **/professional** - Apply professional coding standards and quality requirements
- **/functions** - Ensure methods within classes follow function principles
- **/naming** - Ensure class and method names reveal intent
- **/clean-code-review** - Run comprehensive review after refactoring
