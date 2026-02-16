---
name: functions
description: >-
  Write and refactor clean functions. Activate when writing new functions, refactoring
  existing ones, reviewing code for function quality, or when the user mentions function
  size, arguments, side effects, extract method, or complexity. Functions are the first
  unit of organization — if they're wrong, everything above them inherits the mess.
model: opus
allowed-tools: Read, Write, Edit, Grep, Glob
delegates-to:
  - naming  # for function name quality
  - solid   # when extraction reveals hidden classes
argument-hint: [code or file to analyze]
---

# Functions Skill — Operational Procedure

## Step 0: Detect Context

Before applying function rules, detect the project's stack:

1. **Language detection:**
   - Check file extensions: **PHP/TypeScript-first** → `*.php`, `*.ts`, `*.tsx`. Also support `*.py`, `*.go`, `*.rb`, `*.java`, `*.rs`, etc.
   - Read a representative source file to confirm idioms
2. **Build system and dependencies:**
   - Check for build markers: **PHP** → `composer.json`. **TypeScript** → `package.json`, `tsconfig.json`
   - Grep for language imports: **PHP** → `use` statements, namespaces. **TypeScript** → `import` statements
3. **Function style detection:**
   - **PHP**: Methods on classes, free functions, static methods. Object-oriented or functional style.
   - **TypeScript**: Functions, arrow functions, class methods, async functions. Modular style.
   - Error handling style: **PHP** → exceptions, validation, throw statements. **TypeScript** → try/catch, error states, async error handling.
   - Async pattern: **PHP** → callbacks, `async/await`, async iterators. **TypeScript** → `async/await`, Promises, event handlers.
4. **Project conventions:**
   - Read existing functions to identify the project's baseline size, style, and patterns
   - Check for linter rules: **PHP** → PHPStan, PHP-CS-Fixer. **TypeScript** → ESLint, Prettier.
   - Note the project's test patterns — function design decisions affect testability

All subsequent advice MUST use the detected language's actual syntax and idioms. PHP's exception-based error handling is idiomatic. TypeScript async/await patterns are idiomatic.

---

## Step 1: Generate Context-Specific Rules

Adapt universal function rules to the detected stack:

| Rule | Language-specific adaptation needed |
|------|-------------------------------------|
| Size limits | **PHP**: Methods tend 10-20 lines (setup + validation + action + return). **TypeScript**: Functions should be short. Longer functions are acceptable if they remain readable. Account for language idioms. |
| Argument count | **PHP**: Dependency injection adds parameters (okay). **TypeScript**: Objects/options patterns are common (okay). Builder patterns have different rules. |
| CQS | **PHP**: Mutations should not return business data. Queries should be pure. **TypeScript**: Follow CQS unless language idiom requires otherwise. |
| Error handling | **PHP**: Exceptions with validation. **TypeScript**: try/catch, error states, Promise rejection handling. Also support Python/Go/Rust patterns when present. |
| Side effects | **PHP**: Services encapsulate side effects. **TypeScript**: Async functions may have side effects. Know the idiom. |
| Tell Don't Ask | **PHP**: Fluent method chains are idiomatic. **TypeScript**: Avoid digging into nested objects for behavior. Minimize property drilling. |

---

## Step 2: Apply Decision Rules

### Rule 1: Keep Functions Small

- **WHEN to apply:** Every function. Target 4-10 lines of logic for utilities. Allow 15-20 for **PHP** class methods (setup + action + return). Allow 15-25 for **TypeScript** functions (reasonable complexity is acceptable).
- **WHEN NOT:** Functions that are a single readable pipeline or chain (a 15-line method chain in PHP is fine if each step is clear). Fluent APIs. Language idioms (PHP method chains, TypeScript async chains).
- **Decision test:** Can you see the entire function without scrolling? Can you describe it in one sentence without "and"?
- **Verification:** Count lines. **PHP utility functions** > 20 → refactor. **PHP methods** > 30 → refactor. **TypeScript functions** > 40 → extract sub-functions.
- **Severity:** **Utility > 20** 🟡 Warning. **Utility > 40** 🔴 Red flag. **PHP method > 30** 🟡 Warning. **TypeScript function > 50** 🟡 Warning.

### Rule 2: Do One Thing (Extract Till You Drop)

- **WHEN to apply:** Any function where you can name a coherent sub-operation within it.
- **WHEN NOT:** When extraction would create a function called only once from one place AND the extracted code is only 1-2 lines AND the parent function is already small. Also: don't extract out of hot loops in performance-critical code without benchmarking.
- **Decision test:** Describe what the function does. If you use "and" or "then," it does more than one thing.
- **Verification:** Try to extract a sub-function. If you can give it a meaningful name (not `doPartTwo()`), the original was doing more than one thing.
- **Severity:** Multiple responsibilities 🔴 Red flag.

### Rule 3: One Level of Abstraction (Step-Down Rule)

- **WHEN to apply:** Any function that mixes high-level orchestration with low-level details (string parsing next to business rules, SQL query building next to domain logic).
- **WHEN NOT:** Leaf functions that ARE the low-level detail. Simple CRUD operations where the abstraction IS the database call.
- **Decision test:** For each line, ask "what level of abstraction is this?" If adjacent lines answer differently, extract the lower-level ones.
- **Verification:** Read top-to-bottom. Each function should call functions one level below it. Public → Private helper → utility. No backwards references.
- **Severity:** Mixed abstraction levels 🔴 Red flag.

### Rule 4: Minimize Arguments

- **WHEN to apply:** Functions with 3+ arguments. Functions with boolean arguments. Functions with output arguments.
- **WHEN NOT:** Language conventions that require extra args (Go's `context.Context`, Express's `(req, res, next)`). Constructor dependency injection (args are the dependencies). Type signatures in TypeScript (generic parameters don't count).
- **Decision test:**
  - 0-2 args → fine
  - 3 args → do any travel together? Group into an object.
  - 4+ args → almost certainly wrong. Introduce a parameter object or options object.
  - Single boolean arg → split into two named functions, or use options object.
  - Multiple boolean args → don't mechanically split into 2^N functions. Extract a config/options object or use an enum. Two booleans = 4 behaviors = the function is doing too many things.
  - Optional/null arg → make it optional in the language's idiom (default parameters, optional properties).
- **Verification:** At the call site, can you tell what each argument means without reading the signature? If not, introduce a named object or use the language's named-parameter feature.
- **Severity:** 4+ args 🔴 Red flag. Boolean args 🟡 Warning. 3 args 🟡 Warning.

### Rule 5: Command-Query Separation

- **WHEN to apply:** Functions that both mutate state AND return a value (not an error indicator).
- **WHEN NOT:** Idiomatic patterns in the detected language:
  - **PHP**: Builder chains (fluent), `save()` methods, query builder patterns
  - **TypeScript**: Idiomatic mutation + return patterns (e.g., array methods that mutate and return)
  - **Go**: `(result, error)` returns, **Rust**: `Result<T, E>`, pop/dequeue operations, atomic compare-and-swap
- **Decision test:** Does the function both change something AND answer a question? If yes, split into a command (void/returns nothing meaningful) and a query (returns value, no mutation).
- **Verification:** Check return type. Void → command (should have side effect). Non-void → query (should be pure). Mixed → split (unless language idiom).
- **Severity:** CQS violation 🟡 Warning (unless idiomatic to the language).

### Rule 6: No Hidden Side Effects

- **WHEN to apply:** Functions whose name doesn't reveal all state changes they make.
- **WHEN NOT:** Functions explicitly named for their side effect (`saveToDatabase()`, `sendNotification()`). Event handlers and lifecycle methods.
- **Decision test:** Read only the function name and signature. Now read the body. Did it do something you didn't expect? That's a hidden side effect.
- **Verification:** List every state change the function makes (instance variables, globals, I/O, database, filesystem). Each one should be predictable from the name.
- **Severity:** Hidden side effect 🔴 Red flag. Temporal coupling (must call A before B but nothing enforces it) 🔴 Red flag.

### Rule 7: Tell, Don't Ask (Law of Demeter)

- **WHEN to apply:** Method/property chains that dig into nested objects: `a.getB().getC().doThing()`.
- **WHEN NOT:** Fluent APIs designed for chaining (builders, method chains, pipelines). Data Transfer Objects / plain objects (accessing `order.customer.address.city` on a DTO is fine — it's data, not behavior).
- **Decision test:** Count the dots. If you're calling a method on a result of a method, you're coupling to the structure of the intermediate object.
- **Verification:** Can you replace the intermediate object's type without breaking this code? If not, you have a Demeter violation.
- **Severity:** Deep chains into behavior objects 🟡 Warning. Train wrecks through 3+ levels 🔴 Red flag.

---

## Step 3: Review Checklist

| # | Check | Look for | Severity | Verification |
|---|-------|----------|----------|-------------|
| 1 | Mixed abstraction levels | Business logic interleaved with I/O, parsing, formatting | 🔴 Red flag | Can you label each line's abstraction level? |
| 2 | Hidden side effects | Unexpected mutation, I/O, or state change | 🔴 Red flag | List all state changes — are they in the name? |
| 3 | Function > 40 lines | Scrolling required to read | 🔴 Red flag | `wc -l` on the function body |
| 4 | 4+ arguments | Parameter list requires documentation | 🔴 Red flag | Count args, check if any group into an object |
| 5 | Boolean/flag argument | Function does two things based on a flag | 🟡 Warning | Split into two named functions |
| 6 | CQS violation | Returns value AND mutates state | 🟡 Warning | Check return type vs side effects (skip if idiomatic) |
| 7 | Train wreck / Demeter | `a.b().c().d()` on behavior objects | 🟡 Warning | Count dots, check if intermediate types are coupled |
| 8 | Temporal coupling | Must call A before B, not enforced by API | 🟡 Warning | Is there an `open()`/`close()` pair without a `withX()` wrapper? |
| 9 | Function 20-40 lines | Could likely be extracted further | 🟢 Improve | Try to name an extractable sub-operation |
| 10 | 3 arguments | Approaching sloppy | 🟢 Improve | Do any args travel together? |

---

## Step 4: Refactoring Patterns

### Pattern: Extract Till You Drop

**Problem:** Function does multiple things, mixed abstraction levels.
**Steps:**
1. Read the function and identify distinct operations (setup, validation, core logic, persistence, response)
2. For each operation, extract a function with a name describing WHAT it does, not HOW
3. The parent function becomes an orchestrator that reads like a table of contents
4. Each extracted function should be one abstraction level below the parent
5. Continue extracting from the extracted functions until each does exactly one thing
6. Run tests after each extraction

### Pattern: Introduce Parameter Object

**Problem:** 3+ arguments that travel together, or argument order is error-prone.
**Steps:**
1. Identify arguments that logically group (e.g., `x, y, z` → `Point`; `host, port, protocol` → `ConnectionConfig`)
2. Create a class/struct/type for the group, using the language's idiom (dataclass in Python, interface in TS, struct in Go)
3. Replace arguments with the new object
4. Update all call sites
5. Run tests

### Pattern: Replace Boolean Argument with Two Functions

**Problem:** `render(document, true)` — caller can't tell what `true` means.
**Steps:**
1. Identify the boolean argument and what it controls
2. Create two functions named for the two behaviors: `renderForPrint(doc)`, `renderForScreen(doc)`
3. Move the branching logic into the two functions (or keep a shared private function both call)
4. Replace all call sites
5. Delete the boolean-argument version
6. Run tests

### Pattern: Extract Method Object

**Problem:** Large function with many local variables that make extraction difficult (extracted functions would need 5+ parameters).
**Steps:**
1. Create a new class named after the function's purpose
2. Move the function's parameters to the constructor
3. Promote local variables to fields
4. Move the function body to a `run()`/`execute()`/`invoke()` method
5. Now extract freely — all "shared" state is in fields, no parameter passing needed
6. Run tests

### Pattern: Wrap Temporal Coupling (Passing a Block)

**Problem:** `open()`/`close()` pairs, `acquire()`/`release()`, `begin()`/`commit()` — the second call is easy to forget.
**Steps:**
1. Create a wrapper function that takes a callback/block/lambda
2. The wrapper handles setup and teardown, calling the user's code in between
3. Use the language's idiom: `with` statement (Python), `using` (C#), `defer` (Go), try-with-resources (Java), RAII (Rust/C++)
4. Remove all direct calls to the open/close pair
5. Run tests

---

## When NOT to Apply This Skill

Ignore function strictness when:

- **Language idioms:** Middleware, async handlers, event listeners have conventions that override some rules. Work within the language's design.
- **Performance hot paths:** Inlining a function, avoiding allocation from parameter objects, keeping a large function to avoid call overhead — all valid when profiling confirms the bottleneck. Comment why the function is large.
- **Single-use scripts:** A 50-line deployment script that runs once and is read once doesn't need 12 extracted functions. Keep it readable as a linear procedure.
- **Mathematical/algorithmic code:** Dense numerical algorithms are often clearest as a single function with well-named variables. Extracting `computeHouseholderReflection()` into 6 sub-functions can make the algorithm harder to follow, not easier.
- **DSL/builder patterns:** Fluent interfaces are designed for long chains. Don't break them up to satisfy line count rules.
- **Boolean splitting creates too many variants:** If splitting a boolean arg into two functions would create a combinatorial explosion (e.g., `process(notify, dry_run)` → 4 variants), use an options/config object instead. The goal is clarity at the call site, not a strict "no booleans" rule.

---

## K-Line History (Lessons Learned)

> This section should grow over time with actual project experience.

### What Worked
- **PHP**: Extracting a 200-line method into 8 named helper methods made a hidden race condition visible — two of the extracted methods were accessing the same state unsafely.
- **TypeScript**: Extracting complex logic into a separate module reduced function size and made the code testable in isolation.
- Introducing parameter objects for functions with 4+ args eliminated two categories of bugs: wrong argument order and missing arguments after refactoring.
- The "describe it without AND" test caught more multi-responsibility functions than line counting.
- **PHP**: Wrapping database transaction open/close in a transaction wrapper eliminated 100% of "forgot to rollback" bugs.

### What Failed
- **PHP**: Extracting every class method to < 10 lines created a maze of tiny functions where the request-to-response flow was hard to follow. Methods naturally run 15-25 lines due to setup, validation, and action.
- **TypeScript**: Over-extracting functions led to a scattered codebase—too many small functions made the primary flow hard to follow. Reasonable function size often better than hyper-extraction.
- Blindly applying CQS to idiomatic methods (`save()`, `delete()`) created awkward alternatives.
- Over-applying Tell Don't Ask to a data-access service (which is fundamentally about querying) created unnecessary wrapper methods.
- Extracting helper functions prematurely when a single function would suffice added complexity without benefit.

### Edge Cases
- **PHP error handling:** Class methods naturally have 2-3 lines of validation and exception handling. Don't count these toward the "method too long" threshold. DO extract complex validation or recovery logic into helpers.
- **PHP constructor/dependency injection:** May legitimately have many parameters in DI-heavy architectures. Use the language's idioms rather than manually applying parameter objects to constructors.
- **TypeScript async/await:** Async methods often need setup + action + async wait in one handler. This is acceptable when clearly structured. Extract complex logic to separate functions when helpful.
- **TypeScript arrow functions:** Short arrow functions in callbacks are acceptable when the body is 1-2 lines. Extract to named functions when the logic becomes complex.
- **Property access chains:** Safe to access data on plain objects/DTOs (e.g., `order.customer.address.city`). Unsafe if chaining methods on behavior objects.

---

## Communication Style

When recommending function changes:

1. **Show before/after** in the project's actual language, with real function signatures
2. **Name the refactoring:** "Extract Method," "Introduce Parameter Object," "Replace Boolean with Two Functions" — so the developer can look it up
3. **Estimate effort:** "Safe automated refactoring" vs "Requires updating 23 call sites and re-testing"
4. **Prioritize impact:** Fix 🔴 issues first. A 100-line function with hidden side effects matters more than a 25-line function that could be 20.
5. **Respect the framework:** Don't suggest changes that fight the framework's design. If Express wants `(req, res, next)`, don't argue.
