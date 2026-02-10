---
name: acceptance-testing
description: >-
  Guide acceptance testing practices using Uncle Bob's ATDD teachings. Activates when
  writing acceptance tests, discussing testing pyramid, BDD, FitNesse, Cucumber,
  or when the user mentions acceptance testing, ATDD, testing pyramid, fixtures,
  Given/When/Then, or stakeholder communication through tests.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature or module to test]
---

# Acceptance Testing Workflow

This workflow guides AI agents through writing and structuring acceptance tests using Uncle Bob's Acceptance Test-Driven Development teachings from the Clean Code video series (Episodes E01-E04 on Acceptance Testing). Follow these steps when writing acceptance tests, defining business requirements as executable specifications, or bridging the communication gap between business stakeholders and developers.

## Workflow Steps

### Step 1: Identify Business Requirements and Actors
- Determine who the stakeholders are (product owners, QAs, BAs, designers, developers)
- Identify the business behavior being requested
- Clarify the acceptance criteria with stakeholders before writing any code
- Ask: "How will we know when this feature is done?"

### Step 2: Write Acceptance Criteria in Readable Format
- Write criteria BEFORE any code is written
- Use Given/When/Then format for clarity
- Ensure every stakeholder can read and understand the criteria
- Do NOT reference UI elements -- test business behavior below the surface
- Remove all ambiguity -- if two people could interpret a criterion differently, rewrite it

### Step 3: Create Fixtures Connecting Tests to System
- Build thin adapter code (fixtures) between test framework and production code
- Fixtures translate human-friendly test concepts into technical system calls
- Keep fixtures simple -- NO business logic in fixture code
- Fixtures plug in at the same level as controllers, bypassing the UI entirely

### Step 4: Implement Feature Using TDD
- Use `/tdd` workflow for the inner development loop
- Acceptance tests form the outer loop; unit tests form the inner loop
- Write unit tests (RED-GREEN-REFACTOR) to build toward passing acceptance tests
- Continue TDD cycles until the acceptance test passes

### Step 5: Verify Acceptance Tests Pass
- Run acceptance tests to confirm business expectations are met
- When acceptance tests pass, the feature meets its Definition of Done
- Verify that unit tests, acceptance tests, and any UI tests all pass together

### Step 6: Build Regression Test Suite
- Add passing acceptance tests to the automated regression suite
- Run regression suite in CI to catch regressions early
- Maintain the suite -- update tests when business requirements change intentionally

---

## Core Philosophy

### What Are Acceptance Tests?

Acceptance tests are the ONE kind of test that checks whether software meets BUSINESS expectations. Unlike unit tests and functional tests (written by developers for developers), acceptance tests verify that the system does what the business actually asked for.

They provide a shared, unambiguous language that bridges the business domain and technical implementation. They are the executable specification of what "done" means.

> "There is nothing as wasteful as doing with great care and diligence the wrong thing."

The fundamental problem acceptance tests solve is communication. Business people understand the big picture but lack technical detail. Developers understand the software but often misunderstand the business domain. Acceptance tests provide a shared artifact that both parties can read, verify, and agree upon.

### The Communication Problem

Business-developer communication is the root cause of most software project failures.

> "Quality comes first... almost all problems in software projects do come down to quality and communication problems."

Without acceptance tests, the typical failure mode is:
1. Business writes vague requirements
2. Developers fill in the gaps with assumptions
3. QA cannot tell when something is "correct" because nobody defined it
4. Demos reveal misunderstandings too late
5. Rework consumes the schedule

Acceptance tests break this cycle by forcing precision and shared understanding BEFORE development begins.

---

## The Testing Pyramid

Michael Cohn's Testing Pyramid defines the proper distribution of tests in a healthy system:

```
          /\
         /  \
        / UI \
       /______\
      /        \
     /Acceptance \
    /______________\
   /                \
  /   Functional     \
 /____________________\
/                      \
/      Unit Tests       \
/________________________\
```

### Layer Definitions

#### Bottom: Unit Tests
- The foundation of the pyramid -- the most numerous tests
- Thousands run per second
- Test individual functions and classes in isolation
- Written by developers for developers
- Rock-solid, fast, and deterministic

#### Lower-Middle: Functional Tests
- Test multiple units working together
- May involve more mocks and test doubles
- Verify that components integrate correctly at a technical level
- Still written by developers for developers

#### Middle: Acceptance Tests
- Check BUSINESS expectations, not technical correctness
- Readable by non-developers: QAs, product owners, BAs, designers
- NOT dependent on the UI
- Written collaboratively between business and technical people
- Automated and part of the regression suite

#### Top: UI / System Tests
- Just a small handful -- the most expensive and slowest
- Test the full stack through the actual user interface
- Fragile because they depend on literally everything
- Should be very limited in ambition

> "UI tests should be just a handful and very limited in their ambition."

### The Anti-Pattern: The Ice Cream Cone

The inverted pyramid is a common and destructive anti-pattern:

```
  ________________________
 /                        \
/     Tons of UI Tests     \
\__________________________/
 \                        /
  \   Some Acceptance    /
   \____________________/
    \                  /
     \  Few Functional/
      \______________/
       \            /
        \ No Unit  /
         \________/
```

When teams invert the pyramid, they end up with:
- Massive, fragile UI test suites that break constantly
- Slow feedback loops (hours instead of seconds)
- Enormous maintenance burden
- Tests that are coupled to every layer of the system
- False confidence -- tests pass but business requirements are still wrong

> "We were mostly inventing new ways to do slow, error-prone, expensive testing."

---

## The Problem with UI Testing

UI testing forces computers into a very human-centric view of the software. This creates fundamental problems:

### Why UI Tests Are Fragile
- UI tests depend on literally everything: business rules, database, network, rendering, layout
- The UI is the part of the system MOST likely to change
- A single CSS change, layout tweak, or redesign breaks the entire suite
- Every layer of the system is a potential source of failure

### The Automation Monster
When teams build massive UI test suites, they create what Uncle Bob calls "automation monsters" -- sprawling, fragile test suites that:
- Take hours to run
- Break for reasons unrelated to business logic
- Require constant maintenance
- Give false negatives (tests fail but the system works)
- Give false positives (tests pass but business requirements are wrong)
- Consume more effort to maintain than they save

### The Right Approach
- Test business behavior BELOW the UI surface
- Use acceptance tests that plug in at the controller/API level
- Reserve UI tests for a small handful of critical user journeys
- Think of acceptance tests as "an alternative UI" for the system

---

## Acceptance Test-Driven Development (ATDD)

### The ATDD Workflow

ATDD is the OUTER loop of development. TDD is the INNER loop.

```
Business Requirement
       │
       ▼
Write Acceptance Test (OUTER LOOP)
       │
       ▼
┌──────────────────────┐
│  TDD Cycle (INNER)   │
│  RED → GREEN →       │
│  REFACTOR → REPEAT   │
└──────────────────────┘
       │
       ▼
Acceptance Test Passes
       │
       ▼
Add to Regression Suite
```

### Critical Distinction from TDD

- **TDD** checks the PROGRAMMER'S understanding -- "Does the code do what I think it should?"
- **ATDD** checks BUSINESS expectations -- "Does the system do what the business actually needs?"

Both are necessary. TDD ensures technical correctness. ATDD ensures business correctness. A system can pass all unit tests and still be the wrong product.

### Timing: When to Write Acceptance Criteria

Write acceptance criteria "just in time" -- when a story is picked up for development, NOT during sprint planning or backlog grooming.

**Why not during planning?**
- Requirements evolve between planning and implementation
- Writing criteria too early wastes effort on stories that may never be built
- The conversation between business and developers should happen close to implementation

**Why not after coding?**
- Defeats the purpose -- acceptance tests DEFINE done, they do not verify after the fact
- Developers fill gaps with assumptions that may be wrong
- Rework is far more expensive than getting it right upfront

### Definition of Done

A feature is done when:
1. All acceptance tests pass
2. All unit tests pass
3. All UI tests (if any) pass
4. Code meets Clean Code standards

The acceptance tests ARE the definition of done. There is no ambiguity.

---

## Writing Good Acceptance Tests

### Properties of Good Acceptance Tests

1. **Readable by everyone** -- QAs, product owners, BAs, designers, and developers can all understand them
2. **Unambiguous** -- no room for misinterpretation; if two people could read it differently, rewrite it
3. **Automatable** -- can be executed by a machine without human intervention
4. **UI-independent** -- do NOT reference buttons, pages, screens, or UI elements
5. **Business-focused** -- test what the system DOES, not how it looks

### Good vs. Bad Acceptance Tests

**Bad -- References UI:**
```
Given I am on the login page
When I type "admin" in the username field
And I click the "Login" button
Then I should see the dashboard page
```

**Good -- Tests Business Behavior:**
```
Given a registered user with username "admin"
When the user authenticates with valid credentials
Then the system grants access to the user's account
```

**Bad -- Ambiguous:**
```
Given a customer places an order
Then the order should be processed correctly
```

**Good -- Precise:**
```
Given a customer with a verified shipping address
And an order containing 3 items totaling $45.00
When the order is submitted with standard shipping
Then the order status is set to "CONFIRMED"
And the shipping cost is calculated as $5.99
And the order total is $50.99
```

### The Given/When/Then Pattern

This pattern standardizes the specification language:

- **Given** -- establishes the preconditions (the state of the world before the action)
- **When** -- describes the action being performed (one logical action per test)
- **Then** -- specifies the expected outcomes (observable, verifiable results)

Each section should use business language, not technical jargon.

---

## The Fixture Pattern

### What Are Fixtures?

Fixtures are the glue code that connects acceptance tests to the actual software. They sit between the test framework (FitNesse, Cucumber, etc.) and the production code.

```
┌─────────────────────┐
│   Acceptance Test    │  (Human-readable specification)
│   (Given/When/Then)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│      Fixture         │  (Thin adapter -- translation only)
│  (Glue Code Layer)   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Production Code    │  (Controllers, Use Cases, Entities)
│   (Below the UI)     │
└─────────────────────┘
```

### Fixture Design Principles

1. **Thin adapters** -- Fixtures should contain NO business logic, only translation and conversion
2. **Simple mapping** -- Convert human-friendly test concepts into technical system calls
3. **Same level as controller** -- Fixtures plug in at the same level as the UI controller, bypassing the UI entirely
4. **No UI dependency** -- Acceptance tests are "an alternative UI" for the system
5. **Refactorable** -- Start simple, refactor so the fixture becomes a thin adapter over time

### Fixture Example

```java
// FitNesse fixture -- thin adapter connecting test to system
public class OrderProcessingFixture {
    private OrderService orderService;
    private OrderResponse lastResponse;

    // Given: Set up preconditions
    public void setCustomerId(String customerId) {
        // Simple delegation -- no business logic here
        this.request = new OrderRequest(customerId);
    }

    public void setItemCount(int count) {
        this.request.setItemCount(count);
    }

    // When: Execute the action
    public void submitOrder() {
        // Calls production code directly, bypassing UI
        lastResponse = orderService.submitOrder(request);
    }

    // Then: Query results
    public String orderStatus() {
        return lastResponse.getStatus();
    }

    public String orderTotal() {
        return lastResponse.getFormattedTotal();
    }
}
```

### When Tests Use Human Concepts

Tests often use human-friendly concepts while code uses technical ones. The fixture handles this conversion:

| Test Says | Fixture Converts To |
|-----------|-------------------|
| "a premium customer" | `new Customer(tier=PREMIUM)` |
| "standard shipping" | `ShippingMethod.STANDARD` |
| "order is confirmed" | `status == OrderStatus.CONFIRMED` |
| "$45.00" | `new Money(4500, USD)` |

The fixture is the ONLY place this translation happens. Keep it simple and mechanical.

---

## BDD and Acceptance Testing Tools

### BDD (Behavior-Driven Development)

BDD arrived around 2004 and provides a less technical vocabulary for describing software behavior. The Given/When/Then format standardizes the specification language and makes tests accessible to non-developers.

However, BDD is a broader methodology than acceptance testing alone. BDD encompasses:
- Collaborative specification (three amigos: developer, tester, business)
- Living documentation
- Outside-in development
- Acceptance test automation

Acceptance testing focuses specifically on automation and unambiguous "done" criteria.

### FitNesse

FitNesse is a wiki-based acceptance testing system created by Uncle Bob. Tests are written as tables in wiki pages:

```
|Order Processing                          |
|customer id|item count|submit?|status?    |
|CUST-001   |3         |true   |CONFIRMED  |
|CUST-002   |0         |true   |REJECTED   |
|GUEST      |1         |true   |PENDING    |
```

- Input columns provide test data (no question mark suffix)
- Output columns verify results (question mark suffix)
- Tables map directly to fixture classes and methods
- Non-developers can read, write, and modify tests through the wiki

### Cucumber and Gherkin

Cucumber uses the Gherkin language for human-readable specifications:

```gherkin
Feature: Order Processing

  Scenario: Successful order submission
    Given a customer with id "CUST-001"
    And a verified shipping address
    And an order containing 3 items totaling $45.00
    When the order is submitted with standard shipping
    Then the order status should be "CONFIRMED"
    And the shipping cost should be $5.99
```

### WARNING: Common Misuse of BDD Tools

BDD tools are frequently misused as "fancy front ends to drive robots like Selenium." This completely misses the point.

**Misuse:**
```gherkin
# This is NOT an acceptance test -- this is a UI test in disguise
Given I navigate to "/orders/new"
When I fill in "customer_id" with "CUST-001"
And I click the "Add Item" button 3 times
And I click "Submit Order"
Then the page should contain "Order Confirmed"
```

**Correct use:**
```gherkin
# This tests business behavior, not UI mechanics
Given a registered customer "CUST-001"
And 3 items in the order totaling $45.00
When the order is submitted
Then the order is confirmed with total $50.99
```

The collaborative intent of BDD is lost when it becomes a UI automation wrapper.

---

## Architecture for Testability

### The Fundamental Requirement

The architecture MUST allow access to the core software WITHOUT going through the UI, database, or network. If acceptance tests cannot plug in below the UI, the architecture has a serious design flaw.

```
┌─────────────────────────────────────────────┐
│                    UI                        │
│  ┌───────────────────────────────────────┐  │
│  │            Controller                  │  │
│  │  ┌───────────────────────────────┐    │  │
│  │  │         Use Cases              │    │  │
│  │  │  ┌───────────────────────┐    │    │  │
│  │  │  │      Entities          │    │    │  │
│  │  │  └───────────────────────┘    │    │  │
│  │  └───────────────────────────────┘    │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  ← Fixture plugs in HERE (same as UI)       │
└─────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Fixture plugs in at controller level** -- bypassing the UI entirely
2. **No business logic in UI layer** -- if logic lives in the UI, acceptance tests cannot reach it
3. **Dependencies must be injectable** -- fixtures need to substitute test implementations for databases, services, etc.
4. **Acceptance tests = an alternative UI** -- the system should work identically whether driven by a human through the UI or by a fixture through the API

### Clean Architecture Enables ATDD

Clean Architecture (/architecture) directly supports acceptance testing:
- **Use Cases** define clear input/output boundaries that fixtures can call
- **Dependency Inversion** allows fixtures to inject test doubles
- **Entities** contain business rules testable without infrastructure
- **Interface Adapters** provide the controller-level API that fixtures plug into

If your architecture follows Clean Architecture principles, acceptance testing becomes straightforward. If it does not, acceptance tests will be painful or impossible -- which is a signal that the architecture needs improvement.

---

## The Transformed Role of QA

### Traditional QA (The Bottleneck)

In traditional workflows:
1. Developers write code
2. Code is "thrown over the wall" to QA
3. QA tests manually under time pressure
4. Bugs are found late, fixes are expensive
5. QA becomes a bottleneck at the end of every sprint

### ATDD QA (The Collaborator)

With acceptance testing:
1. QA participates BEFORE development, writing acceptance criteria
2. Developers implement against those criteria using TDD
3. When acceptance tests pass, the feature is done
4. QA shifts focus to exploratory testing -- finding edge cases that automated tests miss
5. QA is no longer a bottleneck

### The "Vague Requirements" Anti-Pattern

Without acceptance tests, requirements are often vague and ambiguous:
- User story: "As a user, I want to manage my orders"
- QA cannot determine when this is "correct"
- Developers invent details
- Everyone discovers the misalignment at demo time

With acceptance tests, requirements are precise and executable:
- "Given a confirmed order older than 30 days, when the customer requests cancellation, then the system rejects the cancellation with reason PAST_CANCELLATION_WINDOW"

---

## Anti-Patterns

### 1. The Automation Monster
Building massive UI test suites that are slow, fragile, and expensive to maintain. These suites often take hours to run and break for reasons unrelated to business logic.

### 2. Skipping the Middle
Going straight from unit tests to UI tests, skipping acceptance tests entirely. This leaves a gap where business requirements are never formally verified against the code.

### 3. QA at the End
Treating QA as a phase that happens after development, creating a bottleneck under time pressure. QA should participate BEFORE development by writing acceptance criteria.

### 4. Vague Requirements
Accepting ambiguous requirements like "the system should handle orders properly." Every acceptance criterion must be precise enough to automate.

### 5. Demo-Driven Development
Showing incomplete work to stakeholders without passing acceptance tests. Demos should only happen when acceptance tests pass -- they ARE the definition of done.

### 6. Cucumber as UI Driver
Using BDD tools like Cucumber as fancy front ends for Selenium, completely missing the collaborative intent. Acceptance tests test business behavior, not UI mechanics.

### 7. Over-Mocking
Mocking so much of the system that acceptance tests verify nothing except the mocks themselves. Acceptance tests should exercise real business logic.

### 8. Writing Tests After Code
Writing acceptance tests after development is complete defeats their purpose. They must be written BEFORE code to serve as the shared definition of done.

---

## Process for Feature

$ARGUMENTS

---

## Example: Order Processing Feature

### Step 1: Identify Business Requirements

**Feature:** Order submission and processing
**Actors:** Customer, Operations team, Finance team
**Business Question:** How do we know when an order is correctly processed?

### Step 2: Write Acceptance Criteria

```gherkin
Feature: Order Processing

  Scenario: Successful order with standard shipping
    Given a customer with verified shipping address
    And an order containing 3 items totaling $45.00
    When the order is submitted with standard shipping
    Then the order status is "CONFIRMED"
    And the shipping cost is $5.99
    And the order total is $50.99

  Scenario: Order rejected for empty cart
    Given a customer with verified shipping address
    And an empty order
    When the order is submitted
    Then the order is rejected with reason "EMPTY_ORDER"

  Scenario: Order pending for unverified address
    Given a customer without a verified shipping address
    And an order containing 1 item totaling $15.00
    When the order is submitted
    Then the order status is "PENDING_ADDRESS_VERIFICATION"
```

### Step 3: Create Fixture

```java
public class OrderProcessingFixture {
    private final OrderService orderService;
    private OrderRequest request;
    private OrderResponse response;

    // Given
    public void setCustomerAddressVerified(boolean verified) {
        request.setAddressVerified(verified);
    }

    public void setOrderItems(int count, String total) {
        request.setItemCount(count);
        request.setSubtotal(Money.parse(total));
    }

    // When
    public void submitOrder(String shippingMethod) {
        request.setShipping(ShippingMethod.fromString(shippingMethod));
        response = orderService.submit(request);
    }

    // Then
    public String orderStatus() {
        return response.getStatus().name();
    }

    public String shippingCost() {
        return response.getShippingCost().format();
    }

    public String orderTotal() {
        return response.getTotal().format();
    }

    public String rejectionReason() {
        return response.getRejectionReason();
    }
}
```

### Step 4: TDD Inner Loop

Use `/tdd` workflow to implement `OrderService.submit()`:
1. RED: Test that empty order is rejected
2. GREEN: Return rejection for empty orders
3. REFACTOR: Clean names and structure
4. RED: Test standard shipping calculation
5. GREEN: Implement shipping calculation
6. REFACTOR: Extract shipping strategy
7. Continue until all acceptance scenarios pass...

### Step 5: Verify

Run acceptance tests. All scenarios pass. Feature is DONE.

---

## Output Format

When analyzing or creating acceptance tests, present findings as:

```
## Acceptance Testing Assessment

**Feature:** [What feature is being tested]
**Actors:** [Who are the stakeholders]
**Acceptance Criteria:** [List of criteria in Given/When/Then]
**Fixture Strategy:** [How tests connect to system]
**Testing Pyramid Level:** [Where these tests sit]
**Architecture Readiness:** [Can fixtures plug in without UI?]
```

For each acceptance test:
```
### Scenario: [Description]
**Given:** [Preconditions]
**When:** [Action]
**Then:** [Expected outcomes]
**Fixture Connection:** [How the fixture maps to production code]
**Pyramid Level:** Acceptance (business behavior, UI-independent)
```

---

## Memorable Quotes

> "There is nothing as wasteful as doing with great care and diligence the wrong thing."

> "The only way to go fast is to go well."

> "Quality comes first... almost all problems in software projects do come down to quality and communication problems."

> "UI tests should be just a handful and very limited in their ambition."

> On business-developer communication: "The answer is usually badly."

> "Software isn't cheap, and software that breaks all the time, well, that's the most expensive kind."

> "We were mostly inventing new ways to do slow, error-prone, expensive testing."

---

## Common Pitfalls

- **Testing through the UI** -- Acceptance tests should bypass the UI and test business behavior directly
- **Writing tests after code** -- Acceptance criteria must be defined BEFORE development begins
- **Ambiguous criteria** -- If two people could interpret a test differently, it is not precise enough
- **Business logic in fixtures** -- Fixtures are thin adapters, not a place for business rules
- **Ignoring the pyramid** -- Too many UI tests and too few acceptance tests create the ice cream cone
- **Treating QA as a gate** -- QA should collaborate on criteria upfront, not test at the end
- **Using BDD tools as Selenium wrappers** -- This misses the collaborative intent entirely
- **Over-mocking** -- Acceptance tests should exercise real business logic, not verify mocks

---

## Self-Review (Back Pressure)

After writing acceptance tests, ALWAYS perform this self-review before presenting work as done:

### Self-Review Steps

1. **Readability Check**: Can a non-developer read and understand these tests?
   - Show the test to a product owner or BA -- would they understand it?
   - Are business concepts used instead of technical jargon?

2. **UI Independence Check**: Do any tests reference UI elements?
   - No button names, page URLs, CSS selectors, or screen layouts
   - Tests describe WHAT the system does, not HOW the user interacts with it

3. **Fixture Simplicity Check**: Are fixtures thin adapters with no business logic?
   - Fixtures only translate and delegate
   - No conditional logic, no calculations, no business rules in fixtures

4. **Architecture Check**: Can tests plug in without going through the UI?
   - Fixtures connect at controller/API level
   - Dependencies are injectable for test doubles
   - No UI layer stands between the test and the business logic

5. **Pyramid Check**: Are we testing at the right level?
   - Business behavior belongs in acceptance tests
   - Technical correctness belongs in unit tests
   - Full-stack user journeys belong in the small handful of UI tests

6. **Ambiguity Check**: Could any criterion be interpreted two different ways?
   - Every Given, When, and Then must have exactly one interpretation
   - Numbers, states, and outcomes must be precise

### If Violations Found
- Fix the violations immediately
- Re-run self-review
- Only present as "done" when all checks pass

### Mandatory Quality Gate

Acceptance tests are NOT complete until:
- [ ] Acceptance criteria written before code
- [ ] Tests readable by all stakeholders
- [ ] No UI element references in acceptance tests
- [ ] Fixtures are simple adapters with no business logic
- [ ] Architecture supports testability without UI
- [ ] Tests automated and fast enough for CI
- [ ] All scenarios have precise, unambiguous expected outcomes
- [ ] Tests added to regression suite

---

## Feature or Module to Test

$ARGUMENTS

---

## Related Skills

Acceptance testing integrates with the full Clean Code workflow:

- **/tdd** - Inner loop of development; acceptance tests are the outer loop that defines "done"
- **/architecture** - Clean Architecture enables testability by separating business rules from delivery mechanisms
- **/solid** - Dependency Inversion Principle enables fixture injection and test double substitution
- **/professional** - Professional responsibility to communicate unambiguously through executable specifications
- **/legacy-code** - Characterization tests for existing systems share techniques with acceptance testing
- **/clean-code-review** - Review test quality alongside production code quality
- **/components** - Component boundaries define where fixtures plug in and where mocking is appropriate
- **/functions** - Keep fixture methods small and focused, one responsibility per method
- **/naming** - Use intention-revealing names in tests and fixtures that match business vocabulary
