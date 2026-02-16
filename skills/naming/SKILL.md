---
name: naming
description: >-
  Analyze and improve naming in code. Activate when writing new code, reviewing
  existing code, renaming, refactoring, or doing code review. Also activate when
  the user mentions naming, unclear names, intent-revealing names, or readability.
  Every name is a chance to communicate or to confuse — when in doubt, activate.
model: opus
allowed-tools: Read, Grep, Glob, Edit, Write
delegates-to:
  - solid  # when noise-word class names reveal SRP violations
argument-hint: [code or file to analyze]
---

# Naming Skill — Operational Procedure

## Step 0: Detect Context

Before applying any naming guidance, detect the project's stack:

1. **Language detection:**
   - Check file extensions in scope: `*.php`, `*.ts`, `*.tsx` (PHP/TypeScript-first). Also support `*.py`, `*.go`, `*.rb`, `*.java`, `*.rs`, etc.
   - Read a representative file to confirm language and style
2. **Build system and testing detection:**
   - Check for build markers: `composer.json` (PHP), `package.json` (TypeScript/Node), `phpunit.xml` (PHP), `jest.config.*` or `vitest.config.*` (TypeScript)
   - Check for `.env`, `tsconfig.json`, root-level config files
   - Grep for language imports: `use` statements (PHP), `import` statements (TypeScript)
3. **Convention detection:**
   - Read existing code to identify naming conventions already in use
   - Check for a linter config (`.eslintrc`, `.php-cs-fixer.php`, `phpstan.neon`, `.editorconfig`)
   - Check for a style guide or CONTRIBUTING.md
   - For PHP: check for PSR-12 compliance. For TypeScript: check for TypeScript strict mode.

All subsequent naming advice MUST use the detected language's casing, idioms, and conventions. For PHP: use PSR-12 (camelCase methods, PascalCase classes, snake_case database columns). For TypeScript: use camelCase functions/variables, PascalCase classes/types.

---

## Step 1: Generate Context-Specific Rules

Based on the detected stack, adapt the universal naming principles to concrete rules:

| Principle | Adapt to... |
|-----------|-------------|
| Parts of speech | **PHP**: `isEmpty()`, `hasPermission()`, `isActive()` (camelCase methods). **TypeScript**: `isLoading`, `hasError`, `canSubmit` (camelCase). PHP classes: descriptive method names like `getUserById()`, `validateEmail()` |
| Scope-length | **PHP**: Methods in classes descriptive. **TypeScript**: Function names short and clear, descriptive for complex operations |
| Encodings | TypeScript generics make encodings unnecessary (`List<User>` is clear). PHP type hints in PHP 8+ also make Hungarian notation absurd. |
| Noise words | **PHP**: Don't say `UserService` if it's in `Services/`. **TypeScript**: Don't say `UserHelper` if it's in `utils/`. Use the module structure. |

---

## Step 2: Apply Decision Rules

### Rule 1: Intent Revelation

- **WHEN to apply:** Every name, every time. No exceptions.
- **WHEN NOT:** Never skip this one.
- **Decision test:** Cover the implementation. Read only the name. Can you explain what this thing does to a colleague? If no → rename.
- **Verification:** `grep` for the name — at every call site, does the code read like prose without needing to jump to the definition?

### Rule 2: No Disinformation

- **WHEN to apply:** Any name that could be misread. Especially return types, collection names, boolean names.
- **WHEN NOT:** Internal helper variables with 2-line scope where the context makes meaning unambiguous.
- **Decision test:** Does the name promise X but deliver Y? Does `getMonths()` return month objects, month numbers, or month name strings?
- **Severity:** RED FLAG — disinformation is the most expensive naming bug. A misleading name costs more than a missing name.
- **Verification:** Read the function signature + body. Does the return type match what the name implies?

### Rule 3: Pronounceability

- **WHEN to apply:** Any name that will be discussed in code reviews, standups, pair programming.
- **WHEN NOT:** Auto-generated code, protobuf field names, wire protocol fields where the name is dictated by an external spec.
- **Decision test:** Say the name out loud in a sentence. If you can't, or you pause to spell it, rename.
- **Verification:** Say "The `<name>` handles..." — does it sound natural?

### Rule 4: Searchability

- **WHEN to apply:** Any name in a scope larger than 3 lines.
- **WHEN NOT:** Loop variables in 1-3 line bodies (`for i in range(3)`), lambda parameters in single-expression lambdas.
- **Decision test:** `grep -r "name" .` — do you get the thing you're looking for, or 500 false positives?
- **Verification:** Run the grep. If the name is a common English word, it needs qualification.

### Rule 5: Scope-Length Proportionality

- **WHEN to apply:** Always, but the direction reverses for variables vs functions:

| Thing | Short scope → | Long scope → |
|-------|--------------|-------------|
| Variable | Short name OK (`e`, `i`) | Long descriptive name required |
| Function (public) | Short convenient name (`save()`) | — |
| Function (private) | — | Long explanatory name (`tryReconnectWithBackoff()`) |

- **WHEN NOT:** When the project has established a convention that contradicts this (e.g., a math library where `x`, `y`, `z` are conventional even at class scope).
- **Verification:** Check the distance between declaration and usage. If > 10 lines, the name should be self-documenting.

### Rule 6: Correct Parts of Speech

- **WHEN to apply:** All names.
- **WHEN NOT:** When the language has conventions that override (e.g., PHP magic methods like `__get()`, TypeScript getters with `get propertyName()`).

| Thing | PHP Examples | TypeScript Examples | Red flag |
|-------|------------------|-----------------|----------|
| Class/type | `User`, `OrderValidator`, `PaymentGateway` | `UserProfile`, `OrderForm`, `type User` | Verb name on a class |
| Method/function | `validateOrder()`, `processPayment()`, `getUserById()` | `handleSubmit()`, `fetchUser()`, `calculateTotal()` | Noun name on a function that does work |
| Boolean | `isActive()`, `hasPermission()`, `canEdit()` | `isLoading`, `hasError`, `shouldRender` | Non-predicate name on a boolean |
| Constant/enum | `const MAX_RETRIES`, `Status::PENDING` | `const RETRY_LIMIT`, `enum Color` | Verb name on a constant |

- **Verification:** Read `if <boolean_name>` — does it form a grammatical English sentence? (E.g., "if user isActive" works; "if user validate" doesn't.)

---

## Step 3: Review Checklist

Run against every name in scope. Each item has a severity and verification test.

| # | Check | Look for | Severity | Verification |
|---|-------|----------|----------|-------------|
| 1 | Name says wrong thing | Return type doesn't match name implication | 🔴 Red flag | Read function body, compare to name |
| 2 | Cryptic abbreviation | `pcguda`, `txnMgr`, `dt` in long scope | 🔴 Red flag | Can you say it in a sentence? |
| 3 | Noise word class name | `UserManager`, `DataProcessor`, `Helper`, `Utils` | 🟡 Warning | Ask: what does this class actually DO? Name it that. |
| 4 | Wrong part of speech | Function named as noun, boolean without predicate | 🟡 Warning | Read the call site as a sentence |
| 5 | Encoding/prefix | `m_`, `I`-prefix, Hungarian, type suffix | 🟡 Warning | Does the language/IDE already provide this info? |
| 6 | Scope mismatch | Single letter in 50-line scope, 40-char name in 3-line loop | 🟢 Good sign to fix | Measure declaration-to-usage distance |
| 7 | Unsearchable | Common word without qualification | 🟢 Good sign to fix | `grep -rn "name" .` — count false hits |

---

## Step 4: Refactoring Patterns

For each pattern: identify the problem in the PROJECT'S language, show before/after using the project's actual syntax.

### Pattern: Reveal Intent (cryptic → descriptive)

**Problem:** Name requires reading implementation to understand.
**Steps:**
1. Read the function/variable body
2. Write a one-sentence description of what it does
3. Turn that sentence into a name using the language's conventions
4. Rename across all call sites (IDE rename or `grep` + `sed`)
5. Run tests

### Pattern: Fix Disinformation (misleading → accurate)

**Problem:** Name implies different behavior than implementation delivers.
**Steps:**
1. Document what the function actually returns/does
2. Either rename to match behavior, or fix behavior to match name (ask which — this is a design decision)
3. Check all callers — some may depend on the "wrong" behavior
4. Run tests

### Pattern: Kill Noise Words (vague → specific)

**Problem:** Class/module named `Manager`, `Helper`, `Utils`, `Service`, `Handler`, `Processor`.
**Steps:**
1. List the class's public methods
2. Identify the common theme — what is this class's single responsibility?
3. Name it after that responsibility
4. If no single responsibility exists, this is a class decomposition problem, not just naming — flag for `/solid` skill
5. Run tests

### Pattern: Extract Boolean Predicate

**Problem:** Boolean variable without predicate prefix, or confusing negation.
**Steps:**
1. Identify all booleans in scope
2. Rename to `is_`, `has_`, `can_`, `should_` + positive condition (adapted to language convention)
3. Eliminate double negatives (`!isNotEmpty` → `isEmpty`)
4. Run tests

---

## When NOT to Apply This Skill

Ignore naming rigor in favor of pragmatism when:

- **Prototyping/spike:** You're exploring an approach and the code will be rewritten. Use TODO comments on bad names instead.
- **Generated code:** Protobuf, OpenAPI codegen, ORM migrations — rename at the boundary, not in the generated files.
- **External API conformance:** Your name must match an external spec (wire protocol, third-party SDK field names). Wrap with a better name at your boundary.
- **Team velocity vs. perfection:** A `Handler` that the whole team knows and has 200 call sites isn't worth a bulk rename during a sprint. Track it as tech debt.
- **Micro-scope:** A 2-line lambda's parameter name doesn't need 20 characters.

---

## K-Line History (Lessons Learned)

> This section should grow over time with actual project experience.

### What Worked
- **PHP**: Renaming a vague `process()` to `validateAndRouteOrder()` made three bugs immediately visible — callers were passing unvalidated data.
- **TypeScript**: Extracting complex logic into a named helper function made its purpose clear and testable in isolation.
- Adopting the rule "if grep gives >10 false positives, the name needs qualification" caught naming issues before code review.
- Using language-specific boolean conventions (`hasPermission()` in PHP, `isLoading` in TypeScript) eliminated an entire class of review comments.

### What Failed
- Aggressive renaming in a legacy PHP codebase without full test coverage caused runtime failures due to string-based method calls or dynamic property access.
- **TypeScript**: Renaming properties without updating type definitions or interfaces caused TypeScript errors in consuming code.
- Renaming database column accessors without updating the mapping layers caused silent data mismatches.
- Over-long method names in hot-path financial calculations reduced readability — `calculateCompoundInterestWithMonthlyCompounding` was worse than `compoundInterest` when the calculation method is documented elsewhere.

### Edge Cases
- **PHP database mapping**: Column name mapping may not match method names in database abstraction layers. Document the mapping.
- **TypeScript with generic types**: Generic names like `Container`, `Wrapper`, `Layout` are fine IF they're structural, not behavioral. But behavioral names must be specific.
- Domain abbreviations that ARE the name: `DNS`, `URL`, `HTML`, `SSR`, `JWT` — don't expand these, they're more recognizable abbreviated. Same in PHP/TypeScript contexts.
- Teams with mixed language backgrounds: what's "pronounceable" varies. Default to full English words, especially in international teams.

---

## Communication Style

When recommending name changes:

1. **Show before/after** in the project's actual language and file
2. **Estimate effort:** "This is a safe IDE rename" vs "This touches 47 files and needs careful testing"
3. **Prioritize:** Fix disinformation first (🔴), then cryptic names in wide scope, then noise words
4. **Be direct about tradeoffs:** "This name is bad but it's in generated code — rename at the boundary instead"
5. **Batch related renames:** If three names in the same module are bad, present them together
