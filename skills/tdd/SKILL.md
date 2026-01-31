---
name: tdd
description: >-
  Guide TDD workflow for implementing features using Uncle Bob's Three Laws of TDD.
  Activates when implementing new features, creating handlers, services, or use cases,
  writing tests, fixing bugs, or when the user mentions test-first, TDD, red-green-refactor,
  failing test, or test-driven.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature description]
---

# TDD Workflow

This workflow guides AI agents through implementing features using Uncle Bob's Test-Driven Development principles from the Clean Code video series. Follow these steps rigorously when implementing any feature.

## Workflow Steps

### Step 1: Understand the Feature
- Analyze what behavior needs to exist
- Identify the acceptance criteria
- Break down into testable increments

### Step 2: List Test Cases
- Enumerate all scenarios that need testing
- Start with degenerate cases (null, empty, single element)
- Progress to more complex scenarios
- Order from simplest to most complex

### Step 3: RED Phase - Write Failing Test
- Write a small test for the next increment
- Run the test to see it fail
- The failure message should clearly indicate what's missing
- **Do not write production code yet**
- Stop as soon as any test fails (including compilation errors)

### Step 4: GREEN Phase - Write Minimum Code
- Write ONLY enough production code to make the test pass
- Use "fake it till you make it" - return constants, use trivial implementations
- Don't worry about elegance yet - just make it pass
- Run the test to see it pass
- **Do not add extra functionality**

### Step 5: REFACTOR Phase - Clean Up
- Clean up both production code AND test code
- Apply /naming workflow for clear, intention-revealing names
- Apply /functions workflow for proper function structure
- Remove duplication
- Run tests to ensure they still pass
- **Only restructure, don't add features**

### Step 6: Repeat Cycle
- Return to Step 3 for the next test case
- Continue until all scenarios are covered
- Cycle time should be seconds to minutes, not hours

### Step 7: Final Review
- Apply /professional workflow for quality standards
- Ensure all tests pass
- Verify code meets Clean Code principles

## The Three Laws of TDD

The three laws are disciplines that must be followed like a doctor washing hands before surgery:

### First Law
**"You are not allowed to write any production code until you have first written a failing unit test."**

- Before writing ANY production code, you must write a test for that code
- The test will fail because the production code doesn't exist yet
- This is where "test first" comes from
- Ask yourself: "What test must I write that will force me to write the code I know I want to write?"

### Second Law
**"You are not allowed to write more of a unit test than is sufficient to fail, and not compiling is failing."**

- As soon as a test fails for ANY reason (including compilation errors), STOP writing the test
- Start writing production code to make it pass
- Even a single compilation error means you must switch to production code

### Third Law
**"You are not allowed to write more production code than is sufficient to pass the currently failing test."**

- Once a test fails, write ONLY enough production code to make it pass
- Then go back to writing more test code
- This creates a cycle approximately 30 seconds long

## The Red-Green-Refactor Cycle

### RED Phase
- Write a failing test
- The test should fail for a specific, expected reason
- See the test fail before making it pass (validates the test works)
- "I want to see this fail"

### GREEN Phase
- Write the minimum production code to make the test pass
- Use "fake it till you make it" - return constants, use trivial implementations
- Don't worry about elegance yet - just make it pass
- "Make it work by hook or crook"

### REFACTOR Phase
- Clean up both production code AND test code
- Remove duplication
- Improve names
- Extract methods
- "Refactoring is the reward for making tests pass"
- Tests are part of your system - treat them with the same care as production code
- "Refactoring never appears on a schedule - you do it all the time like washing your hands"

## TDD Cycle Timing

Uncle Bob's guidance:
- The cycle should be **seconds to minutes**, not hours
- If you're spending more than a few minutes in any phase, the step is too big
- Write the simplest failing test, write the simplest passing code
- "If you follow these three laws, you'll be stuck in a cycle that is perhaps 20 seconds long."
- "Little test, little code, little test, little code."

## The Fundamental TDD Principle

**"As the tests get more specific, the code gets more generic."**

- Each new test case makes the tests more specific
- To pass each test, you generalize the production code
- This is how algorithms emerge incrementally
- The production code becomes more general with each passing test

## Clean Test Principles

### F.I.R.S.T Properties
Tests should be:
- **Fast**: Tests should run quickly (fitness runs 2000 tests in about a minute)
- **Independent**: Tests should not depend on each other
- **Repeatable**: Tests should produce the same results every time
- **Self-validating**: Tests should have a Boolean output - pass or fail
- **Timely**: Tests should be written before the production code

### The Single Assert Rule (AAA/Triple-A)
Every test should have ONE logical assertion following ONE logical action:
- **Arrange**: Set up the test fixture (the state needed to run the test)
- **Act**: Call the function or perform the action being tested
- **Assert**: Verify the result is correct
- **Annihilate** (optional 4th A): Clean up any persistent state

The rule constrains **act-assert pairs**, not physical assert statements:
- Multiple physical asserts forming ONE logical assertion is OK
- act-assert-act-assert-act-assert is NOT OK
- "A test is a Boolean operation - true or false, pass or fail, red or green"

### Also Known As
- **Given-When-Then** (BDD style)
- **Build-Operate-Check**
- Arrange = Given, Act = When, Assert = Then

### Composed Assertions
When you have multiple physical assertions, compose them into a single well-named assertion function:
```java
// Instead of:
assertTrue(hvac.isHeaterOn());
assertTrue(hvac.isFanOn());
assertFalse(hvac.isCoolerOn());

// Use:
assertHvacState("HFc"); // H=heater on, F=fan on, c=cooler off
```

## Test Structure and Organization

### Test Fixtures
Three approaches to managing test fixtures:

1. **Transient Fresh** (preferred): Created and destroyed around each test
   - JUnit creates new instance for each test method
   - No teardown needed
   - Tests cannot communicate with each other

2. **Persistent Fresh**: Persistent parts reset after each test
   - Uses teardown functions
   - For files, sockets, database connections

3. **Persistent Shared**: State accumulates across tests
   - Uses @BeforeClass/@AfterClass (suite setup/teardown)
   - Use sparingly - only for expensive resources like database connections

**"The fresher the better. Transient is tops."**

### Hierarchical Tests
Use test hierarchies to manage growing setups:
- Group tests by context
- Each level has its own setup
- Inner setups execute after outer setups
- Prevents one giant setup method
- Ruby's RSpec does this elegantly with nested `describe`/`context` blocks
- JUnit: Use `@RunWith(Enclosed.class)` with nested static classes

### Test Naming Conventions
Name tests for requirements, not implementation:
- Use Given-When-Then pattern
- Setup functions describe the "Given" part
- Test name describes the "When-Then" part
- Avoid magic numbers - use named constants that reflect requirements
- Example: `whenPayrollIsRun_thenPaymasterWillHoldCheckForHoursWorkedTimesHourlyRate`

### Physical Test Structure
- One test file per production class (generally)
- Interfaces don't have tests
- Inner classes usually tested through outer class tests
- Tests test BEHAVIOR, not implementation details
- Put tests in IDE-designated test directory

## Test Design and SOLID Principles

### Single Responsibility Principle
- Each test function tests one responsibility
- If testing multiple responsibilities, split into separate test classes

### Open-Closed Principle
- Production code should be open for extension
- Tests should be closed for modification
- Hide implementation details from tests
- Tests should not know about internal class structure

### Liskov Substitution Principle
- Test-specific subclasses must conform to LSP
- Don't cheat by making tests pass in derivatives

### Interface Segregation Principle
- Tests shouldn't use interfaces with methods they don't call
- Create test-specific interfaces if needed (not polluting - just an interface)

### Dependency Inversion Principle
- Test code depends on production code (never the reverse)
- Tests are lower-level than production code
- Use polymorphism to invert runtime dependencies while keeping source dependencies correct

## Test Doubles (Mocking)

### The Five Types of Test Doubles

#### 1. Dummy
- Implements an interface where all functions do nothing
- Returns null or zero for everything
- Used when you need to pass an object but don't care about it
- "Like a scarecrow - just sits there, doesn't do nothing"

#### 2. Stub
- A dummy that returns specific fixed values
- Used to drive production code through specific pathways
- Functions do nothing but return values useful to the test
- "Stubs drive the code through the pathway you're trying to test"

#### 3. Spy
- A stub that remembers facts about how it was called
- Records which functions were called, how many times, with what arguments
- Test can later query the spy to verify behavior
- "Spies watch and remember"

#### 4. True Mock
- A spy that knows what should happen
- Has a `verify()` method that checks if everything went as expected
- The test trusts the mock to validate behavior
- "The test doesn't check what the mock spied on - it asks the mock if everything went right"

#### 5. Fake
- A simulator with actual logic
- Responds differently to different inputs
- Can become complex maintenance nightmares
- Use sparingly - mostly for integration tests
- "Fakes grow and get complicated - avoid when you can"
- Always write tests for your fakes using TDD

### When to Mock
- Mock across **dependency inversion boundaries**
- Mocking is useful when testing things that cross architectural boundaries
- The stuff on the other side of the boundary is what you mock out

### The Uncertainty Principle of TDD
**Mockist vs Statist approaches:**

- **Mockist (London School)**: Emphasizes spying on algorithm implementations
  - Higher coupling to implementation
  - Greater assurance algorithm works correctly
  - Tests may break when algorithm changes

- **Statist (Chicago/Detroit/Cleveland School)**: Emphasizes testing return values
  - Lower coupling to implementation
  - Can refactor algorithms freely
  - Cannot guarantee all input combinations work

**"Neither a statist nor a mockist be"** - Use the right tool for the situation:
- Use mockist style when testing across boundaries
- Use statist style when not crossing boundaries

### Mocking Patterns

#### Test-Specific Subclass
- Derive from the class being tested
- Override methods you want to control
- Useful for bypassing certain behaviors during tests
- Methods must be protected (not private) to override

#### Self-Shunt
- The test class itself implements service interfaces
- Pass `this` to the class being tested
- Test becomes its own spy
- Powerful when testing classes with many external connections

#### Humble Object
- Separate testable logic from hard-to-test boundary code
- Make boundary objects "humble" - so simple they don't need testing
- Move interesting logic to testable classes
- Use at I/O boundaries, GUI boundaries, hardware interfaces
- Example: Separate GUI formatting from business logic with a Presenter

### On Mocking Frameworks
Uncle Bob's perspective:
- "I usually don't use mocking frameworks"
- Mocks are easy to write by hand
- Hand-written mocks have nice names that make tests readable
- Hand-written mocks can be reused across tests
- Framework syntax can be "a jumble of dots and parentheses"
- Use frameworks when you need power: sealed/final classes, private access
- Useful in legacy environments

## TDD Techniques

### Fake It Till You Make It
- Make a test pass by returning a constant (faking it)
- Then make the next test pass by faking it a little less
- Continue until you're not faking anymore
- "Making incremental progress towards a goal is not wasting time - it's how you save time"

### Stair-Step Tests
- Write a test just to enable writing the next test
- Delete it once it's served its purpose
- Like digging stairs to reach the bottom of a hole
- Example: First test creates the class, second test calls a method, third test actually tests behavior

### Assert First
- Write the test backwards, starting with the assert
- Let compiler errors guide you to create what's needed
- Forces you to think about the outcome first
- Creates test from back to front

### Triangulation
- Write two tests that force you to generalize
- First test can be passed with a constant
- Second test requires actual logic
- Used to drive generalization of production code

### One-to-Many
- Implement operations on collections by first implementing for one object
- Make it work in singular case first
- Then generalize to plural case
- "Deal with one object first without even the array or the list"

### Getting Stuck
**Signs you're stuck:**
- Nothing incremental you can do to pass the test
- Have to write the whole algorithm at once

**Causes:**
- Wrote the wrong test (went for the gold too early)
- Making production code too specific
- Not approaching from outside in

**Solutions:**
- Start with degenerate test cases (null, empty, single element)
- Test peripheral issues first (validation, simple queries)
- Avoid complicated test cases until simple ones are exhausted
- "Engage as few brain cells as possible at any given moment"

## Test Anti-Patterns

### Fragile Tests
- Tests that break when making small production code changes
- Caused by coupling tests to implementation details
- Violates Open-Closed Principle
- "If you make a small change to production code and a bunch of tests break, you have fragile tests"

### Tests That Know Too Much
- Testing internal structure instead of behavior
- Knowing about classes/methods that are implementation details
- Testing private functions directly
- Solution: Test through public interfaces only

### Dirty Tests
Story: A client had "anything goes in tests" policy
- Tests became fragile and brittle
- Simple changes broke many tests
- Tests were thrown away bit by bit
- Production code rotted because they couldn't refactor
- "If you start throwing away tests, you can't trust your test suite"

### Giant Setups
- One massive setup for all tests
- Contains code only some tests need
- Solution: Use hierarchical tests with targeted setups

### Testing Private Functions
- Generally don't test private functions
- They're tested through public interface
- Private functions come from refactoring - tests already cover them
- If you MUST test private: "Testing trumps encapsulation" - promote to package/protected

### Magic Numbers in Tests
- Numbers whose significance is unclear
- Solution: Use named constants that reflect requirements
- Example: `MAX_REGULAR_HOURS_PER_DAY` instead of `8`

## The Value of Tests

### Tests Enable Refactoring
- "We can't clean code until we eliminate the fear of change"
- Tests eliminate fear by providing safety net
- With tests, you can clean ugly code confidently
- "The only way to go fast is to keep the code clean"

### Tests as Documentation
- Tests are code examples for the whole system
- Show how to create objects, call APIs
- Written in a language you understand
- Utterly unambiguous
- Cannot get out of sync with code (they execute)
- "The perfect kind of low-level design document"

### Tests as Specification
- "If the tests pass, we ship"
- Tests ARE the requirements
- QA trusts the tests
- Write tests you'd want to read
- "Write the test that you'd want to read"

### The Parable of the Two Disks
If you had production code on one disk and tests on another, and one crashed:
- **Lose tests**: Cannot recreate them from production code (trapdoor function)
- **Lose production code**: Can recreate from tests, probably better (second system effect)
- "The tests are more critical than the production code"
- Production code without tests WILL rot

### TDD is Like Double-Entry Bookkeeping
- Everything is said twice: once in tests, once in production code
- They follow separate but complementary execution pathways
- They meet at successful execution (green bar)
- Accounting does this for sensitive financial data
- Software is equally sensitive to single-bit errors

## Rules of Simple Design (for Tests)

Kent Beck's rules (in priority order):
1. **Pass all tests** - Make it work
2. **No duplication** - Focus on structure
3. **Express intent** - Make it communicate
4. **Minimize classes/methods** - Optimize

**For tests, the order changes:**
1. Make tests **expressive first** (since you write tests first)
2. Then make them pass
3. Then clean up

"When we say test first, it means the tests come first - in writing, refactoring, cleaning, maintaining"

## Process for Feature

$ARGUMENTS

## Example Cycle

```
// RED: Write failing test
test('should return empty string for 0', () => {
  expect(fizzBuzz(0)).toBe('');
});
// Run: FAIL - fizzBuzz is not defined

// GREEN: Minimal passing code
function fizzBuzz(n) {
  return '';
}
// Run: PASS

// REFACTOR: (nothing to refactor yet)

// RED: Next test
test('should return "1" for 1', () => {
  expect(fizzBuzz(1)).toBe('1');
});
// Run: FAIL - expected '1', got ''

// GREEN: Make it pass
function fizzBuzz(n) {
  if (n === 0) return '';
  return String(n);
}
// Run: PASS

// Continue the cycle...
```

## Review Checklist

When reviewing tests, check:

1. **Three Laws Compliance**
   - Was production code written only after failing test?
   - Are tests written in small increments?
   - Is only enough code written to pass current test?

2. **Test Cleanliness (F.I.R.S.T)**
   - Are tests fast enough for rapid feedback?
   - Are tests independent of each other?
   - Are tests repeatable in any environment?
   - Do tests have clear pass/fail outcomes?
   - Were tests written before production code?

3. **Structure (AAA/Given-When-Then)**
   - Clear separation of Arrange, Act, Assert?
   - Single logical assertion per test?
   - No act-assert-act-assert patterns?

4. **Mock Usage**
   - Mocking only across boundaries?
   - Using appropriate test double type?
   - Not over-mocking (testing implementation)?

5. **Design Principles**
   - Tests decoupled from implementation details?
   - Tests won't break from internal refactoring?
   - No knowledge of private/internal structure?

6. **Naming and Readability**
   - Test names describe behavior, not implementation?
   - Magic numbers replaced with meaningful constants?
   - Tests readable as specifications?

## Memorable Quotes

- "Code rots because we're afraid to clean it."
- "Tests eliminate the fear of change."
- "If you follow these three laws, you'll be stuck in a cycle that is perhaps 20 seconds long."
- "Little test, little code, little test, little code."
- "Everything always worked a minute or so ago."
- "Debugging is a skill not to be desired."
- "If these tests pass, we ship."
- "As the tests get more specific, the code gets more generic."
- "Refactoring is the reward for making tests pass."
- "Tests are part of your system - not extra, not ancillary, not inferior, not disposable."
- "The tests are the requirements."
- "Write the test that you'd want to read."
- "Neither a statist nor a mockist be."
- "Testing trumps encapsulation."
- "The only way to go fast is to keep the code clean."
- "TDD is double-entry bookkeeping for software."

## Common Pitfalls

- **Writing too much test** - Test only what's needed for the next step
- **Writing too much code** - Only make the current test pass
- **Skipping refactoring** - Technical debt accumulates
- **Testing implementation** - Test behavior, not implementation details
- **Slow tests** - Keep tests fast to maintain rapid cycles

## Self-Review (Back Pressure)

After completing a TDD cycle, ALWAYS perform this self-review before presenting code as done:

### Self-Review Steps
1. **Naming Check**: Review all names against `/naming` principles
   - Do names reveal intent?
   - Are they pronounceable and searchable?
   - Correct parts of speech?

2. **Function Check**: Review all functions against `/functions` principles
   - Are functions small (4-6 lines ideal)?
   - Does each function do ONE thing?
   - Minimal arguments (0-2 ideal)?

3. **Professional Check**: Review against `/professional` standards
   - Do I know what this code does?
   - Do I know that it works (tests prove it)?
   - Would I be proud of this code?

4. **If Violations Found**:
   - Fix the violations
   - Re-run tests
   - Re-run self-review

5. **Only present as "done" when self-review passes**

### Mandatory Quality Gate

Code produced by TDD is NOT complete until:
- [ ] All tests pass
- [ ] Self-review completes with no violations
- [ ] `/clean-code-review` can be run without finding critical issues

## Related Skills

During the REFACTOR phase, leverage these complementary workflows:

- **/professional** - Apply professional coding standards and quality checks
- **/naming** - Use intention-revealing names for variables, functions, and classes
- **/functions** - Structure functions properly with single responsibility and clean arguments
- **/clean-code-review** - Run comprehensive review after TDD cycle completes
