---
name: refactor-suggestion
description: >-
  Analyze code and provide specific, actionable refactoring suggestions based on
  Clean Code principles. Activates when code feels messy or hard to change, after
  implementation to improve code quality, or when the user mentions refactor,
  improve code, clean up, technical debt, or code smells.
allowed-tools: Read, Grep, Glob
argument-hint: [file path to analyze]
model: opus
delegates-to: [naming, functions, solid, tdd, legacy-code, clean-code-review]
---

# Refactoring Suggestions

Analyze code and identify specific refactoring actions. This skill scans for code smells, prioritizes by impact, recommends refactoring techniques with exact locations, and routes to specialized skills.

## Step 0: Detect Context

Before analyzing for smells, establish baseline facts about the code:

**Language & Runtime**
- Identify the programming language(s) in the files
- Note language-specific patterns and conventions
- Check if the code is synchronous or async-heavy (affects coupling patterns)

**Test Coverage Status**
- Check for test files (*Test.php, *.test.tsx, *.test.ts, *.spec.tsx)
- Look for CI configuration (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
- Determine: no tests, some tests, high coverage
- CRITICAL: If no tests exist, recommend /legacy-code for characterization tests before any refactoring

**Scope of Analysis**
- Single function (< 50 lines typically)
- Class/type definition (< 300 lines typically)
- Module/package (multiple classes)
- System-wide (architectural level)

**Code Age**
- Check git blame/log: new code vs legacy (months/years old)
- Note: new code with bad patterns needs refactoring now; legacy code needs characterization tests first

---

## Step 1: Scan for Smells

Apply decision rules for each smell category. For each match, record: smell name, location (file:line or function name), and severity.

### BLOATER Detection

**WHEN:** Function >20 lines AND has multiple sections OR class >200 lines AND >3 responsibilities OR >3 parameters AND parameters unrelated
**WHEN NOT:** Inherently complex algorithms, framework-mandated signatures, data-structure initialization blocks

**Long Function**
- DETECT: Count lines (exclude blank/comment lines). >20 lines = smell. >40 lines = critical.
- DETECT: Can you identify 2+ logical sections with comments or blank lines between them? Extract Method.
- DETECT: Nesting depth >3? Each level is a candidate extraction.

**Large Class**
- DETECT: Count methods and fields. >10 methods OR >5 fields = smell.
- DETECT: Can't describe what the class does in one sentence without "and"? Too many responsibilities.
- DETECT: Fields used by only some methods? Candidate for Extract Class.

**Long Parameter List**
- DETECT: >3 parameters = smell. >5 parameters = critical.
- DETECT: Parameters always used together? Data clump → Introduce Parameter Object.
- DETECT: Parameter rarely/never used in method body? Remove it.

**Data Clumps**
- DETECT: Same 2+ fields/parameters appear together in 3+ places
- DETECT: Remove one field → do the others still make sense? If no, they're a clump.
- Examples: (city, state, zip), (startDate, endDate), (username, password)

### OO ABUSER Detection

**WHEN:** Switch/if chain selects behavior by type OR subclass inherits but doesn't use methods OR class has fields only set in some branches
**WHEN NOT:** Guard clauses at function entry, fluent builder APIs, framework-standard factory patterns

**Switch/If Chain on Type**
- DETECT: Pattern `if obj.type == X: ... else if obj.type == Y: ...`
- DETECT: Pattern `switch value: case TYPE_A: case TYPE_B: ...`
- DETECT: Same switch/if repeated in multiple methods? Extra critical.

**Refused Bequest**
- DETECT: Subclass overrides method to throw NotImplementedError or return null/empty
- DETECT: Subclass inherits fields it never uses
- DETECT: Subclass name includes "Abstract" prefix but has subclasses itself

**Temporary Field**
- DETECT: Field initialized in one branch, null in others
- DETECT: Field read only in some methods, written in others
- Example: field set in `init()` but only used in `process()`, null otherwise

### CHANGE PREVENTER Detection

**WHEN:** Same class modified for 3+ unrelated reasons in recent commits OR one change requires edits to 4+ files
**WHEN NOT:** Cross-cutting concerns (logging, auth, metrics) that naturally span modules

**Divergent Change**
- DETECT: Grep for class name in git log last 10 commits. Do messages mention different domains? (e.g., "fix database query" AND "fix UI formatting" AND "update business rule")
- DETECT: Class has methods grouped by external reason, not internal cohesion
- EXAMPLE: User class with methods for validation, persistence, notification — three reasons to change

**Shotgun Surgery**
- DETECT: One logical change (e.g., "add new payment type") requires edits to 4+ files/classes
- DETECT: Grep for feature branch: track how many files touched for one logical change
- DETECT: Related fields/methods scattered across multiple classes

### DISPENSABLE Detection

**WHEN:** Unreachable code OR method not called OR parameters never used OR abstract class with 1 subclass OR comments explain confusing code
**WHEN NOT:** Public API surface, plugin hooks, framework extension points

**Duplicate Code**
- DETECT: Same logic block (5+ lines) appears 2+ times in same class or 3+ times in codebase
- DETECT: Similar-looking code with different variable names — trace semantics to confirm it's actually duplicate

**Dead Code**
- DETECT: Method never called. Grep for method name in codebase.
- DETECT: Unreachable branches: `if false: ...`, code after `return`
- DETECT: Commented-out code blocks (version control remembers it)
- DETECT: Unused variables, unused imports, unused parameters

**Speculative Generality**
- DETECT: Abstract class with only one concrete subclass
- DETECT: Method parameter that's never used or always passed same value
- DETECT: "Hook" method with no callers, added for future flexibility
- DETECT: Extra level of indirection with no benefit (pass-through methods)

### COUPLER Detection

**WHEN:** Method uses data from another class more than its own OR chain of getter calls (a.b().c().d()) OR two classes access each other's private details
**WHEN NOT:** Fluent APIs (builder pattern), intentional callbacks/observers, dependency injection containers

**Feature Envy**
- DETECT: Method M in class A uses methods/fields from class B more than from class A
- COUNT: How many lines reference `self` vs `parameter`? If parameter >self, envy.
- EXAMPLE: `OrderProcessor.calculateShipping(order)` uses only `order.weight`, `order.destination` — belongs in Order class

**Message Chain**
- DETECT: Pattern `a.getB().getC().getD().doSomething()`
- COUNT: Dots in expression. >2 dots = smell, >3 dots = critical.
- RISK: Breaking change in B's interface cascades to all callers

**Inappropriate Intimacy**
- DETECT: Class A accesses class B's private fields directly (not via methods)
- DETECT: Two-way dependency: A depends on B AND B depends on A
- DETECT: Setter methods exist only to support one caller

---

## Step 2: Prioritize by Impact

Triage identified smells into severity buckets. Severity is contextual — a long function with >80% test coverage is lower risk than the same function with 0% coverage.

### 🔴 CRITICAL — Must Refactor

- Long function (>40 lines) with **zero test coverage** (refactoring risk is highest)
- Duplicate code in 4+ locations (maintenance nightmare, bug propagation risk)
- Long parameter list (>5 params) causing bugs or making testing hard
- Switch/if chain on type that's modified every sprint (violates OCP actively)
- Dead code (safe to delete immediately)
- Unreachable branches (indicates incomplete feature removal)
- Inappropriate intimacy causing tight coupling (blocks parallel development)

### 🟡 WARNING — High Priority

- Long function (20-40 lines) with <50% test coverage
- Duplicate code in 3 locations (Rule of Three)
- Feature envy (method belongs in another class)
- Message chain with 3 dots (tight coupling risk)
- Temporary fields (indicates missing abstraction)
- Classes >200 lines with 2-3 unrelated responsibilities
- Speculative generality that's actively confusing (abstract base with 1 implementation)

### 🟢 IMPROVE — Polish & Readability

- Long function (20-30 lines) with 80%+ test coverage
- Magic numbers/strings without constants
- Primitive obsession where value object would clarify intent
- Lazy classes (low-value wrappers)
- Long parameter lists (2-3 params) with related semantics
- Dead code in rarely-used modules
- Comments that restate obvious code

---

## Step 3: Recommend Refactoring

For each smell at 🔴 or 🟡 severity, provide:

1. **Smell Name** — The specific code smell
2. **Location** — File path and line range or function name
3. **The Problem** — Why this smell matters (blocking changes, hiding defects, tight coupling)
4. **Refactoring Technique** — The specific pattern to apply
5. **Effort Estimate** — Safe IDE rename vs multi-file restructuring
6. **Prerequisite** — Tests exist? If not, recommend /legacy-code first

### Refactoring Pattern Library

#### Extract Till You Drop
**Use for:** Long functions, methods doing multiple things
**Steps:**
1. Identify a logical section (3-5 lines that could be named)
2. Extract to new function with intention-revealing name
3. Inline any temporary variables from extracted section
4. Repeat until each function does one thing
**Effort:** Low (IDE-safe if good test coverage)
**Example Location:** app/Services/OrderService.php lines 42-58 → `validateShippingAddress()`

#### Replace Conditional with Polymorphism
**Use for:** Switch statements or if-else chains selecting by type
**Steps:**
1. Define interface or base class with method representing behavior
2. Create concrete class for each type
3. Move the branch logic into the concrete class implementation
4. Replace switch/if with polymorphic call
**Effort:** Medium (creates new files, may need to restructure)
**Example:** PaymentProcessor.process(payment) → payment.process()

#### Introduce Parameter Object
**Use for:** Data clumps, long parameter lists, parameters always traveling together
**Steps:**
1. Create new value object or data class holding the clumped parameters
2. Update function signature: replace 3+ scattered params with single object param
3. Update all call sites to pass object instead of individual params
4. If same clump appears elsewhere, repeat
**Effort:** Medium (parameter changes ripple to callers)
**Example:** searchEvents(startDate, endDate, minPrice, maxPrice) → searchEvents(dateRange, priceRange)

#### Move Method / Move Field
**Use for:** Feature envy, methods using another class's data more than their own
**Steps:**
1. Create method in target class with same signature
2. Copy method body to target
3. Update original method to delegate to target
4. Update all call sites: obj.methodName() → obj.target.methodName()
5. Delete original method
**Effort:** Medium (callers and dependencies)
**Example:** App\Services\ShippingCalculator::calculateShipping(Order) → Order::calculateShipping(ratePerKgKm)

#### Consolidate Scattered Logic (Shotgun Surgery Fix)
**Use for:** One logical responsibility scattered across 4+ classes
**Steps:**
1. Identify the scattered pieces (related methods and fields)
2. Choose a primary class or create new class to be the home
3. Move each piece to primary class
4. Update call sites to reference primary class
5. Delete empty delegating shells if created
**Effort:** High (cross-file changes)
**Example:** Payment validation scattered in Order, Payment, Account → Payment.validate()

#### Kill Dead Code
**Use for:** Unreachable branches, unused methods, commented-out blocks
**Steps:**
1. Verify code is truly unreachable (grep, control flow analysis, test with no callers)
2. Delete it (version control stores history)
3. Run tests to confirm no side effects
**Effort:** Low (one-way operation, safe with tests)
**Example:** Delete unused calculateTaxLegacy() method, dead if branch, commented-out config

#### Characterize Before Refactoring
**Use for:** Code with zero test coverage (PREREQUISITE for all refactoring of untested code)
**Steps:**
1. Write golden-standard tests capturing current behavior (delegate to /legacy-code)
2. Run tests to verify they capture behavior
3. THEN proceed with refactoring
4. Refactoring tests must still pass
**Effort:** Medium-High (requires understanding behavior first)
**Prerequisite:** No other refactoring proceeds without this step

---

## Step 4: Route to Specialized Skills

Based on the smell type and refactoring technique, delegate to the skill that owns detailed guidance:

| Smell | Technique | Delegate To | What They Provide |
|-------|-----------|-------------|-------------------|
| Bad naming in extracted methods | Extract Method | /naming | Intention-revealing names, conventions |
| Long functions, multiple responsibilities | Extract Till You Drop | /functions | One thing, single level of abstraction, testability |
| Switch on type, type hierarchy | Replace Polymorphism | /solid | Interface design, OCP, LSP, class structure |
| Long parameter lists, data clumps | Introduce Parameter Object | /solid | Value object design, SRP |
| Coupling, feature envy, message chains | Move Method, Hide Delegate | /architecture | Dependency direction, boundaries, coupling analysis |
| Shotgun surgery, scattered responsibility | Consolidate, Move Method | /components | Cohesion metrics (REP/CCP/CRP), module boundaries |
| Dead code, no tests to refactor safely | Characterize Before Refactoring | /legacy-code | Characterization tests, Boy Scout Rule, Strangler Fig |
| Feature work + refactoring mixed | TDD workflow | /tdd | Red-Green-Refactor, test doubles, FIRST properties |
| After refactoring complete | Verify quality improvement | /clean-code-review | Comprehensive 10-dimension review |

---

## Key Decision Rules (WHEN/WHEN NOT)

### Rule 1: Test Coverage Gate
**WHEN:** Code has no tests. **ACTION:** Stop refactoring → delegate to /legacy-code for characterization tests first.
**WHEN NOT:** Code has >50% test coverage. **ACTION:** Proceed directly to smell analysis.

### Rule 2: Bloater Detection
**WHEN:** Function >20 lines AND identifiable sections AND can extract without breaking tests.
**WHEN NOT:** Inherently complex algorithms (FFT, parser combinators), framework-mandated signatures, simple data-structure initialization.

### Rule 3: Duplication Rule of Three
**WHEN:** Same logic appears 3+ times in codebase. **ACTION:** Extract immediately.
**WHEN NOT:** Similar-looking code with different semantics (confirm by tracing data flow, not just visual inspection).

### Rule 4: Coupling Analysis
**WHEN:** Feature envy (method uses another class's data >own data) OR message chain >2 dots.
**WHEN NOT:** Fluent builder pattern, intentional callback chains, dependency injection frameworks.

### Rule 5: Dead Code Safety
**WHEN:** Unreachable code, unused methods, orphaned branches. **ACTION:** Delete (version control remembers).
**WHEN NOT:** Public API surface, plugin hooks, framework extension points.

### Rule 6: Change Pattern Analysis
**WHEN:** Same class modified for 3+ unrelated reasons in recent commits (divergent change).
**WHEN NOT:** Cross-cutting concerns (logging, auth, metrics) that naturally span modules.

---

## Refactoring Checklist

Use this checklist to systematically scan code. Severity markers guide priority.

1. 🔴 **Long function (>40 lines) with multiple responsibilities and zero test coverage**
   - Prerequisite: Write characterization tests first
   - Action: Extract Method recursively until each function does one thing

2. 🔴 **Duplicate logic in 3+ locations**
   - Action: Extract Method (within class) or Extract Class (across classes)
   - Validate: Same behavior, not similar-looking coincidence

3. 🔴 **No test coverage for code being refactored**
   - Action: STOP → Delegate to /legacy-code for characterization tests
   - Never refactor untested code

4. 🟡 **Long parameter list (>3 related parameters)**
   - Action: Introduce Parameter Object to group related data
   - Validate: Parameters always used together

5. 🟡 **Switch/if chain selecting behavior by type**
   - Action: Replace Conditional with Polymorphism
   - Validate: Each type has 2+ cases, code is duplicative

6. 🟡 **Feature envy — method uses another class's data more than its own**
   - Action: Move Method to the class whose data it uses
   - Validate: Call site becomes `otherObj.method()` instead of `processor.method(otherObj)`

7. 🟡 **Message chain (a.b().c().d() pattern, 3+ dots)**
   - Action: Hide Delegate or Extract Method to break the chain
   - Validate: Reduces coupling to intermediate objects

8. 🟡 **Temporary fields (field set in one branch, null in others)**
   - Action: Extract Class to group field + methods that use it
   - Validate: Extracted class has clear responsibility

9. 🟢 **Magic numbers/strings without named constants**
   - Action: Define constant, update all usages
   - Effort: Low, usually IDE-safe refactoring

10. 🟢 **Primitive obsession — using int/string where value object would clarify**
    - Action: Introduce value object (Money, Email, UserId)
    - Validate: Improves readability and type safety

---

## When NOT to Apply

**Do NOT refactor when:**

- **You don't understand the code** — Refactoring requires understanding behavior you're preserving. Read the code and tests first. If tests don't exist, write characterization tests (/legacy-code) before refactoring.

- **Tests don't exist** — There's no safety net. Write tests first (/legacy-code).

- **You should rewrite instead** — If the entire module is broken, incremental refactoring may be slower than rewriting. But rewrites are riskier. Consider Strangler Fig pattern (/legacy-code) instead of all-at-once replacement.

- **You don't have a specific reason** — "The code is ugly" is not enough. Identify the specific smell. What problem does it cause? Will refactoring solve it? Refactoring is purposeful improvement, not cosmetic cleanup.

- **You're adding a feature** — Finish the feature first (get to green), THEN refactor. Mixing new behavior with structural changes makes it impossible to tell if a test failure is a refactoring mistake or a new bug.

- **In the middle of a critical production incident** — Stable code is better than perfect code when systems are down. Refactor after stability is restored.

---

## Communication Style

**Be specific.** Don't say "this function is too long." Say:
- "Extract Method: lines 42-58 into `validateShippingAddress()` because the function currently does three things (validate items, validate customer, calculate totals), and these can be tested independently."

**Lead with impact.** Why refactoring matters:
- "This change prevents bugs because the function's length makes it hard to test edge cases in isolation."
- "This reduces coupling so the Order class can be changed without touching ShippingCalculator."
- "This makes the next feature 2x faster to implement because the code is already split into reusable pieces."

**Provide locations.** File paths and line ranges, not vague references:
- ✅ `/src/OrderProcessor.ts` lines 42-58
- ❌ "somewhere in OrderProcessor"

**Estimate effort.** How much work is this refactoring?
- Low: IDE rename, extract method, simple moves (same file/class)
- Medium: Cross-file moves, parameter changes, new classes
- High: Architectural changes, multi-file restructuring, new patterns

**Mention prerequisites.** What must happen before this refactoring?
- "Prerequisite: Order class must have test coverage for calculateShipping()"
- "Prerequisite: Write characterization tests first (/legacy-code)"

---

## K-Line History

- Refactoring without tests creates more bugs than it fixes — always verify coverage first
- The Rule of Three prevents premature abstraction — don't refactor duplication until you see three instances
- Mixing refactoring with feature work makes failures ambiguous — separate the two into distinct commits

---

## Related Skills

- **/clean-code-review** — Comprehensive review after refactoring to verify improvement
- **/legacy-code** — When code has no tests: characterization tests, Boy Scout Rule
- **/tdd** — Tests first: the safety net that makes refactoring possible
- **/naming** — Intention-revealing names for extracted methods and classes
- **/functions** — One thing, single level of abstraction
- **/solid** — SOLID violations that refactoring fixes
- **/architecture** — Dependency direction, boundaries, layers
- **/components** — Cohesion and coupling metrics
