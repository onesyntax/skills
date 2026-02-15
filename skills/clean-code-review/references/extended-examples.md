# Clean Code Review — Extended Examples

Full review walkthroughs showing how to apply the review checklist systematically, with before/after code.

---

## Example: Reviewing an Order Processing Module

### The Code Under Review

```
// OrderProcessor — handles order placement
processOrder(o, t, d, notify):
    if o == null: return -1
    if o.items == null: return -2
    if o.items.length == 0: return -3

    // calc total
    tot = 0
    for i = 0 to o.items.length:
        if o.items[i].qty > 0:
            tot = tot + (o.items[i].price * o.items[i].qty)
            if o.items[i].taxable:
                tot = tot + (o.items[i].price * o.items[i].qty * t)
    // apply disc
    if d > 0:
        tot = tot - (tot * d)
    if tot < 0: tot = 0

    // save
    db = Database.getConnection()
    db.execute("INSERT INTO orders VALUES (" + o.id + "," + tot + ")")

    // notify
    if notify:
        smtp = SmtpClient.create()
        smtp.send(o.customer.email, "Order confirmed", "Total: " + tot)

    return tot
```

### Review Walkthrough

**Step 1: Naming** — CRITICAL issues

- `o, t, d` — single-letter parameter names reveal nothing. Should be `order, taxRate, discountRate`
- `tot` — abbreviated. Should be `totalAmount`
- `notify` — flag argument (see Functions). But the name is at least clear
- `i` — acceptable only in a simple loop counter context
- `processOrder` — acceptable verb-noun combination

**Step 2: Functions** — CRITICAL issues

- Function does at least 5 things: validates, calculates total, applies discount, saves to database, sends email
- Flag argument `notify` — two functions hiding inside one
- 4 parameters (order, taxRate, discountRate, notify) — too many
- Mixed abstraction levels: business logic (calculate total) mixed with infrastructure (SQL, SMTP)
- Side effects: saves to database AND sends email

**Step 3: Classes** — WARNING issues

- No class structure visible — this is a procedural script
- Database access hardcoded (no dependency injection)
- SMTP client hardcoded (no dependency injection)
- Violates DIP: high-level policy depends on low-level details

**Step 4: Error Handling** — CRITICAL issues

- Returns error codes (-1, -2, -3) instead of exceptions
- No error handling for database failure
- No error handling for email failure
- If email fails after database save, order is saved but customer isn't notified — inconsistent state

**Step 5: Comments** — WARNING issues

- `// calc total` and `// apply disc` are noise comments — the code should be self-documenting
- `// save` and `// notify` are section markers indicating the function does too many things

**Step 6: Formatting** — SUGGESTION

- No vertical separation between logical sections
- SQL string concatenation (also a security issue)

**Step 7: Tests** — CRITICAL

- No tests exist
- Function is untestable due to hardcoded database and SMTP dependencies
- Cannot test calculation logic without side effects

### After Review — Refactored Code

```
placeOrder(order, pricing):
    validateOrder(order)
    total = calculateOrderTotal(order.items, pricing)
    orderRepository.save(order, total)
    notificationService.sendOrderConfirmation(order.customer, total)
    return total

validateOrder(order):
    if order is null: throw InvalidOrderException("Order cannot be null")
    if order.items is empty: throw InvalidOrderException("Order must have items")

calculateOrderTotal(items, pricing):
    subtotal = sumOf(items, item -> item.price * item.quantity)
    tax = sumOf(items.filter(taxable), item -> item.price * item.quantity * pricing.taxRate)
    discount = (subtotal + tax) * pricing.discountRate
    return max(0, subtotal + tax - discount)

// OrderRepository and NotificationService are injected dependencies
// Each can be tested independently with test doubles
```

**Issues resolved:** 5 CRITICAL, 2 WARNING, 1 SUGGESTION. Functions now do one thing each, dependencies are injected, exceptions replace error codes, calculation logic is testable in isolation.

---

## Example: Reviewing Test Code

### The Tests Under Review

```
test "test1":
    o = createOrder([item(10, 2)])
    result = processOrder(o, 0, 0, false)
    assert result == 20

test "test2":
    o = createOrder([item(10, 2), item(5, 3)])
    result = processOrder(o, 0.1, 0, false)
    assert result == 36.5

test "test order processing works":
    o = createOrder([item(100, 1)])
    result = processOrder(o, 0.08, 0.1, true)
    db = Database.getConnection()
    row = db.query("SELECT * FROM orders WHERE id = " + o.id)
    assert row != null
    assert row.total == 97.2
    smtp = SmtpClient.getLastMessage()
    assert smtp.to == o.customer.email
    assert smtp.body.contains("97.2")
```

### Review Walkthrough

**Naming** — CRITICAL

- `test1`, `test2` — meaningless test names. Tests should describe the behavior being verified
- Names should read like specifications: "order total is sum of item prices times quantities"

**One concept per test** — CRITICAL

- `test "test order processing works"` tests three things: calculation, database persistence, and email notification
- Should be three separate tests

**Independence** — CRITICAL

- Tests depend on real database and SMTP server
- Tests are not independent — database state from one test could affect another
- Tests are not repeatable — depend on external infrastructure

**Readability** — WARNING

- No Arrange/Act/Assert structure visible
- Magic numbers (0.1, 0.08, 36.5, 97.2) without explanation
- Reader must mentally compute expected values

### After Review — Refactored Tests

```
test "order total is sum of item prices times quantities":
    items = [item(price: 10, quantity: 2), item(price: 5, quantity: 3)]
    pricing = Pricing(taxRate: 0, discountRate: 0)

    total = calculateOrderTotal(items, pricing)

    assert total == 35  // (10*2) + (5*3)

test "tax is applied only to taxable items":
    items = [item(price: 100, quantity: 1, taxable: true),
             item(price: 50, quantity: 1, taxable: false)]
    pricing = Pricing(taxRate: 0.10, discountRate: 0)

    total = calculateOrderTotal(items, pricing)

    assert total == 160  // 100 + 10 tax + 50 no tax

test "discount applies to total after tax":
    items = [item(price: 100, quantity: 1, taxable: true)]
    pricing = Pricing(taxRate: 0.08, discountRate: 0.10)

    total = calculateOrderTotal(items, pricing)

    assert total == 97.2  // (100 + 8 tax) * 0.90 discount

test "order is persisted after placement":
    order = createOrder([item(price: 10, quantity: 1)])
    mockRepository = MockOrderRepository()
    processor = OrderProcessor(repository: mockRepository, ...)

    processor.placeOrder(order, defaultPricing)

    assert mockRepository.savedOrder == order

test "confirmation email is sent after order placed":
    order = createOrder([item(price: 10, quantity: 1)])
    mockNotifier = MockNotificationService()
    processor = OrderProcessor(..., notifier: mockNotifier)

    processor.placeOrder(order, defaultPricing)

    assert mockNotifier.sentTo == order.customer.email
```

**Issues resolved:** Tests have descriptive names (specifications), each tests one concept, dependencies are mocked, values are explained with comments, Arrange/Act/Assert structure is clear.

---

## Example: Reviewing Error Handling

### The Code Under Review

```
transferFunds(fromAccount, toAccount, amount):
    if fromAccount == null: return "ERROR_NULL_FROM"
    if toAccount == null: return "ERROR_NULL_TO"
    if amount <= 0: return "ERROR_INVALID_AMOUNT"

    fromBalance = accountDb.getBalance(fromAccount)
    if fromBalance == null: return "ERROR_ACCOUNT_NOT_FOUND"
    if fromBalance < amount: return "ERROR_INSUFFICIENT_FUNDS"

    result1 = accountDb.debit(fromAccount, amount)
    if result1 == null: return "ERROR_DEBIT_FAILED"

    result2 = accountDb.credit(toAccount, amount)
    if result2 == null:
        // try to reverse the debit
        accountDb.credit(fromAccount, amount)
        return "ERROR_CREDIT_FAILED"

    logTransaction(fromAccount, toAccount, amount)
    return "SUCCESS"
```

### Review Walkthrough

**Error codes instead of exceptions** — CRITICAL

The function returns 7 different error strings. The caller must check each one with string comparison — fragile and easy to miss. Exceptions would force callers to handle errors or explicitly ignore them.

**No error handling for the reversal** — CRITICAL

If `accountDb.credit(toAccount, amount)` fails and the reversal `accountDb.credit(fromAccount, amount)` also fails, money is lost. The reversal has no error handling of its own.

**Transaction safety** — CRITICAL

This operation should be atomic. If the debit succeeds but the credit fails, manually reversing is unreliable. This needs a database transaction or saga pattern.

**Caller burden** — WARNING

Every caller must write:
```
result = transferFunds(from, to, 100)
if result == "ERROR_NULL_FROM": ...
else if result == "ERROR_NULL_TO": ...
else if result == "ERROR_INVALID_AMOUNT": ...
// ... 7 branches
```

### After Review — Refactored Code

```
transferFunds(fromAccount, toAccount, amount):
    validateTransferRequest(fromAccount, toAccount, amount)
    ensureSufficientFunds(fromAccount, amount)

    try:
        transactionManager.executeAtomically:
            accountRepository.debit(fromAccount, amount)
            accountRepository.credit(toAccount, amount)
    catch DatabaseException as e:
        throw TransferFailedException("Transfer from " + fromAccount.id +
            " to " + toAccount.id + " failed", cause: e)

    auditLog.recordTransfer(fromAccount, toAccount, amount)

validateTransferRequest(from, to, amount):
    if from is null: throw InvalidArgumentException("Source account required")
    if to is null: throw InvalidArgumentException("Target account required")
    if amount <= 0: throw InvalidArgumentException("Amount must be positive: " + amount)

ensureSufficientFunds(account, amount):
    balance = accountRepository.getBalance(account)
    if balance < amount:
        throw InsufficientFundsException(
            "Account " + account.id + " has " + balance + ", needs " + amount)
```

**Issues resolved:** Exceptions replace error codes, atomic transaction replaces manual reversal, exception messages provide context, validation is separated from business logic, callers get clear exception types they can catch selectively.

---

## Example: Architecture Boundary Review

### The Code Under Review

```
// UserController — handles user registration
UserController:
    registerUser(request):
        // Validate
        if request.email == null: return Response(400, "Email required")
        if not request.email.contains("@"): return Response(400, "Invalid email")
        if request.password.length < 8: return Response(400, "Password too short")

        // Check duplicate
        db = PostgresConnection.getInstance()
        existing = db.query("SELECT id FROM users WHERE email = ?", request.email)
        if existing != null: return Response(409, "Email taken")

        // Hash password
        salt = generateSalt()
        hash = bcrypt(request.password, salt)

        // Save
        db.execute("INSERT INTO users (email, password_hash, salt) VALUES (?, ?, ?)",
                   request.email, hash, salt)

        // Send welcome email
        smtp = SmtpClient("smtp.gmail.com", 587)
        smtp.send(request.email, "Welcome!", renderWelcomeTemplate(request.email))

        return Response(201, "User created")
```

### Review Walkthrough

**Dependency direction** — CRITICAL

The controller (outer ring) contains business rules (validation, duplicate checking) and directly accesses infrastructure (PostgreSQL, SMTP). Business rules should be in use cases, infrastructure behind interfaces.

**No boundaries** — CRITICAL

Everything is in one layer. The registration policy (what makes a valid registration) is tangled with how users are stored and how emails are sent. Changing email providers requires modifying the controller.

**Framework coupling** — WARNING

Business rules (password requirements, duplicate checking) are locked inside a web controller. They can't be reused from a CLI tool, a message queue consumer, or a test without HTTP.

### After Review — Refactored with Boundaries

```
// Use Case (inner ring — pure business logic)
RegisterUser:
    userRepository: UserRepository      // interface
    notifier: UserNotifier              // interface
    passwordHasher: PasswordHasher      // interface

    execute(request):
        validateRegistration(request)
        ensureEmailAvailable(request.email)
        hashedPassword = passwordHasher.hash(request.password)
        user = User(email: request.email, password: hashedPassword)
        userRepository.save(user)
        notifier.welcomeNewUser(user)
        return user

    validateRegistration(request):
        if request.email is empty: throw ValidationException("Email required")
        if not isValidEmail(request.email): throw ValidationException("Invalid email")
        if request.password.length < 8: throw ValidationException("Password too short")

    ensureEmailAvailable(email):
        if userRepository.existsByEmail(email):
            throw DuplicateEmailException(email)

// Controller (outer ring — just translates HTTP to use case calls)
UserController:
    registerUser: RegisterUser    // injected use case

    handleRegistration(httpRequest):
        try:
            request = RegistrationRequest(httpRequest.body)
            user = registerUser.execute(request)
            return HttpResponse(201, "User created")
        catch ValidationException as e:
            return HttpResponse(400, e.message)
        catch DuplicateEmailException:
            return HttpResponse(409, "Email taken")

// Infrastructure (outer ring — implements interfaces)
PostgresUserRepository implements UserRepository: ...
SmtpUserNotifier implements UserNotifier: ...
BcryptPasswordHasher implements PasswordHasher: ...
```

**Issues resolved:** Business rules are in the use case (testable without HTTP, database, or SMTP), dependencies point inward through interfaces, infrastructure is pluggable, controller is thin and only translates between HTTP and use cases.
