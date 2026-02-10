---
name: functional-programming
description: >-
  Guide applying functional programming principles from Uncle Bob's teachings. Activates
  when working with pure functions, immutability, higher-order functions, functional
  composition, or when the user mentions functional programming, FP, pure functions,
  immutability, map/filter/reduce, side effects, or functional architecture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [code or module to analyze]
---

# Functional Programming Workflow

Apply Uncle Bob's functional programming principles to analyze code, identify impure constructs, and refactor toward pure, composable, immutable designs. Follow these workflow steps when working with functional code or refactoring imperative code toward a functional style. Based on Uncle Bob's Clean Code video series Episodes 53-61.

## Workflow Steps

1. **Identify mutable state and side effects** - Find variables that change, state that is shared, and functions with hidden dependencies
2. **Extract pure functions from impure code** - Separate calculation from action, isolate side effects at the boundaries
3. **Apply map/filter/reduce patterns** - Replace imperative loops with declarative transformations
4. **Manage state through immutable transformations** - Create new data structures instead of mutating existing ones
5. **Apply functional SOLID principles** - Use protocols, modules, and composition to achieve SOLID in FP
6. **Test with TDD** - TDD works the same in FP; red-green-refactor cycle is unchanged
7. **Apply /professional standards** - Follow professional quality standards

---

## Core Philosophy

### FP Origins

Functional programming is not a new fad. It is the OLDEST computational paradigm:

- **Lambda calculus** was invented by Alonzo Church in **1936** - BEFORE Alan Turing's machine
- The **Church-Turing thesis** proved lambda calculus is equivalent in power to the Turing machine
- Every computation expressible in one is expressible in the other
- Turing was Church's doctoral student; he knew about lambda calculus before building his model
- FP languages (LISP, 1958) predate structured programming, OO, and most paradigms we consider mainstream

Uncle Bob calls FP the "dark matter" of programming - it has always been there, always been powerful, but invisible to the mainstream for decades. It is not something new to learn; it is something old to finally embrace.

### The Data Flow Model

The mental model for FP is fundamentally different from procedural programming:

**Procedural thinking:** Control flow - sequences of instructions, jumps, branches, loops. You think about WHAT THE COMPUTER DOES step by step.

**Functional thinking:** Data flow - data enters a pipeline of transformations, each function takes input and produces output. You think about WHAT THE DATA BECOMES.

```
Input --> [Transform A] --> [Transform B] --> [Transform C] --> Output
```

No variables are mutated along the way. Each transformation creates new data from old data. The pipeline is a composition of pure functions.

### Why FP Matters Now

The critical reason FP matters today is **CONCURRENCY**.

- Hardware stopped getting faster per core around 2005
- Instead, hardware adds MORE cores (2, 4, 8, 16, 64, 128...)
- Software must exploit multiple cores to improve performance
- Shared mutable state is the root cause of concurrency bugs

The concurrency problem reduces to this: **multiple threads accessing and modifying the same variables**. This causes:
- Race conditions
- Deadlocks
- Concurrent update problems
- Non-deterministic behavior

FP eliminates this entire class of bugs by design. If there are no variables changing state, there are no race conditions. If there are no race conditions, there are no deadlocks, no concurrent update problems.

> As hardware moves toward more cores rather than faster cores, safe shared state becomes the central problem of software development. FP eliminates this class of bugs by design.

---

## Pure Functions and Referential Transparency

### What Makes a Function Pure

A pure function has two properties:

1. **Given the same inputs, it always returns the same output** - no dependence on external state
2. **It produces no side effects** - no modification of external state

```java
// PURE: Same input always gives same output, no side effects
int add(int a, int b) {
    return a + b;
}

// IMPURE: Depends on external state
int addToCounter(int a) {
    counter += a;     // Modifies external state!
    return counter;   // Return value depends on external state!
}
```

### Referential Transparency

**Referential transparency** means you can replace any name with its value without changing the program's behavior.

```clojure
;; Referentially transparent
(def x 5)
(def y (+ x 3))     ;; y = 8
;; Replace x with its value:
(def y (+ 5 3))     ;; y = 8 -- same result
```

Every name binding is simply a shorthand for a value. The name IS the value. You can substitute freely.

When a function modifies a global variable, it breaks referential transparency. The name no longer stands for a fixed value - it stands for "whatever this happens to be right now," which depends on call order, timing, and hidden state.

### Harmful vs Beneficial Side Effects

Not all side effects are equal:

**Harmful side effects**: Those that mutate state affecting future computations
- Modifying a global variable
- Changing a shared data structure
- Writing to a file that other functions read
- These create hidden temporal dependencies between functions

**Beneficial side effects**: Output - the purpose of the program
- Displaying results to a screen
- Writing a response to a network socket
- Printing a report
- These are the REASON the program exists

The goal is not to eliminate ALL side effects (that would make programs useless). The goal is to **isolate** side effects at the boundaries and keep the core logic pure.

### Hidden Dependencies

A function that changes a global variable creates hidden dependencies:

```java
// DANGEROUS: Hidden dependency through global state
int totalPrice = 0;

void addItem(Item item) {
    totalPrice += item.getPrice();  // Hidden mutation
}

void applyDiscount(double rate) {
    totalPrice *= (1 - rate);  // Depends on addItem being called first!
}
```

The call order matters. `applyDiscount` depends on `addItem` having been called, but nothing in the code makes this explicit. In FP, dependencies are explicit through function arguments.

---

## Immutability and State Management

### No Assignment Statements

In pure FP, there are no assignment statements. Variables are bound once and never reassigned:

```clojure
;; This is a binding, not an assignment
(def pi 3.14159)

;; You cannot do this:
;; (set! pi 3.0)  -- ILLEGAL in pure FP

;; Need "new" state? Create a new data structure
(def circle {:radius 5 :color :red})
(def bigger-circle (assoc circle :radius 10))
;; circle is unchanged! bigger-circle is a new map
```

Need "new" state? Create a new data structure derived from the old one. The old data structure remains unchanged. This is the fundamental discipline of immutability.

### Persistent Data Structures

FP languages use **persistent data structures** - data structures that preserve their previous versions when modified. Creating a "new" version shares most of the structure with the old version, making it efficient.

```
Original list:  [A] -> [B] -> [C] -> [D]

"Add" E to front:
New list:       [E] -> [A] -> [B] -> [C] -> [D]
Original list:         [A] -> [B] -> [C] -> [D]  (unchanged, shared)
```

This is not copying - it is structural sharing. The "new" list reuses the old list's memory. This makes immutability practical even for large data structures.

### The Update-Draw Loop Pattern

For interactive applications without mutable state, Uncle Bob describes this pattern:

```
1. Setup: Create initial state (a map/dictionary)
2. Update: Take current state, produce NEW state (never mutating old)
3. Draw: Render the new state
4. New state passed back to update, cycle repeats
```

```clojure
(defn setup []
  {:x 100 :y 100 :dx 2 :dy 3 :score 0})

(defn update-state [state]
  ;; Returns a NEW state map - never mutates the input
  (-> state
      (update :x + (:dx state))
      (update :y + (:dy state))
      (check-boundaries)
      (update-score)))

(defn draw [state]
  ;; Pure rendering - reads state, produces pixels
  (clear-screen)
  (draw-player (:x state) (:y state))
  (draw-score (:score state)))

;; The game loop
(defn game-loop [state]
  (draw state)
  (recur (update-state state)))
```

This pattern forces clean separation:
- **Business logic** lives in `update` (pure function)
- **Presentation** lives in `draw` (side effect, isolated)
- They communicate through an **immutable state data structure**

The update function is trivially testable because it is pure. The draw function is tested by visual inspection (eyeball tests). This separation mirrors SRP at the architectural level.

### Atoms for Controlled Mutation

When shared mutable state is absolutely necessary (communicating between threads, for example), FP uses **atoms** - controlled, disciplined mutation:

```clojure
;; Create an atom holding a value
(def counter (atom 0))

;; Read the value
@counter  ;; => 0

;; Swap atomically: takes a function, applies to current value,
;; atomically replaces with result
(swap! counter inc)    ;; counter is now 1
(swap! counter + 10)   ;; counter is now 11
```

The swap operation is **atomic** - it guarantees that no other thread can see the value in a half-updated state. If two threads swap simultaneously, one will retry automatically. This is Compare-And-Swap (CAS) under the hood.

Atoms are the disciplined, controlled way to handle necessary mutation. They make mutation explicit, visible, and safe.

---

## Higher-Order Functions: Map, Filter, Reduce

### Map

Map takes a function and a list, applies the function to each element, and returns a new list:

```clojure
(map inc [1 2 3 4 5])
;; => (2 3 4 5 6)

(map #(* % %) [1 2 3 4 5])
;; => (1 4 9 16 25)
```

```java
// Java equivalent
List<Integer> squares = numbers.stream()
    .map(n -> n * n)
    .collect(Collectors.toList());
```

Map replaces the pattern:
```java
// BEFORE: Imperative loop
List<Integer> results = new ArrayList<>();
for (int n : numbers) {
    results.add(n * n);
}

// AFTER: Declarative map
List<Integer> results = numbers.stream().map(n -> n * n).toList();
```

### Filter

Filter takes a predicate and a list, returns elements where the predicate is true:

```clojure
(filter even? [1 2 3 4 5 6])
;; => (2 4 6)

(filter #(> % 3) [1 2 3 4 5 6])
;; => (4 5 6)
```

```java
List<Integer> evens = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());
```

### Reduce (Fold)

Reduce takes a binary function, an optional initial value, and a list. It applies the function repeatedly, accumulating a result:

```clojure
(reduce + [1 2 3 4 5])
;; => 15
;; Steps: (+ 1 2) => 3, (+ 3 3) => 6, (+ 6 4) => 10, (+ 10 5) => 15

(reduce + 0 [1 2 3 4 5])
;; => 15 (with explicit initial value)
```

```java
int sum = numbers.stream()
    .reduce(0, Integer::sum);
```

Reduce is the most general of the three. You can implement map and filter in terms of reduce.

### The Threading Operator

Nested function calls read inside-out, which is hard to follow:

```clojure
;; Hard to read: inside-out
(reduce + (filter even? (map inc [1 2 3 4 5])))

;; Easy to read: left-to-right pipeline
(->> [1 2 3 4 5]
     (map inc)
     (filter even?)
     (reduce +))
;; => 12
```

The threading operator (`->>`) reads as a pipeline: start with the list, increment each element, keep even ones, sum them. This is the data flow model in action.

### Composing Pipelines

Real-world functional code is built by composing these operations:

```clojure
(->> employees
     (filter #(= :active (:status %)))
     (map :salary)
     (filter #(> % 50000))
     (reduce +))
;; "Sum salaries of active employees earning over 50k"
```

Each step is a pure transformation. The pipeline reads like a description of what you want, not how to get it.

---

## Sequence, Selection, Iteration in FP

### Sequence

In procedural code, sequence is achieved through statement ordering. In FP, sequence is achieved through **dependent function calls** - function B depends on function A's output:

```clojure
;; Sequence through data dependency
(let [raw-data   (read-input)
      parsed     (parse raw-data)
      validated  (validate parsed)
      result     (process validated)]
  result)
```

Each step depends on the previous step's output. The sequence is implicit in the data flow.

### Selection

In FP, if/cond expressions **return values** rather than jumping to code blocks:

```clojure
;; Selection returns a value
(def status
  (cond
    (> score 90) :excellent
    (> score 70) :good
    (> score 50) :average
    :else        :poor))
```

```java
// Java equivalent using ternary or switch expression
String status = score > 90 ? "excellent"
              : score > 70 ? "good"
              : score > 50 ? "average"
              : "poor";
```

Selection is an expression, not a statement. It produces a value that flows into the next transformation.

### Iteration

FP has **NO loops**. Iteration is achieved through **recursion**:

```clojure
;; Recursive factorial
(defn factorial [n]
  (if (<= n 1)
    1
    (* n (factorial (dec n)))))
```

**Tail-call optimization** prevents stack overflow for recursive functions:

```clojure
;; Tail-recursive factorial using recur
(defn factorial [n]
  (loop [i n acc 1]
    (if (<= i 1)
      acc
      (recur (dec i) (* acc i)))))
```

The `recur` form tells the compiler this is a tail call - it can reuse the current stack frame instead of creating a new one. This makes recursion as efficient as a loop.

In practice, most iteration in FP uses map/filter/reduce rather than explicit recursion. Explicit recursion is reserved for cases where these higher-order functions do not fit.

---

## Functional SOLID Principles

**OO and FP are NOT mutually exclusive. They are COMPLEMENTARY.**

Uncle Bob emphasizes this repeatedly. FP does not replace OO. FP and OO address different concerns:
- **OO** manages dependencies between modules (through polymorphism and dependency inversion)
- **FP** manages state and side effects (through immutability and pure functions)

Both are needed for well-designed systems. The SOLID principles apply to FP through protocols, modules, and composition.

### SRP in FP

The Single Responsibility Principle applies naturally in FP through the separation of concerns:

- **Separate game logic from UI code** (update vs draw in the Update-Draw Loop)
- **Business rules** in pure functions, **presentation** in side-effecting functions
- Communication through immutable state data structures

```clojure
;; SRP: update-state is pure business logic
(defn update-state [state event]
  (case (:type event)
    :move  (move-player state (:direction event))
    :score (update state :score inc)
    state))

;; SRP: render is presentation only
(defn render [state]
  (draw-world (:world state))
  (draw-player (:player state))
  (draw-hud (:score state)))
```

Each function serves one actor. Business logic changes do not affect rendering and vice versa.

### OCP in FP

The Open-Closed Principle is achieved through **protocols** (interfaces) for extension without modification:

Three dispatch mechanisms exist in FP:

**1. Switch/Cond dispatch:**
```clojure
(defn area [shape]
  (case (:type shape)
    :circle (* Math/PI (:radius shape) (:radius shape))
    :rectangle (* (:width shape) (:height shape))))
;; Adding :triangle requires modifying this function -- violates OCP
```

**2. Dictionary dispatch:**
```clojure
(def area-fns
  {:circle    (fn [s] (* Math/PI (:radius s) (:radius s)))
   :rectangle (fn [s] (* (:width s) (:height s)))})

(defn area [shape]
  ((get area-fns (:type shape)) shape))

;; Extend without modifying:
(def area-fns (assoc area-fns :triangle
  (fn [s] (* 0.5 (:base s) (:height s)))))
```

**3. Polymorphic dispatch via protocols (BEST):**
```clojure
(defprotocol Shape
  (area [this])
  (perimeter [this]))

(defrecord Circle [radius]
  Shape
  (area [_] (* Math/PI radius radius))
  (perimeter [_] (* 2 Math/PI radius)))

(defrecord Rectangle [width height]
  Shape
  (area [_] (* width height))
  (perimeter [_] (* 2 (+ width height))))

;; Adding Triangle requires NO modification of existing code
(defrecord Triangle [base height side-a side-b]
  Shape
  (area [_] (* 0.5 base height))
  (perimeter [_] (+ base side-a side-b)))
```

Protocols provide the best separation of concerns. New types are added by creating new records that implement existing protocols. No existing code is modified.

### LSP in FP

The Liskov Substitution Principle is MORE important in dynamic languages because there is no compiler safety net:

- Protocol methods that implementations do not implement are "latent open-closed violations"
- If a protocol defines `area` and `perimeter`, every implementation MUST implement both meaningfully
- A Triangle that throws "not implemented" for `perimeter` is an LSP violation

TDD catches many LSP violations but does not relieve the need for principled review. In dynamic languages, you must be especially disciplined about ensuring all protocol implementations fulfill the full contract.

### ISP in FP

The Interface Segregation Principle applies through splitting fat protocols into focused ones:

```clojure
;; FAT protocol -- violates ISP
(defprotocol Shape
  (area [this])
  (perimeter [this])
  (draw [this canvas])
  (serialize [this format]))

;; SEGREGATED protocols
(defprotocol Measurable
  (area [this])
  (perimeter [this]))

(defprotocol Drawable
  (draw [this canvas]))

(defprotocol Serializable
  (serialize [this format]))
```

In dynamic languages, the practical solution is often to implement all methods everywhere, but the conceptual separation still matters for dependency management and clarity.

### DIP in FP

The Dependency Inversion Principle is achieved through protocols:

```clojure
;; High-level policy depends on protocol abstraction
(defprotocol PaymentGateway
  (charge [this amount])
  (refund [this transaction-id]))

;; High-level business logic
(defn process-order [gateway order]
  (let [total (calculate-total order)]
    (charge gateway total)))

;; Low-level detail implements protocol
(defrecord StripeGateway [api-key]
  PaymentGateway
  (charge [_ amount] (stripe/charge api-key amount))
  (refund [_ tx-id] (stripe/refund api-key tx-id)))
```

High-level logic (`process-order`) depends on the protocol abstraction (`PaymentGateway`), not concrete implementations (`StripeGateway`). Dependencies point inward toward policy.

---

## Composition and Category Theory

### Composition: Building Large from Small

Composition is the recursive act of building large things from small things. This is the heart of FP:

```clojure
;; Small functions
(defn double [x] (* 2 x))
(defn increment [x] (+ 1 x))

;; Compose into larger function
(def double-then-increment (comp increment double))
(double-then-increment 5)  ;; => 11

;; Compose into pipeline
(defn process [data]
  (->> data
       (map parse-record)
       (filter valid?)
       (map transform)
       (reduce merge-results {})))
```

Each small function is independently testable, understandable, and reusable. Composition assembles them into complex behavior.

### Categories

A **category** in mathematics consists of:
- A set of values
- Closed single-argument functions (output type matches input type)
- An identity function (returns its argument unchanged)

```clojure
;; Category of integers with increment
;; Values: integers
;; Functions: inc, dec, double, etc. (int -> int)
;; Identity: identity (returns argument unchanged)

(map inc [1 2 3])       ;; Closed: int -> int
(map identity [1 2 3])  ;; Identity: int -> int
```

Categories support **map**. When you have a category (a set of values with closed functions), you can map any function over a collection of those values.

### Monoids

A **monoid** consists of:
- A set of values
- An associative binary function
- An identity element

```clojure
;; Monoid: integers with addition
;; Values: integers
;; Binary function: + (associative: (+ (+ a b) c) = (+ a (+ b c)))
;; Identity element: 0 (+ x 0) = x

(reduce + 0 [1 2 3 4 5])  ;; => 15

;; Monoid: strings with concatenation
;; Values: strings
;; Binary function: str (associative)
;; Identity element: "" (str x "") = x

(reduce str "" ["Hello" " " "World"])  ;; => "Hello World"
```

Monoids support **reduce**. When you have a monoid (values with an associative binary function and identity), you can reduce a collection using that function.

**Categories support map. Monoids support reduce. This is not coincidence - it is mathematical foundation.**

### Functors

A **functor** is a one-to-one correspondence between two categories that maps both values and operations:

```
Category A: {1, 2, 3}  with  inc
     |                         |
     | functor (toString)      | functor maps operation
     v                         v
Category B: {"1", "2", "3"} with  incrementString
```

A functor preserves structure. If you map a function over values in one category, the result corresponds to mapping the transformed function over transformed values in the other category.

This is the mathematical foundation for why `map` works consistently across different data types (lists, optionals, futures, streams). They are all functors.

---

## Testing in FP

### TDD Works the Same Way

TDD in FP follows the identical red-green-refactor cycle:

```clojure
;; RED: Write failing test
(deftest test-update-score
  (let [state {:score 0}]
    (is (= 1 (:score (update-state state {:type :score}))))))
;; FAIL: update-state not defined

;; GREEN: Minimum code to pass
(defn update-state [state event]
  (if (= :score (:type event))
    (update state :score inc)
    state))
;; PASS

;; REFACTOR: Clean up
;; (code is already clean in this case)
```

The cycle is the same. The tests are the same. The discipline is the same.

### Coverage Strategy

Uncle Bob's guidance for FP applications:

- **Game logic / Business rules**: Near-100% test coverage (these are pure functions - easy to test)
- **UI / Rendering**: Eyeball tests (visual inspection)
- **Side effects at boundaries**: Integration tests

Pure functions are trivially testable because they have no hidden dependencies. Give them input, check the output. No mocking needed for pure functions.

### Object Mother Pattern

For creating valid test data, use an Object Mother module:

```clojure
(ns test.mothers)

(defn make-player
  ([] (make-player {}))
  ([overrides]
   (merge {:x 100 :y 100 :health 100 :score 0} overrides)))

(defn make-enemy
  ([] (make-enemy {}))
  ([overrides]
   (merge {:x 200 :y 200 :health 50 :type :basic} overrides)))

;; Usage in tests
(deftest test-collision
  (let [player (make-player {:x 100 :y 100})
        enemy  (make-enemy {:x 100 :y 100})]
    (is (colliding? player enemy))))
```

The Object Mother creates valid default test data. Tests override only the fields relevant to what they are testing.

### TDD vs Static Typing

Uncle Bob's perspective: **TDD almost completely eliminates the need for static type checking.**

When you have comprehensive tests that cover every behavior, the type errors that a compiler catches are a subset of what your tests already catch. The tests provide more thorough coverage because they test BEHAVIOR, not just types.

This does not mean static types are useless - they provide documentation and IDE support. But the SAFETY argument for static types is largely addressed by TDD.

### TDD Is Never Enough Alone

TDD requires **algorithmic insight**. Uncle Bob references HDD - Hammock-Driven Development (Rich Hickey's talk):

- You must THINK about the problem before coding
- TDD helps you implement a solution incrementally
- TDD does NOT help you discover the right algorithm

**The Ron Jeffries vs Peter Norvig Sudoku story:** Ron Jeffries attempted to solve Sudoku using pure TDD without algorithmic insight. After many blog posts and much effort, he never solved it. Peter Norvig wrote a concise solver because he understood the algorithm (constraint propagation + backtracking search).

Lesson: TDD is the inner development loop. Thinking is the outer development loop. You need both.

### The TDD + Forethought Hybrid

The correct approach:
1. **Think first** (HDD) - understand the problem, consider algorithms
2. **Then TDD** to implement - let tests drive the incremental construction
3. Working through wrong solutions often leads to insights for right solutions

---

## The Update-Draw Loop In Depth

### Architecture of Interactive FP Applications

The Update-Draw Loop is the canonical architecture for interactive functional applications:

```
                    +----------+
                    |  Setup   | --> Initial State
                    +----------+
                         |
                         v
              +-------------------+
         +--->|   Update (pure)   |---+
         |    +-------------------+   |
         |            |               |
         |            v               |
         |    +-------------------+   |
         |    |   Draw (effects)  |   |
         |    +-------------------+   |
         |                            |
         +------- New State <---------+
```

**Setup**: Creates the initial state - a map/dictionary containing all game/application state.

**Update**: A pure function that takes the current state and produces a NEW state. It never mutates the old state. All business logic lives here.

**Draw**: A side-effecting function that reads the state and renders it. All presentation lives here.

**The cycle**: New state is passed back to update. The old state is discarded (or retained for undo/replay).

### Why This Architecture Works

1. **Testability**: Update is pure - test it by providing state and checking the result
2. **Reproducibility**: Same initial state + same sequence of events = same result, always
3. **Time travel**: Keep old states for undo, replay, debugging
4. **Concurrency safety**: State is immutable, so multiple readers are safe
5. **Separation of concerns**: Business logic and presentation are cleanly separated

---

## Functional Web Architecture

### Websites Are Intrinsically Functional

Uncle Bob observes that websites are intrinsically functional:

```
HTTP Request --> [Function] --> HTTP Response
```

A web request comes in, a function processes it, a response goes out. This is the purest form of functional computation applied to a real-world problem.

### The Clojure Web Stack

Uncle Bob describes the Clojure web stack as an example of functional web architecture:

- **HTTP Kit**: Low-level HTTP server
- **Ring**: Middleware abstraction (request map -> response map)
- **Compojure**: Routing DSL (maps URLs to handler functions)
- **Hiccup**: HTML generation from Clojure data structures

```clojure
;; Ring handler: request map -> response map (PURE FUNCTION)
(defn hello-handler [request]
  {:status 200
   :headers {"Content-Type" "text/html"}
   :body (html [:h1 "Hello, " (get-in request [:params :name])])})

;; Compojure routes
(defroutes app-routes
  (GET "/hello/:name" [] hello-handler)
  (GET "/users"       [] list-users-handler)
  (POST "/users"      [] create-user-handler))
```

### Routes Map to Interactors

In Clean Architecture terms:
- Routes define the **interface adapters** layer
- Each route handler delegates to an **interactor** (use case)
- Interactors contain **pure business logic**
- Side effects (database, external services) live at the boundaries

```clojure
;; Interactor: pure business logic
(defn calculate-order-total [order tax-rate]
  (let [subtotal (reduce + (map :price (:items order)))
        tax      (* subtotal tax-rate)]
    {:subtotal subtotal :tax tax :total (+ subtotal tax)}))

;; Handler: boundary code (thin, delegates to interactor)
(defn order-total-handler [request]
  (let [order    (parse-order (:body request))
        tax-rate (get-tax-rate (:region order))
        result   (calculate-order-total order tax-rate)]
    {:status 200
     :body   (json/encode result)}))
```

The architecture pattern follows Clean Architecture with functional implementation. Business rules are pure. Boundaries handle the messy real world.

---

## Abstraction in FP

### The Definition

Uncle Bob defines abstraction as:

**"Amplification of the essential and elimination of the irrelevant."**

A good abstraction makes what matters louder and what does not matter invisible. In FP, this manifests as:

- **Pure functions** amplify the transformation logic and eliminate temporal coupling
- **Higher-order functions** amplify the pattern (map, filter, reduce) and eliminate the loop mechanics
- **Composition** amplifies the pipeline and eliminates intermediate state

### The TDD + Forethought Hybrid

**"Working through wrong solutions often leads to insights for right solutions."**

The process:
1. Think about the problem (Hammock-Driven Development)
2. Try an approach using TDD
3. If it does not work, the attempt often reveals WHY it does not work
4. Use that insight to find the right approach
5. TDD again with the new insight

This is not wasted effort. Each failed attempt narrows the solution space. TDD provides the safety net to explore freely.

---

## Functional Architecture Patterns

### Event Sourcing

FP naturally supports event sourcing because state is built from a sequence of immutable events:

```clojure
;; Events are immutable facts
(def events
  [{:type :account-created :id 1 :name "Alice"}
   {:type :deposit :id 1 :amount 100}
   {:type :withdrawal :id 1 :amount 30}
   {:type :deposit :id 1 :amount 50}])

;; Current state is a reduce over events (pure function)
(defn apply-event [state event]
  (case (:type event)
    :account-created (assoc state :name (:name event) :balance 0)
    :deposit         (update state :balance + (:amount event))
    :withdrawal      (update state :balance - (:amount event))
    state))

(reduce apply-event {} events)
;; => {:name "Alice" :balance 120}
```

The event log is the source of truth. Current state is derived. You can replay events to recreate any historical state.

### CQRS (Command Query Responsibility Segregation)

CQRS aligns naturally with FP:
- **Commands**: Functions that produce events (side effects, isolated at boundaries)
- **Queries**: Pure functions that derive views from event history

### Pipelines and Middleware

The middleware pattern in functional web frameworks is function composition:

```clojure
;; Each middleware wraps the next handler
(defn wrap-logging [handler]
  (fn [request]
    (log/info "Request:" (:uri request))
    (let [response (handler request)]
      (log/info "Response:" (:status response))
      response)))

(defn wrap-auth [handler]
  (fn [request]
    (if (authenticated? request)
      (handler request)
      {:status 401 :body "Unauthorized"})))

;; Compose middleware
(def app
  (-> handler
      wrap-auth
      wrap-logging))
```

Each middleware is a higher-order function that takes a handler and returns a new handler. The composition reads as a pipeline of concerns.

---

## Memorable Quotes

- "OO and FP are not mutually exclusive. They are complementary."
- "The only way to go fast is to go well."
- "Abstraction is the amplification of the essential and the elimination of the irrelevant."
- On TDD speed: "TDD was about 10% faster every single time, but it always, always felt slower."
- "As tests get more specific, code gets more generic."
- "No variables changing state means no race conditions. No race conditions means no deadlocks, no concurrent update problems."
- "FP is the dark matter of programming - always there but invisible to mainstream."
- "Working through wrong solutions often leads to insights for right solutions."

---

## Code to Analyze

$ARGUMENTS

---

## Output Format

For each piece of code analyzed, produce this assessment:

```
## Functional Programming Assessment

**Module:** [What code is being analyzed]
**Purity:** [Pure functions vs impure/side effects]
**Mutable State:** [Identified mutable state]
**Transformation Pipeline:** [How data flows through functions]
**Composition Opportunities:** [Where map/filter/reduce apply]
**SOLID Compliance:** [Functional SOLID assessment]
```

For each violation found:
```
**Issue:** [Description of the FP violation]
**Location:** file:line
**Category:** [Purity | Immutability | Side Effect | Composition | SOLID]
**Impact:** [Why this is problematic]
**Refactoring:** [How to fix it with FP principles]
```

---

## Review Process

When reviewing code for FP compliance:

### 1. Scan for Mutable State
- Look for variables that are reassigned after initialization
- Identify shared state accessed by multiple functions
- Find global or module-level mutable variables
- Check for in-place mutation of data structures (push, splice, sort, reverse)

### 2. Identify Impure Functions
- Functions that read from or write to external state
- Functions whose return value depends on something other than their arguments
- Functions that produce different results for the same inputs
- Functions with void return type (likely side-effecting)

### 3. Check for Composition Opportunities
- Imperative loops that could be map/filter/reduce
- Nested conditionals that could be pipeline stages
- Repeated transformation patterns across the codebase
- Functions that do multiple things (could be composed from smaller functions)

### 4. Verify Side Effect Isolation
- Are side effects (I/O, network, database) at the boundaries?
- Is business logic free of side effects?
- Are impure functions thin wrappers around pure logic?
- Is the "functional core, imperative shell" pattern followed?

### 5. Assess Functional SOLID Compliance
- **SRP**: Do functions/modules serve a single actor?
- **OCP**: Can new behavior be added without modifying existing code? Are protocols used?
- **LSP**: Do all protocol implementations fulfill the full contract?
- **ISP**: Are protocols focused and not fat?
- **DIP**: Do high-level modules depend on abstractions (protocols), not concretions?

---

## Self-Review (Back Pressure)

After writing or refactoring functional code, ALWAYS perform this self-review before presenting code as done:

### Self-Review Steps
1. **Purity Check**: Are functions pure where possible? Can any function be made pure by extracting the side effect?
2. **Immutability Check**: Is state managed without mutation? Are new data structures created instead of mutating old ones?
3. **Side Effect Check**: Are side effects isolated at the boundaries? Is the core logic free of I/O?
4. **Composition Check**: Are higher-order functions (map/filter/reduce) used instead of imperative loops? Are small functions composed into larger ones?
5. **SOLID Check**: Do functional SOLID principles apply? Are protocols used for extension?

### If Violations Found
- Fix the violations immediately
- Re-run self-review
- Only present as "done" when self-review passes

### Mandatory Quality Gate

Code is NOT complete until:
- [ ] Pure functions where possible
- [ ] State managed through immutable transformations
- [ ] Side effects isolated and controlled
- [ ] Map/filter/reduce used appropriately instead of imperative loops
- [ ] TDD applied to functional code (red-green-refactor)
- [ ] Composition favored over imperative loops
- [ ] Functional SOLID principles applied through protocols and modules

---

## Common Pitfalls

- **Impure core**: Business logic mixed with I/O operations (database calls inside calculation functions)
- **Mutation hiding**: Using "let" or "var" and reassigning, defeating immutability
- **Over-abstraction**: Creating unnecessary monadic wrappers when simple functions suffice
- **Ignoring the imperative shell**: Trying to eliminate ALL side effects instead of isolating them
- **Premature optimization**: Avoiding immutable data structures for "performance" without measurement
- **FP dogmatism**: Rejecting OO patterns that would genuinely help (protocols, interfaces, polymorphism)
- **Neglecting TDD**: Thinking pure functions do not need tests because they are "obviously correct"
- **Complex recursion**: Using explicit recursion where map/filter/reduce would be clearer

---

## Related Skills

- **/solid** - SOLID principles apply to FP through protocols and modules
- **/tdd** - TDD works identically in FP; inner development loop
- **/architecture** - Clean Architecture with functional implementation
- **/patterns** - Functional patterns complement OO patterns
- **/professional** - Professional discipline applies to all paradigms
- **/clean-code-review** - Review functional code quality
