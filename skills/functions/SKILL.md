---
name: functions
description: >-
  Write and refactor clean functions following Uncle Bob's Clean Code principles.
  Activate whenever writing new functions, refactoring existing ones, reviewing
  code for function quality, or when the user mentions function size, arguments,
  side effects, extract method, or complexity. Functions are the first unit of
  organization above a line of code — if they're wrong, everything above them
  (classes, components, architecture) inherits the mess.
allowed-tools: Read, Grep, Glob
argument-hint: [code or file to analyze]
---

# Functions Skill

A function should be small, do one thing, and communicate its intent through its name. If a function needs a comment to explain what it does, the function is too complex or badly named. This skill covers writing clean functions and identifying dirty ones.

For detailed function decomposition walkthroughs, read `references/extended-examples.md`.

---

## The Core Rules

### 1. Keep Functions Small

The first rule: functions should be small. The second rule: they should be smaller than that.

**Target size:** 4-6 lines ideal. Under 20 acceptable. Over 20 is a red flag.

When functions are this small, if statements and while loops don't need braces — the body is a single function call with a descriptive name. Nested indentation disappears. You can't get lost in a 4-line function.

The worry about function call overhead is misplaced — a call takes a nanosecond. The real cost is in the time humans spend reading bloated functions.

### 2. Do One Thing (Extract Till You Drop)

A function should do one thing, do it well, and do it only.

**The definitive test:** If you can extract another function from it, the original was doing more than one thing. By definition. Keep extracting until you can't extract anymore.

Every pair of braces is an extraction opportunity. The end result: classes full of 4-line functions, each with a clear name, each doing exactly one thing.

A function that mixes levels of abstraction (string manipulation next to business logic, HTTP headers next to domain rules) is doing more than one thing.

### 3. One Level of Abstraction Per Function (Step-Down Rule)

Organize functions like a newspaper article: important stuff at the top, details at the bottom. Readers start at the top and read down until they've seen enough.

**Structure:**
1. Public methods at the top — they tell you what the class can do
2. Private methods below the publics that call them
3. Each level steps down one abstraction level
4. No backwards references — all calls point DOWN the listing

Each function should contain only one level of abstraction. High-level policy calls mid-level orchestration calls low-level detail.

### 4. Minimize Arguments

Arguments are liabilities, not assets. Every argument is something the reader must understand, remember, and get in the right order.

| Count | Name | Verdict |
|-------|------|---------|
| 0 | Niladic | Best |
| 1 | Monadic | Fine |
| 2 | Dyadic | OK, approaching sloppy |
| 3 | Triadic | Borderline sloppy — hard to remember order |
| 4+ | Polyadic | Almost always wrong |

**The cohesion test:** If 3+ arguments travel together, they probably belong in an object.

**Constructor arguments** follow the same rules. Prefer named setters or a Builder pattern over constructors with many arguments.

#### Arguments to avoid

**Boolean/flag arguments** loudly declare "this function does two things." Write two functions instead. Two booleans? The function does four things.

```
// Bad — what does true mean?
render(document, true)

// Good — say what you mean
renderForPrint(document)
renderForScreen(document)
```

**Output arguments** violate expectations — people expect data to go IN through arguments, not come OUT. Use return values instead.

**Null arguments** are disguised booleans — there's a path for null and a path for non-null. Write two functions: one that takes the argument, one that doesn't.

### 5. Command-Query Separation (CQS)

**Commands** change state, return void.
**Queries** return values, change nothing.

Never mix the two. When you see a void return, you know it has side effects. When you see a return value, you know it's safe to call without consequences.

Don't return error codes from commands — throw exceptions instead, keeping the convention that commands return void.

**Multi-threaded exception:** Sometimes you need to change state AND return the old value atomically. Use the Passing a Block pattern (see below).

### 6. No Side Effects

A side effect is a lie — your function promises to do one thing but secretly does another. When a function changes a variable that outlives the call (instance variable, global, file, database), that's a side effect.

Side effects create **temporal coupling** — functions that must be called in a specific order, but nothing in the code makes that order obvious. The system just fails if you get it wrong.

**Solution — the Passing a Block pattern:**

```
// Instead of open/close pair with temporal coupling:
open(file)
doStuff(file)
close(file)    // easy to forget

// Encapsulate the coupling:
withFile(file, (f) -> {
    doStuff(f)
})  // close happens automatically
```

### 7. Tell, Don't Ask

Tell objects what to do. Don't interrogate their state and make decisions for them — they know their own state and can decide for themselves.

```
// Bad — asking, then deciding (train wreck)
o.getX().getY().getZ().doSomething()

// Good — telling
o.doSomething()
```

Train wrecks violate the **Law of Demeter**: you may only call methods on objects that were passed as arguments, created locally, or are instance variables. You may NOT call methods on an object returned by a previous method call. That single chained line knows too much about the system's structure and couples you to all of it.

---

## Error Handling

Error handling is important, but if it obscures logic, it's wrong (Michael Feathers).

**Write error handling first.** Don't paint yourself into an implementation that can't handle errors.

### Key rules

**Exceptions over error codes.** Returning false, null, or -1 to signal errors is the horror of the 70s and 80s. Use exceptions.

**Prefer unchecked/runtime exceptions.** In languages that offer both checked and unchecked exceptions, prefer unchecked. The checked exception experiment failed — it creates reverse dependencies up the hierarchy, breaks OCP, and ruins independent deployability.

**Scope exceptions to classes.** Don't reuse canned exceptions. Create specific ones: `Stack.Overflow`, `Stack.Underflow`, `Stack.Empty`. The name should be so precise that no message is needed.

**Try block structure:**
1. `try` must be the first word in the function (after variable declarations)
2. The try body should contain a single function call
3. `catch`/`finally` are the last thing in the function

**Functions do one thing — error handling IS one thing.** A function should either do work OR handle errors, never both.

### The Null Object / Special Case Pattern

Often better than throwing: return a degenerate object that behaves appropriately for the edge case. A zero-capacity stack returns a ZeroCapacityStack where push overflows, pop underflows, size returns zero. No if-statements needed in calling code.

---

## Switch Statements

Switch statements (and long if-else chains) are a fan-out problem: each case depends on an external module, creating a knot of dependencies that ruins independent deployability.

**Two solutions:**

1. **Replace with polymorphism.** The switch argument becomes an abstract base class. Each case becomes a derived class. Create instances in a factory. Source code dependencies invert — subtypes depend upward on the base, not outward on externals.

2. **Isolate in the main partition.** Move switches to the factory/configuration layer where all dependencies already point toward the application. Main is a plug-in to the application.

---

## Structured Programming Notes

All algorithms compose from sequence, selection, and iteration — each with single entry and single exit.

**Early returns** are fine — they just jump to the exit. **Continue** is fine — it's a no-op to the bottom of the loop. **Break** is problematic — it creates an indirect, unexpressed exit condition. **Labeled break** is worse. But if your functions are 4 lines, these issues rarely arise.

---

## Refactoring Techniques

### Extract Method Object
When a function is too large and has too many shared variables to extract cleanly:
1. Convert the function into its own class
2. Pass original arguments to the constructor
3. Promote local variables to fields
4. Call an `invoke()` method
5. Now extract freely — all the "arguments" are fields

### Finding Hidden Classes
A large function with many variables used across different sections IS a class in disguise. The sections communicate through variables scoped to the whole function — those variables are fields, those sections are methods.

### Replacing Switch with Polymorphism
1. Identify the type code being switched on
2. Create abstract base class with a method for the operation
3. Each case becomes a derived class
4. Move case logic into the derived classes
5. Delete the switch; create instances in a factory

---

## Respect the Language's Idioms

The core function rules are universal. How a language expresses functions (free functions vs methods, error handling style, async patterns, closures) varies. Follow the established conventions of whatever language and project you're working in.

---

## When Writing Functions

Run this checklist before committing:

1. **Size** — Is it under 6 lines? Under 20 at worst? Can I extract more?
2. **One thing** — Can I describe what this function does without using "and" or "then"?
3. **Abstraction** — Is there only one level of abstraction? No string manipulation next to business logic?
4. **Arguments** — 0-2? No booleans? No output arguments? No nulls?
5. **CQS** — Does it either change state (void) or return a value, but not both?
6. **Side effects** — Does it only affect what its name promises?
7. **Name** — Is it a verb/verb phrase that reveals intent? (See `/naming` skill)

---

## When Reviewing Functions

### Process

1. Read the function and understand its purpose
2. Check size (target: 4-6 lines, max 20)
3. Count arguments (target: 0-2)
4. Check for flag/null/output arguments
5. Verify step-down rule (public → private, no backwards calls)
6. Check abstraction mixing
7. Look for side effects and temporal coupling
8. Check CQS compliance
9. Spot train wrecks and Law of Demeter violations
10. Review error handling (exceptions, try block structure)

### Severity levels

| Severity | Type | Example |
|----------|------|---------|
| Critical | Function does multiple things at mixed abstraction levels | Business logic interleaved with HTTP parsing |
| High | Function over 20 lines, or 3+ arguments | 50-line method with 4 parameters |
| Medium | Boolean arguments, CQS violation, train wreck | `render(doc, true, false)` |
| Low | Minor indentation issues, could extract one more level | 12-line function that could be 8 |

### Output Format

```
**Function:** `functionName`
**Location:** file:line
**Issue:** [Size/Arguments/Side Effects/CQS/etc.]
**Problem:** [Why this hurts readability or maintainability]
**Suggestion:** [Specific refactoring — extract method, split function, introduce object, etc.]
```

---

## Related Skills

- `/naming` — function names must be verbs that reveal intent
- `/solid` — functions are the building blocks that SOLID organizes
- `/patterns` — many patterns (Strategy, Template Method, Command) are about function-level design
- `/clean-code-review` — comprehensive review that includes function checks
