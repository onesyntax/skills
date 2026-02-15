---
name: patterns
description: >-
  Guide identifying and applying design patterns appropriately. Activate when code
  could benefit from patterns, when discussing GOF patterns, or when the user mentions
  pattern names like Factory, Strategy, Observer, Command, State, Visitor, etc.
  Patterns are tools for solving specific problems — not ends in themselves.
allowed-tools: Read, Grep, Glob
argument-hint: [code or situation to analyze]
---

# Patterns Skill

Design patterns are named solutions to recurring design problems. The GOF book (Gamma, Helm, Johnson, Vlissides, 1995) gave developers a shared vocabulary — a book full of names. Patterns are not templates to blindly apply but tools to solve specific problems. They represent chunks of design experience that can be communicated efficiently.

For extended examples, implementation deep dives, read `references/extended-examples.md`.

**Critical Warning:** "When you have a nice shiny new hammer, everything looks like a nail." Patterns should emerge from need, not be applied preemptively. The goal is clean, simple code — patterns are tools to achieve that, not ends in themselves.

---

## Pattern Decision Framework

### When You See This Problem → Consider This Pattern

**Object Creation:**

| Problem | Pattern |
|---------|---------|
| Need to isolate concrete type creation | Factory (Abstract Factory or Factory Method) |
| Need copies of existing objects | Prototype |
| Need to construct complex objects step by step | Builder |
| Need exactly one instance | Singleton (cautiously) or Monostate |

**Structural:**

| Problem | Pattern |
|---------|---------|
| Incompatible interfaces need to work together | Adapter |
| M × N class combinations from two dimensions | Bridge |
| Tree structures with uniform treatment | Composite |
| Add behavior dynamically without subclassing | Decorator |
| Simplify complex subsystem | Facade |
| Share fine-grained objects efficiently | Flyweight |
| Control access or cross boundaries | Proxy |

**Behavioral:**

| Problem | Pattern |
|---------|---------|
| Decouple what-to-do from who/when | Command |
| Complex state transitions | State |
| Interchangeable algorithms | Strategy |
| Fixed algorithm, varying steps | Template Method |
| Notify multiple objects of changes | Observer |
| Add operations to hierarchies without modifying them | Visitor |
| Traverse without exposing internals | Iterator |
| Centralized coordination of peers | Mediator |
| Pass request through chain of handlers | Chain of Responsibility |
| Capture/restore object state | Memento |
| Eliminate null checks | Null Object |
| Simple DSL | Interpreter |

### Before Applying Any Pattern

1. Do I have a specific problem this pattern solves?
2. Will this simplify my code or complicate it?
3. Does the pattern fit naturally, or am I forcing it?
4. Can I explain why this pattern is appropriate here?

If you can't answer these confidently, don't use the pattern.

---

## Creational Patterns

### Factory Patterns

The core problem: **type-safe code creates source code dependencies on concrete types.** When you write `new ConcreteClass()`, you create a dependency that propagates.

**Abstract Factory** — creates families of related objects without specifying concrete classes:

```
interface EmployeeFactory:
    makeEmployee(type): Employee

class EmployeeFactoryImpl implements EmployeeFactory:
    makeEmployee(type):
        switch type:
            HOURLY: return new HourlyEmployee()
            SALARIED: return new SalariedEmployee()
```

The factory isolates creation from usage. Code that uses Employee depends only on the Employee interface. Main (or a boundary component) creates the factory and injects it.

**Factory Method** — uses inheritance; a subclass decides which class to instantiate. The parent class defines the algorithm, subclass provides the concrete object.

**The Type Wars:** Type-safe code uses enums/constants (compiler validates); configurable code uses strings (more flexible deployment). Resolution: use type-safe code internally, allow configuration at boundaries.

### Builder

Separates construction of a complex object from its representation. Works naturally with grammars — each grammar production triggers a builder method. A Facade that constructs something is essentially a Builder.

```
interface SyntaxBuilder:
    newState(name)
    newTransition(event, action, nextState)
    done()

class Parser:
    builder: SyntaxBuilder
    parse():
        // Calls builder methods as syntax elements are recognized
```

### Singleton and Monostate

**Singleton:** Ensure one instance with global access. Static initialization is thread-safe but eager. Lazy initialization has threading pitfalls (double-checked locking requires memory barriers).

**When to avoid Singleton:** Creates hidden global state, makes testing difficult, hides dependencies. Better alternative: dependency injection with explicit single-instance management.

**Monostate:** Achieve singleton behavior through static member variables while keeping the class instantiable. Clients don't know they're using a singleton. Unlike Singleton, supports inheritance and polymorphism.

### Prototype

Create new objects by copying existing ones. A registry maps names to prototype instances; `create(name)` clones the appropriate prototype.

---

## Structural Patterns

### Adapter

Convert an incompatible interface into one clients expect.

```
// You have this interface your system uses
interface Switchable:
    turnOn()
    turnOff()

// You have this class you cannot modify
class TableLamp:
    illuminate()
    darken()

// Bridge the gap
class TableLampAdapter implements Switchable:
    lamp: TableLamp
    turnOn(): lamp.illuminate()
    turnOff(): lamp.darken()
```

**Object Adapter** (composition) — more flexible, can adapt subclasses, preferred. **Class Adapter** (inheritance) — more rigid, slightly more efficient. Name the adapter for what clients expect, not for the adaptee.

### Bridge

Decouple abstraction from implementation so both vary independently. Solves the **M × N problem:** M types of abstractions × N types of implementations becomes M + N classes.

```
// Without Bridge: HourlyPrinterPaycheck, HourlEmailPaycheck,
//   SalariedPrinterPaycheck, SalariedEmailPaycheck... M×N!

// With Bridge: M + N
interface PayStation:                    // Implementation dimension
    output(data)

class PrinterStation implements PayStation: ...
class EmailStation implements PayStation: ...

abstract class Paycheck:                 // Abstraction dimension
    station: PayStation
    generate()

class HourlyPaycheck extends Paycheck:
    generate():
        data = calculateHourlyPay()
        station.output(data)             // Delegate to implementation
```

Naturally supports Tell Don't Ask style.

### Composite

Compose objects into tree structures. Clients treat leaves and branches uniformly.

```
abstract class SyntaxNode:
    accept(visitor)

class TerminalNode extends SyntaxNode:    // Leaf
    value: String

class SequenceNode extends SyntaxNode:    // Branch
    children: List<SyntaxNode>
    accept(visitor):
        visitor.visit(this)
        for child in children:
            child.accept(visitor)
```

### Decorator

Add responsibilities dynamically. Part of the Visitor family — adds behavior from outside the class.

```
interface Modem:
    dial(number), hangup(), send(data), receive()

class LoudDialModem implements Modem:
    modem: Modem
    dial(number):
        modem.setVolume(HIGH)
        modem.dial(number)
        modem.setVolume(LOW)
    // Delegate all other methods to wrapped modem
```

Decorators stack: `new RetryModem(new LoggingModem(new LoudDialModem(new RealModem())))`. Unlike inheritance, decoration is dynamic, per-instance, and composable without class explosion.

### Facade

Provide a unified interface to a set of interfaces in a subsystem. "Imposing policy from above" — sits above subsystem classes and provides a simplified interface.

### Mediator

Define an object that encapsulates how a set of objects interact. "Imposing policy from below" — sits among peers, coordinates between them. The Puppeteer metaphor: the puppets (colleagues) don't know about each other; the puppeteer (mediator) makes them appear to interact.

**Facade vs Mediator:** Facade calls down into subsystems. Mediator coordinates among peers.

### Flyweight

Share fine-grained objects efficiently by separating **intrinsic state** (shared, stored in flyweight) from **extrinsic state** (varies by context, stored outside). A factory manages the pool of shared instances.

### Proxy

Provide a surrogate that controls access to another object. Used when crossing boundaries — network, process, database. The proxy implements the same interface as the real object; clients don't know they're using a proxy.

**Virtual Proxy** creates the real object only when needed (lazy loading). Key insight: Proxy can hide the fact that you're crossing a database boundary — business logic stays clean.

---

## Behavioral Patterns

### Command

The simplest of all patterns — a single-method interface:

```
interface Command:
    execute()
```

Decouples "what needs to be done" from "who does it" and "when it happens." Encapsulates a request as an object.

**Key applications:** Button click handlers (GUI decoupled from business logic), undo/redo systems (UndoableCommand with `undo()` method, maintained in undo/redo stacks), thread decoupling and queuing (commands queued and executed by workers), the Actor Model (each actor has a command queue, processes sequentially).

**Temporal decoupling:** Commands separate the moment of decision from the moment of execution — enabling scheduling, batching, persistence, and audit logging.

### Strategy

Define a family of algorithms, encapsulate each, make them interchangeable. **External polymorphism** — the polymorphic behavior happens outside the class hierarchy.

```
interface SortStrategy:
    outOfOrder(i, j, array): boolean
    swap(i, j, array)

class BubbleSorter:
    strategy: SortStrategy
    sort(array):
        for i in 0..length-1:
            for j in 0..length-1-i:
                if strategy.outOfOrder(j, j+1, array):
                    strategy.swap(j, j+1, array)
```

Key insight: Strategy separates the **invariant** algorithm (bubble sort) from the **variant** details (comparison and swap).

### Template Method

Define the skeleton of an algorithm in a base class; subclasses override specific steps. **Internal polymorphism** — through inheritance.

```
abstract class BubbleSorter:
    abstract outOfOrder(i, j): boolean
    abstract swap(i, j)

    sort():
        for i in 0..length-1:
            for j in 0..length-1-i:
                if outOfOrder(j, j+1):
                    swap(j, j+1)
```

**Strategy vs. Template Method:** Strategy uses composition (switch at runtime), Template Method uses inheritance (fixed at compile time). If you write the same loop with minor variations, that's a Template Method candidate.

### State

Manage complex state transitions by representing each state as a class.

```
interface TurnstileState:
    coin(turnstile)
    pass(turnstile)

class LockedState implements TurnstileState:
    coin(turnstile):
        turnstile.unlock()
        turnstile.setState(new UnlockedState())
    pass(turnstile):
        turnstile.alarm()

class UnlockedState implements TurnstileState:
    coin(turnstile): turnstile.thankyou()
    pass(turnstile):
        turnstile.lock()
        turnstile.setState(new LockedState())
```

Three FSM implementation approaches: (1) nested switch/case (simple, becomes unwieldy), (2) table-driven (data-oriented), (3) State pattern (most OO, each state is a class).

### Observer

Define a one-to-many dependency so that when one object changes state, all dependents are notified automatically. Traces to MVC from Smalltalk (Model notifies Views without knowing about them).

**Pull Model:** Observer calls `subject.getData()` in its update method — observers decide what they need. **Push Model:** Subject sends data in the notification — subject decides what to send. Pull is more flexible; push can be more efficient.

**MVP (Model-View-Presenter):** Presenter mediates between Model and View, keeping both clean and testable. Warning: forgetting to deregister observers causes memory leaks.

### Visitor

Add operations to a hierarchy without modifying its classes.

```
interface Visitor:
    visit(terminalNode)
    visit(nonTerminalNode)

abstract class SyntaxNode:
    accept(visitor)

class TerminalNode extends SyntaxNode:
    accept(visitor): visitor.visit(this)
```

**The 90-degree rotation:** Without Visitor, easy to add types, hard to add operations. With Visitor, easy to add operations, hard to add types. This trade-off is fundamental.

**The Visitor Family:** Visitor (adds operations), Decorator (adds behavior), Extension Object (adds interfaces). All add capability from outside the class.

**Acyclic Visitor:** Breaks the dependency cycle by using separate visitor interfaces per node type with an empty marker base. Uses runtime type checking but allows visitors to handle only some types.

### Iterator

Access elements sequentially without exposing internal representation. Key power: **lazy evaluation** — compute values on demand, enabling infinite sequences.

**Internal vs external iteration:** Internal iteration (forEach) — the collection controls traversal. External iteration (hasNext/next) — the client controls when to advance, stop, or interleave iterators.

### Chain of Responsibility

Pass a request through a chain of handlers until one handles it. Each handler either processes the request or passes it to the next. Always include a default handler at the end.

### Memento

Capture and externalize an object's internal state for later restoration without violating encapsulation. The memento is **opaque** to everyone except the originator — others can hold mementos but cannot inspect or modify them.

### Null Object

Provide an object with neutral behavior to eliminate null checks. Enables Tell Don't Ask style:

```
// Bad — ask then tell
if employee != null:
    employee.calculatePay()

// Good — just tell (NullEmployee.calculatePay() does nothing)
employee.calculatePay()
```

The null object's methods should do "nothing" — but what "nothing" means depends on context (NullLogger discards messages, NullIterator returns `hasNext() = false`).

### Extension Object

Add interfaces to objects dynamically. Objects maintain a map of extensions; clients query by interface type. Part of the Visitor family. Useful when you can't modify the original hierarchy.

### Interpreter

Define a grammar representation and an interpreter for it. About creating domain-specific languages.

**Warning (Greenspun's Tenth Rule):** "Any sufficiently complicated program contains an ad hoc, informally-specified, bug-ridden, slow implementation of half of Common Lisp." Creating your own language is seductive but dangerous. For complex languages, use parser generators.

---

## When Reviewing Pattern Usage

For each pattern found in code, verify:

1. **Justified:** Does it solve a specific, actual problem? (Not preemptive)
2. **Natural fit:** Does it simplify the code, or add unnecessary indirection?
3. **Correct:** Does the implementation follow the pattern's intent, not just its structure?
4. **Complete:** Are edge cases handled? (Observer deregistration, Command undo state, Chain default handler, Singleton thread safety)
5. **Named well:** Do class/interface names communicate the pattern's role?

### Pattern-Specific Checks

- **Command:** Truly decouples what/who/when? Undo captures required state?
- **Factory:** Concrete types isolated from business logic? Main owns factory creation?
- **Strategy/Template Method:** Invariant/variant split clean? Right choice between composition and inheritance?
- **State:** All transitions explicit? Each state handles all events?
- **Observer:** Registration/deregistration handled? No memory leak risk?
- **Singleton:** Thread safety correct? Would DI be better?
- **Visitor:** 90-degree rotation trade-off appropriate for this hierarchy?
- **Bridge:** Actually reduces M×N to M+N?

---

## Related Skills

- `/solid` — patterns implement SOLID principles (Strategy/State enable OCP, Factory enables DIP)
- `/functions` — pattern methods must follow function principles
- `/naming` — pattern classes and interfaces must reveal intent
- `/architecture` — patterns at the architectural level (boundaries, plug-ins)
- `/clean-code-review` — comprehensive review including pattern usage
