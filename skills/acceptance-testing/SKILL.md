---
name: acceptance-testing
description: >-
  Guide acceptance testing practices using Uncle Bob's ATDD teachings. Activates when
  writing acceptance tests, discussing testing pyramid, BDD, acceptance criteria,
  or when the user mentions acceptance testing, ATDD, testing pyramid, fixtures,
  Given/When/Then, or stakeholder communication through tests.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature or module to test]
---

# Acceptance Testing

Follow this workflow when writing acceptance tests, defining business requirements as executable specifications, or bridging the communication gap between business and developers.

For extended examples (fixture implementations, tool-specific walkthroughs, full feature examples), read `references/extended-examples.md`.

## Workflow Steps

1. **Identify business requirements and actors** — who are the stakeholders? What behavior is being requested?
2. **Write acceptance criteria in Given/When/Then** — BEFORE any code is written
3. **Create fixtures** — thin adapter code connecting tests to production code
4. **Implement feature using TDD** — acceptance tests are the outer loop, unit tests are the inner loop
5. **Verify acceptance tests pass** — when they pass, the feature meets its Definition of Done
6. **Add to regression suite** — maintain the suite in CI

---

## What Are Acceptance Tests?

Acceptance tests are the ONE kind of test that checks whether software meets BUSINESS expectations. Unlike unit tests (written by developers for developers), acceptance tests verify that the system does what the business actually asked for.

They provide a shared, unambiguous language that bridges the business domain and technical implementation. They are the executable specification of what "done" means.

The fundamental problem acceptance tests solve is communication. Business people understand the big picture but lack technical detail. Developers understand the software but often misunderstand the business domain. Acceptance tests force precision and shared understanding BEFORE development begins.

Without acceptance tests, the typical failure mode is: business writes vague requirements, developers fill in gaps with assumptions, QA cannot tell when something is "correct" because nobody defined it, demos reveal misunderstandings too late, and rework consumes the schedule. Acceptance tests break this cycle.

---

## The Testing Pyramid

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

**Unit Tests (bottom):** The foundation — thousands run per second. Test individual functions and classes in isolation. Written by developers for developers.

**Functional Tests (lower-middle):** Test multiple units working together. Verify components integrate correctly at a technical level. Still developer-facing.

**Acceptance Tests (middle):** Check BUSINESS expectations, not technical correctness. Readable by non-developers: QAs, product owners, BAs, designers. NOT dependent on the UI. Automated and part of the regression suite.

**UI / System Tests (top):** Just a small handful — the most expensive and slowest. Test the full stack through the actual user interface. Fragile because they depend on everything. Should be very limited in ambition.

### The Ice Cream Cone Anti-Pattern

The inverted pyramid — tons of UI tests at the top, few or no unit tests at the bottom:

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

Teams with the ice cream cone end up with massive, fragile UI test suites that break constantly, slow feedback loops (hours instead of seconds), enormous maintenance burden, and false confidence — tests pass but business requirements are still wrong.

---

## The Problem with UI Testing

UI tests depend on literally everything: business rules, database, network, rendering, layout. The UI is the part of the system MOST likely to change. A single CSS change or redesign breaks the entire suite.

When teams build massive UI test suites, they create "automation monsters" — sprawling, fragile suites that take hours to run, break for reasons unrelated to business logic, and consume more effort to maintain than they save.

**The right approach:** Test business behavior BELOW the UI surface. Use acceptance tests that plug in at the controller/API level. Reserve UI tests for a small handful of critical user journeys. Think of acceptance tests as "an alternative UI" for the system.

---

## ATDD: Acceptance Test-Driven Development

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

**TDD** checks the PROGRAMMER'S understanding — "Does the code do what I think it should?"
**ATDD** checks BUSINESS expectations — "Does the system do what the business actually needs?"

Both are necessary. A system can pass all unit tests and still be the wrong product.

### When to Write Acceptance Criteria

Write acceptance criteria "just in time" — when a story is picked up for development, NOT during sprint planning or backlog grooming.

**Why not during planning?** Requirements evolve between planning and implementation. Writing criteria too early wastes effort on stories that may never be built. The conversation should happen close to implementation.

**Why not after coding?** Defeats the purpose — acceptance tests DEFINE done, they do not verify after the fact. Developers fill gaps with assumptions that may be wrong. Rework is far more expensive than getting it right upfront.

### Definition of Done

A feature is done when all acceptance tests pass, all unit tests pass, all UI tests (if any) pass, and code meets Clean Code standards. The acceptance tests ARE the definition of done. There is no ambiguity.

---

## Writing Good Acceptance Tests

### Properties

1. **Readable by everyone** — QAs, product owners, BAs, designers, and developers can all understand them
2. **Unambiguous** — no room for misinterpretation; if two people could read it differently, rewrite it
3. **Automatable** — can be executed by a machine without human intervention
4. **UI-independent** — do NOT reference buttons, pages, screens, or UI elements
5. **Business-focused** — test what the system DOES, not how it looks

### Good vs. Bad

**Bad — references UI:**
```
Given I am on the login page
When I type "admin" in the username field
And I click the "Login" button
Then I should see the dashboard page
```

**Good — tests business behavior:**
```
Given a registered user with username "admin"
When the user authenticates with valid credentials
Then the system grants access to the user's account
```

**Bad — ambiguous:**
```
Given a customer places an order
Then the order should be processed correctly
```

**Good — precise:**
```
Given a customer with a verified shipping address
And an order containing 3 items totaling $45.00
When the order is submitted with standard shipping
Then the order status is set to "CONFIRMED"
And the shipping cost is calculated as $5.99
And the order total is $50.99
```

### The Given/When/Then Pattern

- **Given** — establishes the preconditions (the state of the world before the action)
- **When** — describes the action being performed (one logical action per test)
- **Then** — specifies the expected outcomes (observable, verifiable results)

Each section should use business language, not technical jargon.

---

## The Fixture Pattern

Fixtures are thin adapter code that connects acceptance tests to production code. They sit between the test specification and the system under test.

```
┌─────────────────────┐
│   Acceptance Test    │  (Human-readable specification)
│   (Given/When/Then)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│      Fixture         │  (Thin adapter — translation only)
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

1. **Thin adapters** — fixtures contain NO business logic, only translation and delegation
2. **Simple mapping** — convert human-friendly test concepts into technical system calls
3. **Same level as controller** — fixtures plug in at the same level as the UI controller, bypassing the UI entirely
4. **No UI dependency** — acceptance tests are "an alternative UI" for the system
5. **Refactorable** — start simple, refactor so the fixture becomes a thin adapter over time

### Concept Translation

Tests use human-friendly concepts while code uses technical ones. The fixture handles this conversion:

```
Test says:              Fixture converts to:
"a premium customer"    → Customer(tier: PREMIUM)
"standard shipping"     → ShippingMethod.STANDARD
"order is confirmed"    → status == CONFIRMED
"$45.00"                → Money(4500, USD)
```

The fixture is the ONLY place this translation happens. Keep it simple and mechanical.

### Fixture Example

```
// Fixture — thin adapter connecting test to system
OrderProcessingFixture:
    orderService: OrderService
    request: OrderRequest
    response: OrderResponse

    // Given — set up preconditions
    setCustomerAddressVerified(verified):
        request.addressVerified = verified

    setOrderItems(count, total):
        request.itemCount = count
        request.subtotal = parseMoney(total)

    // When — execute the action
    submitOrder(shippingMethod):
        request.shipping = parseShippingMethod(shippingMethod)
        response = orderService.submit(request)

    // Then — query results
    orderStatus(): return response.status
    shippingCost(): return formatMoney(response.shippingCost)
    orderTotal(): return formatMoney(response.total)
    rejectionReason(): return response.rejectionReason
```

No business logic in the fixture. Only translation (parseMoney, parseShippingMethod) and delegation (orderService.submit).

---

## BDD and Acceptance Testing

BDD (Behavior-Driven Development) provides a less technical vocabulary for describing software behavior. The Given/When/Then format standardizes the specification language and makes tests accessible to non-developers.

BDD encompasses more than acceptance testing alone — collaborative specification (three amigos: developer, tester, business), living documentation, outside-in development, and acceptance test automation. Acceptance testing focuses specifically on automation and unambiguous "done" criteria.

### Common Misuse of BDD Tools

BDD tools are frequently misused as UI automation wrappers. This completely misses the point.

**Misuse — UI test in disguise:**
```
Given I navigate to "/orders/new"
When I fill in "customer_id" with "CUST-001"
And I click the "Add Item" button 3 times
And I click "Submit Order"
Then the page should contain "Order Confirmed"
```

**Correct — tests business behavior:**
```
Given a registered customer "CUST-001"
And 3 items in the order totaling $45.00
When the order is submitted
Then the order is confirmed with total $50.99
```

The collaborative intent of BDD is lost when it becomes a UI automation wrapper.

---

## Architecture for Testability

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

**Key principles:**
- Fixture plugs in at controller level — bypassing the UI entirely
- No business logic in UI layer — if logic lives in the UI, acceptance tests cannot reach it
- Dependencies must be injectable — fixtures need to substitute test implementations
- Acceptance tests = an alternative UI — the system should work identically whether driven by a human or by a fixture

Clean Architecture directly supports ATDD: Use Cases define clear boundaries that fixtures can call, Dependency Inversion allows fixtures to inject test doubles, Entities contain business rules testable without infrastructure, and Interface Adapters provide the controller-level API that fixtures plug into.

---

## The Transformed Role of QA

### Traditional QA (The Bottleneck)

Developers write code, throw it over the wall to QA, QA tests manually under time pressure, bugs are found late, fixes are expensive, QA becomes a bottleneck at the end of every sprint.

### ATDD QA (The Collaborator)

QA participates BEFORE development, writing acceptance criteria. Developers implement against those criteria using TDD. When acceptance tests pass, the feature is done. QA shifts focus to exploratory testing — finding edge cases that automated tests miss. QA is no longer a bottleneck.

---

## Review Checklist

When reviewing acceptance tests:

**Test Quality:**
- [ ] Acceptance criteria written BEFORE code
- [ ] Tests readable by all stakeholders (not just developers)
- [ ] No UI element references in acceptance tests
- [ ] Every Given/When/Then is precise and unambiguous
- [ ] One logical action per test (one When)

**Fixture Quality:**
- [ ] Fixtures are thin adapters with NO business logic
- [ ] Fixtures plug in at controller/API level, not through UI
- [ ] Concept translation is simple and mechanical

**Architecture:**
- [ ] System accessible without going through UI
- [ ] Dependencies are injectable for test doubles
- [ ] Business rules are in entities/use cases, not in UI layer

**Process:**
- [ ] Tests automated and fast enough for CI
- [ ] Tests added to regression suite
- [ ] QA involved in writing criteria, not just verifying after

---

## Common Pitfalls

**Testing through the UI.** Acceptance tests should bypass the UI and test business behavior directly. UI tests are the top of the pyramid — a small handful, not the primary testing strategy.

**Writing tests after code.** Acceptance criteria must be defined BEFORE development begins. Writing them after defeats their purpose — they DEFINE done, they do not verify after the fact.

**Ambiguous criteria.** If two people could interpret a test differently, it is not precise enough. Every acceptance criterion must have exactly one interpretation.

**Business logic in fixtures.** Fixtures are thin adapters. If you find conditionals, calculations, or business rules in fixture code, something is wrong — that logic belongs in production code.

**Using BDD tools as UI automation wrappers.** Cucumber, FitNesse, and similar tools are for specifying business behavior, not for driving Selenium. The collaborative intent is lost when they become UI test frameworks.

**Over-mocking.** Acceptance tests should exercise real business logic. If you mock so much that the test only verifies the mocks themselves, the test proves nothing about the system.

**Demo-driven development.** Showing incomplete work to stakeholders without passing acceptance tests. Demos should only happen when acceptance tests pass — they ARE the definition of done.

---

## Related Skills

- **/tdd** — Inner loop of development; acceptance tests are the outer loop that defines "done"
- **/architecture** — Clean Architecture enables testability by separating business rules from delivery mechanisms
- **/solid** — Dependency Inversion enables fixture injection and test double substitution
- **/components** — Component boundaries define where fixtures plug in
- **/professional** — Professional responsibility to communicate unambiguously through executable specifications
