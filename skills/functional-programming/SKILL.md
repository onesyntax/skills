---
name: functional-programming
description: >-
  Guide applying functional programming principles from Uncle Bob's teachings. Activate
  when working with pure functions, immutability, higher-order functions, functional
  composition, or when the user mentions FP, pure functions, immutability, map/filter/reduce,
  side effects, or functional architecture. FP is the oldest paradigm and the key to
  safe concurrency — it eliminates shared mutable state by design.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [code or module to analyze]
---

# Functional Programming Skill

Functional programming is the discipline of building software through pure functions, immutable data, and function composition. It is not a new fad — lambda calculus (Alonzo Church, 1936) predates the Turing machine. FP is the oldest computational paradigm, yet it solves the most modern problem: safe concurrency.

For category theory foundations (categories, monoids, functors), extended architecture examples, read `references/extended-examples.md`.

**OO and FP are NOT mutually exclusive. They are COMPLEMENTARY.** OO manages dependencies between modules (through polymorphism and dependency inversion). FP manages state and side effects (through immutability and pure functions). Both are needed for well-designed systems.

---

## Core Philosophy

### The Data Flow Model

**Procedural thinking:** Control flow — sequences of instructions, jumps, branches, loops. You think about WHAT THE COMPUTER DOES step by step.

**Functional thinking:** Data flow — data enters a pipeline of transformations, each function takes input and produces output. You think about WHAT THE DATA BECOMES.

```
Input --> [Transform A] --> [Transform B] --> [Transform C] --> Output
```

No variables are mutated along the way. Each transformation creates new data from old data.

### Why FP Matters Now: Concurrency

Hardware stopped getting faster per core around 2005. Instead, it adds MORE cores. Software must exploit multiple cores. Shared mutable state is the root cause of concurrency bugs — race conditions, deadlocks, concurrent update problems, non-deterministic behavior.

FP eliminates this entire class of bugs by design. No variables changing state means no race conditions. No race conditions means no deadlocks, no concurrent update problems.

---

## Pure Functions and Referential Transparency

### What Makes a Function Pure

A pure function has two properties:

1. **Given the same inputs, it always returns the same output** — no dependence on external state
2. **It produces no side effects** — no modification of external state

```
// PURE: Same input always gives same output, no side effects
add(a, b): return a + b

// IMPURE: Depends on and modifies external state
addToCounter(a):
    counter += a         // Modifies external state!
    return counter       // Return value depends on external state!
```

### Referential Transparency

Referential transparency means you can replace any name with its value without changing the program's behavior. Every name binding is simply a shorthand for a value. When a function modifies a global variable, it breaks referential transparency — the name no longer stands for a fixed value but for "whatever this happens to be right now."

### Side Effects: Harmful vs Beneficial

**Harmful:** Those that mutate state affecting future computations — modifying a global variable, changing a shared data structure, writing to a file other functions read. These create hidden temporal dependencies.

**Beneficial:** Output — displaying results, writing a network response, printing a report. These are the REASON the program exists.

The goal is not to eliminate ALL side effects (that makes programs useless). The goal is to **isolate** side effects at the boundaries and keep the core logic pure. This is the "functional core, imperative shell" pattern.

### Hidden Dependencies

```
// DANGEROUS: Hidden dependency through global state
totalPrice = 0

addItem(item):
    totalPrice += item.price       // Hidden mutation

applyDiscount(rate):
    totalPrice *= (1 - rate)       // Depends on addItem being called first!
```

Call order matters but nothing makes this explicit. In FP, dependencies are explicit through function arguments:

```
// SAFE: Dependencies are explicit
addItem(currentTotal, item): return currentTotal + item.price
applyDiscount(total, rate): return total * (1 - rate)
```

---

## Immutability and State Management

### No Assignment Statements

In pure FP, variables are bound once and never reassigned:

```
circle = {radius: 5, color: "red"}
biggerCircle = circle.with(radius: 10)
// circle is unchanged! biggerCircle is a new map
```

Need "new" state? Create a new data structure derived from the old one. The old data structure remains unchanged.

### Persistent Data Structures

FP uses **persistent data structures** that preserve previous versions through structural sharing:

```
Original list:  [A] -> [B] -> [C] -> [D]

"Add" E to front:
New list:       [E] -> [A] -> [B] -> [C] -> [D]
Original list:         [A] -> [B] -> [C] -> [D]  (unchanged, shared)
```

Not copying — structural sharing. The "new" list reuses the old list's memory. This makes immutability practical even for large data structures.

### The Update-Draw Loop

For interactive applications without mutable state:

```
1. Setup: Create initial state (a map/dictionary)
2. Update: Take current state + events, produce NEW state (pure function)
3. Draw: Render the new state (side effect, isolated)
4. New state passed back to update, cycle repeats
```

```
setup():
    return {x: 100, y: 100, dx: 2, dy: 3, score: 0}

updateState(state, events):          // PURE — business logic
    newState = state
    for event in events:
        newState = applyEvent(newState, event)
    return checkBoundaries(newState)

draw(state):                          // SIDE EFFECT — presentation
    clearScreen()
    drawPlayer(state.x, state.y)
    drawScore(state.score)
```

Update is trivially testable (pure). Draw is tested by visual inspection. Business logic and presentation are cleanly separated — SRP at the architectural level.

### Atoms for Controlled Mutation

When shared mutable state is absolutely necessary (communicating between threads), use **atoms** — controlled, disciplined mutation with atomic Compare-And-Swap:

```
counter = atom(0)

read(counter)           // => 0
swap(counter, inc)      // atomically: counter is now 1
swap(counter, add, 10)  // atomically: counter is now 11
```

If two threads swap simultaneously, one retries automatically. Atoms make mutation explicit, visible, and safe.

---

## Higher-Order Functions: Map, Filter, Reduce

### Map

Apply a function to each element, return a new collection:

```
map(inc, [1, 2, 3, 4, 5])           // => [2, 3, 4, 5, 6]
map(square, [1, 2, 3, 4, 5])        // => [1, 4, 9, 16, 25]

// Replaces:
results = []
for n in numbers:
    results.add(n * n)
// With:
results = map(square, numbers)
```

### Filter

Keep elements where a predicate is true:

```
filter(isEven, [1, 2, 3, 4, 5, 6])       // => [2, 4, 6]
filter(greaterThan(3), [1, 2, 3, 4, 5])   // => [4, 5]
```

### Reduce (Fold)

Accumulate a result by applying a binary function repeatedly:

```
reduce(add, 0, [1, 2, 3, 4, 5])     // => 15
// Steps: add(0,1)=1, add(1,2)=3, add(3,3)=6, add(6,4)=10, add(10,5)=15
```

Reduce is the most general — you can implement map and filter in terms of reduce.

### Composing Pipelines

Real-world functional code chains these operations:

```
// "Sum salaries of active employees earning over 50k"
employees
    |> filter(e -> e.status == ACTIVE)
    |> map(e -> e.salary)
    |> filter(s -> s > 50000)
    |> reduce(add, 0)
```

Each step is a pure transformation. The pipeline reads like a description of what you want, not how to get it.

---

## Sequence, Selection, Iteration in FP

### Sequence

Achieved through **dependent function calls** — function B depends on function A's output:

```
rawData   = readInput()
parsed    = parse(rawData)
validated = validate(parsed)
result    = process(validated)
```

### Selection

If/cond expressions **return values** rather than jumping to code blocks:

```
status = cond:
    score > 90: "excellent"
    score > 70: "good"
    score > 50: "average"
    else:       "poor"
```

Selection is an expression, not a statement. It produces a value that flows into the next transformation.

### Iteration

FP has **no loops**. Iteration is achieved through **recursion** or higher-order functions:

```
// Recursive factorial
factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

// Tail-recursive (compiler reuses stack frame)
factorial(n):
    loop(i = n, acc = 1):
        if i <= 1: return acc
        recur(i - 1, acc * i)
```

In practice, most iteration uses map/filter/reduce. Explicit recursion is reserved for cases where higher-order functions don't fit.

---

## Functional SOLID Principles

### SRP in FP

Separate business logic (pure functions) from presentation (side-effecting functions). The Update-Draw Loop is SRP at the architectural level. Each function serves one actor.

### OCP in FP

Three dispatch mechanisms, from worst to best:

**1. Switch dispatch** — adding a new type requires modifying existing code (violates OCP):

```
area(shape):
    switch shape.type:
        CIRCLE: return PI * shape.radius^2
        RECTANGLE: return shape.width * shape.height
    // Adding TRIANGLE requires modifying this function
```

**2. Dictionary dispatch** — extend without modifying:

```
areaFns = {
    CIRCLE: (s) -> PI * s.radius^2,
    RECTANGLE: (s) -> s.width * s.height
}
area(shape): return areaFns[shape.type](shape)

// Extend without modifying existing code:
areaFns[TRIANGLE] = (s) -> 0.5 * s.base * s.height
```

**3. Protocol dispatch (BEST)** — new types implement existing protocols:

```
protocol Shape:
    area()
    perimeter()

record Circle(radius) implements Shape:
    area(): return PI * radius^2
    perimeter(): return 2 * PI * radius

// Adding Triangle requires NO modification of existing code
record Triangle(base, height, sideA, sideB) implements Shape:
    area(): return 0.5 * base * height
    perimeter(): return base + sideA + sideB
```

### LSP in FP

MORE important in dynamic languages because there's no compiler safety net. Every protocol implementation MUST implement all methods meaningfully. A Triangle that throws "not implemented" for `perimeter` is an LSP violation.

### ISP in FP

Split fat protocols into focused ones:

```
// FAT — violates ISP
protocol Shape: area(), perimeter(), draw(canvas), serialize(format)

// SEGREGATED
protocol Measurable: area(), perimeter()
protocol Drawable:   draw(canvas)
protocol Serializable: serialize(format)
```

### DIP in FP

Achieved through protocols — high-level logic depends on protocol abstractions, not concrete implementations:

```
protocol PaymentGateway:
    charge(amount)
    refund(transactionId)

// High-level business logic depends on abstraction
processOrder(gateway: PaymentGateway, order):
    total = calculateTotal(order)
    gateway.charge(total)

// Low-level detail implements protocol
record StripeGateway(apiKey) implements PaymentGateway:
    charge(amount): stripe.charge(apiKey, amount)
```

---

## Composition

Composition is the recursive act of building large things from small things — the heart of FP:

```
// Small functions
double(x): return 2 * x
increment(x): return x + 1

// Compose into larger function
doubleThenIncrement = compose(increment, double)
doubleThenIncrement(5)    // => 11

// Compose into pipeline
process(data):
    data |> map(parseRecord)
         |> filter(isValid)
         |> map(transform)
         |> reduce(mergeResults, {})
```

Each small function is independently testable, understandable, and reusable.

---

## Functional Architecture Patterns

### Event Sourcing

FP naturally supports event sourcing — state is built from a sequence of immutable events:

```
events = [
    {type: ACCOUNT_CREATED, id: 1, name: "Alice"},
    {type: DEPOSIT, id: 1, amount: 100},
    {type: WITHDRAWAL, id: 1, amount: 30}
]

applyEvent(state, event):          // Pure function
    switch event.type:
        ACCOUNT_CREATED: return state.with(name: event.name, balance: 0)
        DEPOSIT: return state.with(balance: state.balance + event.amount)
        WITHDRAWAL: return state.with(balance: state.balance - event.amount)

currentState = reduce(applyEvent, {}, events)
// => {name: "Alice", balance: 70}
```

The event log is the source of truth. Current state is derived. Replay events to recreate any historical state.

### CQRS

Aligns naturally with FP: **Commands** produce events (side effects at boundaries). **Queries** are pure functions that derive views from event history.

### Middleware as Composition

The middleware pattern is function composition — each middleware wraps the next handler:

```
wrapLogging(handler):
    return (request) ->
        log("Request:", request.uri)
        response = handler(request)
        log("Response:", response.status)
        return response

wrapAuth(handler):
    return (request) ->
        if not authenticated(request): return {status: 401}
        return handler(request)

app = compose(wrapLogging, wrapAuth, handler)
```

### Functional Web Architecture

Websites are intrinsically functional: `HTTP Request --> [Function] --> HTTP Response`. A request comes in, a function processes it, a response goes out. In Clean Architecture terms: routes define interface adapters, each handler delegates to an interactor (pure business logic), side effects live at the boundaries.

---

## Testing in FP

### TDD Works the Same Way

The red-green-refactor cycle is identical in FP:

```
// RED: Write failing test
test "update score increments":
    state = {score: 0}
    result = updateState(state, {type: SCORE})
    assert result.score == 1
// FAIL: updateState not defined

// GREEN: Minimum code
updateState(state, event):
    if event.type == SCORE: return state.with(score: state.score + 1)
    return state
// PASS

// REFACTOR: (already clean)
```

### Coverage Strategy

- **Business rules / game logic**: Near-100% coverage (pure functions — trivially testable)
- **UI / rendering**: Eyeball tests (visual inspection)
- **Side effects at boundaries**: Integration tests

Pure functions need no mocking. Give them input, check the output.

### TDD Is Never Enough Alone

TDD requires algorithmic insight. Ron Jeffries attempted to solve Sudoku using pure TDD without understanding the algorithm — after many blog posts, he never solved it. Peter Norvig wrote a concise solver because he understood constraint propagation + backtracking search.

TDD is the inner development loop. Thinking is the outer development loop. You need both.

---

## When Reviewing FP Code

1. **Mutable state:** Variables reassigned? Shared state across functions? In-place mutation (push, splice, sort)?
2. **Impure functions:** Return value depends on something other than arguments? Void return type?
3. **Composition opportunities:** Imperative loops that could be map/filter/reduce? Nested conditionals that could be pipeline stages?
4. **Side effect isolation:** Are side effects at the boundaries? Is business logic free of I/O? Functional core, imperative shell?
5. **Functional SOLID:** Protocols used for extension? Fat protocols that need segregation? High-level logic depending on concretions?

---

## Common Pitfalls

- **Impure core**: Business logic mixed with I/O (database calls inside calculation functions)
- **Mutation hiding**: Reassigning "variables" that should be bindings
- **Over-abstraction**: Unnecessary monadic wrappers when simple functions suffice
- **Ignoring the imperative shell**: Trying to eliminate ALL side effects instead of isolating them
- **FP dogmatism**: Rejecting OO patterns that genuinely help (protocols, interfaces, polymorphism)
- **Neglecting TDD**: Thinking pure functions don't need tests because they're "obviously correct"
- **Complex recursion**: Using explicit recursion where map/filter/reduce would be clearer

---

## Related Skills

- `/solid` — SOLID principles apply to FP through protocols and modules
- `/tdd` — TDD works identically in FP
- `/architecture` — Clean Architecture with functional implementation
- `/patterns` — Functional patterns complement OO patterns
- `/clean-code-review` — Review functional code quality
