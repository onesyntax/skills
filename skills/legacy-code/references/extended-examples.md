# Legacy Code — Extended Examples

Detailed walkthroughs of characterization tests, strangulation strategies, and real-world acts of kindness.

---

## Example: Writing Characterization Tests for a Report Generator

### The Legacy Module

A 500-line `ReportGenerator` that reads from the database and produces formatted text reports. No tests exist. Nobody understands all the formatting rules. The business wants to change the date format from MM/DD/YYYY to YYYY-MM-DD.

### Step 1: Identify I/O Boundaries

```
Input:  Database with known test data + report type + date range
Output: Formatted text report (string)

The module has clear boundaries — data goes in, a report string comes out.
This is a perfect candidate for characterization tests.
```

### Step 2: Capture the Golden Standard

```
// Set up known test data
testDb = createTestDatabase()
testDb.insert(salesRecords: [
    {date: "2024-01-15", customer: "Acme Corp", amount: 1500.00},
    {date: "2024-01-20", customer: "Beta Inc",  amount: 750.00},
    {date: "2024-02-01", customer: "Acme Corp", amount: 2200.00}
])

// Run the legacy module and capture output
report = legacyReportGenerator.generate("sales", "2024-01-01", "2024-02-28")

// Save as golden standard
writeFile("golden/sales-report-jan-feb.txt", report)
```

The golden standard file now contains the exact output the legacy code produces. We don't need to understand every formatting rule — we just capture the result.

### Step 3: Create the Characterization Test

```
test "sales report matches golden standard":
    testDb = loadTestFixture("sales-test-data")
    report = legacyReportGenerator.generate("sales", "2024-01-01", "2024-02-28")
    expected = readFile("golden/sales-report-jan-feb.txt")
    assert report == expected
```

### Step 4: Now It's Safe to Refactor

Change the date format. Regenerate. Compare. If only the dates changed and everything else matches, you know the refactoring is correct.

```
// After changing date format
newReport = legacyReportGenerator.generate("sales", "2024-01-01", "2024-02-28")

// Compare with golden standard — expect ONLY date format differences
diff(newReport, goldenStandard):
  Line 3: "01/15/2024" → "2024-01-15"  ✓ Expected
  Line 4: "01/20/2024" → "2024-01-20"  ✓ Expected
  Line 5: "02/01/2024" → "2024-02-01"  ✓ Expected
  (no other differences)               ✓ Safe!

// Update the golden standard with new expected output
writeFile("golden/sales-report-jan-feb.txt", newReport)
```

### Step 5: Snowball — Now Add Real Tests

With the date format changed, you notice the date formatting logic is now in its own function (an act of kindness from the refactoring). Now you can write a proper unit test:

```
test "formatDate converts to ISO format":
    assert formatDate("01/15/2024") == "2024-01-15"
    assert formatDate("12/31/2023") == "2023-12-31"
```

One characterization test led to one refactoring, which led to one unit test. The snowball is rolling.

---

## Example: Strangulation Over Six Months

### Month 1: The Starting Point

A monolithic `PaymentProcessor` handles Stripe, PayPal, and bank transfers in one 2000-line class. No tests. The team needs to add Apple Pay.

```
PaymentProcessor (2000 lines, 0 tests):
    processStripePayment()    // 400 lines
    processPayPalPayment()    // 350 lines
    processBankTransfer()     // 300 lines
    calculateFees()           // 200 lines
    generateReceipt()         // 250 lines
    handleRefund()            // 300 lines
    validatePayment()         // 200 lines
```

### Month 1: Add Apple Pay as Clean Module

Don't touch the legacy code. Write Apple Pay in a clean module with TDD:

```
ApplePayProcessor:  // new, clean, 80 lines, 15 tests
    processPayment(token, amount): ...
    validateToken(token): ...
    calculateFees(amount): ...

// Integration — ONE line added to legacy code
PaymentProcessor:
    processPayment(method, ...):
        if method == "apple_pay":
            return applePayProcessor.processPayment(token, amount)
        ... existing legacy code ...
```

### Month 2: Characterization Tests for Fee Calculation

While fixing a fee calculation bug, write characterization tests for `calculateFees`:

```
test "fees match golden standard":
    assert calculateFees("stripe", 100.00) == 3.20
    assert calculateFees("paypal", 100.00) == 3.49
    assert calculateFees("bank", 100.00) == 0.50
```

Act of kindness: extract `calculateFees` into its own class.

```
FeeCalculator:  // extracted, now testable
    calculate(method, amount): ...

PaymentProcessor:
    calculateFees(method, amount):
        return feeCalculator.calculate(method, amount)  // delegate
```

### Month 3: Extract Receipt Generation

While adding a receipt format change, extract `generateReceipt`:

```
ReceiptGenerator:  // extracted, 12 tests
    generate(payment): ...
    formatLineItems(items): ...
    formatTotal(amount, fees): ...
```

### Month 4: Extract Validation

While fixing a validation bug:

```
PaymentValidator:  // extracted, 20 tests
    validate(request): ...
    validateAmount(amount): ...
    validateCurrency(currency): ...
```

### Month 5: Extract Refund Handling

```
RefundProcessor:  // extracted, 18 tests
    processRefund(payment): ...
    calculateRefundAmount(payment, reason): ...
```

### Month 6: Strangle the Core

The original `PaymentProcessor` is now surrounded:

```
Before (Month 1):
  PaymentProcessor: 2000 lines, 0 tests

After (Month 6):
  PaymentProcessor: 400 lines (just Stripe + PayPal + bank routing)
  ApplePayProcessor: 80 lines, 15 tests
  FeeCalculator: 60 lines, 10 tests
  ReceiptGenerator: 100 lines, 12 tests
  PaymentValidator: 80 lines, 20 tests
  RefundProcessor: 120 lines, 18 tests

Total: same functionality, 75 tests, core is surrounded
```

Now the remaining 400 lines of routing logic (Stripe/PayPal/bank) can be safely strangled — extract each into its own processor class, protected by the surrounding tests.

---

## Example: Acts of Kindness in Practice

### Act 1: Rename for Clarity

```
// Before — what does 'proc' do? What is 'x'?
proc(x, y, z):
    if x > 0:
        r = y * z
        db.update(r)
    return r

// After — one rename, now it's readable
calculateOrderTotal(quantity, unitPrice, taxRate):
    if quantity > 0:
        total = unitPrice * taxRate
        db.update(total)
    return total
```

Time: 2 minutes. Risk: near zero. The code is now understandable.

### Act 2: Extract a Block

```
// Before — 80-line function with a clear section
processApplication(app):
    ... 30 lines of validation ...

    // Calculate eligibility score
    score = 0
    if app.income > 50000: score += 20
    if app.creditScore > 700: score += 30
    if app.yearsEmployed > 2: score += 15
    if app.existingCustomer: score += 10
    if app.hasCollateral: score += 25

    ... 40 more lines of processing ...

// After — extracted one block
processApplication(app):
    ... 30 lines of validation ...
    score = calculateEligibilityScore(app)
    ... 40 more lines of processing ...

calculateEligibilityScore(app):
    score = 0
    if app.income > 50000: score += 20
    if app.creditScore > 700: score += 30
    if app.yearsEmployed > 2: score += 15
    if app.existingCustomer: score += 10
    if app.hasCollateral: score += 25
    return score
```

Time: 5 minutes. Risk: low. Now `calculateEligibilityScore` can be tested independently.

### Act 3: Break a Dependency

```
// Before — hard-coded database dependency, untestable
NotificationService:
    sendWelcomeEmail(userId):
        user = Database.query("SELECT * FROM users WHERE id = ?", userId)
        email = EmailClient.create()
        email.setTo(user.email)
        email.setSubject("Welcome!")
        email.setBody(renderTemplate("welcome", user))
        email.send()

// After — dependency injected, now testable
NotificationService:
    userRepository: UserRepository  // injected
    emailSender: EmailSender        // injected

    sendWelcomeEmail(userId):
        user = userRepository.findById(userId)
        emailSender.send(
            to: user.email,
            subject: "Welcome!",
            body: renderTemplate("welcome", user)
        )
```

Time: 15 minutes. Risk: medium (need to verify callers pass dependencies). But now the service is testable with test doubles.

### Act 4: Remove Dead Code

```
// Before — commented-out code from 2019
processPayment(payment):
    // Old payment flow — replaced in Q3 2019
    // if payment.type == "legacy":
    //     return legacyProcessor.process(payment)
    //     // NOTE: this was causing double charges, see JIRA-4521
    //     // if payment.amount > 10000:
    //     //     return splitPayment(payment)

    return modernProcessor.process(payment)

// After — deleted. Version control remembers.
processPayment(payment):
    return modernProcessor.process(payment)
```

Time: 1 minute. Risk: zero (code was already unreachable). The file is now easier to read.

---

## Example: Non-Deterministic Characterization Tests

### The Problem

A transaction processor produces log output, but thread ordering varies between runs:

```
Run 1 output:
  [Thread-1] Processing order ORD-001
  [Thread-2] Processing order ORD-002
  [Thread-1] Order ORD-001 complete: $50.99
  [Thread-2] Order ORD-002 complete: $23.50

Run 2 output:
  [Thread-2] Processing order ORD-002
  [Thread-1] Processing order ORD-001
  [Thread-2] Order ORD-002 complete: $23.50
  [Thread-1] Order ORD-001 complete: $50.99
```

Different order, same substance.

### The Solution: Normalize Before Comparing

```
normalizeLog(logOutput):
    lines = logOutput.split("\n")
    // Remove thread IDs (non-deterministic)
    lines = lines.map(line -> line.replaceAll("\\[Thread-\\d+\\]", "[Thread]"))
    // Remove timestamps (non-deterministic)
    lines = lines.map(line -> line.replaceAll("\\d{4}-\\d{2}-\\d{2}T.*?\\s", ""))
    // Sort so order doesn't matter
    lines = lines.sort()
    return lines.join("\n")

test "transaction processing matches golden standard":
    output = transactionProcessor.process(testTransactions)
    normalized = normalizeLog(output)
    expected = normalizeLog(readFile("golden/transaction-log.txt"))
    assert normalized == expected
```

The normalization strips away non-deterministic elements (thread IDs, timestamps) and sorts lines so thread ordering doesn't matter. What remains is the substance — which orders were processed and what the results were.
