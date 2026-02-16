---
name: patterns
description: >-
  Apply design patterns appropriately. Activate when code has recurring problems
  (creation, behavior variation, structural composition), when discussing pattern
  choice, or when reviewing pattern implementations. Patterns solve specific
  problems — activate when the problem is clear and a pattern can simplify.
model: opus
allowed-tools: Read, Grep, Glob
delegates-to: naming, solid, functions, architecture
argument-hint: [code or problem to solve]
---

# Patterns Skill

Design patterns are named solutions to recurring design problems. They represent chunks of design experience communicable efficiently. This skill focuses on the decision framework — when to apply which pattern — not a catalog of all 23 GOF patterns.

**Core Truth:** Patterns should emerge from need, not be applied preemptively. Simple code that solves the problem is always better than an over-engineered pattern. When you have a hammer, everything looks like a nail.

---

## Step 0: Detect Context

Patterns manifest differently in PHP and TypeScript. Before recommending a pattern, identify:

- **PHP:** OOP paradigm, static type system, dependency injection patterns, plain class hierarchies
- **TypeScript:** Static type system, classes and functions, modules for DI, composition and interfaces
- **Built-in abstractions:** Does the language provide this as a feature?

**PHP and TypeScript Equivalents:**

| Pattern | PHP Equivalent | TypeScript Equivalent | Notes |
|---------|---|---|---|
| Strategy | Interface binding, factory functions | Class composition, strategy pattern | Multiple algorithm families |
| Observer | Observer interface pattern | Classes with subscription methods | Decouple state changes from handlers |
| Factory | Factory classes, static methods | Factory functions, classes | Isolate type creation |
| Decorator | Decorator classes, composition | Decorator classes, wrapper functions | Add behavior dynamically |
| Null Object | Null-safe operators, optional values | Optional chaining, default values | Eliminate null checks |
| Facade | Facade classes | Facade classes, module exports | Hide complexity behind clean interface |
| State | State machine classes | State classes, enums | Manage transitions explicitly |

---

## Step 1: Generate Context-Specific Rules

Map GOF pattern names to the stack's idioms. A pattern in Python decorators is not an OOP Decorator pattern—it's language-native decoration. A pattern in Go is often implicit (interfaces are structural, not nominal).

**Rule:** Always ask: "Does the language or framework already provide this abstraction?"

If yes, use the language feature. If no, implement the pattern as an idiom for your stack.

---

## Step 2: Apply Decision Rules

NOT a catalog of patterns. Instead, decision rules: **"When you see this problem, consider this pattern."**

### Problem → Pattern Mapping

**OBJECT CREATION PROBLEMS:**

| What's the problem? | Pattern to consider | Why? |
|-------------------|-------------------|------|
| Concrete types leak into business logic | Factory / Abstract Factory | Isolate type dependency to a boundary |
| Construction is complex, multi-step | Builder | Separate construction logic from the object |
| Need exactly one instance, globally | Singleton (cautiously) or Monostate | Ensure single instance; DI usually better |
| Need copies with state variation | Prototype | Registry of templates, clone on demand |

**BEHAVIOR VARIATION PROBLEMS:**

| What's the problem? | Pattern to consider | Why? |
|-------------------|-------------------|------|
| Type-based conditional (`if type == X then Y`) | Strategy / Polymorphism | External polymorphism; family of algorithms |
| Complex state machine, many transitions | State | Each state is a class; transitions are clear |
| Same algorithm, different implementations | Template Method | Inheritance-based; fix at compile time |
| Decouple "what to do" from "who/when" | Command | Encapsulate request as object; enables undo, queuing, audit |
| Multiple objects need to change together | Observer | Notify dependents of state change automatically |
| Need to traverse without exposing structure | Visitor / Iterator | Add operations from outside; lazy evaluation |

**COMPOSITION & STRUCTURAL PROBLEMS:**

| What's the problem? | Pattern to consider | Why? |
|-------------------|-------------------|------|
| M type abstractions × N implementations = MxN classes | Bridge | Separate abstraction from implementation; M+N classes |
| Incompatible interface needs wrapping | Adapter | Bridge the interface gap; object or class adapter |
| Tree structure, uniform leaf/branch treatment | Composite | Recursive composition; same operations on all nodes |
| Add behavior dynamically without subclassing | Decorator | Stack behavior; per-instance, not class-wide |
| Complex subsystem needs simplified interface | Facade | Impose policy from above; reduce coupling to subsystem |
| Share fine-grained objects efficiently | Flyweight | Separate intrinsic (shared) from extrinsic (context) state |
| Control access or cross boundary | Proxy | Lazy loading, remote access, access control |

**SPECIAL PROBLEMS:**

| What's the problem? | Pattern to consider | Why? |
|-------------------|-------------------|------|
| Null checks everywhere | Null Object | Provide object with neutral behavior |
| Need to restore previous state | Memento | Capture state without breaking encapsulation |
| Request should pass through handlers | Chain of Responsibility | Each handler decides: process or pass |
| Avoid cascading changes | Mediator | Coordinate peers without direct coupling |
| DSL or language definition | Interpreter | Grammar production → builder method |

### When NOT to Apply Patterns

**Pattern application is a smell if:**

1. **The code is already simple** — if no pattern needed, don't add one
2. **Premature abstraction** — you've only seen one variant, you predict three; wait for actual need
3. **Team doesn't know the pattern** — the cost of explanation/maintenance outweighs benefit
4. **The framework already provides it** — use the framework abstraction, not your own
5. **Fewer than 2-3 variants exist** — pattern overhead only pays off with meaningful variation
6. **The pattern adds more code than it removes** — measure the coupling benefit vs. complexity cost

---

## Step 3: Review Checklist

For each potential pattern application, verify:

| Question | Red Flag | Remedy |
|----------|----------|--------|
| **Justified?** Is there an actual, recurring problem this solves? | "I might need multiple implementations someday" without evidence | Wait for actual variation; apply pattern only after 2-3 variants exist |
| **Natural fit?** Does the pattern simplify the code or add indirection? | More classes, more files, more indirection than the original conditional | Simple if/switch may be clearer; complexity should decrease |
| **Correct?** Does implementation follow the pattern's intent, not just structure? | Implements the class structure but violates key intent | Review pattern rules; fix intent violations |
| **Complete?** Are edge cases handled? | Thread safety gaps, deregistration memory leaks, missing default handlers | Add defensive code: thread checks, cleanup, defaults |
| **Named well?** Do class/interface names communicate the pattern's role? | `DataProcessor`, `Manager`, `Helper` — naming hides intent | Names should hint at pattern role: `SortStrategy`, `TurnstileState` |

---

## Step 4: Refactoring Patterns

Named refactorings to apply when patterns are needed:

### Replace Conditional with Strategy

**PHP Example:**
```php
// Before: Switch on payment method
class PaymentProcessor {
    public function process(Order $order, string $method): Receipt {
        if ($method === 'stripe') {
            return $this->processStripe($order->total());
        } elseif ($method === 'paypal') {
            return $this->processPayPal($order->total());
        }
    }
}

// After: Strategy via interface
interface PaymentGateway {
    public function charge(Money $amount): Receipt;
}

class PaymentProcessor {
    public function __construct(private PaymentGateway $gateway) {}
    public function process(Order $order): Receipt {
        return $this->gateway->charge($order->total());
    }
}
```

TypeScript: Same pattern with `interface` and dependency injection through constructor.

**When:** Type-based conditionals with multiple branches. Each branch is an algorithm variant.

### Extract Factory

**PHP Example:**
```php
// Before: Type creation scattered throughout
// After: Factory interface isolates creation
interface EmployeeFactory {
    public function createHourly(string $name): Employee;
    public function createSalaried(string $name): Employee;
}

class PayrollService {
    public function __construct(private EmployeeFactory $factory) {}
    public function create(string $type, string $name): Employee {
        return match($type) {
            'hourly' => $this->factory->createHourly($name),
            'salaried' => $this->factory->createSalaried($name),
        };
    }
}
```

TypeScript: Same pattern with factory methods in a class; inject as dependency.

**When:** Concrete type creation scattered throughout codebase; isolate to factory boundary.

### Introduce Null Object

**PHP Example:**
```php
// Before: Null checks everywhere
class PayrollService {
    public function calculatePaycheck(?Employee $employee): Money {
        if ($employee !== null) {
            return $employee->calculatePay();
        }
        return Money::zero();
    }
}

// After: Null Object pattern
abstract class Employee {
    abstract public function calculatePay(): Money;
}

class NullEmployee extends Employee {
    public function calculatePay(): Money { return Money::zero(); }
}

class PayrollService {
    public function calculatePaycheck(Employee $employee): Money {
        return $employee->calculatePay();  // Always safe
    }
}
```

TypeScript: Same pattern using abstract class or interface with concrete null implementation.

**When:** Repeated null checks throughout codebase; enable Tell Don't Ask pattern.

### Simplify with Facade

**PHP Example:**
```php
// Before: Complex setup scattered
// After: Facade hides complexity
class ReportFacade {
    public function __construct(
        private DataService $data,
        private FormatterService $formatter,
        private ValidationService $validator,
        private ExportService $exporter
    ) {}

    public function generate(string $type): Report {
        $data = $this->data->fetch();
        $this->validator->validate($data);
        $formatted = $this->formatter->format($data);
        return $this->exporter->export($formatted);
    }
}

// Client code: simple interface
class ReportService {
    public function __construct(private ReportFacade $facade) {}
    public function show(): Report {
        return $this->facade->generate('pdf');
    }
}
```

TypeScript: Same pattern; use a class with public methods hiding subsystem details.

**When:** Complex subsystem; clients need simplified, stable interface.

### Compose with Decorator

**PHP Example:**
```php
// Before: Inheritance explosion (LoggingModem + RetryModem = ??)
// After: Composition via decorator
abstract class ModemDecorator implements Modem {
    public function __construct(protected Modem $modem) {}
}

class LoggingModemDecorator extends ModemDecorator {
    public function send(string $data): void {
        echo "Sending: $data";
        $this->modem->send($data);
    }
}

// Compose at runtime: stack behaviors
$modem = new LoggingModemDecorator(new BaseModem());
```

TypeScript: Same pattern; decorate wraps and delegates to inner component.

**When:** Multiple optional behaviors; avoid inheritance explosion, favor composition.

---

## K-Line History

Tracks decisions for pattern application. Log entries should note:
- What problem you identified
- Which pattern you chose
- Key implementation decision (composition vs inheritance, etc.)

**Example entries:**
- "Type-based conditionals in `PaymentProcessor`. Applied Strategy with interface. Tests for swapping strategies at runtime."
- "Rejected Decorator; used framework middleware instead. Team unfamiliar with pattern."
- "State transitions in `Turnstile`. Applied State pattern; each state is a class."

---

## Communication Style

When recommending or reviewing patterns:

- **Show the problem first** — "I see type-based conditionals here; this suggests a pattern."
- **Name the pattern** — Be explicit: "This would be Strategy."
- **Explain the fit** — Why this pattern for this problem (not just its definition).
- **Identify the tradeoff** — What becomes easier? What becomes harder?
- **Flag the cost** — Extra classes, extra files, extra indirection; is it worth it?

---

## Related Skills

- `/naming` — Pattern classes must have clear, intent-revealing names
- `/functions` — Pattern methods must follow function principles (small, focused, pure)
- `/solid` — Patterns implement SOLID (Factory implements DIP, Strategy implements OCP)
- `/architecture` — Patterns at module/component boundaries (where they live matters)
- `/clean-code-review` — Comprehensive review including pattern usage appropriateness
