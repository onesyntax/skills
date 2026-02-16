---
name: acceptance-testing
description: >-
  Operational guide for acceptance testing using ATDD principles. Activates when
  writing acceptance tests, implementing features with acceptance criteria,
  fixing acceptance test suites, or designing architecture for testability.
model: opus
delegates-to: [tdd, architecture, solid, components]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [feature or module to test]
---

# Acceptance Testing

## K-Line History

- **Acceptance tests as outer loop**: Run after WHEN designing a feature with acceptance criteria.
- **Fixture pattern**: Use WHEN acceptance tests exist but lack testable architecture.
- **ATDD before code**: Run WHEN picking up a user story.
- **Pyramid balance**: Run WHEN test suite grows; check ratio before adding more UI tests.
- **Thin fixture pattern**: Extract business logic into production code; keep fixtures as pure adapters.

---

## Step 0: Detect Context

Before applying acceptance testing strategy, detect the current state:

1. **Test Framework**
   - **PHP:** Check for `phpunit.xml`, test files in `tests/` directories, test runner in composer scripts.
   - **TypeScript:** Check for `jest.config.*`, test files matching `*.test.ts` or `*.test.tsx`, test runner in package.json, Cypress or Playwright config.
   - Language determines syntax and tooling, not strategy.

2. **Architecture Testability**
   - Can tests plug in below the UI (controller/API layer)?
   - If no: flag architectural barrier before proceeding.
   - If yes: fixtures can delegate directly to use cases.

3. **Existing Acceptance Tests**
   - Count: how many? (0, <10, 10-50, 50+)
   - Patterns: Given/When/Then? BDD? Ad-hoc?
   - Fixture quality: thin adapters or logic-heavy?
   - In CI pipeline? Running on every commit?

4. **Development Process**
   - Are acceptance tests written BEFORE code? (ATDD outer loop)
   - Or written AFTER code? (verification, not specification)
   - QA involved in writing criteria? Or only reviewing?

---

## Step 1: Classify the Situation

| Situation | Action |
|-----------|--------|
| **New feature with acceptance criteria** | Go to Step 2, Rule 1 (Given/When/Then). Write tests BEFORE code. |
| **Reviewing existing acceptance tests** | Go to Step 3 (Review Checklist). Check for UI references, fixture quality, precision. |
| **Broken/flaky acceptance test suite** | Go to Step 4 (Refactoring Patterns). Diagnose root cause: flaky fixture? Ambiguous criteria? Over-mocking? |
| **Architecture blocks acceptance testing** | Go to Step 2, Rule 2 (UI Independence). Restructure to allow controller-level access. |
| **Bug fix (not new feature)** | May not need acceptance test. Use characterization test only if no reproduction test exists. |

---

## Step 2: Apply Decision Rules

### Rule 1: Given/When/Then Structure

**WHEN:** Writing ANY acceptance test (new feature, bug reproduction, regression).
**WHEN NOT:** Writing performance/load tests, stress tests, or infrastructure tests.

**Pattern:**
- **Given:** Setup preconditions. Use business language. Each Given = one fact.
- **When:** One logical action. (Multiple "When" = split into separate tests.)
- **Then:** Expected outcomes. Verifiable. Observable. Specific values, not vague assertions.

**Red Flags:**
- Multiple actions in a single When ❌
- Ambiguous Then clauses ❌
- Technical jargon instead of business language ❌
- "Should work correctly" (vague) vs. "status is CONFIRMED" (precise) ✓

---

### Rule 2: UI Independence

**WHEN:** Every acceptance test. Tests must NOT reference UI elements.
**WHEN NOT:** UI/E2E tests are a separate layer (small handful, top of pyramid).

**Pattern:**
- Acceptance test plugs in at **controller/API level** (same entry point as UI).
- Fixture translates business concepts → system calls.
- Tests are "an alternative UI" — system behaves identically whether driven by human or fixture.

**Red Flags:**
- References to buttons, pages, forms, CSS selectors ❌
- "Click the 'Submit' button" ❌
- Navigation to URLs as test precondition ❌
- UI element assertions ✓ → Business assertion at controller level

**Fix:** Rewrite test at controller layer. Move UI references to separate E2E test.

**PHP Example:**
```php
// Acceptance test at controller level (not UI):
public function testUserAuthenticatesWithValidCredentials(): void {
    $this->userRepository->save(new User(['email' => 'admin@example.com']));
    $response = $this->authController->login(new LoginRequest('admin@example.com', 'password'));
    $this->assertTrue($response->isSuccess() && $response->token() !== null);
}
```

---

### Rule 3: Thin Fixture

**WHEN:** Fixture code exists and acceptance tests run.
**WHEN NOT:** Simple in-memory tests with no adapter needed (pure unit tests).

**Pattern:**
- Fixtures = pure adapters. NO business logic. NO conditionals. NO calculations.
- One-to-one mapping: test concept → system call.
- Example: "premium customer" → `Customer(tier: PREMIUM)`. Translation only.

**Red Flags:**
- Conditionals in fixture ❌
- Calculations (e.g., shipping cost) in fixture ❌
- Complex setup logic in fixture ❌
- If/else branches ❌

**Fix:** Move logic to production code (service, entity). Fixture stays as thin translator.

**PHP Example:**
```php
// Before: business logic in test setup
$discount = $customer->tier === 'PREMIUM' ? 0.1 : 0;
$total = array_sum(array_column($items, 'price')) * (1 - $discount);

// After: fixture delegates to service
$result = $this->orderService->submit($orderRequest);
```

---

### Rule 4: ATDD Outer Loop

**WHEN:** Starting a new feature (user story pickup).
**WHEN NOT:** Bug fixes with clear reproduction. (Use step-to-reproduce, not acceptance test.)

**Sequence:**
1. Pick up story; collaborate: acceptance criteria (Given/When/Then).
2. Write failing acceptance test (RED).
3. TDD loop: unit tests + code (GREEN → REFACTOR).
4. Acceptance test passes = feature done.

**Anti-pattern:** Write code first, tests after. Tests verify, not define.

---

### Rule 5: Acceptance Test Timing

**WHEN:** Write BEFORE code. During story pickup. With BA/QA present.
**WHEN NOT:** Characterization tests (legacy code with no tests). Those are POST-code.

**Discipline:**
- Tests are the **specification**, not verification.
- Written during **"three amigos"** session: developer, tester, business.
- Accepted by business BEFORE coding starts.
- Prevents rework: "That's not what we meant" discovered too late.

---

### Rule 6: Pyramid Balance

**WHEN:** Test suite exists. Check before adding more tests.
**WHEN NOT:** New project (build foundation first: units, then acceptance, then UI).

**Ideal Ratio (by count):** 70% unit : 20% acceptance : 10% UI.
**Anti-pattern (Ice Cream Cone):** 10% unit : 20% acceptance : 70% UI.

**Assessment (PHP + TypeScript):**
```bash
# Count tests in each layer
find . -path "*/tests/*" -name "*Test.php" | wc -l              # PHP unit/integration tests
find . -name "*.test.ts" -o -name "*.test.tsx" | wc -l         # TypeScript component tests
find . -name "*.e2e.ts" -o -name "*.spec.ts" -path "*cypress*" | wc -l  # E2E
```

**Action:** If pyramid is inverted (UI heavy), migrate high-cost UI tests down to acceptance or unit.

---

## Step 3: Review Checklist

### Acceptance Test Quality

| Check | Severity | Fix |
|-------|----------|-----|
| Test references UI elements (buttons, pages, CSS selectors) | 🔴 CRITICAL | Rewrite at controller layer. Move UI references to E2E test. |
| Multiple "When" actions in one test | 🔴 CRITICAL | Split into separate tests. One logical action per test. |
| Ambiguous Given/When/Then (could be interpreted multiple ways) | 🔴 CRITICAL | Rewrite with specific values. "Order confirmed" → "status = CONFIRMED, total = $50.99". |
| No acceptance tests for user-facing feature | 🔴 CRITICAL | Write ATDD criteria before code. |
| Acceptance test written AFTER code | 🟡 MAJOR | Document why (legacy code?). Plan to move to pre-code for future work. |
| Given/When/Then mixes business and technical language | 🟡 MAJOR | Rewrite in business terms. Fixture handles translation. |
| Acceptance tests not in CI pipeline | 🟡 MAJOR | Add to CI. Acceptance tests must run on every commit. |

### Fixture Quality

| Check | Severity | Fix |
|-------|----------|-----|
| Business logic in fixture code | 🔴 CRITICAL | Extract to use case, entity, or service. Fixture is adapter only. |
| Fixture sets up complex state through multiple system calls | 🔴 CRITICAL | Use test doubles or builder for setup. Simplify to one call per Given. |
| Fixture references UI (DOM, CSS selectors, page objects) | 🔴 CRITICAL | Rewrite to use API/controller directly. |
| Fixture assumes specific implementation details | 🟡 MAJOR | Decouple from implementation. Use contracts/interfaces. |
| Over-mocking in fixture | 🟡 MAJOR | Mock only external dependencies (DB, HTTP). Exercise real business logic. |

### Architecture & Process

| Check | Severity | Fix |
|-------|----------|-----|
| System not testable without going through UI | 🔴 CRITICAL | Refactor to expose controller/API layer. Dependencies must be injectable. |
| Dependencies not injectable | 🔴 CRITICAL | Apply Dependency Inversion. Fixtures need to substitute test doubles. |
| Business logic lives in UI layer | 🔴 CRITICAL | Migrate business logic to entities/use cases. UI is thin adapter. |
| Tests pass but feature doesn't match business requirements | 🟡 MAJOR | Acceptance criteria were ambiguous. Rewrite with business involvement. |
| Test suite slow (>1 minute for all acceptance tests) | 🟡 MAJOR | Migrate from DB/HTTP to in-memory test doubles. Parallel execution. |
| QA not involved in writing criteria | 🟡 MAJOR | Shift QA to specification (ATDD) phase, not just verification. |

---

## Step 4: Refactoring Patterns

### Pattern 1: Extract UI from Acceptance Test

**Symptom:** Acceptance test references buttons, pages, form fields, CSS selectors.

**Cause:** Test written as UI automation instead of business specification.

**Solution:**
1. Identify the business intent (what outcome does clicking the button achieve?).
2. Rewrite test at controller/API level.
3. Move UI references to separate E2E test.

**Before:**
```gherkin
Given I am on the login page
When I type "admin" in the username field
And I click the "Login" button
Then I should see the dashboard page
```

**After (Acceptance Test):**
```gherkin
Given a registered user "admin"
When the user authenticates with valid credentials
Then the user gains access to their account
```

**After (Separate E2E Test):**
```gherkin
Given the login page is displayed
When the user enters "admin" in the username field
And clicks the "Login" button
Then the dashboard page loads
```

---

### Pattern 2: Thin the Fixture

**Symptom:** Fixture contains conditionals, calculations, setup logic.

**Cause:** Business logic crept into adapter code.

**Solution:**
1. Identify all non-translation code in fixture.
2. Move calculations/conditionals to production code (service, entity, domain model).
3. Fixture becomes pure mapping: test concept → system call.

**Before (PHP):**
```php
class OrderFixture {
    public function submitOrder(): void {
        // WRONG: Business logic in fixture
        $discount = $this->customer->tier === "PREMIUM" ? 0.1 : 0;
        $subtotal = array_sum(array_column($this->items, 'price'));
        $total = $subtotal * (1 - $discount);
        $this->orderService->submit($total);
    }
}
```

**After (PHP):**
```php
class OrderFixture {
    public function submitOrder(): void {
        // RIGHT: Pure delegation
        $this->orderService->submit($this->orderRequest);
    }
}
// Discount calculation moves to OrderService::calculateTotal()
```

---

### Pattern 3: Convert Ambiguous to Precise

**Symptom:** Given/When/Then could be interpreted multiple ways.

**Cause:** Test written too abstractly. Business language without concrete values.

**Solution:**
1. Identify ambiguous words: "correct", "appropriate", "valid", "properly".
2. Add concrete values: amounts, status codes, counts.
3. Rewrite so only one interpretation is possible.

**Before (Business-facing, ambiguous):**
```gherkin
Given a customer places an order
When the order is processed correctly
Then the order should be valid
```

**After (Business-facing, precise):**
```gherkin
Given a customer with verified shipping address
And an order containing 3 items totaling $45.00
When the order is submitted
Then the order status is "CONFIRMED"
And the shipping cost is $5.99
And the order total is $50.99
```

**TypeScript Example (acceptance-level service test):**
```typescript
import { AuthService } from './auth-service';

test('user authenticates with valid credentials', async () => {
    const authService = new AuthService(userRepository, tokenGenerator);

    const result = await authService.authenticate({
        email: 'admin@example.com',
        password: 'password'
    });

    expect(result.isSuccess()).toBe(true);
    expect(result.token()).toBeDefined();
});
```

---

### Pattern 4: Add Acceptance Outer Loop to Existing Feature

**Symptom:** Feature coded but no acceptance tests.

**Solution:** Write acceptance test (will PASS immediately). Test becomes regression guard. For future features: start with acceptance test RED.

---

### Pattern 5: Fix Pyramid Balance

**Symptom:** Test suite inverted (mostly UI tests, few unit tests).

**Solution:** Count tests per layer. Migrate high-cost UI tests down to acceptance or unit level. Incremental replacement: write acceptance + unit tests, then delete UI test.

---

## When NOT to Apply

1. **Performance/Load Tests** — Not acceptance tests. Use separate benchmarking framework.
2. **Infrastructure Tests** — Database connectivity, cache warmup. Use separate layer.
3. **Bug Fix with Clear Reproduction** — If bug is reproducible with unit test, prefer unit test. Acceptance test may be overkill.
4. **Unstable Architecture** — If system cannot be tested without going through UI, fix architecture first (Rule 2). Acceptance tests will be brittle until then.
5. **One-Off Spike/Prototype** — Acceptance tests require discipline. Prototypes don't need them.

---

## Communication Style

**Direct. Not prescriptive. Evidence-based.**

❌ "You should write acceptance tests." (Vague.)
✓ "Given/When/Then format removed ambiguity in your acceptance criteria. 'Order confirmed' → 'status = CONFIRMED'. One test now, instead of rework later." (Specific, outcome-focused.)

❌ "Fixtures are thin adapters." (Teaching.)
✓ "Discount logic in your fixture should move to OrderService.calculateTotal(). Fixture is pure translator: order concept → system call." (Action-oriented.)

❌ "Test through the controller, not the UI." (Rule.)
✓ "Your acceptance test references login form and dashboard page. That couples the test to UI changes. Rewrite at the authentication boundary (controller): 'user authenticates' → 'user gains access'. UI can change; test stays stable." (Why + how.)

---

## Related Skills

- **/tdd** — TDD is the inner loop; acceptance tests are the outer loop that defines "done".
- **/architecture** — Clean Architecture (layers, use cases, entities) enables acceptance test design.
- **/solid** — Dependency Inversion allows fixtures to inject test doubles.
- **/components** — Component boundaries define where fixtures plug in.
- **/refactor-suggestion** — Use when acceptance test fixture grows too complex.
