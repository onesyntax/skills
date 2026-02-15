# SOLID Principles — Extended Examples

Detailed walkthroughs showing each SOLID principle applied to real code.

---

## Example: SRP — Splitting a God Class

### Before

```
Employee:
    name, email, department, salary, taxRate

    calculatePay():
        gross = salary / 12
        tax = gross * taxRate
        return gross - tax

    saveToDatabase():
        db.execute("INSERT INTO employees ...")

    generateReport():
        return formatAsHtml(name, department, calculatePay())

    sendPayslipEmail():
        email.send(this.email, "Payslip", generateReport())
```

Four reasons to change: pay calculation rules, database schema, report format, email provider.

### After

```
Employee:
    name, email, department, salary, taxRate

PayCalculator:
    calculateMonthlyPay(employee):
        gross = employee.salary / 12
        tax = gross * employee.taxRate
        return gross - tax

EmployeeRepository:
    save(employee):
        db.execute("INSERT INTO employees ...")

PayslipReporter:
    generatePayslip(employee, pay):
        return formatAsHtml(employee.name, employee.department, pay)

PayslipNotifier:
    sendPayslip(employee, payslip):
        email.send(employee.email, "Payslip", payslip)
```

Each class has one reason to change. The orchestration moves to a higher-level use case:

```
ProcessMonthlyPayroll:
    calculator, repository, reporter, notifier

    execute(employee):
        pay = calculator.calculateMonthlyPay(employee)
        payslip = reporter.generatePayslip(employee, pay)
        notifier.sendPayslip(employee, payslip)
```

---

## Example: OCP — Adding Payment Types Without Modification

### Before — Violates OCP

```
PaymentProcessor:
    process(payment):
        if payment.type == "credit":
            chargeCredit(payment)
        else if payment.type == "debit":
            chargeDebit(payment)
        else if payment.type == "paypal":
            chargePaypal(payment)
        // Adding Apple Pay means modifying this function
```

### After — Open for Extension, Closed for Modification

```
PaymentStrategy:  // interface
    charge(payment)

CreditCardStrategy implements PaymentStrategy:
    charge(payment): // credit card logic

DebitCardStrategy implements PaymentStrategy:
    charge(payment): // debit card logic

PaypalStrategy implements PaymentStrategy:
    charge(payment): // paypal logic

// Adding Apple Pay = adding a new class, not modifying existing ones
ApplePayStrategy implements PaymentStrategy:
    charge(payment): // apple pay logic

PaymentProcessor:
    strategies: map<string, PaymentStrategy>

    process(payment):
        strategy = strategies[payment.type]
        strategy.charge(payment)
```

---

## Example: LSP — The Rectangle/Square Problem

### The Violation

```
Rectangle:
    width, height
    setWidth(w): width = w
    setHeight(h): height = h
    area(): return width * height

Square extends Rectangle:
    setWidth(w): width = w; height = w   // maintains square invariant
    setHeight(h): width = h; height = h  // maintains square invariant
```

This breaks any code that assumes Rectangle behavior:

```
testAreaCalculation(rectangle):
    rectangle.setWidth(5)
    rectangle.setHeight(3)
    assert rectangle.area() == 15  // FAILS for Square! Gets 9 instead
```

### The Fix — Separate Types

```
Shape:  // interface
    area()

Rectangle implements Shape:
    width, height
    area(): return width * height

Square implements Shape:
    side
    area(): return side * side

// Or use immutable value objects:
ImmutableRectangle:
    width, height  // set only in constructor
    area(): return width * height
    withWidth(w): return ImmutableRectangle(w, height)
    withHeight(h): return ImmutableRectangle(width, h)
```

---

## Example: ISP — Fat Interface Decomposition

### Before — One Interface Forces Unnecessary Implementation

```
Printer:  // interface
    print(document)
    scan(document)
    fax(document)
    staple(document)

SimpleLaserPrinter implements Printer:
    print(document): // works
    scan(document): throw NotSupportedException  // forced to implement
    fax(document): throw NotSupportedException   // forced to implement
    staple(document): throw NotSupportedException // forced to implement
```

### After — Segregated Interfaces

```
Printable:
    print(document)

Scannable:
    scan(document)

Faxable:
    fax(document)

Stapleable:
    staple(document)

SimpleLaserPrinter implements Printable:
    print(document): // only implements what it can do

MultiFunctionDevice implements Printable, Scannable, Faxable:
    print(document): ...
    scan(document): ...
    fax(document): ...
```

Each client depends only on the interface it actually uses.

---

## Example: DIP — Inverting a Database Dependency

### Before — Business Logic Depends on Infrastructure

```
OrderService:
    processOrder(order):
        db = MySqlConnection("localhost:3306/shop")
        db.insert("orders", order.toRow())

        stripe = StripeClient("sk_live_key")
        stripe.charge(order.total, order.paymentToken)
```

OrderService knows about MySQL and Stripe. Testing requires real infrastructure.

### After — Both Depend on Abstractions

```
OrderRepository:  // interface — owned by the business layer
    save(order)

PaymentGateway:   // interface — owned by the business layer
    charge(amount, token)

OrderService:
    repository: OrderRepository
    payment: PaymentGateway

    processOrder(order):
        repository.save(order)
        payment.charge(order.total, order.paymentToken)

// Infrastructure implements the interfaces
MySqlOrderRepository implements OrderRepository:
    save(order): db.insert("orders", order.toRow())

StripePaymentGateway implements PaymentGateway:
    charge(amount, token): stripe.charge(amount, token)

// Tests use simple implementations
MockOrderRepository implements OrderRepository:
    savedOrders = []
    save(order): savedOrders.add(order)
```

The key insight: the interfaces are owned by the business layer, not the infrastructure layer. Dependencies point inward.
