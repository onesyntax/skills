# TDD — Extended Examples

Detailed walkthroughs showing TDD cycles in practice.

---

## Example: TDD a Stack Data Structure

### Cycle 1 — Empty Stack

```
// RED
test "new stack is empty":
    stack = Stack()
    assert stack.isEmpty() == true

// GREEN
Stack:
    isEmpty(): return true
```

### Cycle 2 — Push Makes It Non-Empty

```
// RED
test "stack with one element is not empty":
    stack = Stack()
    stack.push(42)
    assert stack.isEmpty() == false

// GREEN
Stack:
    elements = []
    isEmpty(): return elements.length == 0
    push(item): elements.add(item)
```

### Cycle 3 — Pop Returns Last Pushed

```
// RED
test "pop returns the last pushed element":
    stack = Stack()
    stack.push(42)
    assert stack.pop() == 42

// GREEN
Stack:
    elements = []
    isEmpty(): return elements.length == 0
    push(item): elements.add(item)
    pop(): return elements.removeLast()
```

### Cycle 4 — LIFO Order

```
// RED
test "pop returns elements in LIFO order":
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1

// GREEN — already passes! The implementation handles this naturally.
```

### Cycle 5 — Error on Empty Pop

```
// RED
test "pop on empty stack throws":
    stack = Stack()
    assertThrows(EmptyStackException, -> stack.pop())

// GREEN
Stack:
    pop():
        if elements.length == 0: throw EmptyStackException()
        return elements.removeLast()
```

### Cycle 6 — Peek

```
// RED
test "peek returns top without removing":
    stack = Stack()
    stack.push(42)
    assert stack.peek() == 42
    assert stack.isEmpty() == false  // still there

// GREEN
Stack:
    peek():
        if elements.length == 0: throw EmptyStackException()
        return elements.last()
```

### What TDD Gave Us

- Complete, correct implementation built incrementally
- Every behavior has a test
- Edge case (empty pop) discovered through the test-first process
- Design emerged naturally — no upfront design needed for a simple data structure
- Total confidence in the implementation

---

## Example: TDD a Price Calculator with Discounts

### Cycle 1 — Single Item, No Discount

```
// RED
test "single item price is quantity times unit price":
    calculator = PriceCalculator()
    total = calculator.calculate([Item(price: 10, quantity: 2)])
    assert total == 20

// GREEN
PriceCalculator:
    calculate(items):
        return items[0].price * items[0].quantity
```

### Cycle 2 — Multiple Items

```
// RED
test "total is sum of all item prices":
    calculator = PriceCalculator()
    total = calculator.calculate([
        Item(price: 10, quantity: 2),
        Item(price: 5, quantity: 3)
    ])
    assert total == 35

// GREEN
PriceCalculator:
    calculate(items):
        return sumOf(items, item -> item.price * item.quantity)
```

### Cycle 3 — Percentage Discount

```
// RED
test "percentage discount reduces total":
    calculator = PriceCalculator()
    total = calculator.calculate(
        [Item(price: 100, quantity: 1)],
        discount: PercentageDiscount(10)
    )
    assert total == 90

// GREEN
PriceCalculator:
    calculate(items, discount = null):
        subtotal = sumOf(items, item -> item.price * item.quantity)
        if discount != null:
            return subtotal - (subtotal * discount.percentage / 100)
        return subtotal
```

### Cycle 4 — REFACTOR

The conditional is a smell. We'll need more discount types.

```
// REFACTOR — introduce Discount interface
Discount:
    apply(subtotal)

PercentageDiscount implements Discount:
    percentage
    apply(subtotal): return subtotal * (1 - percentage / 100)

NoDiscount implements Discount:
    apply(subtotal): return subtotal

PriceCalculator:
    calculate(items, discount = NoDiscount()):
        subtotal = sumOf(items, item -> item.price * item.quantity)
        return discount.apply(subtotal)
```

All existing tests still pass. Now adding a new discount type is trivial:

### Cycle 5 — Fixed Amount Discount

```
// RED
test "fixed discount subtracts amount from total":
    calculator = PriceCalculator()
    total = calculator.calculate(
        [Item(price: 100, quantity: 1)],
        discount: FixedDiscount(15)
    )
    assert total == 85

// GREEN — just add a new class
FixedDiscount implements Discount:
    amount
    apply(subtotal): return max(0, subtotal - amount)
```

### Cycle 6 — Discount Floor

```
// RED
test "discount cannot make total negative":
    calculator = PriceCalculator()
    total = calculator.calculate(
        [Item(price: 10, quantity: 1)],
        discount: FixedDiscount(50)
    )
    assert total == 0  // not -40

// GREEN — already handled by max(0, ...) in FixedDiscount!
```

### What TDD Gave Us

- OCP emerged naturally (Discount interface) during the REFACTOR step
- The design was driven by the tests, not by upfront planning
- Edge case (negative total) was caught by writing the test first
- Adding new discount types requires zero modification of existing code
