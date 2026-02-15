# Architecture — Extended Examples

Detailed walkthroughs showing Clean Architecture applied to real systems.

---

## Example: E-Commerce System — Full Architecture

### The Entities (Innermost Ring)

```
Order:
    id, customer, items, status, createdAt
    
    calculateTotal():
        return sumOf(items, item -> item.price * item.quantity)
    
    canBeCancelled():
        return status == "pending" or status == "confirmed"

OrderItem:
    product, quantity, price

Customer:
    id, name, email, shippingAddress
```

Entities contain enterprise business rules. They know nothing about databases, HTTP, or UI. They can be used in any application context.

### The Use Cases (Second Ring)

```
PlaceOrder:
    orderRepository: OrderRepository       // interface
    paymentGateway: PaymentGateway         // interface
    inventoryService: InventoryService     // interface
    notifier: OrderNotifier                // interface

    execute(request):
        order = createOrderFromRequest(request)
        ensureItemsAvailable(order.items)
        chargeCustomer(order)
        orderRepository.save(order)
        notifier.sendOrderConfirmation(order)
        return OrderConfirmation(order.id, order.calculateTotal())

    ensureItemsAvailable(items):
        for item in items:
            if not inventoryService.isAvailable(item.product, item.quantity):
                throw OutOfStockException(item.product)

    chargeCustomer(order):
        result = paymentGateway.charge(order.customer, order.calculateTotal())
        if not result.success:
            throw PaymentFailedException(result.reason)

CancelOrder:
    orderRepository: OrderRepository
    paymentGateway: PaymentGateway
    notifier: OrderNotifier

    execute(orderId):
        order = orderRepository.findById(orderId)
        if not order.canBeCancelled():
            throw OrderNotCancellableException(orderId, order.status)
        paymentGateway.refund(order)
        order.status = "cancelled"
        orderRepository.save(order)
        notifier.sendCancellationConfirmation(order)
```

Use cases orchestrate entities and define application-specific business rules. They depend on interfaces (not implementations) for all external interactions.

### The Interface Adapters (Third Ring)

```
// Controller — translates HTTP to use case calls
OrderController:
    placeOrder: PlaceOrder
    cancelOrder: CancelOrder

    handlePlaceOrder(httpRequest):
        try:
            request = PlaceOrderRequest.fromJson(httpRequest.body)
            confirmation = placeOrder.execute(request)
            return HttpResponse(201, confirmation.toJson())
        catch OutOfStockException as e:
            return HttpResponse(409, {"error": "Out of stock: " + e.product})
        catch PaymentFailedException as e:
            return HttpResponse(402, {"error": "Payment failed: " + e.reason})

    handleCancelOrder(httpRequest):
        try:
            orderId = httpRequest.params["id"]
            cancelOrder.execute(orderId)
            return HttpResponse(200, {"status": "cancelled"})
        catch OrderNotCancellableException as e:
            return HttpResponse(409, {"error": "Cannot cancel: " + e.status})

// Presenter — translates use case output to view format
OrderPresenter:
    presentConfirmation(confirmation):
        return {
            orderId: confirmation.id,
            total: formatCurrency(confirmation.total),
            message: "Order placed successfully"
        }
```

Controllers are thin — they translate between HTTP and use case calls. No business logic here.

### The Frameworks (Outermost Ring)

```
// Database implementation
PostgresOrderRepository implements OrderRepository:
    save(order):
        db.execute("INSERT INTO orders ...")
    
    findById(id):
        row = db.query("SELECT * FROM orders WHERE id = ?", id)
        return mapRowToOrder(row)

// Payment implementation
StripePaymentGateway implements PaymentGateway:
    charge(customer, amount):
        result = stripe.charges.create(amount, customer.paymentToken)
        return PaymentResult(result.success, result.message)

// Email implementation
SendGridNotifier implements OrderNotifier:
    sendOrderConfirmation(order):
        sendgrid.send(order.customer.email, "Order Confirmed", ...)
```

Infrastructure implements interfaces defined by the use cases. Swapping Postgres for MongoDB, or Stripe for PayPal, requires changing only this ring.

### The Dependency Direction

```
Frameworks → Adapters → Use Cases → Entities
   (outer)                           (inner)

Every arrow points INWARD. Inner rings never mention outer rings.
- Entities don't know about use cases
- Use cases don't know about controllers or databases
- Use case interfaces (OrderRepository, PaymentGateway) are defined
  in the use case ring, implemented in the frameworks ring
```

---

## Example: Testing Each Ring Independently

### Testing Entities (No Dependencies)

```
test "order total is sum of item prices":
    order = Order(items: [
        OrderItem(product: "A", quantity: 2, price: 10),
        OrderItem(product: "B", quantity: 1, price: 25)
    ])
    assert order.calculateTotal() == 45

test "pending order can be cancelled":
    order = Order(status: "pending")
    assert order.canBeCancelled() == true

test "shipped order cannot be cancelled":
    order = Order(status: "shipped")
    assert order.canBeCancelled() == false
```

No mocks, no setup, no infrastructure. Pure business logic.

### Testing Use Cases (Mocked Infrastructure)

```
test "place order charges customer and saves":
    mockRepo = MockOrderRepository()
    mockPayment = MockPaymentGateway(alwaysSucceeds: true)
    mockInventory = MockInventoryService(alwaysAvailable: true)
    mockNotifier = MockNotifier()

    useCase = PlaceOrder(mockRepo, mockPayment, mockInventory, mockNotifier)
    result = useCase.execute(validOrderRequest)

    assert mockPayment.chargedAmount == 45
    assert mockRepo.savedOrder != null
    assert mockNotifier.sentConfirmation == true

test "place order fails when item out of stock":
    mockInventory = MockInventoryService(available: {"A": true, "B": false})
    useCase = PlaceOrder(mockRepo, mockPayment, mockInventory, mockNotifier)

    assertThrows(OutOfStockException,
        -> useCase.execute(requestWithItems("A", "B")))
    assert mockPayment.chargedAmount == null  // never charged
```

Use case tests verify business rules without any real infrastructure.

### Testing Adapters (Verify Translation)

```
test "controller returns 201 on successful order":
    mockPlaceOrder = MockPlaceOrder(returns: OrderConfirmation("123", 45))
    controller = OrderController(placeOrder: mockPlaceOrder)

    response = controller.handlePlaceOrder(validHttpRequest)

    assert response.status == 201
    assert response.body.orderId == "123"

test "controller returns 409 when out of stock":
    mockPlaceOrder = MockPlaceOrder(throws: OutOfStockException("Widget"))
    controller = OrderController(placeOrder: mockPlaceOrder)

    response = controller.handlePlaceOrder(validHttpRequest)

    assert response.status == 409
```

Adapter tests verify HTTP translation only — no business logic, no infrastructure.
