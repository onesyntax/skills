# Teach Clean Code Concept — Extended Examples

Lesson plan walkthroughs showing the teaching methodology in action.

---

## Example: Teaching SRP to a Beginner

### The Setup

A junior developer asks: "What is the Single Responsibility Principle? I keep hearing about it."

### The Lesson

**Step 1 — Start with a problem they recognize.**

"Have you ever changed something in one part of a class and broken something completely unrelated? Like you fixed the email formatting and suddenly the invoice calculation was wrong?"

Wait for them to connect. Most developers have experienced this.

**Step 2 — Show the messy code.**

```
OrderProcessor:
    processOrder(order):
        // Validate
        if order.items is empty: throw Error("No items")
        if order.total < 0: throw Error("Invalid total")

        // Calculate tax
        tax = 0
        for item in order.items:
            if item.category == "food": tax += item.price * 0.0
            else if item.category == "luxury": tax += item.price * 0.20
            else: tax += item.price * 0.10

        // Save to database
        db.execute("INSERT INTO orders ...")

        // Send confirmation
        emailService.send(order.customer.email, "Your order is confirmed...")

        // Generate report entry
        report.addLine(order.id, order.total, tax, today())
```

"This class has five reasons to change. If the tax rules change, you edit this class. If the database schema changes, you edit this class. If the email template changes, you edit this class. If the report format changes, you edit this class. If the validation rules change, you edit this class."

**Step 3 — Show the transformation.**

```
OrderValidator:
    validate(order):
        if order.items is empty: throw Error("No items")
        if order.total < 0: throw Error("Invalid total")

TaxCalculator:
    calculateTax(items):
        return sumOf(items, item -> taxRateFor(item.category) * item.price)

OrderRepository:
    save(order, tax):
        db.execute("INSERT INTO orders ...")

OrderNotifier:
    sendConfirmation(order):
        emailService.send(order.customer.email, ...)

OrderReporter:
    record(order, tax):
        report.addLine(order.id, order.total, tax, today())

OrderProcessor:
    validator, taxCalculator, repository, notifier, reporter

    processOrder(order):
        validator.validate(order)
        tax = taxCalculator.calculateTax(order.items)
        repository.save(order, tax)
        notifier.sendConfirmation(order)
        reporter.record(order, tax)
```

"Now each class has one reason to change. Tax rules? Edit TaxCalculator. Database schema? Edit OrderRepository. Email template? Edit OrderNotifier. And look — OrderProcessor reads like a recipe. You can understand what it does without reading the details."

**Step 4 — Name the principle.**

"What we just did is called the Single Responsibility Principle. A class should have only one reason to change. Not one thing it does — one reason to change. The distinction matters because 'one thing' is subjective, but 'one reason to change' maps to one stakeholder or one axis of business change."

**Step 5 — Connect it.**

"This is the same idea behind small functions — just applied at the class level. And notice how the refactored OrderProcessor now depends on abstractions (validator, calculator, repository) rather than doing everything itself. That's the Dependency Inversion Principle, which we'll talk about next."

**Step 6 — Give them something to do.**

"Find the largest class in your codebase. List every reason it might need to change. If you find more than two reasons, sketch how you'd split it."

---

## Example: Teaching TDD to a Skeptic

### The Setup

An experienced developer says: "I've been coding for 10 years without TDD. My code works fine. Why should I start now?"

### The Lesson

**Step 1 — Don't argue. Acknowledge.**

"Your code does work, and you've been successful without TDD. The question isn't whether you can write working code — it's what happens to that code over the next two years."

**Step 2 — Show the consequence, not the rule.**

"Let me describe a pattern I've seen in dozens of codebases. Month 1-3: everything is clean, velocity is high. Month 4-6: some functions are getting long, but changes are still quick. Month 7-12: changes start breaking things. You're afraid to touch certain modules. Month 12-18: every feature takes twice as long because you're debugging side effects. By month 24, the team is talking about a rewrite."

"The question is: at month 12, when you know the code is getting tangled, do you refactor? Most developers don't — because they're afraid refactoring will break something. That fear is the absence of TDD."

**Step 3 — Show TDD as courage, not ceremony.**

"TDD isn't about writing tests. It's about having the courage to change code. When you have a comprehensive test suite that runs in seconds, you can refactor fearlessly. See a messy function? Extract it, run tests, green, done. Without tests, you see that same messy function and think 'better not touch it.' The mess grows."

**Step 4 — Demonstrate on a real problem.**

Walk through a concrete TDD cycle on something small. Not a toy example — something the developer would actually build. Show the rhythm: test, code, refactor. Show how the design emerges from the tests. Show how the tests document the behavior.

```
// RED: What should happen?
test "new account has zero balance":
    account = Account()
    assert account.balance == 0

// GREEN: Simplest thing that works
Account:
    balance = 0

// RED: Next behavior
test "deposit increases balance":
    account = Account()
    account.deposit(100)
    assert account.balance == 100

// GREEN
Account:
    balance = 0
    deposit(amount):
        balance += amount

// RED: Edge case
test "cannot deposit negative amount":
    account = Account()
    assertThrows(InvalidAmount, -> account.deposit(-50))

// GREEN
Account:
    deposit(amount):
        if amount <= 0: throw InvalidAmount("Amount must be positive: " + amount)
        balance += amount

// REFACTOR: Name improvement
// "amount" is fine, but "InvalidAmount" could be more specific
// Change to "InvalidDepositAmount" to distinguish from withdrawal errors
```

"Notice what happened: the tests drove us to handle the negative amount case. We might not have thought of it without the test. The test suite is now documentation — anyone can read these tests and know exactly what Account does."

**Step 5 — Address the time objection.**

"Yes, TDD is slower at first. About 15-20% slower for the first month. After that, it's faster — because you spend less time debugging, less time afraid to refactor, and less time dealing with regressions. The slowdown is an investment, not a cost."

**Step 6 — Give them a small commitment.**

"Try it for one week on one module. Not the whole codebase. Pick something new you're building and use TDD for just that. After a week, decide if the test suite gives you confidence you didn't have before."

---

## Example: Teaching DIP Through Architecture

### The Setup

A mid-level developer asks: "I understand the Dependency Inversion Principle in theory, but I don't see why it matters in practice. Why should I create interfaces for everything?"

### The Lesson

**Step 1 — Show the problem at small scale.**

```
OrderService:
    processOrder(order):
        // Directly depends on PostgreSQL
        db = PostgresConnection("localhost:5432/orders")
        db.insert("orders", order.toRow())

        // Directly depends on SendGrid
        mailer = SendGridClient("api-key-123")
        mailer.send(order.customerEmail, "Order confirmed")
```

"What happens when you need to switch from PostgreSQL to MongoDB? Or from SendGrid to Mailgun? You edit OrderService. What happens when you want to test processOrder without a real database or email server? You can't."

**Step 2 — Apply DIP.**

```
// Abstractions (interfaces)
OrderRepository:
    save(order)

NotificationService:
    sendOrderConfirmation(order)

// High-level policy depends on abstractions
OrderService:
    repository: OrderRepository
    notifier: NotificationService

    processOrder(order):
        repository.save(order)
        notifier.sendOrderConfirmation(order)

// Low-level details implement abstractions
PostgresOrderRepository implements OrderRepository:
    save(order): db.insert("orders", order.toRow())

SendGridNotifier implements NotificationService:
    sendOrderConfirmation(order): client.send(order.customerEmail, ...)
```

**Step 3 — Scale it up to architecture.**

"What we just did at the class level IS Clean Architecture at the system level. The Dependency Rule says dependencies point inward — from infrastructure toward business rules. Your business logic (OrderService) should never know about PostgreSQL or SendGrid. Those are details."

```
Architecture rings (inside → outside):
    Entities:     Order, Customer, Product
    Use Cases:    ProcessOrder, CancelOrder
    Adapters:     OrderController, PostgresRepository
    Frameworks:   Express, PostgreSQL driver, SendGrid SDK
```

"Every arrow points inward. The inner rings never mention the outer rings. This means you can swap your entire database or web framework without touching a single line of business logic."

**Step 4 — Connect to the "why."**

"DIP isn't about creating interfaces for everything. It's about protecting your business logic from change. Frameworks change. Databases change. Email providers change. Your business rules — how orders are processed, how prices are calculated — change much less often. DIP puts a firewall between the things that change often and the things that change rarely."

**Step 5 — Address 'isn't this overkill?'**

"For a 200-line script, yes, DIP is overkill. But the moment your codebase grows past a few thousand lines, the cost of NOT having DIP starts compounding. Every direct dependency is a coupling that makes change expensive. DIP is cheap to add upfront and expensive to add later."

**Step 6 — Exercise.**

"Find a class in your code that directly creates database connections or HTTP clients. Create an interface for that dependency and inject it. Write one test using a mock implementation. Notice how much easier it is to test when the dependency is injected."
