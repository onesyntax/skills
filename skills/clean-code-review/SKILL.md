---
name: clean-code-review
description: >-
  Comprehensive code review against all Clean Code principles from Uncle Bob's teachings.
  Activates after completing implementation tasks, before marking work as done, before
  committing code, or when the user mentions review, quality check, clean code review,
  code quality, or wants to verify code meets standards.
allowed-tools: Read, Grep, Glob
argument-hint: [file or directory path]
---

# Clean Code Review

Comprehensive code review against all Clean Code principles. This is the final quality gate — code is NOT complete until this review passes with no critical issues.

For full review walkthroughs with before/after examples, read `references/extended-examples.md`.

## When to Activate

- After ANY code modification task is completed
- Before marking ANY implementation work as "done"
- Before committing code
- After TDD cycles complete
- After refactoring

## Review Philosophy

Clean code is code that is easy to read, understand, and modify. The ratio of time spent reading versus writing code is well over 10 to 1. Every review decision should optimize for readability first, because that's what developers spend most of their time doing.

A review is not a gatekeeping exercise — it's a collaborative quality check. The goal is to catch issues early, when they're cheap to fix, not to prove the code is bad.

---

## The Review Checklist

Work through each dimension. For dimensions covered by dedicated skills, delegate to that skill for deep analysis.

### 1. Naming
**Delegate to `/naming` for deep analysis.**

- Names reveal intent — you can understand what something does without reading the implementation
- No disinformation or misleading names
- Meaningful distinctions (not number-series like `a1, a2` or noise words like `data, info`)
- Pronounceable and searchable names (no magic numbers or strings)
- No encodings (Hungarian notation, member prefixes)
- Class names are nouns, method names are verbs
- One word per concept, consistent vocabulary

### 2. Functions
**Delegate to `/functions` for deep analysis.**

- Functions are small (under 20 lines ideal)
- Functions do ONE thing
- One level of abstraction per function
- Step-down rule followed (high to low abstraction)
- Few arguments (0-2 ideal, 3 suspicious, more than 3 requires justification)
- No flag arguments
- No side effects
- Command-query separation maintained
- Prefer exceptions to error codes
- DRY — no duplication

### 3. Classes and Objects
**Delegate to `/solid` for deep analysis.**

- Classes are small (single responsibility)
- High cohesion — methods use most instance variables
- Low coupling — minimal dependencies on other classes
- SOLID principles followed (SRP, OCP, LSP, ISP, DIP)
- Proper encapsulation — implementation details hidden
- Law of Demeter respected — don't talk to strangers

### 4. Error Handling

- Use exceptions, not return codes
- Write try-catch-finally first when dealing with operations that can fail
- Provide context with exceptions — enough information for the caller to understand what went wrong
- Define exception classes by the caller's needs, not by the source of the error
- Don't return null — use special case objects, empty collections, or optionals
- Don't pass null — validate inputs at boundaries instead

### 5. Comments

Code should be self-documenting. Comments are a last resort — they compensate for failure to express intent in code.

**Acceptable comments:** legal headers, informative (regex explanations), intent clarification, warnings, TODOs

**Red flags:** redundant comments that repeat the code, misleading comments, commented-out code (delete it — version control remembers), noise comments (`// default constructor`), journal comments, position markers (`// END SECTION`)

### 6. Formatting

- Consistent style throughout the codebase
- Vertical openness between concepts (blank lines separate thoughts)
- Vertical density for related code (no unnecessary blank lines within a concept)
- Variable declarations close to usage
- Dependent functions vertically close, caller above callee
- Reasonable line length (under 120 characters)
- Horizontal alignment only when it genuinely aids readability

### 7. Tests
**Delegate to `/tdd` for deep analysis.**

- Tests exist for all functionality
- Tests follow FIRST: Fast, Independent, Repeatable, Self-validating, Timely
- One concept per test
- Adequate coverage of edge cases and error paths
- Tests are readable — they tell a story (Arrange, Act, Assert)

### 8. Architecture
**Delegate to `/architecture` for deep analysis.**

- Clear separation of concerns
- Dependencies point inward (toward business rules)
- Business logic isolated from frameworks and infrastructure
- Appropriate abstraction layers
- Boundaries properly defined between components

### 9. Design Patterns
**Delegate to `/patterns` for deep analysis.**

- Patterns used appropriately — solving a real problem, not showing off
- Pattern implementations are correct and complete
- No unnecessary complexity or premature abstraction

### 10. Professional Standards
**Delegate to `/professional` for verification.**

- Code demonstrates professional responsibility
- Quick, sure, repeatable proof that code works (tests)
- Code represents your best work — you'd be comfortable showing it to a colleague
- Knowledge is shared — others can understand and maintain the code

---

## Severity Classification

When reporting issues, classify by impact:

**CRITICAL** — Significantly impacts maintainability or correctness. Must fix before the code can be considered done. Examples: untested business logic, function doing 5 things, misleading names, null returns in public APIs.

**WARNING** — Should be addressed but won't cause immediate problems. Examples: slightly long functions, imperfect names, missing edge-case tests.

**SUGGESTION** — Nice-to-have improvements. Examples: minor formatting inconsistencies, comments that could be clearer, slightly better name choices.

---

## The Review Mindset

### Start with Structure
Before diving into details, step back. Does the architecture scream its intent? Can you tell what the system does from the file and module structure? If you have to read code to understand what the system is for, the architecture has failed.

### Follow the Dependency Arrows
Trace dependencies. Do they point inward toward business rules, or outward toward infrastructure? Every outward-pointing dependency is a potential problem — it means business logic depends on a detail that could change.

### Read Functions as Prose
Read each function top to bottom. Does it tell a clear story? Can you understand what it does without scrolling? If you have to hold more than one concept in your head to understand a function, it's doing too much.

### Check the Tests Last
Tests are the specification. Read them after the production code. Do the tests tell you what the system does? Are there gaps — scenarios with no test coverage? Do the tests give you confidence to refactor?

---

## Common Review Mistakes

**Nitpicking formatting while ignoring design.** Catching a misaligned bracket while missing that a function has 8 parameters is prioritizing the wrong thing. Design issues first, formatting last.

**Reviewing too much at once.** Large reviews lead to rubber-stamping. If the changeset is too large, ask the author to break it into smaller pieces. A 500-line review catches 10x more issues than a 5000-line review.

**Accepting "it works" as sufficient.** Working code is the minimum bar, not the goal. The question is whether the code is maintainable, testable, and clear — whether it will still be easy to work with six months from now.

**Skipping tests.** If a review doesn't examine tests, it's not a review. Tests are half the codebase and the primary documentation of behavior.

**Being too gentle.** A review that finds zero issues is suspicious. Every piece of code can be improved. If you can't find anything, look harder — or question whether you're being thorough enough.

---

## Related Skills

- **/naming** — Naming analysis
- **/functions** — Function analysis
- **/solid** — SOLID principles and class design
- **/architecture** — Clean Architecture and boundaries
- **/tdd** — Test quality and TDD compliance
- **/patterns** — Design patterns
- **/acceptance-testing** — Acceptance test quality and testing pyramid
- **/components** — Component cohesion and coupling principles
- **/functional-programming** — Purity, immutability, side effect isolation
- **/legacy-code** — Boy Scout Rule, characterization tests
- **/professional** — Professional standards and responsibility
