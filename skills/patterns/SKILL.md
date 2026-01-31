---
name: patterns
description: >-
  Guide identifying and applying design patterns appropriately. Activates when
  code could benefit from patterns, when discussing GOF patterns, or when the user
  mentions pattern names like Factory, Strategy, Observer, Command, etc.
allowed-tools: Read, Grep, Glob
argument-hint: [code or situation to analyze]
---

# Patterns Workflow

Follow this workflow when identifying and applying design patterns to code.

## Step 1: Identify Code That Could Benefit From Patterns

1. Search for code exhibiting pattern-solvable problems:
   - Nested switch statements on types (State Pattern candidate)
   - Object creation scattered throughout codebase (Factory candidate)
   - Complex conditional behavior based on object state (Strategy/State candidate)
   - Tight coupling between UI and business logic (Observer/MVP candidate)
   - Duplicate loop structures with varying operations (Template Method candidate)
   - Need to add operations to existing hierarchies (Visitor candidate)
   - Complex subsystem coordination (Facade/Mediator candidate)

2. Analyze the problem context:
   - What specific problem needs solving?
   - Is there actual complexity that a pattern would address?
   - Would a pattern simplify or complicate the code?

## Step 2: Select Appropriate Pattern Based on Problem Context

Use this decision framework:

**For Object Creation Problems:**
- Need to isolate concrete type creation? -> Factory (Abstract Factory or Factory Method)
- Need to create copies of existing objects? -> Prototype
- Need to construct complex objects step by step? -> Builder
- Need exactly one instance? -> Singleton (use cautiously) or Monostate

**For Structural Problems:**
- Need incompatible interfaces to work together? -> Adapter
- Have M x N class combinations? -> Bridge
- Need tree structures with uniform treatment? -> Composite
- Need to add behavior dynamically? -> Decorator
- Need to simplify complex subsystems? -> Facade
- Need to share fine-grained objects efficiently? -> Flyweight
- Need to control access or cross boundaries? -> Proxy

**For Behavioral Problems:**
- Need to decouple request from execution? -> Command
- Need to manage complex state transitions? -> State
- Need interchangeable algorithms? -> Strategy
- Need fixed algorithm with varying steps? -> Template Method
- Need to notify multiple objects of changes? -> Observer
- Need to add operations to hierarchies? -> Visitor
- Need to traverse without exposing internals? -> Iterator
- Need centralized coordination? -> Mediator
- Need to pass requests through handlers? -> Chain of Responsibility
- Need to capture/restore object state? -> Memento
- Need to eliminate null checks? -> Null Object
- Need a simple DSL? -> Interpreter

## Step 3: Apply Pattern Correctly Following GOF Guidelines

Before implementing, verify:
- [ ] The pattern solves a specific problem you actually have
- [ ] The pattern fits naturally without forcing
- [ ] You can explain why this pattern is appropriate
- [ ] The pattern will simplify, not complicate, the code

## Step 4: Avoid Pattern Misuse

**Critical Warning from Uncle Bob:**
"When you have a nice shiny new hammer, everything looks like a nail."

Do NOT use patterns:
- Just to use patterns (they add complexity)
- Before you have a problem (let need emerge)
- To show off (simple code beats clever code)
- When they don't fit naturally (forcing is wrong)

## Step 5: Apply /professional Workflow for Quality Standards

After implementing patterns, ensure code meets professional standards by applying the /professional workflow for quality verification.

---

# Design Patterns - Uncle Bob's Clean Code Teachings

This is a comprehensive guide to Design Patterns as taught by Robert C. Martin (Uncle Bob) in his Clean Code video series. It covers the philosophy behind patterns, when to use them, when to avoid them, and the implementation nuances that separate good pattern usage from cargo cult programming.

## Pattern Philosophy

### The Gang of Four Legacy

The Design Patterns book by Gamma, Helm, Johnson, and Vlissides (1995) transformed software development. As Uncle Bob explains, the GOF book was revolutionary because it gave developers a shared vocabulary - "a book full of names."

**The True Value of Patterns:**
- Patterns provide a common language for developers to communicate design concepts
- They are not templates to blindly apply, but tools to solve specific problems
- The GOF book documents solutions that experienced developers discovered through practice
- Patterns represent "chunks of design experience" that can be communicated efficiently

**Critical Warning - Pattern Overuse:**
Uncle Bob warns strongly against pattern abuse: "When you have a nice shiny new hammer, everything looks like a nail." Patterns should emerge from need, not be applied preemptively. The goal is clean, simple code - patterns are tools to achieve that, not ends in themselves.

### Christopher Alexander's Influence

Design patterns originated from architect Christopher Alexander's work. Alexander proposed that good buildings could be constructed from a pattern language - a set of proven solutions to recurring design problems. The GOF adapted this idea for software, recognizing that good software designs also exhibit recurring patterns.

---

## Command Pattern

### Core Concept

The Command Pattern decouples "what needs to be done" from "who does it" and "when it happens." It encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations.

### The Simplest Pattern

```java
public interface Command {
    void execute();
}
```

This is the simplest of all design patterns - just a single method interface. Its power lies not in its structure but in its application.

### Key Applications

**1. Decoupling Button Clicks from Actions:**

```java
public class Button {
    private Command command;

    public Button(Command command) {
        this.command = command;
    }

    public void click() {
        command.execute();
    }
}
```

The button doesn't know what it does - it just knows how to be clicked. This separates the GUI from the business logic.

**2. Undo/Redo Systems:**

Commands can remember their previous state and reverse their actions:

```java
public interface UndoableCommand extends Command {
    void undo();
}

public class CommandHistory {
    private Stack<UndoableCommand> undoStack = new Stack<>();
    private Stack<UndoableCommand> redoStack = new Stack<>();

    public void execute(UndoableCommand command) {
        command.execute();
        undoStack.push(command);
        redoStack.clear();
    }

    public void undo() {
        if (!undoStack.isEmpty()) {
            UndoableCommand command = undoStack.pop();
            command.undo();
            redoStack.push(command);
        }
    }

    public void redo() {
        if (!redoStack.isEmpty()) {
            UndoableCommand command = redoStack.pop();
            command.execute();
            undoStack.push(command);
        }
    }
}
```

**3. Thread Decoupling and Queuing:**

Commands can be queued and executed by worker threads:

```java
public class CommandQueue {
    private BlockingQueue<Command> queue = new LinkedBlockingQueue<>();

    public void submit(Command command) {
        queue.add(command);
    }

    public void processCommands() {
        while (true) {
            Command command = queue.take();
            command.execute();
        }
    }
}
```

**4. The Actor Model:**

Uncle Bob describes how the Command Pattern forms the foundation of the Actor Model used in systems like Erlang:

- Each "actor" is an object with a command queue
- Actors communicate by sending commands to each other's queues
- Each actor processes its queue sequentially (no internal threading concerns)
- This creates highly concurrent systems with isolated state

### Temporal Decoupling

Commands separate the moment of decision from the moment of execution. This "temporal decoupling" enables:
- Scheduling commands for later execution
- Batching commands for efficient processing
- Persisting commands for crash recovery
- Auditing all operations through command logs

---

## Factory Patterns

### The Problem Factories Solve

Uncle Bob identifies the core problem: **type-safe code creates source code dependencies on concrete types.** When you write `new ConcreteClass()`, you create a dependency that can propagate throughout your system.

### Abstract Factory Pattern

Creates families of related objects without specifying their concrete classes.

```java
public interface EmployeeFactory {
    Employee makeEmployee(EmployeeType type);
}

public class EmployeeFactoryImplementation implements EmployeeFactory {
    public Employee makeEmployee(EmployeeType type) {
        switch (type) {
            case HOURLY: return new HourlyEmployee();
            case SALARIED: return new SalariedEmployee();
            case COMMISSIONED: return new CommissionedEmployee();
            default: throw new IllegalArgumentException();
        }
    }
}
```

**The Partition of Dependency:**
- Code that uses Employee depends only on the Employee interface
- Code that creates employees depends on concrete types
- The factory isolates creation from usage
- Main (or a similar boundary component) creates the factory and injects it

### Factory Method Pattern

Uses inheritance instead of composition - a subclass decides which class to instantiate.

```java
public abstract class Document {
    public abstract Page createPage();

    public void addPage() {
        pages.add(createPage());
    }
}

public class Resume extends Document {
    @Override
    public Page createPage() {
        return new SkillsPage();
    }
}

public class Report extends Document {
    @Override
    public Page createPage() {
        return new ReportPage();
    }
}
```

### Prototype Pattern

Create new objects by copying existing ones.

```java
public interface Prototype {
    Prototype clone();
}

public class PrototypeRegistry {
    private Map<String, Prototype> prototypes = new HashMap<>();

    public void register(String name, Prototype prototype) {
        prototypes.put(name, prototype);
    }

    public Prototype create(String name) {
        return prototypes.get(name).clone();
    }
}
```

### The Type Wars

Uncle Bob describes the fundamental tension in typed languages:

**Type-Safe Code:**
```java
Employee e = factory.makeEmployee(HOURLY);
```
- Compiler validates types
- Creates source code dependencies on type enums/constants

**Configurable Code:**
```java
Employee e = factory.makeEmployee("hourly");
```
- Types determined at runtime (from config files, databases)
- No compile-time type checking
- More flexible deployment

**Resolution:** Uncle Bob suggests using type-safe code internally but allowing configuration at boundaries. The factory can read configuration to determine which types to create, isolating the string-to-type mapping to a single location.

---

## Strategy Pattern

### Core Concept

The Strategy Pattern lets you define a family of algorithms, encapsulate each one, and make them interchangeable. It enables the algorithm to vary independently from clients that use it.

**This is "external polymorphism"** - the polymorphic behavior happens outside the class hierarchy.

### Classic Example: Application/Server Architecture

```java
public interface Application {
    void handle(Request request);
}

public class Server {
    private Application application;

    public Server(Application application) {
        this.application = application;
    }

    public void run() {
        while (true) {
            Request request = waitForRequest();
            application.handle(request);
        }
    }
}
```

The Server is the high-level policy. It doesn't know about specific applications - it just knows the Application interface. Concrete applications (web apps, API servers, etc.) can be plugged in without changing the Server.

### Bubble Sort with Strategy

Uncle Bob's teaching example shows how to parameterize sorting:

```java
public interface SortStrategy {
    boolean outOfOrder(int i, int j, Object[] array);
    void swap(int i, int j, Object[] array);
}

public class BubbleSorter {
    private SortStrategy strategy;

    public BubbleSorter(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public void sort(Object[] array) {
        for (int i = 0; i < array.length - 1; i++) {
            for (int j = 0; j < array.length - 1 - i; j++) {
                if (strategy.outOfOrder(j, j + 1, array)) {
                    strategy.swap(j, j + 1, array);
                }
            }
        }
    }
}
```

### Key Insight

Strategy separates the invariant algorithm (the thing that doesn't change) from the variant details (the things that do change). The bubble sort algorithm is invariant; the comparison and swap operations are variant.

---

## Template Method Pattern

### Core Concept

The Template Method Pattern defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm's structure.

**This is "internal polymorphism"** - the polymorphic behavior happens inside the class hierarchy through inheritance.

### The Key Difference from Strategy

- **Strategy:** Uses composition (has-a relationship)
- **Template Method:** Uses inheritance (is-a relationship)

### Classic Example: Bubble Sort with Template Method

```java
public abstract class BubbleSorter {
    protected abstract boolean outOfOrder(int i, int j);
    protected abstract void swap(int i, int j);

    public void sort() {
        for (int i = 0; i < length - 1; i++) {
            for (int j = 0; j < length - 1 - i; j++) {
                if (outOfOrder(j, j + 1)) {
                    swap(j, j + 1);
                }
            }
        }
    }
}

public class IntBubbleSorter extends BubbleSorter {
    private int[] array;

    public IntBubbleSorter(int[] array) {
        this.array = array;
        this.length = array.length;
    }

    @Override
    protected boolean outOfOrder(int i, int j) {
        return array[i] > array[j];
    }

    @Override
    protected void swap(int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
```

### Uncle Bob's Principle: "Write a Loop Once"

If you find yourself writing the same loop structure multiple times with only minor variations, that's a candidate for Template Method. The loop is the invariant; the operations within are the variants.

### When to Choose Each

**Use Strategy when:**
- You need to switch algorithms at runtime
- Multiple unrelated classes need the same algorithm family
- The algorithm needs to be completely independent

**Use Template Method when:**
- The algorithm variation is tightly coupled to the class
- Subclasses naturally represent variations
- You want to enforce an algorithm structure

---

## State Pattern

### The Problem: Complex State Logic

Uncle Bob uses the subway turnstile as a teaching example:

**States:** Locked, Unlocked
**Events:** Coin inserted, Person passes through

**The naive approach - nested switch statements:**

```java
public void event(Event event) {
    switch (state) {
        case LOCKED:
            switch (event) {
                case COIN:
                    unlock();
                    state = UNLOCKED;
                    break;
                case PASS:
                    alarm();
                    break;
            }
            break;
        case UNLOCKED:
            switch (event) {
                case COIN:
                    thankyou();
                    break;
                case PASS:
                    lock();
                    state = LOCKED;
                    break;
            }
            break;
    }
}
```

This becomes unmaintainable as states and events multiply.

### The State Pattern Solution

```java
public interface TurnstileState {
    void coin(Turnstile turnstile);
    void pass(Turnstile turnstile);
}

public class LockedState implements TurnstileState {
    public void coin(Turnstile turnstile) {
        turnstile.unlock();
        turnstile.setState(new UnlockedState());
    }

    public void pass(Turnstile turnstile) {
        turnstile.alarm();
    }
}

public class UnlockedState implements TurnstileState {
    public void coin(Turnstile turnstile) {
        turnstile.thankyou();
    }

    public void pass(Turnstile turnstile) {
        turnstile.lock();
        turnstile.setState(new LockedState());
    }
}

public class Turnstile {
    private TurnstileState state = new LockedState();

    public void coin() { state.coin(this); }
    public void pass() { state.pass(this); }

    public void setState(TurnstileState state) {
        this.state = state;
    }

    // Actions
    public void unlock() { /* ... */ }
    public void lock() { /* ... */ }
    public void alarm() { /* ... */ }
    public void thankyou() { /* ... */ }
}
```

### Finite State Machine Approaches

Uncle Bob describes three approaches to implementing FSMs:

**1. Nested Switch/Case (shown above)**
- Simple for small state machines
- Becomes unwieldy as complexity grows

**2. Table-Driven:**
```java
// Transition table: [currentState][event] -> {action, nextState}
Transition[][] table = {
    // LOCKED state
    { {this::unlock, UNLOCKED}, {this::alarm, LOCKED} },
    // UNLOCKED state
    { {this::thankyou, UNLOCKED}, {this::lock, LOCKED} }
};
```

**3. State Pattern (shown above)**
- Most object-oriented approach
- Each state is a class
- Transitions are method calls

### SMC - State Machine Compiler

Uncle Bob developed a State Machine Compiler that takes a domain-specific language and generates state machine code:

```
Initial: Locked

Locked {
    coin unlock Unlocked
    pass alarm Locked
}

Unlocked {
    coin thankyou Unlocked
    pass lock Locked
}
```

This is compiled into whatever implementation approach you choose.

---

## Builder Pattern

### Core Concept

The Builder Pattern separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

### Parser Example from SMC

Uncle Bob demonstrates Builder with a parser that builds syntax data structures:

```java
public interface SyntaxBuilder {
    void newFSM(String name);
    void newState(String name);
    void newTransition(String event, String action, String nextState);
    void done();
}

public class Parser {
    private SyntaxBuilder builder;
    private Lexer lexer;

    public Parser(SyntaxBuilder builder, Lexer lexer) {
        this.builder = builder;
        this.lexer = lexer;
    }

    public void parse() {
        // BNF-based parsing logic
        // Calls builder methods as syntax elements are recognized
        builder.newFSM(parseName());
        while (hasMoreStates()) {
            builder.newState(parseStateName());
            while (hasMoreTransitions()) {
                builder.newTransition(
                    parseEvent(),
                    parseAction(),
                    parseNextState()
                );
            }
        }
        builder.done();
    }
}
```

### The BNF Connection

Builder works naturally with BNF (Backus-Naur Form) grammars:

```
fsm         ::= header states
header      ::= "Initial:" name
states      ::= state*
state       ::= name "{" transitions "}"
transitions ::= transition*
transition  ::= event action nextState
```

Each grammar production can trigger a builder method.

### Facade as Builder's Special Case

Uncle Bob notes that a Facade that constructs something is essentially a Builder. The pattern names overlap - what matters is understanding the underlying concept of separating construction from representation.

---

## Visitor Pattern

### The Problem: Adding Operations to a Hierarchy

You have a class hierarchy (like an abstract syntax tree) and need to add new operations without modifying the classes.

### The Standard Visitor

```java
public interface Visitor {
    void visit(TerminalNode node);
    void visit(NonTerminalNode node);
    void visit(RepetitionNode node);
}

public abstract class SyntaxNode {
    public abstract void accept(Visitor visitor);
}

public class TerminalNode extends SyntaxNode {
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

// Each node type implements accept() similarly
```

**The 90-Degree Rotation:**
- Without Visitor: Easy to add new node types, hard to add new operations
- With Visitor: Easy to add new operations, hard to add new node types

This trade-off is fundamental - Visitor inverts the natural extension points of inheritance.

### The Visitor Family

Uncle Bob identifies several patterns as variations on the Visitor theme:
- **Visitor** - adds operations to hierarchies
- **Decorator** - adds behavior to objects
- **Extension Object** - adds interfaces to objects

All share the concept of adding capability from outside the class.

### Acyclic Visitor

The standard Visitor creates a dependency cycle:
- Nodes depend on Visitor interface
- Visitor interface depends on all node types

**Acyclic Visitor breaks the cycle:**

```java
public interface Visitor {
    // Empty marker interface
}

public interface TerminalNodeVisitor {
    void visit(TerminalNode node);
}

public interface NonTerminalNodeVisitor {
    void visit(NonTerminalNode node);
}

public class TerminalNode extends SyntaxNode {
    public void accept(Visitor visitor) {
        if (visitor instanceof TerminalNodeVisitor) {
            ((TerminalNodeVisitor) visitor).visit(this);
        }
    }
}

public class CodeGenerator implements Visitor,
                                      TerminalNodeVisitor,
                                      NonTerminalNodeVisitor {
    // Implement only the visit methods you need
}
```

**Trade-offs:**
- Breaks the dependency cycle
- Allows visitors to handle only some node types
- Uses runtime type checking (instanceof)
- Slightly slower due to type checks

---

## Composite Pattern

### Core Concept

Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions uniformly.

### AST Example

```java
public abstract class SyntaxNode {
    public abstract void accept(Visitor visitor);
}

public class TerminalNode extends SyntaxNode {
    private String value;
    // Single leaf node
}

public class SequenceNode extends SyntaxNode {
    private List<SyntaxNode> children;
    // Contains other nodes

    public void accept(Visitor visitor) {
        visitor.visit(this);
        for (SyntaxNode child : children) {
            child.accept(visitor);
        }
    }
}
```

### Key Insight

Composite allows you to build tree structures where the client code doesn't need to know whether it's dealing with a leaf or a branch. The same operations work on both.

---

## Observer Pattern

### Core Concept

Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

### Historical Context: MVC

Uncle Bob traces Observer to the Model-View-Controller pattern from Smalltalk:

- **Model:** The data and business logic
- **View:** The visual representation
- **Controller:** Handles user input

The Model uses Observer to notify Views of changes without knowing about them.

### Pull Model vs Push Model

**Pull Model:**
```java
public interface Observer {
    void update();
}

public class ConcreteObserver implements Observer {
    private Subject subject;

    public void update() {
        // Pull data from subject
        Object data = subject.getData();
        // Process data
    }
}
```

**Push Model:**
```java
public interface Observer {
    void update(Object data);
}

public class Subject {
    private List<Observer> observers;

    public void notifyObservers() {
        Object data = getData();
        for (Observer observer : observers) {
            observer.update(data);  // Push data to observers
        }
    }
}
```

**Trade-offs:**
- Pull: Observers decide what data they need
- Push: Subject decides what data to send
- Push can be more efficient (less querying)
- Pull is more flexible (observers are independent)

### MVP - Model View Presenter

Uncle Bob describes MVP as a refinement of MVC:

```java
public interface View {
    void displayData(String data);
    void setPresenter(Presenter presenter);
}

public class Presenter implements Observer {
    private Model model;
    private View view;

    public void update() {
        String data = model.getData();
        String formattedData = format(data);
        view.displayData(formattedData);
    }

    public void onUserAction() {
        model.doSomething();
    }
}
```

The Presenter mediates between Model and View, keeping both clean and testable.

### Implementation Considerations

**Registration/Deregistration:**
```java
public class Subject {
    private List<Observer> observers = new ArrayList<>();

    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }
}
```

**Warning:** Forgetting to deregister observers is a common source of memory leaks in languages without garbage collection, and even in GC languages can prevent objects from being collected.

---

## Singleton Pattern

### Core Concept

Ensure a class has only one instance and provide a global point of access to it.

### Static Initialization

```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();

    private Singleton() {}

    public static Singleton getInstance() {
        return INSTANCE;
    }
}
```

**Characteristics:**
- Instance created at class load time
- Thread-safe by virtue of class loading mechanism
- Cannot control initialization timing
- Instance exists even if never used

### Dynamic (Lazy) Initialization

```java
public class Singleton {
    private static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
```

**Problem:** This is NOT thread-safe!

### Threading Issues

**Race Condition:**
```
Thread A: checks (instance == null) -> true
Thread B: checks (instance == null) -> true
Thread A: creates new Singleton
Thread B: creates ANOTHER new Singleton!
```

**Naive Fix - Synchronized:**
```java
public static synchronized Singleton getInstance() {
    if (instance == null) {
        instance = new Singleton();
    }
    return instance;
}
```

**Problem:** Synchronization overhead on EVERY call, even after instance exists.

### Double-Checked Locking

```java
public class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {                    // First check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {            // Second check (with lock)
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**Critical:** The `volatile` keyword is REQUIRED!

### Why Volatile is Necessary

Uncle Bob explains the subtle bug without volatile:

Without volatile, the compiler/JVM can reorder operations. The assignment `instance = new Singleton()` involves:
1. Allocate memory
2. Initialize the object
3. Assign reference to `instance`

The compiler might reorder to: 1, 3, 2

**Race condition:**
```
Thread A: Allocates memory, assigns to instance (but not yet initialized!)
Thread B: Checks (instance == null) -> false (sees the reference)
Thread B: Returns partially constructed object!
Thread A: Finishes initialization (too late for Thread B)
```

**Volatile prevents this reordering** by creating a memory barrier.

### When to Avoid Singleton

Uncle Bob warns about Singleton overuse:
- Creates hidden global state
- Makes testing difficult
- Hides dependencies
- Often a sign of poor design

**Better alternative:** Dependency injection with explicit single-instance management.

---

## Monostate Pattern

### Core Concept

Achieve singleton behavior through static member variables while keeping the class instantiable.

```java
public class Monostate {
    private static int value;

    public int getValue() { return value; }
    public void setValue(int v) { value = v; }
}

// Usage:
Monostate a = new Monostate();
Monostate b = new Monostate();
a.setValue(42);
System.out.println(b.getValue());  // Prints 42!
```

### Hidden Singularity

The key feature: **clients don't know they're using a singleton.** Every instance shares the same state through static variables, but the API looks like a normal class.

### Polymorphic Derivatives

Unlike Singleton, Monostate supports inheritance:

```java
public class BaseMonostate {
    private static String sharedData;

    public String getData() { return sharedData; }
    public void setData(String data) { sharedData = data; }
}

public class ExtendedMonostate extends BaseMonostate {
    // Can override behavior while sharing state
    @Override
    public void setData(String data) {
        super.setData(data.toUpperCase());
    }
}
```

### Monostate vs Singleton

**Singleton:**
- Explicit - callers know it's a singleton
- Controlled instantiation (private constructor)
- Cannot have polymorphic behavior
- Instance is optional (lazy creation)

**Monostate:**
- Hidden - callers don't know about shared state
- Normal instantiation
- Supports inheritance and polymorphism
- All instances always share state

---

## Null Object Pattern

### Core Concept

Provide an object with defined neutral ("null") behavior, avoiding the need for null checks.

### The Problem

```java
// Code littered with null checks
Employee employee = database.getEmployee(id);
if (employee != null) {
    employee.calculatePay();
}
```

### The Solution

```java
public interface Employee {
    void calculatePay();
    boolean isNull();
}

public class RealEmployee implements Employee {
    public void calculatePay() {
        // Actual calculation
    }

    public boolean isNull() { return false; }
}

public class NullEmployee implements Employee {
    public void calculatePay() {
        // Do nothing - inconsequential behavior
    }

    public boolean isNull() { return true; }
}

// In database:
public Employee getEmployee(int id) {
    Employee e = findEmployee(id);
    return (e != null) ? e : new NullEmployee();
}

// Usage - no null checks needed!
Employee employee = database.getEmployee(id);
employee.calculatePay();
```

### Tell Don't Ask

The Null Object Pattern enables "Tell Don't Ask" style programming:

**Bad (Ask then Tell):**
```java
if (employee != null) {
    employee.calculatePay();
}
```

**Good (Just Tell):**
```java
employee.calculatePay();
```

### Inconsequential Behavior

The Null Object's methods should do "nothing" - but what "nothing" means depends on context:

```java
public class NullLogger implements Logger {
    public void log(String message) {
        // Do nothing - messages disappear
    }
}

public class NullIterator<T> implements Iterator<T> {
    public boolean hasNext() { return false; }
    public T next() { throw new NoSuchElementException(); }
}
```

---

## Proxy Pattern

### Core Concept

Provide a surrogate or placeholder for another object to control access to it.

### Crossing Boundaries

Uncle Bob emphasizes that Proxy is used when you need to cross a boundary - network, process, database, or similar.

**Database Proxy:**

```java
public interface Employee {
    String getName();
    double getSalary();
    void calculatePay();
}

public class EmployeeProxy implements Employee {
    private int employeeId;
    private Employee realEmployee;

    public EmployeeProxy(int employeeId) {
        this.employeeId = employeeId;
    }

    private Employee getRealEmployee() {
        if (realEmployee == null) {
            realEmployee = Database.loadEmployee(employeeId);
        }
        return realEmployee;
    }

    public String getName() {
        return getRealEmployee().getName();
    }

    public double getSalary() {
        return getRealEmployee().getSalary();
    }

    public void calculatePay() {
        getRealEmployee().calculatePay();
    }
}
```

### Handle-Body / Envelope-Letter Idiom

This pattern goes by several names:
- **Proxy** (GOF name)
- **Handle-Body** (common C++ name)
- **Envelope-Letter** (alternative name)

The proxy (handle/envelope) wraps and controls access to the real object (body/letter).

### Hiding Database Presence

Uncle Bob's key insight: **Proxy can hide the fact that you're using a database.**

```java
// Client code doesn't know this crosses a database boundary
Employee employee = employeeRepository.find(42);
employee.calculatePay();  // May trigger database load
```

The business logic remains clean - it doesn't know about persistence.

### Virtual Proxy

A variation that creates the real object only when needed:

```java
public class ImageProxy implements Image {
    private String filename;
    private RealImage realImage;

    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename);  // Expensive loading
        }
        realImage.display();
    }
}
```

---

## Decorator Pattern

### Core Concept

Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

### Part of the Visitor Family

Uncle Bob classifies Decorator as part of the Visitor family - patterns that add behavior to existing hierarchies from the outside.

### Modem Volume Example

```java
public interface Modem {
    void dial(String number);
    void hangup();
    void send(String data);
    String receive();
}

public class RealModem implements Modem {
    // Actual modem implementation
}

public class LoudDialModem implements Modem {
    private Modem modem;

    public LoudDialModem(Modem modem) {
        this.modem = modem;
    }

    public void dial(String number) {
        modem.setVolume(HIGH);
        modem.dial(number);
        modem.setVolume(LOW);
    }

    public void hangup() { modem.hangup(); }
    public void send(String data) { modem.send(data); }
    public String receive() { return modem.receive(); }
}
```

### Stacking Decorators

Decorators can be stacked:

```java
Modem modem = new RealModem();
modem = new LoudDialModem(modem);
modem = new LoggingModem(modem);
modem = new RetryModem(modem);

// Now modem has all three decorations
modem.dial("555-1234");
```

### When to Use Decorator

- When you need to add responsibilities to objects dynamically
- When extension by subclassing is impractical (too many combinations)
- When you want to add behavior that can be withdrawn

### Decorator vs Inheritance

**Inheritance:**
- Static - fixed at compile time
- Affects all instances of a class
- Can lead to class explosion (LoudModem, LoggingModem, LoudLoggingModem, etc.)

**Decorator:**
- Dynamic - can be changed at runtime
- Affects only decorated instances
- Compose behaviors freely

---

## Facade Pattern

### Core Concept

Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

### Imposing Policy from Above

Uncle Bob describes Facade as "imposing policy from above" - it sits above a set of classes and provides a simplified interface.

```java
public class OrderFacade {
    private InventorySystem inventory;
    private PaymentSystem payment;
    private ShippingSystem shipping;
    private NotificationSystem notification;

    public void placeOrder(Order order) {
        // Facade coordinates the subsystems
        if (inventory.checkAvailability(order.getItems())) {
            inventory.reserve(order.getItems());
            PaymentResult result = payment.charge(order.getPayment());
            if (result.isSuccessful()) {
                shipping.scheduleDelivery(order);
                notification.sendConfirmation(order);
            } else {
                inventory.release(order.getItems());
                notification.sendPaymentFailure(order);
            }
        } else {
            notification.sendOutOfStock(order);
        }
    }
}
```

### Builder as Facade

Uncle Bob notes that Builder is essentially a Facade that constructs something. The builder coordinates multiple components to create a complex object.

### When to Use Facade

- When you want to provide a simple interface to a complex subsystem
- When there are many dependencies between clients and implementation classes
- When you want to layer your subsystems

---

## Mediator Pattern

### Core Concept

Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

### Imposing Policy from Below

Uncle Bob contrasts Mediator with Facade: while Facade imposes policy "from above," Mediator imposes policy "from below."

**Facade:** Sits above subsystems, calls down into them
**Mediator:** Sits among peers, coordinates between them

### Quick Entry Example

Uncle Bob describes a medical records system:

```java
public class QuickEntryMediator {
    private PatientField patientField;
    private DiagnosisField diagnosisField;
    private MedicationField medicationField;

    public void onPatientSelected(Patient patient) {
        // Load patient's common diagnoses
        diagnosisField.populateOptions(patient.getCommonDiagnoses());
        medicationField.clear();
    }

    public void onDiagnosisSelected(Diagnosis diagnosis) {
        // Load appropriate medications for this diagnosis
        medicationField.populateOptions(diagnosis.getCommonMedications());
    }
}
```

The fields don't know about each other - the Mediator coordinates their interactions.

### VTR Robot Example

Uncle Bob describes a video tape duplication system with robot arms:

```java
public class DuplicationMediator {
    private RobotArm robotA;
    private RobotArm robotB;
    private SourcePlayer source;
    private List<Recorder> recorders;

    public void duplicateTape(Tape master) {
        // Coordinate the robots and machines
        robotA.pickUp(master);
        robotA.loadInto(source);

        for (Recorder recorder : recorders) {
            Tape blank = robotB.getBlankTape();
            robotB.loadInto(recorder);
        }

        source.play();
        // ... coordinate playback and recording
    }
}
```

### The Puppeteer Metaphor

Think of the Mediator as a puppeteer controlling marionettes:
- The puppets (colleagues) don't know about each other
- The puppeteer (mediator) makes them appear to interact
- Complex choreography is centralized in the puppeteer

---

## Flyweight Pattern

### Core Concept

Use sharing to support large numbers of fine-grained objects efficiently.

### The Weight Metaphor

Uncle Bob explains the name: imagine a list of objects where the full object is "heavyweight" (lots of data) but the reference is "lightweight." Flyweight creates objects that look heavyweight from the outside but share internal data.

### Movie Rental Example

```java
// Without Flyweight - each rental duplicates movie data
public class Rental {
    private String movieTitle;
    private String movieDirector;
    private int movieYear;
    private int rentalDays;
    private Date rentalDate;
    // Movie data repeated for every rental!
}

// With Flyweight - share movie data
public class Movie {  // Flyweight - shared
    private String title;
    private String director;
    private int year;
}

public class Rental {
    private Movie movie;  // Reference to shared flyweight
    private int rentalDays;
    private Date rentalDate;
}

public class MovieFactory {
    private Map<String, Movie> movies = new HashMap<>();

    public Movie getMovie(String title) {
        if (!movies.containsKey(title)) {
            movies.put(title, loadMovieFromDatabase(title));
        }
        return movies.get(title);
    }
}
```

### Intrinsic vs Extrinsic State

**Intrinsic state:** Stored in the flyweight, shared among contexts (movie title, director)
**Extrinsic state:** Stored outside, varies by context (rental date, rental duration)

### When to Use Flyweight

- When an application uses a large number of objects
- When storage costs are high due to object quantity
- When most object state can be made extrinsic
- When many groups of objects can be replaced by few shared objects

---

## Memento Pattern

### Core Concept

Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

### Opaque State Capture

The key insight: the memento is **opaque** to everyone except the originator. Other classes can hold and pass mementos, but cannot inspect or modify them.

### Chess Board Example

Uncle Bob provides a detailed example of saving chess board state:

```java
public class ChessBoard {
    private Piece[][] board = new Piece[8][8];

    public ChessBoardMemento createMemento() {
        return new ChessBoardMemento(packState());
    }

    public void restore(ChessBoardMemento memento) {
        unpackState(memento.getState());
    }

    private byte[] packState() {
        // Pack entire board into 32 bytes using nibbles!
        // Each square: 4 bits (piece type + color)
        // 64 squares * 4 bits = 256 bits = 32 bytes
        byte[] state = new byte[32];
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                int index = row * 8 + col;
                int byteIndex = index / 2;
                int nibble = encodeSquare(board[row][col]);
                if (index % 2 == 0) {
                    state[byteIndex] = (byte)(nibble << 4);
                } else {
                    state[byteIndex] |= (byte)nibble;
                }
            }
        }
        return state;
    }

    private int encodeSquare(Piece piece) {
        // 4 bits: 0=empty, 1-6=white pieces, 9-14=black pieces
        if (piece == null) return 0;
        int code = piece.getType().ordinal() + 1;  // 1-6
        if (piece.getColor() == Color.BLACK) code += 8;
        return code;
    }
}

public class ChessBoardMemento {
    private final byte[] state;  // Opaque to external classes

    ChessBoardMemento(byte[] state) {  // Package-private constructor
        this.state = state.clone();
    }

    byte[] getState() {  // Package-private accessor
        return state.clone();
    }
}
```

### Implementation Details

**32 bytes for entire chess board:**
- 64 squares on board
- 4 bits (nibble) per square
- 64 * 4 = 256 bits = 32 bytes

**Nibble encoding:**
- 0 = empty
- 1-6 = white pieces (pawn, rook, knight, bishop, queen, king)
- 9-14 = black pieces (pawn, rook, knight, bishop, queen, king)
- (7, 8, 15 unused)

### Encapsulation Through Access Control

The Memento class uses package-private (default) access:
- Constructor is package-private: only ChessBoard can create mementos
- State accessor is package-private: only ChessBoard can read state
- External code can hold mementos but cannot peek inside

---

## Extension Object Pattern

### Core Concept

Add interfaces to objects dynamically without changing their class definitions.

### Part of the Visitor Family

Uncle Bob classifies Extension Object as part of the Visitor family - another way to add behavior to hierarchies from outside.

### Degenerate Marker Interface

The base pattern uses a marker interface:

```java
public interface Extension {
    // Marker interface - intentionally empty
}

public interface Printable extends Extension {
    void print(PrintStream out);
}

public interface Persistable extends Extension {
    void save(Database db);
    void load(Database db);
}
```

### Dynamic Type Checking

Objects maintain a map of extensions:

```java
public class ExtensibleObject {
    private Map<Class<?>, Extension> extensions = new HashMap<>();

    public <T extends Extension> void addExtension(Class<T> type, T extension) {
        extensions.put(type, extension);
    }

    public <T extends Extension> T getExtension(Class<T> type) {
        return type.cast(extensions.get(type));
    }

    public boolean hasExtension(Class<?> type) {
        return extensions.containsKey(type);
    }
}

// Usage:
ExtensibleObject obj = new ExtensibleObject();
obj.addExtension(Printable.class, new MyPrintable());

if (obj.hasExtension(Printable.class)) {
    obj.getExtension(Printable.class).print(System.out);
}
```

### Bill of Materials Example

Uncle Bob describes an assembly/part hierarchy:

```java
public abstract class Part extends ExtensibleObject {
    private String partNumber;
    private String description;
}

public class PiecePart extends Part {
    // Individual manufactured part
}

public class Assembly extends Part {
    private List<Part> components;
    // Composed of other parts
}

// Add CSV export capability without modifying Part hierarchy
public class CsvExportExtension implements Extension {
    public String toCsv(Part part) {
        // Generate CSV representation
    }
}
```

### When to Use Extension Object

- When you need to add optional interfaces to existing hierarchies
- When the added interfaces vary independently from the core hierarchy
- When modifying the original classes is not possible or desirable

---

## Bridge Pattern

### Core Concept

Decouple an abstraction from its implementation so that the two can vary independently.

### The M x N Problem

Uncle Bob explains Bridge with a practical problem:

You have:
- M types of abstractions (e.g., different paycheck formats)
- N types of implementations (e.g., different output devices)

Without Bridge: M x N classes
With Bridge: M + N classes

### Paycheck Station Example

```java
// Without Bridge - Explosion of classes
class PrinterPaycheck { }
class EmailPaycheck { }
class DirectDepositPaycheck { }
class ManagerPrinterPaycheck extends PrinterPaycheck { }
class ManagerEmailPaycheck extends EmailPaycheck { }
class HourlyPrinterPaycheck extends PrinterPaycheck { }
class HourlyEmailPaycheck extends EmailPaycheck { }
// ... M x N combinations!

// With Bridge
public interface PayStation {  // Implementation
    void output(PaycheckData data);
}

public class PrinterStation implements PayStation {
    public void output(PaycheckData data) {
        // Print to printer
    }
}

public class EmailStation implements PayStation {
    public void output(PaycheckData data) {
        // Send via email
    }
}

public abstract class Paycheck {  // Abstraction
    protected PayStation station;

    public Paycheck(PayStation station) {
        this.station = station;
    }

    public abstract void generate();
}

public class HourlyPaycheck extends Paycheck {
    public void generate() {
        PaycheckData data = calculateHourlyPay();
        station.output(data);  // Delegate to implementation
    }
}

public class SalariedPaycheck extends Paycheck {
    public void generate() {
        PaycheckData data = calculateSalariedPay();
        station.output(data);
    }
}
```

### Tell Don't Ask Compliance

Uncle Bob notes that Bridge naturally supports "Tell Don't Ask":

```java
// Good - Tell the paycheck where to go
paycheck.setStation(printerStation);
paycheck.generate();

// Bad - Ask and then tell
if (outputType == PRINTER) {
    printer.print(paycheck.getData());
} else if (outputType == EMAIL) {
    email.send(paycheck.getData());
}
```

### When to Use Bridge

- When you want to avoid permanent binding between abstraction and implementation
- When both abstractions and implementations should be extensible by subclassing
- When implementation changes should not affect client code
- When you have a proliferation of classes due to multiple dimensions of variation

---

## Chain of Responsibility Pattern

### Core Concept

Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along until one handles it.

### Decoupled Server Selection

```java
public interface Handler {
    void setNext(Handler next);
    void handle(Request request);
}

public abstract class BaseHandler implements Handler {
    private Handler next;

    public void setNext(Handler next) {
        this.next = next;
    }

    public void handle(Request request) {
        if (canHandle(request)) {
            doHandle(request);
        } else if (next != null) {
            next.handle(request);
        }
    }

    protected abstract boolean canHandle(Request request);
    protected abstract void doHandle(Request request);
}
```

### Enum-Based Checking

Uncle Bob shows a common implementation where handlers check against an enum:

```java
public enum RequestType {
    TYPE_A, TYPE_B, TYPE_C
}

public class TypeAHandler extends BaseHandler {
    protected boolean canHandle(Request request) {
        return request.getType() == RequestType.TYPE_A;
    }

    protected void doHandle(Request request) {
        // Handle TYPE_A requests
    }
}

// Build the chain
Handler chain = new TypeAHandler();
chain.setNext(new TypeBHandler());
chain.getNext().setNext(new TypeCHandler());

// Use - sender doesn't know which handler will respond
chain.handle(request);
```

### All Derivatives in Chain

A common pattern: create handlers for all known types and chain them together:

```java
public class HandlerChainFactory {
    public static Handler createChain() {
        Handler chain = new DefaultHandler();  // Catch-all at end

        // Add all specific handlers
        for (RequestType type : RequestType.values()) {
            Handler specific = createHandlerFor(type);
            specific.setNext(chain);
            chain = specific;
        }

        return chain;
    }
}
```

### When to Use Chain of Responsibility

- When more than one object may handle a request and the handler is not known beforehand
- When you want to issue a request to one of several objects without specifying explicitly
- When the set of objects that can handle a request should be specified dynamically

---

## Interpreter Pattern

### Core Concept

Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.

### Domain-Specific Languages

Uncle Bob emphasizes: Interpreter is about creating domain-specific languages (DSLs) to solve specific problems more elegantly.

### Reverse Polish Notation Example

```java
// Expression: 3 4 + 5 * = 35
public interface Expression {
    int interpret(Context context);
}

public class NumberExpression implements Expression {
    private int number;

    public NumberExpression(int number) {
        this.number = number;
    }

    public int interpret(Context context) {
        return number;
    }
}

public class AddExpression implements Expression {
    private Expression left;
    private Expression right;

    public int interpret(Context context) {
        return left.interpret(context) + right.interpret(context);
    }
}

public class MultiplyExpression implements Expression {
    private Expression left;
    private Expression right;

    public int interpret(Context context) {
        return left.interpret(context) * right.interpret(context);
    }
}
```

### Script Nodes and AST Execution

For more complex DSLs, build an Abstract Syntax Tree:

```java
public abstract class ScriptNode {
    public abstract Object execute(Environment env);
}

public class AssignmentNode extends ScriptNode {
    private String variable;
    private ScriptNode expression;

    public Object execute(Environment env) {
        Object value = expression.execute(env);
        env.setVariable(variable, value);
        return value;
    }
}

public class IfNode extends ScriptNode {
    private ScriptNode condition;
    private ScriptNode thenBranch;
    private ScriptNode elseBranch;

    public Object execute(Environment env) {
        if ((Boolean) condition.execute(env)) {
            return thenBranch.execute(env);
        } else if (elseBranch != null) {
            return elseBranch.execute(env);
        }
        return null;
    }
}
```

### Warning: Overengineering

Uncle Bob includes a strong warning about Interpreter:

**Greenspun's Tenth Rule:** "Any sufficiently complicated C or Fortran program contains an ad hoc, informally-specified, bug-ridden, slow implementation of half of Common Lisp."

The warning: Creating your own language is seductive but dangerous. You may end up building a poorly designed programming language when you should have just used an existing one.

### When to Use Interpreter

- When the grammar is simple and efficiency is not critical
- When the problem naturally maps to a language
- When you need to evaluate expressions frequently with different contexts
- **Caution:** For complex languages, use parser generators instead

---

## Iterator Pattern

### Core Concept

Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

### Standard Implementation

```java
public interface Iterator<T> {
    boolean hasNext();
    T next();
}

public interface Iterable<T> {
    Iterator<T> iterator();
}

public class LinkedList<T> implements Iterable<T> {
    private Node<T> head;

    public Iterator<T> iterator() {
        return new LinkedListIterator();
    }

    private class LinkedListIterator implements Iterator<T> {
        private Node<T> current = head;

        public boolean hasNext() {
            return current != null;
        }

        public T next() {
            T value = current.value;
            current = current.next;
            return value;
        }
    }
}
```

### Lazy Evaluation

Uncle Bob emphasizes a powerful aspect of Iterator: **lazy evaluation.**

```java
// Eager - computes all values upfront
List<Integer> squares = new ArrayList<>();
for (int i = 1; i <= 1000000; i++) {
    squares.add(i * i);
}

// Lazy - computes values on demand
public class SquaresIterator implements Iterator<Integer> {
    private int current = 1;

    public boolean hasNext() {
        return true;  // Infinite!
    }

    public Integer next() {
        int result = current * current;
        current++;
        return result;
    }
}
```

### Infinite Lists

Uncle Bob describes the "integers.all" concept:

```java
public class Integers {
    public static Iterable<Integer> all() {
        return () -> new Iterator<Integer>() {
            private int current = 0;

            public boolean hasNext() { return true; }

            public Integer next() { return current++; }
        };
    }

    public static Iterable<Integer> from(int start) {
        return () -> new Iterator<Integer>() {
            private int current = start;

            public boolean hasNext() { return true; }

            public Integer next() { return current++; }
        };
    }
}

// Usage - take first 10 squares
Iterator<Integer> squares = Integers.all().map(n -> n * n).iterator();
for (int i = 0; i < 10; i++) {
    System.out.println(squares.next());
}
```

### Turning Algorithms Inside Out

Uncle Bob describes how Iterator inverts control:

**Without Iterator (internal iteration):**
```java
public void processAll(List<Item> items, Processor processor) {
    for (Item item : items) {
        processor.process(item);
    }
}
```

**With Iterator (external iteration):**
```java
Iterator<Item> iter = items.iterator();
while (iter.hasNext()) {
    Item item = iter.next();
    // Client controls the loop
    if (shouldStop(item)) break;
    process(item);
}
```

The client controls when to advance, when to stop, and can interleave multiple iterators.

---

## Adapter Pattern

### Core Concept

Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

### Object Adapter vs Class Adapter

**Object Adapter (composition):**

```java
public interface Target {
    void request();
}

public class Adaptee {
    public void specificRequest() {
        // Original implementation
    }
}

public class ObjectAdapter implements Target {
    private Adaptee adaptee;

    public ObjectAdapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }

    public void request() {
        adaptee.specificRequest();
    }
}
```

**Class Adapter (inheritance):**

```java
public class ClassAdapter extends Adaptee implements Target {
    public void request() {
        specificRequest();  // Call inherited method
    }
}
```

### Flexibility vs Rigidity Trade-off

Uncle Bob explains the trade-off:

**Object Adapter:**
- More flexible - can adapt any subclass of Adaptee
- Can be changed at runtime
- Requires extra object allocation
- Uses composition (generally preferred)

**Class Adapter:**
- More rigid - committed to specific Adaptee class
- Slightly more efficient (no delegation)
- Cannot adapt Adaptee subclasses
- Uses inheritance (less flexible)

### Table Lamp Exercise

Uncle Bob provides a teaching exercise:

```java
// You have this interface
public interface Switchable {
    void turnOn();
    void turnOff();
}

// And this class you cannot modify
public class TableLamp {
    public void illuminate() { /* ... */ }
    public void darken() { /* ... */ }
}

// Create an adapter
public class TableLampAdapter implements Switchable {
    private TableLamp lamp;

    public TableLampAdapter(TableLamp lamp) {
        this.lamp = lamp;
    }

    public void turnOn() {
        lamp.illuminate();
    }

    public void turnOff() {
        lamp.darken();
    }
}
```

### Interface Naming Convention

Uncle Bob discusses naming: the Adapter should implement the interface the client expects, not an interface named after the Adaptee.

```java
// Good - named for what client expects
public class TableLampAdapter implements Switchable { }

// Bad - named for implementation detail
public class SwitchableTableLamp implements Switchable { }
```

---

## Pattern Selection Guidelines

### When NOT to Use Patterns

Uncle Bob strongly cautions against premature pattern application:

1. **Don't use patterns just to use patterns.** They add complexity.
2. **Don't use patterns before you have a problem.** Let the need emerge.
3. **Don't use patterns to show off.** Simple code is better than clever code.
4. **Don't force patterns.** If it doesn't fit naturally, it's wrong.

### Pattern Relationships

**Creational Patterns (manage object creation):**
- Abstract Factory, Factory Method, Prototype - isolate creation decisions
- Singleton, Monostate - control instance count
- Builder - separate construction from representation

**Structural Patterns (compose objects):**
- Adapter - make incompatible interfaces work together
- Bridge - separate abstraction from implementation
- Composite - tree structures
- Decorator - add behavior dynamically
- Facade - simplify complex subsystems
- Flyweight - share fine-grained objects
- Proxy - control access to objects

**Behavioral Patterns (manage algorithms and communication):**
- Chain of Responsibility - pass request along chain
- Command - encapsulate requests as objects
- Interpreter - define grammar and interpret
- Iterator - sequential access
- Mediator - centralize complex communication
- Memento - capture and restore state
- Observer - notify dependents of changes
- State - alter behavior when state changes
- Strategy - encapsulate interchangeable algorithms
- Template Method - define algorithm skeleton
- Visitor - add operations to hierarchies

### The Pattern Test

Before applying a pattern, ask:
1. Do I have a specific problem this pattern solves?
2. Will this simplify my code or complicate it?
3. Does the pattern fit naturally, or am I forcing it?
4. Can I explain why this pattern is appropriate here?

If you can't answer these confidently, don't use the pattern.

---

## Code Review Checklist for Patterns

When reviewing code that uses design patterns:

### Command Pattern
- [ ] Does it truly decouple what from who/when?
- [ ] If using undo/redo, does each command properly capture required state?
- [ ] Is the execute() method focused on a single responsibility?

### Factory Patterns
- [ ] Are concrete types properly isolated from business logic?
- [ ] Is the factory interface stable (won't change frequently)?
- [ ] Does Main (or similar) own the factory creation?

### Strategy vs Template Method
- [ ] Is Strategy used when runtime switching is needed?
- [ ] Is Template Method used when the algorithm is fixed?
- [ ] Is the invariant/variant split clean?

### State Pattern
- [ ] Are all state transitions explicit and clear?
- [ ] Does each state class handle all possible events?
- [ ] Is there a clear initial state?

### Observer Pattern
- [ ] Are observers properly registered and deregistered?
- [ ] Is the notification granularity appropriate (not too chatty)?
- [ ] Are there any memory leak risks from forgotten observers?

### Singleton/Monostate
- [ ] Is global state actually necessary?
- [ ] For Singleton: Is thread safety handled correctly?
- [ ] Would dependency injection be a better solution?

### Null Object
- [ ] Is the null behavior truly "inconsequential"?
- [ ] Does it eliminate all null checks in client code?
- [ ] Is it clear when null objects are in use?

### Proxy/Decorator
- [ ] Does the proxy/decorator implement the same interface as the real object?
- [ ] Is the wrapping transparent to clients?
- [ ] For Proxy: Is the boundary crossing justified?

### Facade/Mediator
- [ ] Does Facade simplify the subsystem API appropriately?
- [ ] Does Mediator keep colleagues properly decoupled?
- [ ] Is the coordination logic in the right place?

### Visitor Family (Visitor, Decorator, Extension Object)
- [ ] Is the trade-off (easy to add operations vs types) appropriate?
- [ ] For Acyclic Visitor: Is the instanceof usage acceptable?
- [ ] Is the double-dispatch mechanism clear?

### Bridge
- [ ] Does it reduce M x N to M + N?
- [ ] Are both dimensions of variation independent?
- [ ] Does it enable Tell Don't Ask style?

### Chain of Responsibility
- [ ] Is there a proper termination (default handler)?
- [ ] Is the chain order intentional and documented?
- [ ] Can all requests be handled?

### Interpreter
- [ ] Is the grammar simple enough to warrant this pattern?
- [ ] Is performance acceptable for the use case?
- [ ] Would a parser generator be more appropriate?

### Iterator
- [ ] Is lazy evaluation used when beneficial?
- [ ] Are there resource cleanup concerns (close/dispose)?
- [ ] Is concurrent modification handled?

### Adapter
- [ ] Is object adapter preferred over class adapter?
- [ ] Does the adapter add only translation, no business logic?
- [ ] Is the naming client-centric (not adaptee-centric)?

---

## Summary

Design patterns are tools for solving specific problems. They provide a shared vocabulary and proven solutions, but they must be applied judiciously. As Uncle Bob teaches: the goal is clean, maintainable code. Patterns should serve that goal, not become the goal themselves.

Remember:
- **Patterns are discovered, not invented** - they emerge from solving real problems
- **Simplicity trumps cleverness** - don't use patterns just because you know them
- **The GOF book is a reference, not a rulebook** - adapt patterns to your needs
- **Names matter** - patterns give us vocabulary to communicate design decisions
- **Context is everything** - a pattern that's perfect in one situation may be wrong in another

---

## Related Skills

- **/professional** - Apply professional standards workflow for code quality verification after implementing patterns
