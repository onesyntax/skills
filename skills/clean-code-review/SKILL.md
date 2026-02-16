---
name: clean-code-review
description: >-
  Comprehensive code review across 10 dimensions (Naming, Functions, Classes, Error Handling,
  Comments, Formatting, Tests, Architecture, Patterns, Professional Standards). Coordinates
  specialized skills for deep analysis. Final quality gate: code must pass with no critical issues.
allowed-tools: Read, Grep, Glob
argument-hint: [file or directory path]
model: opus
delegates-to: [naming, functions, solid, tdd, architecture, patterns, components, functional-programming, acceptance-testing, legacy-code, professional]
---

# Clean Code Review (Operational)

Comprehensive code review against Clean Code principles. **Final quality gate** — code is NOT complete until review passes with no critical issues.

This skill is a COORDINATOR. It detects change scope, delegates to specialized skills for deep analysis, and produces a structured review report. It enforces the quality gate (no CRITICAL issues = pass).

---

## When to Activate

- After ANY code modification task is completed
- Before marking ANY implementation work as "done"
- Before committing code
- After TDD cycles complete
- After refactoring
- User mentions: review, quality check, code quality, verify standards

## When NOT to Apply

- Trivial changes (1-2 line fixes, typo corrections)
- Generated code (scaffolding, schema generators, transpiled output)
- Third-party vendor code or dependencies
- Configuration files with no business logic
- Single-file, single-function changes under 10 lines (use `/naming` or `/functions` inline instead)

---

## Step 0: Detect Context

Before starting the review, gather context about the change:

**Detect Language & Framework**
- Primary language(s) in changed files
- Runtime (PHP, Node.js, Python, Java, Go, Rust, etc.)
- Language-specific idioms or testing approaches

**Detect Scope of Change**
- Count changed files
- Count lines changed (estimate: small <50, medium 50-500, large >500)
- Is this a new feature, refactor, bug fix, or configuration change?

**Detect Test Existence**
- Do test files exist for changed modules?
- Is coverage reasonable? (check test/src ratio, coverage reports if available)
- Are new tests present for new logic?

**Classify Change Size**
- **Small:** 1 file, <50 lines changed, single function or class
- **Medium:** 2-3 files, 50-500 lines, multiple functions or one new class
- **Large:** 4+ files, >500 lines, new module/feature, or architecture change

**Output of Step 0:**
```
Context: [Language] [Framework]
Scope: [small|medium|large] ([# files] files, [~# lines] lines)
Tests: [exist|missing] ([coverage info if available])
Change Type: [feature|refactor|bugfix|config]
```

---

## Step 1: Scope the Review

Apply review depth proportionally to change size.

**WHEN Small change:**
- Run inline checks only (naming, formatting, basic function checks)
- Skip delegation
- Complete in 5 minutes
- Checklist: items 1, 5, 6, 10 only

**WHEN Medium change:**
- Run inline checks on all 10 dimensions
- Delegate only to skills relevant to changed code (e.g., if functions changed → `/functions`, if classes changed → `/solid`)
- Complete in 15-30 minutes
- Checklist: all 10 items, selective delegation

**WHEN Large change (feature, architecture, new module):**
- Run full review across all 10 dimensions
- Delegate to ALL relevant skills
- Multiple review passes if needed (architecture first, then details)
- Complete in 30+ minutes
- Checklist: all 10 items, full delegation

**Output of Step 1:**
```
Review Depth: [inline-only|selective-delegation|full-delegation]
Dimensions to check: [list 1-10]
Skills to delegate to: [list if applicable]
Estimated Time: [5|15|30]+ minutes
```

---

## Step 2: Execute Review Dimensions

Work through each of the 10 dimensions (use checklist below as quick reference). For each, apply the **inline check**, then decide whether to **delegate for deep analysis**.

### Dimension 1: NAMING
**Severity:** 🔴 CRITICAL | **Inline Check:** Names clear and intent-revealing? No cryptic/misleading names (a1, data, temp)? Consistent vocabulary? | **Delegate `/naming` if:** 5+ names changed or touches public API | **Pass:** Clear intent-revealing names, no misleading vocabulary

### Dimension 2: FUNCTIONS
**Severity:** 🔴 CRITICAL | **Inline Check:** Functions <40 lines? 0-3 arguments? Each does ONE thing? No flag arguments or unwanted side effects? | **Delegate `/functions` if:** >40 lines, >3 args, or refactoring call sites | **Pass:** Small functions, 0-3 args, single purpose, no side effects

### Dimension 3: CLASSES & OBJECTS
**Severity:** 🔴 CRITICAL | **Inline Check:** Single responsibility? High cohesion? Low coupling? Clear encapsulation? | **Delegate `/solid` if:** New class or major refactor | **Pass:** Single responsibility, high cohesion, SOLID respected

### Dimension 4: ERROR HANDLING
**Severity:** 🔴 CRITICAL | **Inline Check:** No bare except/catch-all? No null returns? Exceptions carry context? | **Delegate:** Rarely needed | **Pass:** Exceptions not codes, no bare except, no null returns, input validation

### Dimension 5: COMMENTS
**Severity:** 🟡 WARNING | **Inline Check:** No commented-out code? Comments explain WHY not WHAT? | **Delegate:** Not needed | **Pass:** Self-documenting code, WHY comments only, no redundant comments

### Dimension 6: FORMATTING
**Severity:** 🟡 WARNING | **Inline Check:** Consistent indentation, line length <120 chars, vertical openness? | **Delegate:** Use formatter instead | **Pass:** Consistent style, reasonable line length

### Dimension 7: TESTS
**Severity:** 🔴 CRITICAL | **Inline Check:** Tests for new logic? Happy path AND error cases? Readable (AAA pattern)? Independent? | **Delegate `/tdd` if:** No tests for new code or <70% coverage | **Pass:** Tests for ALL new logic, happy path + errors, readable

### Dimension 8: ARCHITECTURE
**Severity:** 🟡 WARNING | **Inline Check:** File structure reveals intent? Dependencies inward? Clear boundaries? | **Delegate `/architecture` if:** New module or dependency rule violations | **Pass:** Clear separation of concerns, dependencies inward, boundaries defined

### Dimension 9: DESIGN PATTERNS
**Severity:** 🟡 WARNING | **Inline Check:** Patterns necessary (solving real problem)? Implemented correctly? | **Delegate `/patterns` if:** New pattern or uncertain correctness | **Pass:** Patterns solve real problems, correct implementation

### Dimension 10: PROFESSIONAL STANDARDS
**Severity:** 🟡 WARNING (🔴 if worse) | **Inline Check:** Best effort? Code no worse than before? Knowledge shared? | **Delegate `/professional` if:** Ethical concerns | **Pass:** Best work, no worse than before, maintainable

---

## Step 3: Produce Review Report

Generate a structured review report following this template:

```
## Code Review Report

**Date:** [date] | **Files:** [count] | **Type:** [feature|refactor|bugfix] | **Scope:** [small|medium|large]

### VERDICT: [PASS | PASS WITH WARNINGS | FAIL]

Critical Issues: [#] | Warnings: [#] | Suggestions: [#]

### CRITICAL ISSUES
[List: Dimension (X), File, Line, Issue, Action]

### WARNINGS
[List: Dimension (X), File, Issue, Suggestion]

### SUGGESTIONS
[List: Dimension (X), Brief note]

### QUALITY GATE DECISION

✅ PASS — No critical issues. Ready to commit.
⚠️ PASS WITH WARNINGS — No critical issues. Address warnings in follow-up PR.
❌ FAIL — Critical issues found. Must fix before merge.
```

---

## Step 4: Quality Gate

**PASS:** Zero CRITICAL issues
- Code is done
- Ready to commit

**PASS WITH WARNINGS:** Zero CRITICAL issues, 1+ WARNINGS
- Code is done
- Schedule follow-up PR to address warnings
- Document why warnings weren't critical

**FAIL:** 1+ CRITICAL issues
- Code is NOT done
- Fix critical issues
- Re-run review (may run Steps 2-3 only)

---

## Review Checklist (10 Dimensions)

Use this checklist to ensure all dimensions are covered:

| # | Dimension | Severity | Inline Check | Delegate To | Pass Criteria |
|---|-----------|----------|--------------|-------------|---------------|
| 1 | Naming | 🔴 CRITICAL | Scan for misleading/cryptic names | `/naming` if 5+ names changed | Clear, intent-revealing names; no misleading vocabulary |
| 2 | Functions | 🔴 CRITICAL | Check line count, arity, single responsibility | `/functions` if >40 lines or >3 args | Small (<40 lines), 0-3 args, ONE thing, no side effects |
| 3 | Classes | 🔴 CRITICAL | Check cohesion, coupling, SRP | `/solid` if new class or major refactor | Single responsibility, high cohesion, low coupling |
| 4 | Error Handling | 🔴 CRITICAL | Check for null returns, bare except, swallowed exceptions | (inline) | Exceptions (not codes), no bare except, no null returns |
| 5 | Comments | 🟡 WARNING | Check for commented-out code, redundancy | (inline) | No commented-out code, comments explain WHY |
| 6 | Formatting | 🟡 WARNING | Check indentation, line length, blank lines | (inline or use formatter) | Consistent style, reasonable line length, vertical openness |
| 7 | Tests | 🔴 CRITICAL | Check for test existence, coverage, readability | `/tdd` if no tests for new logic | Tests for ALL new logic, cover happy path + errors |
| 8 | Architecture | 🟡 WARNING | Check dependencies, separation of concerns, boundaries | `/architecture` if new module or major change | Dependencies point inward, clear boundaries |
| 9 | Patterns | 🟡 WARNING | Check for unnecessary or incorrect patterns | `/patterns` if new pattern introduced | Patterns solve real problems, correct implementation |
| 10 | Professional Standards | 🟡 WARNING (🔴 if worse) | Check Boy Scout Rule, knowledge sharing | `/professional` if ethical concerns | Code is best effort, no worse than before, maintainable |

---

## Refactoring Patterns for This Skill

This skill does NOT refactor code — it produces review reports and makes quality gate decisions. Key operational patterns:

**Triage Review:** Prioritize critical issues, defer suggestions. Fix CRITICALs, schedule WARNINGs in follow-up, mention SUGGESTIONs informally.

**Scoped Delegation:** Only delegate dimensions relevant to the change. Small function rename → `/naming` only. New class → `/solid` + `/components`. New feature → full delegation.

**Incremental Review:** For large PRs (500+ lines), review commit-by-commit or file-by-file to avoid missing issues. Apply Steps 0-3 for each logical group.

**Boy Scout Check:** Before finalizing review, ask: "Is this code cleaner than we found it?" If not, escalate to FAIL or WARNING.

**Delegation Report:** When delegating, include context in the report explaining why delegation occurred and what sub-skill should verify.

---

## K-Line History

**What Worked:**
- Detecting scope first (Step 0) prevents over-reviewing small changes
- Selective delegation based on change size prevents unnecessary context switching
- CRITICAL/WARNING/SUGGESTION triage focuses effort on real issues
- Structured report template ensures consistency and clarity

**What Failed:**
- Reviewing all 10 dimensions equally for 1-line changes wastes time
- Reviewing without detecting language/framework context leads to inapplicable advice
- Skipping tests during review misses major issues
- Nitpicking formatting while ignoring design wastes energy

---

## Communication Style

**Direct, operational, outcome-focused.**

- State findings concisely: "Dimension 2: `validateAndTransform()` is 65 lines doing 3 things. Refactor into 3 functions."
- Avoid vague criticism: ❌ "This doesn't feel clean" → ✅ "Function has 4 arguments; reduce to 2-3 by extracting object parameter."
- Use severity labels: 🔴 CRITICAL, 🟡 WARNING, 🟢 SUGGESTION
- Explain reasoning briefly: "Tests are CRITICAL because this is public API — callers depend on error behavior."
- Propose next steps: "Fix 2 CRITICAL issues, then re-run review on those files only."

---

## Related Skills

- **/naming** — Deep naming analysis and refactoring
- **/functions** — Function decomposition, arity, abstraction levels
- **/solid** — SOLID principles, class design, dependency injection
- **/architecture** — Clean Architecture, dependency rules, layer boundaries
- **/tdd** — Test quality, test-driven design, testing pyramid
- **/patterns** — Design pattern correctness and necessity
- **/components** — Component cohesion, coupling, dependency management
- **/functional-programming** — Purity, immutability, side effect isolation
- **/acceptance-testing** — Acceptance test quality, ATDD
- **/legacy-code** — Boy Scout Rule, characterization tests, strangulation
- **/professional** — Professional responsibility, estimation, ethical standards
