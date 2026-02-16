---
name: functional-programming
description: >-
  Apply functional programming principles to improve code quality. Activate when
  reviewing code with pure functions, immutability, state management, higher-order
  functions, functional composition, or when the user mentions FP, pure functions,
  immutability, map/filter/reduce, side effects, or functional architecture.
model: opus
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
delegates-to:
  - solid
  - architecture
argument-hint: [code or module to analyze]
---

# Functional Programming Skill — Operational Procedure

## Step 0: Detect Context

Before applying any FP guidance, detect the project's stack and FP support level:

1. **Language detection:**
   - Check file extensions: `*.php`, `*.ts`, `*.tsx`, etc.
   - Read a representative file to identify functional support level
2. **FP support classification:**
   - **PHP:** FP supported through discipline, arrays, immutable libraries
   - **TypeScript:** FP supported through libraries and discipline, no enforcement
3. **Ecosystem detection:**
   - Check for FP libraries: Immutable.php, fp-ts, Ramda, lodash/fp
   - Check for state management: Reducer patterns, custom immutable implementations
   - Read composer.json / package.json to understand available tools
4. **Codebase FP maturity:**
   - Scan existing code: are functions pure? is mutation present? do pipelines exist?
   - Grep for mutation patterns: assignment, array mutations, state modifications
   - Identify current side effect boundaries

---

## Step 1: Generate Context-Specific Rules

Based on detected language and FP support level, adapt principles to concrete rules:

| Language | Purity | Immutability | Pipeline | HO-Functions | State |
|----------|--------|-------------|----------|------------|-------|
| **PHP** | Discipline-based | readonly properties (8.1+), value objects | array_map/array_filter chains | array_map/array_filter | Manual/Immutable DTOs |
| **TypeScript** | Discipline-based | Object.freeze, const, Immer | Array methods, pipe | .map/.filter/.reduce | Reducer pattern, custom immutable |

All subsequent FP advice MUST use the detected language's idioms, available libraries, and performance characteristics.

---

## Step 2: Apply Decision Rules

### Rule 1: Purity — Pure Business Logic

- **WHEN to apply:** Any function computing a result from inputs that could theoretically be memoized
- **WHEN NOT:** I/O boundary functions (database reads, HTTP calls, file reads), system interaction (time, random, logging)
- **Decision test:** Cover the function body. Are the only inputs the parameters? Is the only output the return value? No reads from mutable global state? No writes to files, databases, or fields? YES → must be pure.
- **Severity:** 🔴 RED — impure core logic mixing business rules with I/O creates non-deterministic, untestable, unmemoizable code
- **Verification:** For each statement in the function, ask: "Does this read from or write to anything other than parameters/return value?" If yes, move that I/O outside.

### Rule 2: Immutability — Persistent Data Structures

- **WHEN to apply:** Data structures passed between functions, function arguments, module state
- **WHEN NOT:** Performance-critical tight loops where allocation overhead dominates, local stack variables with obvious short scope (< 5 lines)
- **Decision test:** Does this variable's value change after binding? YES → should it? Can you instead create a new binding? Always prefer new bindings over reassignment.
- **Severity:** 🔴 RED — shared mutable data is the root cause of all concurrency bugs (race conditions, deadlocks)
- **Verification:** Grep for reassignment patterns (`var x = ...` then `x = ...`). Each reassignment is a mutation opportunity. Replace with `val`/`const`/`let`-only bindings.

### Rule 3: Side Effect Isolation (Functional Core, Imperative Shell)

- **WHEN to apply:** Any function mixing business logic (pure computation) with side effects (I/O, time, randomness)
- **WHEN NOT:** Trivial single-purpose I/O functions (just a database call with no logic), middleware frameworks that mandate mixing (some web frameworks require this — extract and test the pure part separately)
- **Decision test:** Can you describe the function's purpose in one sentence without using the words "call", "read", "write", "send", "fetch"? If no, it has hidden business logic — extract it.
- **Severity:** 🔴 RED — mixing breaks testability, reproducibility, and composability
- **Verification:**
  - Identify side effects: I/O, time access, randomness, global/field mutation
  - Extract logic that uses only those effects: move to a parameter (dependency injection)
  - Remaining function should be 100% pure
  - Example: `processOrder(order)` calls DB inside → extract to `processOrder(order, getInventory, chargePayment)` where those are pure simulators or injected functions

### Rule 4: Pipeline Composition — Sequential Transformations

- **WHEN to apply:** Multiple sequential transformations on data (parse → validate → transform → aggregate)
- **WHEN NOT:** Early-exit control flow where intermediate results short-circuit processing, complex stateful iteration, exception-based control flow
- **Decision test:** Can you describe the data flow as a sequence of transformations? Does each intermediate result contribute to the final output without side effects? YES → use pipeline.
- **Severity:** 🟡 YELLOW — missing opportunities reduce readability and make future transformations harder to add
- **Verification:**
  - Identify all intermediate values
  - Check if they flow left-to-right or branch
  - Rewrite using language pipeline operator: `data |> transform1 |> transform2 |> transform3` or `data.map().filter().reduce()`
  - Result should read like a description, not a procedure

### Rule 5: Higher-Order Functions over Loops

- **WHEN to apply:** For-loops iterating a collection into a new result (map pattern), filtering to a subset (filter), or accumulating a value (reduce)
- **WHEN NOT:** Complex stateful iteration (zip two lists with interleaved reads), performance-critical tight loops where allocation overhead matters (but benchmark first!), early-exit patterns where break/return is essential to correctness
- **Decision test:** What is the loop doing? Transforming each element → map. Keeping some elements → filter. Combining into one value → reduce. If one of these, use HO-function.
- **Severity:** 🟡 YELLOW — for-loops are harder to understand and more error-prone than their HO-function equivalents
- **Verification:**
  - Identify loop body pattern: does it read `result.push(f(item))`? Replace with `map(f, items)`
  - Does it read `if (predicate(item)) result.push(item)`? Replace with `filter(predicate, items)`
  - Does it accumulate with `acc = op(acc, item)`? Replace with `reduce(op, init, items)`

### Rule 6: Referential Transparency — Functions as Values

- **WHEN to apply:** Any function that could benefit from memoization (same inputs → same output guaranteed), or that is passed as an argument to higher-order functions
- **WHEN NOT:** Functions intentionally non-deterministic (random, timestamps, UUIDs), functions depending on external state that changes intentionally
- **Decision test:** Is this function pure (Rule 1)? Can I safely cache its result? Can I pass it as an argument without losing correctness? YES → referentially transparent.
- **Severity:** 🟢 GREEN — enables optimization, composition, testing, reasoning
- **Verification:** If the function is pure (Rule 1), it's automatically referentially transparent. Use this to enable memoization and function composition without fear of hidden state changes.

---

## Step 3: Review Checklist

Run against every function/data structure in scope. Each item has a severity and verification test.

| # | Check | Look For | Severity | Verification |
|---|-------|----------|----------|-------------|
| 1 | Impure core logic | Business calculation depends on global state, I/O, or current time | 🔴 Red flag | Extract pure parameters from side effects; inject as function args |
| 2 | Hidden mutation | Function modifies input arguments or module fields | 🔴 Red flag | Trace all mutations; replace with new bindings |
| 3 | Shared mutable state | Multiple functions read/write same variable; concurrent access possible | 🔴 Red flag | Use immutable data structures or atoms with explicit synchronization |
| 4 | Side effects scattered | I/O interspersed with pure logic (e.g., DB call inside calculation) | 🔴 Red flag | Extract I/O to function arguments; move to boundaries |
| 5 | Imperative loop (map pattern) | for-loop with result.push(f(item)) | 🟡 Yellow | Replace with map(f, items) or language equivalent |
| 6 | Imperative loop (filter pattern) | for-loop with if(predicate(item)) result.push(item) | 🟡 Yellow | Replace with filter(predicate, items) |
| 7 | Imperative loop (reduce pattern) | for-loop accumulating: acc = op(acc, item) | 🟡 Yellow | Replace with reduce(op, init, items) |
| 8 | Missing immutability | Data structure reassigned after binding; mutable collection passed between functions | 🟡 Yellow | Use const/val bindings; pass frozen copies |
| 9 | Composition opportunity | Sequential function calls that could be piped | 🟢 Opportunity | Chain with pipeline operator or compose function |
| 10 | Partial application candidate | Same function called repeatedly with fixed first N arguments | 🟢 Opportunity | Extract to named function or use partial application |

---

## Step 4: Refactoring Patterns

For each pattern: identify the problem in the PROJECT'S language, show before/after using the project's actual syntax.

### Pattern: Extract Functional Core (impure → separated)

**Problem:** Business logic mixed with I/O — function is untestable, non-deterministic, unoptimizable.

**Before (PHP):**
```php
public function processOrder(int $orderId): array
{
    $order = $this->orderRepository->findById($orderId);  // I/O
    $total = array_sum(array_map(fn($item) => $item['price'], $order['items'])); // Logic
    $tax = $total * 0.1;                      // Logic
    $finalPrice = $total + $tax;              // Logic
    $this->paymentService->charge($finalPrice); // I/O
    $this->orderRepository->update($orderId, ['status' => 'paid']); // I/O
    return ['orderId' => $orderId, 'finalPrice' => $finalPrice, 'status' => 'paid'];
}
```

**After (PHP):**
```php
// Pure core — testable, deterministic, composable
function calculateTotal(array $items): float
{
    return array_sum(array_map(fn($item) => $item['price'], $items));
}

function calculateFinalPrice(float $total): float
{
    return $total + ($total * 0.1);
}

// Imperative shell — at boundary (Service)
public function processOrder(int $orderId): array
{
    $order = $this->orderRepository->findById($orderId);
    $total = calculateTotal($order['items']);
    $finalPrice = calculateFinalPrice($total);
    $this->paymentService->charge($finalPrice);
    $this->orderRepository->update($orderId, ['status' => 'paid']);
    return ['orderId' => $orderId, 'finalPrice' => $finalPrice, 'status' => 'paid'];
}
```

**Steps:**
1. Identify all I/O operations in the function (grep for: `::`, `->`, `DB::`, `Model::`)
2. Extract pure logic into separate functions that take values as parameters
3. Inject I/O as function parameters (dependency injection)
4. Move I/O calls to a boundary function that orchestrates (the "imperative shell")
5. Test pure functions directly; test shell with mock injections

### Pattern: Replace Loop with Pipeline (imperative → declarative)

**Problem:** For-loop harder to understand than transformation chain; more error-prone (off-by-one bugs, accumulator mistakes).

**Before (PHP):**
```php
function getActiveEmployeeNames(array $employees): array
{
    $result = [];
    foreach ($employees as $employee) {
        if ($employee['status'] === 'ACTIVE') {
            $result[] = strtoupper($employee['name']);
        }
    }
    return $result;
}
```

**After (PHP):**
```php
function getActiveEmployeeNames(array $employees): array
{
    return array_map(
        fn($e) => strtoupper($e['name']),
        array_filter($employees, fn($e) => $e['status'] === 'ACTIVE')
    );
}
```

**Or in TypeScript:**
```typescript
const activeNames = employees
    .filter(e => e.status === 'ACTIVE')
    .map(e => e.name.toUpperCase());
```

**Steps:**
1. Identify loop pattern: transformation (map), filtering (filter), or reduction (reduce)
2. Replace with language's native HO-function or comprehension
3. Verify output matches original
4. If multiple transformations, chain them (pipeline)
5. Read the result aloud — should sound like a description, not an instruction

### Pattern: Introduce Immutable Data (mutable → persistent)

**Problem:** Mutable data structure passed between functions; hard to reason about state; concurrency-unsafe.

**Before (PHP):**
```php
$order = ['items' => [], 'total' => 0];

function addItem(&$order, $item) {
    $order['items'][] = $item;      // Mutates!
    $order['total'] += $item['price'];  // Mutates!
}

function applyDiscount(&$order, $rate) {
    $order['total'] *= (1 - $rate);  // Mutates!
}
```

**After (Immutable pattern):**
```php
class Order {
    public readonly array $items;
    public readonly float $total;

    public function __construct(array $items = [], float $total = 0) {
        $this->items = $items;
        $this->total = $total;
    }
}

function addItem(Order $currentOrder, array $item): Order {
    return new Order(
        [...$currentOrder->items, $item],
        $currentOrder->total + $item['price']
    );
}

function applyDiscount(Order $currentOrder, float $rate): Order {
    return new Order(
        $currentOrder->items,
        $currentOrder->total * (1 - $rate)
    );
}

// Usage: each call returns a new order
$order = new Order();
$order = addItem($order, ['name' => 'Widget', 'price' => 10]);
$order = applyDiscount($order, 0.1);
```

**Or in TypeScript:**
```typescript
function addItem(currentOrder: Order, item: Item): Order {
    return {
        ...currentOrder,
        items: [...currentOrder.items, item],
        total: currentOrder.total + item.price
    };
}
```

**Steps:**
1. Identify all mutation points: reassignment, field mutation, array/object methods that mutate (`push`, `pop`, `splice`, `sort`, `reverse`, `shift`, assignment to field)
2. Replace with copy-and-transform: use spread operator, immutable.js, or language equivalent
3. Change all callers to accept the new state and return it (or use reducer pattern)
4. If many mutations: consider a `Reducer` function instead
5. Test: old state should be unchanged after operation

### Pattern: Compose Functions (sequential calls → pipeline)

**Problem:** Multiple sequential function calls not composed; harder to add intermediate steps; less reusable.

**Before (PHP):**
```php
function processUser(int $userId): User {
  $user = $this->userRepository->find($userId);
  $user = validateUser($user);
  $user = enrichWithDefaults($user);
  return $this->userRepository->save($user);
}
```

**After (with composition):**
```php
function pipe(mixed $value, callable ...$fns): mixed {
    return array_reduce(
        $fns,
        fn ($v, $fn) => $fn($v),
        $value
    );
}

function processUser(int $userId): User {
    return pipe(
        $userId,
        fn ($id) => $this->userRepository->find($id),
        fn ($user) => validateUser($user),
        fn ($user) => enrichWithDefaults($user),
        fn ($user) => $this->userRepository->save($user)
    );
}
```

**Or in TypeScript:**
```typescript
const pipe = (...fns: Array<(x: any) => any>) => (x: any) =>
    fns.reduce((v, f) => f(v), x);

const processUser = pipe(
    (id: number) => fetchUser(id),
    (user) => validateUser(user),
    (user) => enrichWithDefaults(user),
    (user) => save(user)
);
```

**Steps:**
1. Identify all intermediate values in a sequence
2. Extract each step to a named function (if not already)
3. Use `compose()` or `pipe()` to chain them (pipe is left-to-right, easier to read)
4. If composition isn't available, write it: `pipe = (...fns) => x => fns.reduce((v, f) => f(v), x)`
5. Test: composed function should match sequential version

### Pattern: Isolate Side Effects (scattered → boundaries)

**Problem:** Side effects (time, randomness, I/O) interspersed with pure logic; code is non-deterministic and hard to test.

**Before (PHP):**
```php
function generateUniqueToken(string $prefix): string
{
    $timestamp = time();              // Side effect: time
    $randomPart = random_int(1, 1000);  // Side effect: randomness
    $token = "{$prefix}-{$timestamp}-{$randomPart}";
    DB::table('tokens')->insert(['token' => $token]);  // Side effect: I/O
    return $token;
}
```

**After (PHP):**
```php
// Pure core
function generateToken(string $prefix, int $timestamp, int $randomPart): string
{
    return "{$prefix}-{$timestamp}-{$randomPart}";
}

// Side effects at boundary
function generateAndStoreToken(
    string $prefix,
    callable $getTime,
    callable $getRandom,
    callable $save
): string {
    $timestamp = $getTime();
    $randomPart = $getRandom();
    $token = generateToken($prefix, $timestamp, $randomPart);
    $save($token);
    return $token;
}

// In boundary (Controller/Service):
$result = generateAndStoreToken(
    "user",
    fn () => time(),
    fn () => random_int(1, 1000),
    fn ($token) => DB::table('tokens')->insert(['token' => $token])
);
```

**Or in TypeScript:**
```typescript
// Pure core
function generateToken(prefix: string, timestamp: number, randomPart: number): string {
    return `${prefix}-${timestamp}-${randomPart}`;
}

// Side effects at boundary
function generateAndStoreToken(
    prefix: string,
    getTime: () => number,
    getRandom: () => number,
    save: (token: string) => void
): string {
    const timestamp = getTime();
    const randomPart = getRandom();
    const token = generateToken(prefix, timestamp, randomPart);
    save(token);
    return token;
}
```

**Steps:**
1. Identify all side effects: I/O, time, randomness, system calls, logging (not output — that's intentional)
2. Move them to function arguments (inject them)
3. Make the main logic pure — it just uses what it's given
4. At the boundary, call the side effects and pass results to the pure function
5. For testing: pass mock side-effect functions that return predictable values

---

## When NOT to Apply This Skill

Ignore strict FP purity in favor of pragmatism when:

- **Performance-critical hot paths:** Immutability-by-default allocates aggressively. If profiling shows allocation is the bottleneck, use mutable data in that inner loop only; wrap it in a pure interface. Benchmark before optimizing.
- **Framework-imposed mixing:** Some frameworks (web servers, game engines, UI frameworks) mandate I/O inside event handlers. Extract and test the pure part separately; accept the framework constraint at the boundary.
- **Prototype/spike:** You're exploring an approach and the code will be rewritten. Accept imperative code for speed; refactor later.
- **Legacy codebase with no test coverage:** Refactoring to FP without tests risks introducing bugs. Use `/legacy-code` skill first to add characterization tests.
- **External API boundaries:** You must match an external contract (database driver, HTTP client library). Wrap the impure boundary with a pure interface at your system boundary.
- **Trivial single-statement functions:** A function that just calls `db.find()` and returns the result doesn't need pure refactoring — it IS the boundary.

---

## K-Line History (Lessons Learned)

### What Worked

- **Separating business logic from I/O:** Moving database calls to function arguments made three architectural problems immediately visible — callers weren't validating data before passing it. Fixed three bugs without touching logic.
- **Immutability-first discipline in shared state:** One team adopted "all state bindings are const/val first" and saw 80% reduction in race conditions in multithreaded code. No architectural change — just discipline.
- **Pipeline composition for data transformations:** Converting nested for-loops to `.filter().map().reduce()` chains eliminated 5 off-by-one bugs in one sprint. Readability improved enough that new team members could modify data flows on day 1.
- **Pure functions for testing:** Business logic extracted to pure functions eliminated test doubles/mocks for that logic. Test suite got faster and clearer.

### What Failed

- **Dogmatic FP in latency-sensitive code:** Immutable-by-default in a real-time audio processor caused 40% performance regression. Switched to mutable inner loop with pure interface; problem solved.
- **Lazy evaluation without understanding:** Clojure sequences looked elegant but caused memory leaks when used carelessly with large datasets. Required explicit `doall` or materialization. Dogmatism beat pragmatism.
- **Forcing composition where early exit matters:** A pipeline that filters and processes failed because some intermediate steps needed to abort. Rewritten as imperative code was clearer and more correct.
- **Over-abstraction with monadic wrappers:** Scala code wrapped everything in `Option`/`Either` to the point that simple logic became hard to read. Stripped back to selective wrapping for genuinely risky operations.

### Edge Cases

- **Concurrency model mismatches:** FP shines with immutable data + message passing (Erlang, channels). In imperative languages, FP immutability + imperative concurrency (threads/locks) causes friction. Use the language's concurrency model.
- **Domain-specific abbreviations:** In mathematical/scientific code, single letters (`x`, `y`, `ssr`, `df`) ARE the domain names. Don't force descriptive names; but do make the domain clear in function headers.
- **Performance profiling surprises:** What looked slow (immutability) was actually fast (structural sharing). What looked fast (mutable loop) was actually slow (allocation in aggregate). Always measure.

---

## Communication Style

When recommending FP refactoring:

1. **Show before/after in the project's actual language** — Include the full function, not pseudocode. Use the team's syntax and idioms.
2. **Identify the specific rule violated** (Rule 1: Purity, Rule 2: Immutability, etc.) — Not "this code isn't FP enough" but "this function depends on global state (Rule 1: Purity) — here's how to fix it"
3. **Estimate effort and risk:**
   - "Safe rename + inject parameters" (low risk)
   - "Extract core to new functions + refactor callers" (medium risk, needs tests)
   - "Rewrite with immutable data structure" (high risk without test coverage)
4. **Prioritize fixes:** Rule 1 (Purity: impure core) >> Rule 2 (Immutability: shared mutable state) >> Rule 3 (Side effect isolation) >> Rules 4-6 (Composition, HO-functions, transparency)
5. **Acknowledge tradeoffs honestly:** "This is less performant in the hot path but more testable — benchmark to decide if it matters" or "This application requires I/O in handlers — we'll extract the pure part separately"
6. **Batch related refactorings** — If five functions all need the same injection pattern, show one example and apply systematically
7. **Never say "this isn't FP"** — Say "this function violates Rule X because [specific observation] — we can fix it by [concrete steps]"
