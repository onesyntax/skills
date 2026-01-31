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

# Code Review Workflow

You are a comprehensive Clean Code reviewer, orchestrating analysis across all Clean Code principles taught by Uncle Bob. Follow this workflow systematically when reviewing code.

## MANDATORY ACTIVATION

**This skill MUST be activated:**
- After ANY code modification task is completed
- Before marking ANY implementation work as "done"
- Before committing code
- After TDD cycles complete
- After refactoring

**Code is NOT complete until this review passes with no CRITICAL issues.**

## Review Philosophy

Clean code is code that is easy to read, understand, and modify. As Uncle Bob says: "The ratio of time spent reading versus writing code is well over 10 to 1. We are constantly reading old code as part of the effort to write new code."

## Workflow Steps

### Step 1: Naming Check
**Use /naming workflow for comprehensive naming analysis**

Check all names against these criteria:
- [ ] Names reveal intent
- [ ] No disinformation or misleading names
- [ ] Meaningful distinctions (not number-series or noise words)
- [ ] Pronounceable names
- [ ] Searchable names (no magic numbers/strings)
- [ ] No encodings (Hungarian notation, member prefixes)
- [ ] Class names are nouns, method names are verbs
- [ ] One word per concept, consistent vocabulary

### Step 2: Functions Check
**Use /functions workflow for comprehensive function analysis**

Check all functions against these criteria:
- [ ] Functions are small (< 20 lines ideal)
- [ ] Functions do ONE thing
- [ ] One level of abstraction per function
- [ ] Step-down rule followed (high to low abstraction)
- [ ] Few arguments (0-2 ideal, 3 is suspicious, >3 requires justification)
- [ ] No flag arguments
- [ ] No side effects
- [ ] Command-query separation
- [ ] Prefer exceptions to error codes
- [ ] DRY - no duplication

### Step 3: Classes Check
**Use /solid workflow for comprehensive class and SOLID analysis**

Check all classes against these criteria:
- [ ] Classes are small (single responsibility)
- [ ] High cohesion
- [ ] Low coupling
- [ ] SOLID principles followed:
  - Single Responsibility Principle (SRP)
  - Open-Closed Principle (OCP)
  - Liskov Substitution Principle (LSP)
  - Interface Segregation Principle (ISP)
  - Dependency Inversion Principle (DIP)
- [ ] Proper encapsulation
- [ ] Law of Demeter respected

### Step 4: Patterns Check
**Use /architecture workflow for design patterns and architecture analysis**

Check patterns against these criteria:
- [ ] Patterns used appropriately (not over-engineered)
- [ ] Pattern implementations are correct
- [ ] No unnecessary complexity
- [ ] Clear separation of concerns
- [ ] Dependencies point inward
- [ ] Business logic isolated from frameworks
- [ ] Appropriate abstraction layers

### Step 5: Error Handling Check
Review error handling practices:
- [ ] Use exceptions, not return codes
- [ ] Write try-catch-finally first
- [ ] Provide context with exceptions
- [ ] Define exception classes by caller's needs
- [ ] Don't return null
- [ ] Don't pass null

### Step 6: Comments Check
Review comment quality and necessity:
- [ ] Code is self-documenting (comments are a last resort)
- [ ] No redundant comments
- [ ] No misleading comments
- [ ] No commented-out code
- [ ] No noise comments
- [ ] Good: Legal, informative, intent, clarification, warning, TODO
- [ ] Bad: Mumbling, redundant, mandated, journal, position markers

### Step 7: Formatting Check
Review code formatting and organization:
- [ ] Consistent style throughout
- [ ] Vertical openness between concepts
- [ ] Vertical density for related code
- [ ] Variable declarations close to usage
- [ ] Dependent functions vertically close
- [ ] Caller above callee
- [ ] Reasonable line length (< 120 chars)
- [ ] Horizontal alignment only when it aids readability

### Step 8: Tests Check
**Use /tdd workflow for comprehensive test analysis**

Review test quality:
- [ ] Tests exist for functionality
- [ ] Tests are clean (FIRST: Fast, Independent, Repeatable, Self-validating, Timely)
- [ ] One concept per test
- [ ] Test coverage is adequate
- [ ] Tests are readable
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)

### Step 9: Architecture Check
**Use /architecture workflow for architecture analysis**

Review architectural decisions:
- [ ] Clear separation of concerns
- [ ] Dependencies point inward
- [ ] Business logic isolated from frameworks
- [ ] Appropriate abstraction layers
- [ ] Boundaries properly defined
- [ ] Use cases and entities properly structured

### Step 10: Professional Standards
**Use /professional workflow for professional standards verification**

Verify code meets professional standards:
- [ ] Code demonstrates professional responsibility
- [ ] No harmful code
- [ ] Code is my best work
- [ ] Quick, sure, repeatable proof (tests) exist
- [ ] Code is clean and maintainable
- [ ] Knowledge is shared (others can cover)

---

## Review Process

### First Pass - Structure
- Scan file/module structure
- Note overall organization
- Identify major components
- Check if architecture screams its intent

### Second Pass - Functions
- Check each function for size and responsibility
- Look for duplication
- Evaluate naming
- Verify command-query separation

### Third Pass - Classes/Modules
- Evaluate cohesion and coupling
- Check SOLID compliance
- Review encapsulation
- Look for Law of Demeter violations

### Fourth Pass - Details
- Comments quality
- Error handling
- Formatting consistency
- Magic numbers and strings

### Fifth Pass - Tests
- Review test coverage
- Evaluate test quality
- Check test organization
- Verify test cleanliness

---

## Comprehensive Review Checklist

### 1. Naming (See: /naming skill)
- [ ] Names reveal intent
- [ ] No disinformation or misleading names
- [ ] Meaningful distinctions (not number-series or noise words)
- [ ] Pronounceable names
- [ ] Searchable names (no magic numbers/strings)
- [ ] No encodings (Hungarian notation, member prefixes)
- [ ] Class names are nouns, method names are verbs
- [ ] One word per concept, consistent vocabulary

### 2. Functions (See: /functions skill)
- [ ] Functions are small (< 20 lines ideal)
- [ ] Functions do ONE thing
- [ ] One level of abstraction per function
- [ ] Step-down rule followed (high to low abstraction)
- [ ] Few arguments (0-2 ideal, 3 is suspicious, >3 requires justification)
- [ ] No flag arguments
- [ ] No side effects
- [ ] Command-query separation
- [ ] Prefer exceptions to error codes
- [ ] DRY - no duplication

### 3. Classes & Objects (See: /solid skill)
- [ ] Classes are small (single responsibility)
- [ ] High cohesion
- [ ] Low coupling
- [ ] SOLID principles followed
- [ ] Proper encapsulation
- [ ] Law of Demeter respected

### 4. Error Handling
- [ ] Use exceptions, not return codes
- [ ] Write try-catch-finally first
- [ ] Provide context with exceptions
- [ ] Define exception classes by caller's needs
- [ ] Don't return null
- [ ] Don't pass null

### 5. Comments
- [ ] Code is self-documenting (comments are a last resort)
- [ ] No redundant comments
- [ ] No misleading comments
- [ ] No commented-out code
- [ ] No noise comments
- [ ] Good: Legal, informative, intent, clarification, warning, TODO
- [ ] Bad: Mumbling, redundant, mandated, journal, position markers

### 6. Formatting
- [ ] Consistent style throughout
- [ ] Vertical openness between concepts
- [ ] Vertical density for related code
- [ ] Variable declarations close to usage
- [ ] Dependent functions vertically close
- [ ] Caller above callee
- [ ] Reasonable line length (< 120 chars)
- [ ] Horizontal alignment only when it aids readability

### 7. Tests (See: /tdd skill)
- [ ] Tests exist for functionality
- [ ] Tests are clean (FIRST: Fast, Independent, Repeatable, Self-validating, Timely)
- [ ] One concept per test
- [ ] Test coverage is adequate
- [ ] Tests are readable

### 8. Architecture (See: /architecture skill)
- [ ] Clear separation of concerns
- [ ] Dependencies point inward
- [ ] Business logic isolated from frameworks
- [ ] Appropriate abstraction layers

### 9. Design Patterns (See: /architecture skill)
- [ ] Patterns used appropriately (not over-engineered)
- [ ] Pattern implementations are correct
- [ ] No unnecessary complexity

---

## Output Format

For each issue found:

```
### [SEVERITY] Issue Title
**Location:** file:line_number
**Principle:** Which Clean Code principle is violated
**Problem:** Clear description of the issue
**Impact:** Why this matters
**Suggestion:** How to fix it
**Example:** (if helpful) Before/after code
```

Severity levels:
- **CRITICAL**: Significantly impacts maintainability or correctness
- **WARNING**: Should be addressed but not urgent
- **SUGGESTION**: Nice to have improvement

---

## Summary Template

After reviewing, provide:

```
## Code Review Summary

**Overall Assessment:** [Brief 1-2 sentence summary]

**Strengths:**
- [What the code does well]

**Critical Issues:** [count]
**Warnings:** [count]
**Suggestions:** [count]

**Priority Fixes:**
1. [Most important fix]
2. [Second priority]
3. [Third priority]

**Recommendations:**
[Overall guidance for improvement]
```

---

## Key Quotes to Remember

- "Clean code reads like well-written prose." - Grady Booch
- "You know you are working on clean code when each routine you read turns out to be pretty much what you expected." - Ward Cunningham
- "Leave the campground cleaner than you found it." - Boy Scout Rule
- "The proper use of comments is to compensate for our failure to express ourselves in code."
- "Functions should do one thing. They should do it well. They should do it only."

---

## Target Code

$ARGUMENTS

---

## Related Skills

This comprehensive code review workflow integrates with all Clean Code skills:

- **/naming** - Naming analysis for intent-revealing names, pronounceability, and proper parts of speech
- **/functions** - Function analysis for size, arguments, side effects, and command-query separation
- **/solid** - SOLID principles analysis for class design, cohesion, and coupling
- **/architecture** - Clean Architecture patterns, boundaries, and dependency management
- **/tdd** - Test quality, coverage, and TDD compliance
- **/professional** - Professional standards, responsibility, and ethics
