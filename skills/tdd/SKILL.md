---
name: tdd
description: >-
  Guide TDD workflow. Activate when implementing features, writing tests, fixing bugs,
  creating handlers/services/use cases, or when the user mentions test-first, TDD,
  red-green-refactor, failing test, or test-driven. TDD is the mandatory discipline
  for all feature work — activate proactively, not just when asked.
model: opus
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
delegates-to:
  - naming      # during REFACTOR phase
  - functions   # during REFACTOR phase
  - legacy-code # when retrofitting tests to existing codebase
argument-hint: [feature description]
---

# TDD Skill — Operational Procedure

## Step 0: Detect Context

Before writing any test, detect the project's testing stack:

1. **Language and build system:**
   - Check file extensions and build markers: **PHP/TypeScript-first** → `composer.json`, `package.json`. Also support `go.mod`, `Cargo.toml`, `pom.xml`, etc.
   - Read a representative source file to confirm language
2. **Test framework:**
   - **PHP**: Check for `phpunit.xml`, `tests/` directory, or `pest.xml` config
   - **TypeScript**: Check for `jest.config.*`, `vitest.config.*`, `*.test.ts`, `*.test.tsx`
   - Also check: `pytest.ini`, `*_test.go`, `Cargo.toml [dev-dependencies]`, `.rspec`
   - Read an existing test file to learn the project's test patterns
   - If no tests exist: check the package manager's default test runner and set up accordingly
3. **Test location convention:**
   - **PHP**: `tests/Unit/`, `tests/Feature/`, or co-located `*Test.php`
   - **TypeScript**: `__tests__/`, `*.test.ts`/`*.test.tsx` co-located with source
   - Match whatever the project already does
4. **Assertion style:**
   - Read existing tests: **PHP** uses `assertEquals`, `assertTrue`, `assertArrayHasKey`; **TypeScript** uses `expect().toBe()`, `expect().toHaveBeenCalled()`
   - Match the project's established assertion library
5. **Mock/stub tooling:**
   - **PHP**: PHPUnit's built-in mocks, or Mockery
   - **TypeScript**: Jest mocks, vi.mock (Vitest), testdouble
   - Identify dependency injection patterns already in use
6. **Run command:**
   - **PHP**: `./vendor/bin/phpunit`, or test runner configured in `composer.json`
   - **TypeScript**: `npm test`, `npm run test:watch`, `yarn test`
   - Identify how to run a single test file or test case

All subsequent test code MUST use the detected language's actual syntax, assertion style, and conventions.

---

## Step 1: Generate Context-Specific Rules

Adapt TDD mechanics to the detected stack:

| Concern | Adapt to... |
|---------|-------------|
| Test structure | **PHP**: PHPUnit test class with `test` methods. **TypeScript**: Jest `describe/it` blocks. Also support: pytest `def test_`, Go `func Test`, Rust `#[test]` |
| Assertions | **PHP**: `assertEquals`, `assertTrue`, `assertArrayHasKey`. **TypeScript**: `expect().toBe()`, `expect().toHaveBeenCalled()`. Match project's library. |
| Mocking | **PHP**: PHPUnit's `createMock()`, or Mockery. **TypeScript**: Jest/Vitest `vi.mock()`. Hand-roll only if no library exists. |
| File naming | **PHP**: `tests/Unit/UserRepositoryTest.php`, `tests/Feature/OrderProcessorTest.php`. **TypeScript**: `UserProfile.test.tsx`, `useCart.test.ts`. Match project convention. |
| Setup/teardown | **PHP**: `setUp()`, `tearDown()` in test class. **TypeScript**: `beforeEach`, `afterEach` in describe block. |
| Running | **PHP**: `./vendor/bin/phpunit`. **TypeScript**: `npm test -- --watch`. Single test command for fast feedback during the cycle. |

---

## Step 2: Execute the TDD Cycle

### Phase 0: Break Down the Feature

1. Read the feature/bug description
2. List acceptance criteria
3. Enumerate test cases, ordered simplest → most complex:
   - Degenerate cases first (null, empty, zero, single element)
   - Happy path
   - Edge cases
   - Error cases
4. Each test case should be writable in under 2 minutes

### Phase 1: RED — Write a Failing Test

**Decision rules:**

- **WHEN:** Always start here. No production code exists yet for this behavior.
- **WHEN NOT:** Never skip RED. If you're writing production code without a failing test, stop.
- **HOW:**
  1. Write ONE test for the next simplest case
  2. Run it — it MUST fail
  3. The failure message should clearly describe what's missing
  4. Stop writing test code the moment compilation fails or an assertion fails
- **Verification:** Test runner shows RED (failure). If the test passes immediately, it's testing nothing — delete it and write a real one.

**Techniques by situation:**

| Situation | Technique |
|-----------|-----------|
| Don't know where to start | **Assert First** — write the assertion, let errors guide you backward |
| Need infrastructure before real test | **Stair-Step** — write a test that just creates the class, then delete it after the real test works |
| Test could pass with a constant | **Triangulation** — write a second test that forces generalization |
| Collection behavior | **One-to-Many** — test singular case first, then generalize to collection |

### Phase 2: GREEN — Make It Pass

**Decision rules:**

- **WHEN:** Exactly one test is failing.
- **WHEN NOT:** If multiple tests fail, you jumped too far. Back up and make the previous test pass first.
- **HOW:**
  1. Write the MINIMUM code to make the test pass
  2. Fake it if needed — return a constant, use a trivial implementation
  3. Run the test — it MUST pass
  4. Do NOT add functionality beyond what the failing test demands
- **Verification:** All tests GREEN. If any test broke, you changed too much.
- **Time limit:** If GREEN takes more than 5 minutes, the RED step was too big. Delete the test, write a simpler one.

### Phase 3: REFACTOR — Clean Up

**Decision rules:**

- **WHEN:** All tests are GREEN. Always. Never skip this phase.
- **WHEN NOT:** If tests are RED, fix them first — don't refactor broken code.
- **HOW:**
  1. Clean BOTH production code AND test code
  2. Apply `/naming` — do all names reveal intent?
  3. Apply `/functions` — are functions small, single-purpose, low-argument?
  4. Remove duplication between test and production code
  5. Remove duplication between tests (extract shared setup, compose assertions)
  6. Run all tests after each refactoring move — stay GREEN
- **Verification:** All tests still GREEN. Code is cleaner than before. No behavior changed.

### Phase 4: REPEAT

Return to RED for the next test case. Cycle time target: 1-5 minutes per RED-GREEN-REFACTOR iteration.

**Getting stuck indicators:**
- Can't think of a small enough test → you're trying to test too much at once. Test a degenerate case.
- GREEN requires writing an entire algorithm → the RED test was too ambitious. Delete it, write something simpler.
- Lots of tests breaking during REFACTOR → tests are coupled to implementation, not behavior. Fix the tests.

---

## Step 3: Review Checklist

Run after the TDD cycle completes, before presenting work as done.

| # | Check | Look for | Severity | Verification |
|---|-------|----------|----------|-------------|
| 1 | Three Laws compliance | Production code written without failing test first | 🔴 Red flag | Check git history: test commit should precede implementation commit |
| 2 | Test tests behavior, not implementation | Test references private methods, internal data structures | 🔴 Red flag | Refactor internals without touching tests — do they still pass? |
| 3 | Missing degenerate cases | No tests for null, empty, zero, boundary values | 🔴 Red flag | List inputs: null, empty, 0, 1, MAX, negative — are they covered? |
| 4 | God Test | Single test with multiple Act-Assert sequences testing different behaviors | 🔴 Red flag | Count Act phases — if > 1, split into separate tests. Name each behavior independently. |
| 5 | AAA structure | Mixed Arrange-Act-Assert within a single behavior test | 🟡 Warning | Each test has exactly one Act section |
| 6 | F.I.R.S.T. violations | Slow test (I/O in unit test), test order dependency, non-deterministic | 🟡 Warning | Run tests in random order — do they all pass? |
| 7 | Mock overuse | Mocking within the same module, not across boundaries | 🟡 Warning | Draw the dependency boundary — mocks should only appear at the boundary |
| 8 | Test naming | Test name doesn't describe the scenario | 🟢 Improve | Read test name alone — do you know what it tests without reading the body? |
| 9 | Magic values | Raw numbers/strings in assertions without explanation | 🟢 Improve | Extract to named constants reflecting requirements |
| 8 | Magic values | Raw numbers/strings in assertions without explanation | 🟢 Improve | Extract to named constants reflecting requirements |

---

## Step 4: Refactoring Patterns

### Pattern: Extract Composed Assertion

**Problem:** Multiple physical asserts checking one logical state, repeated across tests.
**Steps:**
1. Identify assertion groups that always appear together
2. Extract into a named function: `assertHeatingState(hvac)`, `expectValidUser(response)`
3. The function name should describe the LOGICAL assertion, not the physical checks
4. Replace all occurrences
5. Run tests

### Pattern: Introduce Test Hierarchy

**Problem:** Growing `beforeEach`/`setUp` with code only some tests need.
**Steps:**
1. Group tests by the context they need (e.g., "when user is admin", "when cart is empty")
2. Create nested `describe`/`context` blocks (or equivalent in the test framework)
3. Move setup code to the appropriate level
4. Inner setup executes after outer setup
5. Run tests

### Pattern: Replace Mock with Fake (at boundary)

**Problem:** Complex mock setup that's brittle and hard to read.
**Steps:**
1. Identify the boundary being mocked
2. Create a simple in-memory fake implementing the same interface
3. Write tests for the fake itself
4. Replace mock with fake in tests
5. Run tests

### Pattern: Break Up God Test

**Problem:** Single test function with multiple Act-Assert sequences testing different behaviors.
**Steps:**
1. Identify each Act-Assert pair
2. Extract each into its own test function with a descriptive name
3. Move shared setup to `beforeEach`/`setUp`
4. Run tests — count should increase, coverage should stay the same

### Pattern: Decouple Test from Implementation

**Problem:** Tests break when refactoring internals (not changing behavior).
**Steps:**
1. Identify what the test is actually verifying — input → output? Side effect? State change?
2. Rewrite the test to verify through the public API only
3. Remove references to private/internal methods
4. If testing side effects: use a spy at the boundary, not deep inside
5. Run tests — refactor the internals — tests should still pass

---

## When NOT to Apply This Skill

Ignore strict TDD discipline when:

- **Spike/prototype:** You're exploring whether an approach is feasible. Write throwaway code, then rewrite with TDD once the design is clear. Never keep spike code.
- **Trivial glue code:** A one-line function that delegates to a well-tested library. Don't test the wrapper; test the behavior it enables.
- **UI layout/styling:** Pure visual concerns where the "test" is looking at the screen. Use snapshot tests or visual regression tools instead of unit TDD.
- **Framework-imposed patterns:** Some frameworks generate code with specific structure (Rails scaffolds, Django admin). Test the customized behavior, not the generated boilerplate.
- **Existing codebase with zero tests:** Don't try to retrofit TDD to the entire codebase. Use `/legacy-code` skill instead — add characterization tests, then apply TDD to new changes.
- **Performance-critical hot paths:** When you need to profile and optimize, you may need to write the implementation first, benchmark, then add tests to lock in the optimized behavior.

---

## K-Line History (Lessons Learned)

> This section should grow over time with actual project experience.

### What Worked
- **PHP**: Starting with degenerate test cases (empty list, null input) consistently uncovered missing guard clauses and edge cases before they became production bugs.
- **TypeScript**: Writing tests that verify return values and callbacks first made refactoring internals safe and fast.
- Keeping cycle time under 3 minutes made refactoring feel safe — you never lose more than 3 minutes of work.
- Writing test names as sentences — **PHP**: `testReturnsEmptyWhenNoItemsMatchFilter()`, **TypeScript**: `should return loading state when data is fetching` — served as living documentation.
- Using stair-step tests to bootstrap new modules eliminated "blank page" paralysis.

### What Failed
- Trying to TDD a complex algorithm top-down led to a 30-minute RED phase with no progress. Bottom-up (smallest subproblem first) worked better.
- **PHP**: Over-mocking database interactions without testing with a real in-memory database made tests pass but missed N+1 queries and transaction bugs.
- **TypeScript**: Over-mocking dependencies made tests pass but missed integration issues. Testing with real or near-real dependencies > mocking everything.
- Writing tests for generated code created a maintenance burden with near-zero value.
- Skipping the REFACTOR phase "just this once" always led to more skipping. The test suite became its own legacy code within weeks.

### Edge Cases
- **PHP event-driven systems:** The RED phase needs to test event dispatch and listeners. Use test doubles for events, but test the real event flow in integration tests.
- **TypeScript async/promises:** The RED phase often involves `waitFor()` or async/await to verify state updates. Use test utilities appropriate to the framework.
- **Database-dependent logic (PHP):** Use an in-memory SQLite database for tests or test transactions that roll back. Don't mock database interactions unless necessary — the mock won't catch relationship or query bugs.
- **Third-party API integration:** TDD the adapter interface, then use contract tests or recorded HTTP cassettes (VCR, MSW) for the real API. Don't TDD against a live external service.
- **TypeScript async/await:** TDD the sequential logic first, then add async tests as a separate concern. Test data fetching with mocked HTTP for predictable async behavior.

---

## Communication Style

When guiding TDD:

1. **Show the cycle:** Always show RED (failing test), GREEN (minimal code), REFACTOR (cleanup) — in the project's actual language and test framework
2. **Name the technique:** "I'm using Triangulation here because..." or "This is a stair-step test to bootstrap the class"
3. **Be direct about shortcuts:** "I'm skipping the test for this one-line delegation because..." (and explain why it's justified)
4. **Show test output:** Include the test run command and its pass/fail result
5. **Prioritize:** When reviewing existing tests, fix 🔴 issues first, then 🟡, then 🟢
