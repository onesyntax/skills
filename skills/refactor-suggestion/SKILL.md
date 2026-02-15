---
name: refactor-suggestion
description: >-
  Analyze code and provide specific, actionable refactoring suggestions based on
  Clean Code principles. Activates when code feels messy or hard to change, after
  implementation to improve code quality, or when the user mentions refactor,
  improve code, clean up, technical debt, or code smells.
allowed-tools: Read, Grep, Glob
argument-hint: [file path to analyze]
---

# Refactoring Suggestions

Analyze code and provide specific, actionable refactoring suggestions. This skill identifies what's wrong, explains why it matters, and recommends the appropriate Clean Code skill for detailed guidance.

For extended examples (full before/after refactoring walkthroughs), read `references/extended-examples.md`.

## Refactoring Workflow

1. **Ensure tests exist** — NEVER refactor without tests. If tests are missing, write characterization tests first (/legacy-code).
2. **Identify code smells** — scan for the patterns listed below
3. **Prioritize by impact** — critical bugs first, then maintainability, then readability, then polish
4. **Apply one refactoring at a time** — small, safe, reversible changes
5. **Run tests after each change** — if a test breaks, you changed behavior, not structure
6. **Verify with /clean-code-review** — confirm the refactoring actually improved things

---

## Code Smells Catalog

Code smells are symptoms that suggest deeper problems. They're not bugs — the code works — but they make the code harder to understand, change, and maintain.

### Bloaters — Things That Have Grown Too Large

**Long Function:** A function that does too many things. If you need to scroll to read it, or if you can identify sections that could be named, it's too long. Extract Method is the primary fix.

**Large Class:** A class with too many responsibilities, too many fields, or too many methods. If you can't describe what the class does in one sentence without using "and," it violates SRP. Extract Class.

**Long Parameter List:** More than 2-3 parameters signals that the function is doing too much, or that a group of parameters should be a single concept. Introduce Parameter Object or extract a method that derives the values.

**Data Clumps:** Groups of data that always appear together (city + state + zip, start + end dates). They should be their own object. If you remove one and the others don't make sense alone, it's a clump.

**Primitive Obsession:** Using primitives (strings, ints, booleans) where a domain object would be clearer. Money as integers, email as strings, status as magic numbers. Introduce value objects.

### Object-Orientation Abusers

**Switch/If Chains:** Long switch statements or cascading if-else chains that select behavior based on type. Replace Conditional with Polymorphism — let each type handle its own behavior.

**Refused Bequest:** A subclass that inherits methods it doesn't need or want. The class hierarchy is wrong. Replace Inheritance with Delegation, or restructure the hierarchy.

**Temporary Field:** Fields that are only set in some circumstances and null/empty otherwise. Extract Class for the fields and the code that uses them.

**Alternative Classes with Different Interfaces:** Two classes that do the same thing but have different method signatures. Rename Methods to align, or Extract Superclass/Interface.

### Change Preventers — Things That Make Change Hard

**Divergent Change:** One class is frequently changed for different reasons. If you change the class for database reasons AND for business rule reasons AND for display reasons, it has too many responsibilities. Extract Class by reason for change.

**Shotgun Surgery:** One change requires modifying many classes. The opposite of Divergent Change — a single responsibility is scattered across the codebase. Move Method and Move Field to consolidate.

**Parallel Inheritance Hierarchies:** Every time you add a subclass to one hierarchy, you have to add a subclass to another. Merge the hierarchies or use composition.

### Dispensables — Things That Can Be Removed

**Duplicate Code:** The same structure or logic in multiple places. Extract Method for duplicates within a class. Extract Class or Pull Up Method for duplicates across classes. The Rule of Three — if you see it three times, extract it.

**Dead Code:** Code that is never executed. Unreachable branches, unused variables, commented-out blocks, unused methods. Delete it. Version control remembers.

**Speculative Generality:** Code designed for "future use" that never arrives. Abstract classes with only one subclass. Parameters that are never varied. Hooks that are never hooked into. YAGNI — delete it until you actually need it.

**Lazy Class:** A class that doesn't do enough to justify its existence. If a class is just a thin wrapper with no added value, Inline Class.

**Comments as Deodorant:** Comments that explain what confusing code does, rather than the code being clear on its own. The fix is not to delete the comment — it's to refactor the code so the comment becomes unnecessary. Extract Method with an intention-revealing name.

### Couplers — Things That Create Excessive Dependencies

**Feature Envy:** A method that uses more data from another class than from its own. The method probably belongs in the other class. Move Method.

**Inappropriate Intimacy:** Two classes that access each other's private details excessively. They're too tightly coupled. Move Method, Extract Class, or Hide Delegate.

**Message Chains:** `a.getB().getC().getD().doSomething()` — a chain of calls that navigates the object graph. Violates the Law of Demeter. Hide Delegate or Extract Method.

**Middle Man:** A class that delegates almost everything to another class. If most methods just forward to a delegate, Remove Middle Man — let callers use the delegate directly.

---

## Refactoring Safety

### The Cardinal Rule

**NEVER refactor without tests.** Refactoring changes structure without changing behavior. The only way to prove behavior is preserved is to have tests that pass before AND after.

If tests don't exist:
1. Write characterization tests first (/legacy-code) — tests that capture current behavior
2. Only then refactor
3. If you can't write tests because the code is untestable, that's the FIRST refactoring: make the code testable

### Small Steps

Each refactoring should be a small, safe, reversible change. Extract one method. Rename one variable. Move one field. Run tests. Repeat.

Large refactorings are sequences of small refactorings. If you're making a large change all at once, you're not refactoring — you're rewriting. Rewriting is riskier and harder to validate.

### The Boy Scout Rule

Leave the code cleaner than you found it. You don't have to fix everything. You don't have to refactor the whole module. But when you touch code, improve it slightly. Over time, the codebase improves.

### When NOT to Refactor

**Don't refactor when you don't understand the code.** Refactoring requires understanding the behavior you're preserving. If you don't know what the code does, write characterization tests first.

**Don't refactor when you should rewrite.** If the code is so broken that incremental improvement won't help, a rewrite may be more practical. But rewrites are risky — consider the Strangler Fig pattern (/legacy-code).

**Don't refactor without a reason.** "The code is ugly" is not enough. What specific smell do you see? What specific problem does it cause? Refactoring is purposeful improvement, not cosmetic cleanup.

**Don't refactor in the middle of adding a feature.** Finish the feature first (get to green), THEN refactor. Mixing new behavior with structural changes makes it impossible to tell if a test failure is a refactoring mistake or a new bug.

---

## Refactoring Techniques

### Extract Method

The most common refactoring. Take a section of code and turn it into a named method.

**When:** You see a block of code that can be named — a comment explaining what the code does is a strong signal.

```
// Before
processOrder(order):
    // validate the order
    if order.items.isEmpty(): throw EmptyOrderError()
    if order.customer == nil: throw NoCustomerError()
    for item in order.items:
        if item.quantity <= 0: throw InvalidQuantityError(item)

    // calculate totals
    subtotal = 0
    for item in order.items:
        subtotal += item.price * item.quantity
    tax = subtotal * taxRate
    total = subtotal + tax

    // save and notify
    order.total = total
    repository.save(order)
    notifier.send(order.customer, "Order confirmed: $" + total)

// After
processOrder(order):
    validateOrder(order)
    total = calculateTotal(order)
    confirmOrder(order, total)
```

Each extracted method does one thing and has an intention-revealing name. The comments are now unnecessary — the method names say the same thing.

### Replace Conditional with Polymorphism

**When:** You see a switch statement or if-else chain that selects behavior based on type.

```
// Before — switch on type
calculatePay(employee):
    switch employee.type:
        SALARIED:  return employee.salary / 12
        HOURLY:    return employee.hoursWorked * employee.hourlyRate
        COMMISSION: return employee.basePay + employee.sales * employee.commissionRate

// After — each type knows how to calculate its own pay
interface Employee:
    calculatePay(): Money

SalariedEmployee implements Employee:
    calculatePay(): return salary / 12

HourlyEmployee implements Employee:
    calculatePay(): return hoursWorked * hourlyRate

CommissionEmployee implements Employee:
    calculatePay(): return basePay + sales * commissionRate
```

Adding a new employee type no longer requires modifying the switch statement (OCP).

### Introduce Parameter Object

**When:** Multiple parameters always travel together.

```
// Before — scattered parameters
searchEvents(startDate, endDate, minPrice, maxPrice, category, location):
    ...

// After — grouped into meaningful objects
searchEvents(dateRange, priceRange, filter):
    ...

DateRange = {start, end}
PriceRange = {min, max}
EventFilter = {category, location}
```

### Move Method / Move Field

**When:** A method uses more data from another class than its own (Feature Envy).

```
// Before — calculateShipping uses order data, not calculator data
ShippingCalculator:
    calculateShipping(order):
        weight = order.totalWeight()
        distance = order.destination.distanceFrom(warehouse)
        return weight * distance * ratePerKgKm

// After — the method belongs with the data it uses
Order:
    calculateShipping(ratePerKgKm):
        weight = totalWeight()
        distance = destination.distanceFrom(warehouse)
        return weight * distance * ratePerKgKm
```

### Replace Magic Numbers/Strings with Constants

**When:** Literals appear in code without explanation.

```
// Before
if account.balance < 500: chargeFee(25)
if user.role == "ADM": grantFullAccess()
if retryCount > 3: throw TimeoutError()

// After
MINIMUM_BALANCE = 500
OVERDRAFT_FEE = 25
ADMIN_ROLE = "ADM"
MAX_RETRIES = 3

if account.balance < MINIMUM_BALANCE: chargeFee(OVERDRAFT_FEE)
if user.role == ADMIN_ROLE: grantFullAccess()
if retryCount > MAX_RETRIES: throw TimeoutError()
```

---

## Skill Routing

When you identify a specific type of problem, use the specialized skill for detailed guidance:

| Code Smell | Skill | What It Covers |
|------------|-------|----------------|
| Bad names | /naming | Intention-revealing names, conventions, avoiding misleading names |
| Long functions, too many parameters | /functions | Small functions, one thing, single level of abstraction |
| SRP/OCP/LSP/ISP/DIP violations | /solid | SOLID principles, class design |
| Missing or poor tests | /tdd | Red-Green-Refactor, test doubles, FIRST properties |
| Layer violations, wrong dependencies | /architecture | Dependency Rule, boundaries, Clean Architecture |
| Repeated structures needing patterns | /patterns | GOF patterns, when to apply, when NOT to apply |
| Module boundaries, deployment units | /components | Cohesion (REP/CCP/CRP), coupling (ADP/SDP/SAP) |
| Need acceptance tests before refactoring | /acceptance-testing | ATDD, fixtures, testing pyramid |
| Mutation, side effects, impure functions | /functional-programming | Pure functions, immutability, composition |
| Legacy code, no tests, afraid to change | /legacy-code | Characterization tests, Strangler Fig, Boy Scout Rule |
| Overall quality check after refactoring | /clean-code-review | Comprehensive review across all principles |

---

## Priority Order

Present refactoring suggestions in order of impact:

1. **Critical** — Bugs, race conditions, data corruption risks, security issues
2. **High** — Clear violations of Clean Code principles that actively impede maintenance
3. **Medium** — Improvements that would significantly help readability and changeability
4. **Low** — Polish: naming tweaks, minor restructuring, cosmetic improvements

For each suggestion, state the smell, the location, why it matters, and the specific technique to fix it. Don't just say "refactor this" — say "Extract Method: lines 42-58 into `validateShippingAddress()` because the function does three things."

---

## Related Skills

- **/clean-code-review** — Comprehensive review after refactoring to verify improvement
- **/legacy-code** — When code has no tests and you need to make it safe to refactor
- **/tdd** — Tests first — the safety net that makes refactoring possible
- **/professional** — The Boy Scout Rule and professional responsibility to improve code
