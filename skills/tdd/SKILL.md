---
name: tdd
description: >-
  Guide TDD workflow using Uncle Bob's Three Laws. Activate when implementing features,
  writing tests, fixing bugs, creating handlers/services/use cases, or when the user
  mentions test-first, TDD, red-green-refactor, failing test, or test-driven. TDD is
  the discipline that makes clean code possible — without it, refactoring is too risky
  and code rots.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature description]
---

# TDD Skill

Test-Driven Development is the discipline of writing tests before production code. It creates a rapid feedback loop that keeps code clean, provably correct, and safe to change. Without TDD, refactoring is too risky, and without refactoring, code rots.

**The Fundamental Principle:** As the tests get more specific, the code gets more generic. Each new test case makes the tests more specific; to pass each test, you generalize the production code. This is how algorithms emerge incrementally.

For detailed TDD cycle walkthroughs, read `references/extended-examples.md`.

---

## The Three Laws of TDD

These laws are disciplines that must be followed like a doctor washing hands before surgery:

**First Law:** You are not allowed to write any production code until you have first written a failing unit test.

**Second Law:** You are not allowed to write more of a unit test than is sufficient to fail, and not compiling is failing.

**Third Law:** You are not allowed to write more production code than is sufficient to pass the currently failing test.

Following all three laws locks you into a cycle approximately 20-30 seconds long: little test, little code, little test, little code. Everything always worked a minute or so ago.

---

## The Red-Green-Refactor Cycle

### Step 1: Understand the Feature

- Analyze what behavior needs to exist
- Identify the acceptance criteria
- Break down into testable increments

### Step 2: List Test Cases

- Enumerate all scenarios that need testing
- Start with degenerate cases (null, empty, single element)
- Progress to more complex scenarios
- Order from simplest to most complex

### Step 3: RED — Write Failing Test

- Write a small test for the next increment
- Run the test to see it fail
- The failure message should clearly indicate what's missing
- **Do not write production code yet**
- Stop as soon as any test fails (including compilation errors)

### Step 4: GREEN — Write Minimum Code

- Write ONLY enough production code to make the test pass
- Use "fake it till you make it" — return constants, use trivial implementations
- Don't worry about elegance — just make it pass
- Run the test to see it pass
- **Do not add extra functionality**

### Step 5: REFACTOR — Clean Up

- Clean up both production code AND test code
- Apply `/naming` principles for clear, intention-revealing names
- Apply `/functions` principles for proper function structure
- Remove duplication
- Run tests to ensure they still pass
- **Only restructure, don't add features**
- Refactoring never appears on a schedule — you do it all the time

### Step 6: Repeat

- Return to Step 3 for the next test case
- Continue until all scenarios are covered
- Cycle time should be seconds to minutes, not hours

### Example Cycle

```
// RED: Write failing test
test "returns empty for zero":
    assert fizzBuzz(0) == ""
// Run: FAIL — fizzBuzz is not defined

// GREEN: Minimal passing code
fizzBuzz(n):
    return ""
// Run: PASS

// RED: Next test
test "returns '1' for 1":
    assert fizzBuzz(1) == "1"
// Run: FAIL — expected "1", got ""

// GREEN: Make it pass
fizzBuzz(n):
    if n == 0: return ""
    return toString(n)
// Run: PASS

// REFACTOR: (nothing to refactor yet — continue cycle)
```

---

## TDD Techniques

### Fake It Till You Make It

Make a test pass by returning a constant (faking it). Then the next test forces you to fake less. Continue until you're not faking anymore. Making incremental progress toward a goal is not wasting time — it's how you save time.

### Stair-Step Tests

Write a test just to enable writing the next test — then delete it once it's served its purpose. Like digging stairs to reach the bottom of a hole. Example: first test creates the class, second test calls a method, third test actually tests behavior.

### Assert First

Write the test backwards, starting with the assert. Let compiler errors guide you to create what's needed. Forces you to think about the desired outcome first.

### Triangulation

Write two tests that force you to generalize. First test can be passed with a constant. Second test requires actual logic. Used to drive generalization of production code.

### One-to-Many

Implement operations on collections by first implementing for a single object. Make it work in the singular case first, then generalize to the plural case.

### Getting Stuck

**Signs:** Nothing incremental you can do to pass the test. You have to write the whole algorithm at once.

**Causes:** Wrote the wrong test (went for the gold too early). Making production code too specific. Not approaching from outside in.

**Solutions:** Start with degenerate test cases (null, empty, single element). Test peripheral issues first (validation, simple queries). Avoid complicated test cases until simple ones are exhausted. Engage as few brain cells as possible at any given moment.

---

## Clean Test Principles

### F.I.R.S.T. Properties

Tests should be:

- **Fast**: Tests should run quickly (thousands of tests in seconds)
- **Independent**: Tests should not depend on each other
- **Repeatable**: Tests should produce the same results every time
- **Self-validating**: Tests should have a boolean output — pass or fail
- **Timely**: Tests should be written before the production code

### The Single Assert Rule (AAA / Triple-A)

Every test should have ONE logical assertion following ONE logical action:

- **Arrange**: Set up the test fixture (the state needed to run the test)
- **Act**: Call the function or perform the action being tested
- **Assert**: Verify the result is correct
- **Annihilate** (optional 4th A): Clean up any persistent state

The rule constrains **act-assert pairs**, not physical assert statements. Multiple physical asserts forming ONE logical assertion is fine. `act-assert-act-assert-act-assert` is NOT fine.

Also known as **Given-When-Then** (BDD style) or **Build-Operate-Check**. Arrange = Given, Act = When, Assert = Then.

### Composed Assertions

When you have multiple physical assertions checking one logical state, compose them into a single well-named function:

```
// Instead of:
assert hvac.isHeaterOn()
assert hvac.isFanOn()
assert not hvac.isCoolerOn()

// Use:
assertHvacState("HFc")  // H=heater on, F=fan on, c=cooler off
```

---

## Test Structure and Organization

### Test Fixtures

Three approaches to managing test state:

1. **Transient Fresh** (preferred): Created and destroyed around each test. No teardown needed. Tests cannot communicate with each other.

2. **Persistent Fresh**: Persistent parts reset after each test using teardown functions. For files, sockets, database connections.

3. **Persistent Shared**: State accumulates across tests using suite-level setup/teardown. Use sparingly — only for expensive resources like database connections.

The fresher the better. Transient is tops.

### Hierarchical Tests

Use test hierarchies to manage growing setups. Group tests by context, each level with its own setup. Inner setups execute after outer setups. This prevents one giant setup method that contains code only some tests need.

### Test Naming Conventions

Name tests for requirements, not implementation:

- Use Given-When-Then pattern
- Setup functions describe the "Given" part
- Test name describes the "When-Then" part
- Avoid magic numbers — use named constants that reflect requirements
- Example: `whenPayrollIsRun_thenPaymasterHoldsCheckForHoursTimesRate`

### Physical Test Structure

- One test file per production class (generally)
- Interfaces don't have tests
- Inner classes usually tested through outer class tests
- Tests test BEHAVIOR, not implementation details

---

## Test Doubles

### The Five Types

**Dummy:** Implements an interface where all functions do nothing. Returns null or zero for everything. Used when you need to pass an object but don't care about it.

**Stub:** A dummy that returns specific fixed values. Used to drive production code through specific pathways.

**Spy:** A stub that remembers facts about how it was called. Records which functions were called, how many times, with what arguments. The test can later query the spy to verify behavior.

**True Mock:** A spy that knows what should happen. Has a `verify()` method that checks if everything went as expected. The test doesn't check what the mock spied on — it asks the mock if everything went right.

**Fake:** A simulator with actual logic. Responds differently to different inputs. Can become complex maintenance nightmares — use sparingly, mostly for integration tests. Always write tests for your fakes.

### When to Mock

Mock across **dependency inversion boundaries**. The stuff on the other side of the boundary is what you mock out. If there's no boundary, prefer testing with real collaborators.

### Mockist vs. Statist

**Mockist (London School):** Emphasizes spying on algorithm implementations. Higher coupling to implementation, greater assurance algorithm works correctly. Tests may break when algorithm changes.

**Statist (Chicago/Detroit School):** Emphasizes testing return values. Lower coupling to implementation, can refactor algorithms freely. Cannot guarantee all input combinations work.

Neither a statist nor a mockist be — use the right tool for the situation. Use mockist style when testing across boundaries, statist style when not crossing boundaries.

### Mocking Patterns

**Test-Specific Subclass:** Derive from the class being tested, override methods you want to control. Useful for bypassing certain behaviors during tests.

**Self-Shunt:** The test class itself implements service interfaces. Pass the test object to the class being tested. The test becomes its own spy. Powerful when testing classes with many external connections.

**Humble Object:** Separate testable logic from hard-to-test boundary code. Make boundary objects "humble" — so simple they don't need testing. Move interesting logic to testable classes. Use at I/O boundaries, GUI boundaries, hardware interfaces.

### On Mocking Frameworks

Uncle Bob's perspective: mocks are easy to write by hand. Hand-written mocks have nice names that make tests readable and can be reused across tests. Framework syntax can obscure intent. Use frameworks when you need power — sealed/final classes, private access, legacy environments.

---

## Test Anti-Patterns

### Fragile Tests

Tests that break when making small production code changes. Caused by coupling tests to implementation details. If you make a small change to production code and a bunch of tests break, you have fragile tests. This violates the Open-Closed Principle.

### Tests That Know Too Much

Testing internal structure instead of behavior. Knowing about classes/methods that are implementation details. Testing private functions directly. Solution: test through public interfaces only.

### The Dirty Tests Story

A client had an "anything goes in tests" policy. Tests became fragile and brittle. Simple changes broke many tests. Tests were thrown away bit by bit. Production code rotted because they couldn't refactor without the safety net. If you start throwing away tests, you can't trust your test suite — and without trust, tests are worthless.

### Testing Private Functions

Generally don't test private functions — they're tested through the public interface. Private functions come from refactoring, so tests already cover them. If you MUST test a private function: testing trumps encapsulation — promote to package/protected visibility.

---

## The Value of Tests

### Tests Enable Refactoring

We can't clean code until we eliminate the fear of change. Tests eliminate fear by providing a safety net. With tests, you can clean ugly code confidently. The only way to go fast is to keep the code clean — and the only way to keep it clean is to have tests.

### Tests as Documentation

Tests are code examples for the whole system. They show how to create objects, call APIs. Written in a language you understand, utterly unambiguous, and they cannot get out of sync with code because they execute. The perfect low-level design document.

### Tests as Specification

If the tests pass, we ship. Tests ARE the requirements. QA trusts the tests. Write the test that you'd want to read.

### The Parable of the Two Disks

If you had production code on one disk and tests on another, and one disk crashed: if you lose tests, you cannot recreate them from production code (trapdoor function). If you lose production code, you can recreate it from tests — probably better (second system effect). The tests are more critical than the production code. Production code without tests WILL rot.

### TDD as Double-Entry Bookkeeping

Everything is said twice: once in tests, once in production code. They follow separate but complementary execution pathways and meet at successful execution (green bar). Accounting uses double-entry for sensitive financial data. Software is equally sensitive to single-bit errors.

---

## Test Design and SOLID

**SRP:** Each test function tests one responsibility. If testing multiple responsibilities, split into separate test classes.

**OCP:** Production code should be open for extension, tests closed for modification. Hide implementation details from tests — they should not know about internal class structure.

**LSP:** Test-specific subclasses must conform to LSP. Don't cheat by making tests pass in derivatives.

**ISP:** Tests shouldn't use interfaces with methods they don't call. Create test-specific interfaces if needed.

**DIP:** Test code depends on production code (never the reverse). Use polymorphism to invert runtime dependencies while keeping source dependencies correct.

---

## Rules of Simple Design (Kent Beck)

In priority order:

1. **Pass all tests** — make it work
2. **No duplication** — focus on structure
3. **Express intent** — make it communicate
4. **Minimize classes/methods** — optimize

For tests, the order shifts: make tests **expressive first** (since you write tests first), then make them pass, then clean up.

---

## When Reviewing Tests

1. **Three Laws:** Was production code written only after a failing test? Small increments? Only enough code to pass the current test?
2. **F.I.R.S.T.:** Fast? Independent? Repeatable? Self-validating? Timely?
3. **Structure (AAA):** Clear Arrange/Act/Assert? Single logical assertion per test? No act-assert-act-assert patterns?
4. **Mock Usage:** Mocking only across boundaries? Appropriate test double type? Not over-mocking?
5. **Design:** Tests decoupled from implementation details? Won't break from internal refactoring? No knowledge of private structure?
6. **Readability:** Test names describe behavior? Magic numbers replaced with meaningful constants? Tests readable as specifications?

---

## Related Skills

- `/naming` — intention-revealing names in tests and production code
- `/functions` — clean function structure during refactor phase
- `/solid` — SOLID principles applied to test design
- `/acceptance-testing` — acceptance TDD, testing pyramid, BDD
- `/clean-code-review` — comprehensive review after TDD cycle completes
