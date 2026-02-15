# Component Principles — Extended Examples

Detailed walkthroughs of component analysis, metric calculations, and cycle-breaking strategies.

---

## Example: E-Commerce System Component Analysis

### Initial Component Structure

An e-commerce system with poorly designed components:

```
Component: "Commerce"
  - Order
  - OrderValidator
  - OrderRepository
  - Product
  - ProductCatalog
  - ProductRepository
  - Customer
  - CustomerProfile
  - ShoppingCart
  - PaymentProcessor
  - InvoiceGenerator
  - EmailNotifier
  - ShippingCalculator
  - TaxCalculator
```

Everything in one component. Let's apply the principles.

### Step 1: Apply CCP — What Changes Together?

Ask: "When the business changes X, what classes change?"

```
Change: "New tax rule"        → TaxCalculator (only)
Change: "New shipping method" → ShippingCalculator (only)
Change: "New payment gateway" → PaymentProcessor (only)
Change: "New order status"    → Order, OrderValidator, OrderRepository
Change: "New product field"   → Product, ProductCatalog, ProductRepository
Change: "Email template"      → EmailNotifier, InvoiceGenerator
```

This reveals natural groupings by reason for change.

### Step 2: Apply CRP — What's Reused Together?

Ask: "If I depend on Order, do I also need ShippingCalculator?"

```
Uses Order: checkout flow, order history, admin dashboard
Uses ShippingCalculator: checkout flow only
Uses EmailNotifier: checkout flow, marketing, support tools

Conclusion: Order and ShippingCalculator should NOT be in the same component.
Marketing tools shouldn't pull in Order just to send emails.
```

### Step 3: Redesigned Components

```
Component: "Orders" (Order, OrderValidator, OrderRepository)
  Changes when: order rules change

Component: "Products" (Product, ProductCatalog, ProductRepository)
  Changes when: product model changes

Component: "Customers" (Customer, CustomerProfile, ShoppingCart)
  Changes when: customer features change

Component: "Payments" (PaymentProcessor)
  Changes when: payment gateway changes

Component: "Pricing" (TaxCalculator, ShippingCalculator)
  Changes when: pricing/tax rules change

Component: "Notifications" (EmailNotifier, InvoiceGenerator)
  Changes when: notification templates change
```

### Step 4: Check Dependencies

```
Dependency graph:
  Customers → Orders → Products
  Customers → Payments
  Orders → Pricing
  Orders → Notifications
  Notifications → Products (for product names in emails)
```

Is this a DAG? Let's check for cycles:
```
Customers → Orders → Products ✓ (no cycle)
Customers → Payments ✓ (no cycle)
Orders → Pricing ✓ (no cycle)
Orders → Notifications → Products ✓ (no cycle)
```

No cycles. Good.

### Step 5: Calculate Metrics

```
Component     Fan-in  Fan-out  I(Instability)  Abstract?  A  D
Products      3       0        0.00            No         0  1.00 ⚠️
Orders        2       3        0.60            No         0  0.40
Customers     0       2        1.00            No         0  0.00 ✓
Payments      1       0        0.00            No         0  1.00 ⚠️
Pricing       1       0        0.00            No         0  1.00 ⚠️
Notifications 1       1        0.50            No         0  0.50
```

**Problem:** Products, Payments, and Pricing are in the Zone of Pain (stable but concrete, D=1.00). If they need to change, many components break.

### Step 6: Fix with SAP

Add abstractions to stable components:

```
Component: "Products"
  + ProductGateway (interface)      ← abstract
  + ProductCatalogGateway (interface) ← abstract
  ProductImpl, CatalogImpl           ← concrete implementations

  Now: A = 2/4 = 0.50, I = 0.00, D = |0.50 + 0 - 1| = 0.50 ✓ Better!

Component: "Payments"
  + PaymentGateway (interface)       ← abstract
  StripePaymentProcessor             ← concrete

  Now: A = 1/2 = 0.50, I = 0.00, D = 0.50 ✓ Better!
```

Other components depend on the *interfaces*, not the concrete implementations. Now stable components CAN be extended without modification.

---

## Example: Breaking a Dependency Cycle

### The Problem

Three components form a cycle:

```
Auth → UserProfile → Permissions → Auth

Auth needs UserProfile to get user details for login.
UserProfile needs Permissions to check what profile fields are visible.
Permissions needs Auth to verify who's asking for permissions.
```

This means you can't build or test any of these independently. Changing any one might break all three.

### Technique 1: Dependency Inversion

Identify the weakest dependency (the one easiest to invert). Here: Permissions → Auth.

```
Before:
  Permissions module directly calls Auth.getCurrentUser()

After:
  Permissions defines an interface: CurrentUserProvider
  Auth implements CurrentUserProvider

  Auth → UserProfile → Permissions
  Auth implements Permissions.CurrentUserProvider

  // Permissions no longer imports Auth — it imports its own interface
```

The cycle is broken. Permissions doesn't know Auth exists. It just knows that someone will provide a CurrentUserProvider.

### Technique 2: Extract New Component

Extract the shared concept into a new component:

```
Before:
  Auth → UserProfile → Permissions → Auth

After:
  New component "Identity" contains: UserId, UserRole, UserContext

  Auth → Identity
  UserProfile → Identity
  Permissions → Identity
  Auth → UserProfile (still needs user details)
  UserProfile → Permissions (still checks visibility)

  // No more cycle — all three depend on Identity, none depend on each other circularly
```

### How to Choose

- **Dependency Inversion** when one direction of the cycle is clearly "wrong" (a low-level module depending on a high-level module). Invert that one dependency.
- **Extract New Component** when the cycle exists because multiple components share a concept that deserves its own home. The cycle reveals a missing abstraction.

---

## Example: Tension Triangle in Practice

### Early-Stage Startup (Favor CCP)

```
// Two developers, features changing daily
// ONE big component: "App"
Component: "App"
  - User, UserAuth, UserProfile
  - Product, ProductSearch, ProductRecommendation
  - Order, Cart, Checkout, Payment
  - EmailService, NotificationService

Why this is fine:
  - Team is small, communication is instant
  - Features change constantly — keeping everything together means fewer cross-component changes
  - No external consumers — nobody reuses these components
  - CCP is maximized: everything that changes together IS together
```

### Growing System (Shift toward CRP)

```
// Team growing to 15, microservices emerging
// Split by domain boundaries
Component: "UserService"    (User, UserAuth, UserProfile)
Component: "CatalogService" (Product, ProductSearch)
Component: "OrderService"   (Order, Cart, Checkout)
Component: "PaymentService" (Payment)
Component: "CommsService"   (EmailService, NotificationService)

Why this shift:
  - Teams own specific domains — need independent deployment
  - CRP matters now: OrderService shouldn't redeploy when email templates change
  - Dependencies are managed: OrderService → PaymentService → (nothing)
```

### Mature Platform (Favor REP)

```
// Multiple products reusing core capabilities
// Package for external consumption
Component: "user-auth-sdk" v2.3.1     (published, versioned, documented)
Component: "payment-gateway" v1.8.0   (published, versioned, documented)
Component: "notification-sdk" v3.1.0  (published, versioned, documented)

Why this shift:
  - External teams depend on these — need stable, versioned releases
  - REP is critical: each release must be coherent
  - Backward compatibility matters — can't break consumers
```

---

## Example: Main Sequence Analysis of a Real System

### Calculating Metrics for a Blog Platform

```
Components and their classes:

1. "Core" (Post, Comment, User, Tag — all concrete)
   Fan-in: 4 (UI, API, Search, Admin all depend on it)
   Fan-out: 0
   I = 0/(4+0) = 0.00
   A = 0/4 = 0.00
   D = |0 + 0 - 1| = 1.00 ← Zone of Pain!

2. "UI" (PostView, CommentView, UserView, Layout — all concrete)
   Fan-in: 0
   Fan-out: 2 (depends on Core, Search)
   I = 2/(0+2) = 1.00
   A = 0/4 = 0.00
   D = |0 + 1 - 1| = 0.00 ← On the Main Sequence ✓

3. "Search" (SearchIndex, SearchQuery, SearchResult — all concrete)
   Fan-in: 2 (UI, API depend on it)
   Fan-out: 1 (depends on Core)
   I = 1/(2+1) = 0.33
   A = 0/3 = 0.00
   D = |0 + 0.33 - 1| = 0.67 ← Drifting toward Zone of Pain

4. "API" (PostController, CommentController, UserController — all concrete)
   Fan-in: 0
   Fan-out: 2 (depends on Core, Search)
   I = 2/(0+2) = 1.00
   A = 0/3 = 0.00
   D = |0 + 1 - 1| = 0.00 ← On the Main Sequence ✓

5. "Admin" (AdminDashboard, UserManager, ContentModerator — all concrete)
   Fan-in: 0
   Fan-out: 1 (depends on Core)
   I = 1/(0+1) = 1.00
   A = 0/3 = 0.00
   D = |0 + 1 - 1| = 0.00 ← On the Main Sequence ✓
```

### Diagnosis

"Core" is in the Zone of Pain (D=1.00). It's maximally stable (everyone depends on it) but has zero abstractions. If Post needs a new field, every dependent component is affected.

"Search" is drifting (D=0.67). Two components depend on it, but it's all concrete.

### Fix

```
"Core" refactored:
  + PostGateway (interface)
  + CommentGateway (interface)
  + UserGateway (interface)
  Post, Comment, User, Tag (concrete)

  A = 3/7 = 0.43
  D = |0.43 + 0 - 1| = 0.57 ← Better (was 1.00)

"Search" refactored:
  + SearchGateway (interface)
  SearchIndex, SearchQuery, SearchResult (concrete)

  A = 1/4 = 0.25
  D = |0.25 + 0.33 - 1| = 0.42 ← Better (was 0.67)
```

Other components now depend on the interfaces. Concrete implementations can be swapped without affecting dependents.
