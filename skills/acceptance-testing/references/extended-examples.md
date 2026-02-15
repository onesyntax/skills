# Acceptance Testing — Extended Examples

Full feature walkthroughs, tool-specific examples, and detailed fixture patterns.

---

## Example: Complete Order Processing Feature

### Step 1: Identify Business Requirements

**Feature:** Order submission and processing
**Actors:** Customer, Operations team, Finance team
**Business Question:** How do we know when an order is correctly processed?

### Step 2: Write Acceptance Criteria

```
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

```
OrderProcessingFixture:
    orderService: OrderService
    request: OrderRequest
    response: OrderResponse

    // Given
    setCustomerAddressVerified(verified):
        request.addressVerified = verified

    setOrderItems(count, total):
        request.itemCount = count
        request.subtotal = parseMoney(total)

    setEmptyOrder():
        request.itemCount = 0
        request.subtotal = parseMoney("$0.00")

    // When
    submitOrder(shippingMethod):
        request.shipping = parseShippingMethod(shippingMethod)
        response = orderService.submit(request)

    submitOrderDefault():
        response = orderService.submit(request)

    // Then
    orderStatus(): return response.status
    shippingCost(): return formatMoney(response.shippingCost)
    orderTotal(): return formatMoney(response.total)
    rejectionReason(): return response.rejectionReason
```

### Step 4: TDD Inner Loop

Use TDD to implement `orderService.submit()`:

```
Cycle 1:
  RED:      test "empty order is rejected"
  GREEN:    if request.itemCount == 0: return rejected("EMPTY_ORDER")
  REFACTOR: extract OrderValidator

Cycle 2:
  RED:      test "standard shipping adds $5.99"
  GREEN:    if shipping == STANDARD: cost = Money(599, USD)
  REFACTOR: extract ShippingCalculator

Cycle 3:
  RED:      test "order total includes shipping"
  GREEN:    total = subtotal + shippingCost
  REFACTOR: extract OrderTotal value object

Cycle 4:
  RED:      test "unverified address creates pending order"
  GREEN:    if not addressVerified: return pending("PENDING_ADDRESS_VERIFICATION")
  REFACTOR: extract AddressVerificationPolicy

Continue until all acceptance scenarios pass...
```

### Step 5: Verify

Run acceptance tests. All scenarios pass. Feature is DONE.

---

## Example: User Registration Feature

### Acceptance Criteria

```
Feature: User Registration

  Scenario: Successful registration
    Given a new user with email "alice@example.com"
    And a password meeting strength requirements
    When the user registers
    Then the account is created with status "ACTIVE"
    And a welcome email is queued for "alice@example.com"

  Scenario: Duplicate email rejected
    Given an existing user with email "bob@example.com"
    And a new user attempting to register with email "bob@example.com"
    When the user registers
    Then the registration is rejected with reason "EMAIL_ALREADY_EXISTS"
    And no new account is created

  Scenario: Weak password rejected
    Given a new user with email "carol@example.com"
    And a password "123"
    When the user registers
    Then the registration is rejected with reason "PASSWORD_TOO_WEAK"
    And the minimum requirements are listed

  Scenario: Email verification required
    Given a new user with email "dave@example.com"
    And the system requires email verification
    When the user registers
    Then the account is created with status "PENDING_VERIFICATION"
    And a verification email is queued for "dave@example.com"
```

### Fixture

```
UserRegistrationFixture:
    registrationService: RegistrationService
    emailQueue: TestEmailQueue  // test double — captures emails without sending
    request: RegistrationRequest
    response: RegistrationResponse

    // Given
    setEmail(email): request.email = email
    setPassword(password): request.password = password
    setEmailVerificationRequired(required): config.emailVerification = required

    createExistingUser(email):
        registrationService.register(RegistrationRequest(email: email, password: "ValidPass1!"))

    // When
    register():
        response = registrationService.register(request)

    // Then
    accountStatus(): return response.status
    rejectionReason(): return response.rejectionReason
    emailQueuedFor(): return emailQueue.lastRecipient()
    accountCreated(): return response.accountId != nil
    minimumRequirementsListed(): return response.passwordRequirements != nil
```

Notice: the fixture uses a TestEmailQueue (a test double) so we can verify emails were "sent" without actually sending them. The test double is injected through Dependency Inversion.

---

## Example: FitNesse Table Format

FitNesse represents acceptance tests as wiki tables. Input columns have no suffix; output columns have a `?` suffix:

```
|Order Processing                                           |
|customer id|address verified|item count|submit?|status?    |
|CUST-001   |true            |3         |true   |CONFIRMED  |
|CUST-002   |true            |0         |true   |REJECTED   |
|GUEST      |false           |1         |true   |PENDING    |
```

Each column maps to a fixture method:
- `customer id` → `setCustomerId(value)`
- `address verified` → `setAddressVerified(value)`
- `item count` → `setItemCount(value)`
- `submit?` → `submit()` (action column)
- `status?` → `status()` (query column, checked against expected value)

FitNesse renders results with colors: green for pass, red for fail, yellow for exceptions.

### Decision Table

Tests multiple scenarios in a single table — each row is a separate test case:

```
|Shipping Cost Calculator                              |
|weight kg|destination|method  |cost?  |delivery days?|
|1.0      |domestic   |standard|$5.99  |5-7           |
|1.0      |domestic   |express |$12.99 |1-2           |
|5.0      |domestic   |standard|$9.99  |5-7           |
|1.0      |international|standard|$15.99|10-14        |
|10.0     |international|express |$45.99|3-5          |
```

### Query Table

Verifies a set of results returned by the system:

```
|Query: Active Orders for Customer CUST-001|
|order id |status    |total  |
|ORD-101  |CONFIRMED |$50.99 |
|ORD-102  |SHIPPED   |$23.50 |
```

---

## Example: Multi-Scenario Feature with Edge Cases

### Inventory Management

```
Feature: Inventory Reservation

  Scenario: Reserve available stock
    Given product "WIDGET-A" with 100 units in stock
    When 5 units are reserved for order "ORD-001"
    Then the reservation is confirmed
    And available stock for "WIDGET-A" is 95

  Scenario: Reject reservation for insufficient stock
    Given product "WIDGET-B" with 2 units in stock
    When 5 units are reserved for order "ORD-002"
    Then the reservation is rejected with reason "INSUFFICIENT_STOCK"
    And available stock for "WIDGET-B" remains 2

  Scenario: Concurrent reservations
    Given product "WIDGET-C" with 10 units in stock
    When 7 units are reserved for order "ORD-003"
    And 5 units are reserved for order "ORD-004"
    Then the first reservation is confirmed
    And the second reservation is rejected with reason "INSUFFICIENT_STOCK"
    And available stock for "WIDGET-C" is 3

  Scenario: Release reservation restores stock
    Given product "WIDGET-D" with 50 units in stock
    And 10 units reserved for order "ORD-005"
    When the reservation for order "ORD-005" is released
    Then available stock for "WIDGET-D" is 50

  Scenario: Reservation expires after timeout
    Given product "WIDGET-E" with 20 units in stock
    And 5 units reserved for order "ORD-006"
    When the reservation timeout of 30 minutes expires
    Then the reservation is automatically released
    And available stock for "WIDGET-E" is 20
```

### What Makes This Good

- **No UI references** — tests business behavior only
- **Precise numbers** — every scenario has exact quantities and expected results
- **Edge cases covered** — insufficient stock, concurrent access, expiration
- **Business language** — "reserved," "released," "available stock" — not database terms
- **Each scenario is independent** — no test depends on another test's state
- **One logical action per When** — except the concurrent test, which explicitly tests two actions

---

## Example: Fixture Architecture for Large Systems

In large systems, fixtures can be organized into layers:

```
┌─────────────────────────────────────┐
│         Acceptance Tests             │
│  (Given/When/Then specifications)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        Domain Fixtures               │
│  OrderFixture, UserFixture, etc.     │
│  (translate business concepts)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        System Driver                 │
│  (shared setup: test DB, test        │
│   email, test clock, etc.)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        Production Code               │
│  (Use Cases, Entities, Gateways)     │
└─────────────────────────────────────┘
```

**Domain Fixtures** translate business concepts to system calls. Each fixture covers one domain (orders, users, inventory). They share NO state with each other.

**System Driver** manages shared infrastructure: test database setup/teardown, test email queue, controllable clock for time-dependent tests, test payment gateway. Each test gets a clean state.

This layering keeps individual fixtures thin while supporting complex multi-domain scenarios.
