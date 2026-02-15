# Patterns: Extended Examples, Deep Dives

Deep reference material for the `/patterns` skill. Load on demand when teaching, providing detailed examples, or explaining implementation nuances.

---

## Extended Examples and Deep Dives

### Command: Undo/Redo Implementation

```
interface UndoableCommand extends Command:
    undo()

class CommandHistory:
    undoStack: Stack<UndoableCommand>
    redoStack: Stack<UndoableCommand>

    execute(command):
        command.execute()
        undoStack.push(command)
        redoStack.clear()

    undo():
        if undoStack.isNotEmpty():
            command = undoStack.pop()
            command.undo()
            redoStack.push(command)

    redo():
        if redoStack.isNotEmpty():
            command = redoStack.pop()
            command.execute()
            undoStack.push(command)
```

### Command: The Actor Model

Uncle Bob describes how Command forms the foundation of the Actor Model (used in Erlang-style systems): each "actor" is an object with a command queue. Actors communicate by sending commands to each other's queues. Each actor processes its queue sequentially — no internal threading concerns. This creates highly concurrent systems with isolated state.

### Factory: The Partition of Dependency

The factory creates a clean separation:
- Code that USES Employee depends only on the Employee interface
- Code that CREATES employees depends on concrete types
- The factory isolates creation from usage
- Main (or a similar boundary component) creates the factory and injects it

This is DIP in action — the high-level policy doesn't know about low-level details.

### Singleton: Threading Deep Dive

**The Double-Checked Locking Problem:**

```
class Singleton:
    instance: volatile Singleton  // volatile is REQUIRED

    getInstance():
        if instance == null:                    // First check (no lock)
            synchronized:
                if instance == null:            // Second check (with lock)
                    instance = new Singleton()
        return instance
```

**Why volatile is necessary:** Without it, the compiler can reorder operations. The assignment `instance = new Singleton()` involves: (1) allocate memory, (2) initialize the object, (3) assign reference. The compiler might reorder to 1, 3, 2. Thread B could see the reference (step 3) before initialization completes (step 2), returning a partially constructed object. Volatile creates a memory barrier preventing this reordering.

**Simplest safe approach:** Static initialization — instance created at class load time. Thread-safe by virtue of the class loading mechanism. Cannot control timing, but avoids all threading complexity.

### Monostate: Hidden Singularity

```
class Monostate:
    static value: int

    getValue(): return value
    setValue(v): value = v

// Usage:
a = new Monostate()
b = new Monostate()
a.setValue(42)
print(b.getValue())  // Prints 42!
```

Clients don't know they're using a singleton. Unlike Singleton, Monostate supports polymorphic derivatives — subclasses can override behavior while sharing the same static state.

### State: SMC — State Machine Compiler

Uncle Bob developed a State Machine Compiler that takes a domain-specific language:

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

This is compiled into whatever implementation approach you choose (nested switch, table-driven, or State pattern classes). The DSL cleanly describes the state machine without implementation noise.

### State: The Subway Turnstile (Nested Switch)

The naive approach that the State pattern replaces:

```
event(e):
    switch state:
        LOCKED:
            switch e:
                COIN: unlock(); state = UNLOCKED
                PASS: alarm()
        UNLOCKED:
            switch e:
                COIN: thankyou()
                PASS: lock(); state = LOCKED
```

Simple for small state machines but becomes unmaintainable as states and events multiply.

### State: Table-Driven Approach

```
// Transition table: [currentState][event] -> {action, nextState}
table = {
    LOCKED:   { COIN: {unlock, UNLOCKED}, PASS: {alarm, LOCKED} },
    UNLOCKED: { COIN: {thankyou, UNLOCKED}, PASS: {lock, LOCKED} }
}
```

Data-oriented approach — the state machine is described as data rather than code.

### Observer: Registration/Deregistration

```
class Subject:
    observers: List<Observer>

    addObserver(observer): observers.add(observer)
    removeObserver(observer): observers.remove(observer)

    notifyObservers():
        for observer in observers:
            observer.update()
```

**Memory leak warning:** Forgetting to call `removeObserver` prevents garbage collection even in GC languages. The subject holds a reference to the observer, keeping it alive. This is one of the most common sources of memory leaks in event-driven systems.

### Observer: MVP Implementation

```
class Presenter implements Observer:
    model: Model
    view: View

    update():
        data = model.getData()
        formattedData = format(data)
        view.displayData(formattedData)

    onUserAction():
        model.doSomething()
```

The Presenter mediates between Model and View, keeping both clean and testable. The View becomes a humble object — so simple it doesn't need testing.

### Visitor: Acyclic Visitor

Standard Visitor creates a dependency cycle (nodes depend on Visitor, Visitor depends on all node types). Acyclic Visitor breaks this:

```
interface Visitor:         // Empty marker interface

interface TerminalNodeVisitor:
    visit(terminalNode)

interface NonTerminalNodeVisitor:
    visit(nonTerminalNode)

class TerminalNode extends SyntaxNode:
    accept(visitor):
        if visitor is TerminalNodeVisitor:
            (visitor as TerminalNodeVisitor).visit(this)

class CodeGenerator implements Visitor, TerminalNodeVisitor, NonTerminalNodeVisitor:
    // Implement only the visit methods you need
```

Trade-offs: breaks the dependency cycle, allows partial handling, but uses runtime type checking.

### Memento: Chess Board Encoding

Uncle Bob's detailed example — packing an entire chess board into 32 bytes:

- 64 squares on the board
- 4 bits (nibble) per square
- 64 × 4 = 256 bits = 32 bytes
- Nibble encoding: 0=empty, 1-6=white pieces (pawn through king), 9-14=black pieces
- The memento is opaque — only ChessBoard can create and read it
- Access control (package-private constructor and getter) enforces encapsulation

### Extension Object: Bill of Materials

```
abstract class Part extends ExtensibleObject:
    partNumber, description

class PiecePart extends Part:    // Individual manufactured part
class Assembly extends Part:      // Composed of other parts
    components: List<Part>

// Add CSV export without modifying Part hierarchy
class CsvExportExtension implements Extension:
    toCsv(part): // Generate CSV representation
```

Objects maintain a map of extensions. Clients query `hasExtension(type)` and `getExtension(type)`.

### Flyweight: Movie Rental

```
// Without Flyweight — movie data duplicated for every rental
class Rental:
    movieTitle, movieDirector, movieYear  // Repeated!
    rentalDays, rentalDate

// With Flyweight — share movie data
class Movie:           // Intrinsic state (shared)
    title, director, year

class Rental:          // Extrinsic state (per-context)
    movie: Movie       // Reference to shared flyweight
    rentalDays, rentalDate

class MovieFactory:    // Manages pool
    movies: Map<String, Movie>
    getMovie(title): return cached or load from database
```

### Iterator: Lazy Evaluation and Infinite Sequences

```
class SquaresIterator:
    current = 1

    hasNext(): return true    // Infinite!
    next():
        result = current * current
        current++
        return result

// Take first 10 squares — computes on demand
iter = new SquaresIterator()
for i in 0..9:
    print(iter.next())
```

Uncle Bob describes the "integers.all" concept — an infinite lazy sequence of all integers that you can map, filter, and take from.

### Iterator: Turning Algorithms Inside Out

**Internal iteration (collection controls traversal):**
```
items.forEach(processor)
```

**External iteration (client controls traversal):**
```
iter = items.iterator()
while iter.hasNext():
    item = iter.next()
    if shouldStop(item): break
    process(item)
```

The client decides when to advance, when to stop, and can interleave multiple iterators.

### Facade: Order Processing

```
class OrderFacade:
    inventory, payment, shipping, notification

    placeOrder(order):
        if inventory.checkAvailability(order.items):
            inventory.reserve(order.items)
            result = payment.charge(order.payment)
            if result.isSuccessful():
                shipping.scheduleDelivery(order)
                notification.sendConfirmation(order)
            else:
                inventory.release(order.items)
                notification.sendPaymentFailure(order)
        else:
            notification.sendOutOfStock(order)
```

The facade coordinates subsystems behind a single `placeOrder` call.

### Mediator: Quick Entry (Medical Records)

```
class QuickEntryMediator:
    patientField, diagnosisField, medicationField

    onPatientSelected(patient):
        diagnosisField.populateOptions(patient.commonDiagnoses)
        medicationField.clear()

    onDiagnosisSelected(diagnosis):
        medicationField.populateOptions(diagnosis.commonMedications)
```

Fields don't know about each other. The Mediator coordinates their interactions.

### Mediator: VTR Robot System

Uncle Bob describes a video tape duplication system with robot arms. The duplication mediator coordinates robots, source player, and recorders to perform the complex choreography of tape duplication — no component knows about any other.

---

## Philosophy and Context

### Christopher Alexander's Influence

Design patterns originated from architect Christopher Alexander's work. Alexander proposed that good buildings could be constructed from a pattern language — proven solutions to recurring design problems. The GOF adapted this idea for software, recognizing that good software designs also exhibit recurring patterns.

### Patterns Are Discovered, Not Invented

The GOF book documents solutions that experienced developers discovered through practice. They didn't invent these patterns — they named them. The patterns existed in good code long before they had names. The book's primary contribution was giving developers a shared vocabulary.

### The Visitor Family Concept

Uncle Bob groups three patterns as the Visitor family: Visitor (adds operations to hierarchies), Decorator (adds behavior to objects), Extension Object (adds interfaces to objects). All share the concept of adding capability from outside the class. This grouping reveals the deeper pattern behind these patterns.

### Facade Imposes Policy from Above, Mediator from Below

This distinction clarifies when to use which: Facade sits above a set of subsystems and provides a simplified interface downward. Mediator sits among peers and coordinates between them. The difference is in the direction of dependencies and the relationship between the coordinated objects.
