---
name: architecture
description: >-
  Map Clean Architecture to your actual stack. Detect your framework, deployment model, and existing
  patterns. Convert architecture principles into decision rules you can verify. Draw boundaries the
  way your codebase needs — not from a textbook. Activate when designing system structure, defining
  use cases, placing modules, reviewing dependency direction, or choosing monolith vs microservices.
model: opus
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
delegates-to: components, solid
argument-hint: [feature/module to design or directory to analyze]
---

# Architecture Skill

Architecture is the art of drawing lines — boundaries that separate software and restrict dependencies. The goal: minimize human resources to build and maintain the system. Good architecture keeps options open, defers decisions, and makes the system easy to change.

Dependencies are everything. When dependencies point the right way, the rest of the system arranges itself. When they don't, no amount of clean code at the function level will save you.

---

## Step 0: Detect Your Context

Before applying any architecture rule, understand your actual stack. Architecture principles map differently depending on framework, structure, and deployment.

### Detect: Monolith vs Microservices

```bash
# Find service boundaries — separate Dockerfiles, separate git repos, separate deployments
find . -name "Dockerfile" | wc -l
find . -name "docker-compose.yml" -o -name "kubernetes.yml"
ls -la | grep -E "^d" | awk '{print $NF}' | head -20  # Top-level dirs (service breakdown hint)
```

**Decision Point:** Monolith (one deployment, all code) vs Microservices (multiple deployments, network boundaries)?

### Detect: Framework

```bash
# PHP: composer.json + app/ directory structure
test -f composer.json && grep -i "php" composer.json

# TypeScript: package.json + src/ directory structure
test -f package.json && grep -i "typescript" package.json

# Full stack detection
if test -f composer.json && test -f package.json; then
    echo "PHP + TypeScript stack detected"
fi
```

**Why it matters:** Pure domain entities should not depend on framework libraries. Business logic must be isolated from both the backend and frontend presentation layers.

### Detect: Directory Convention

```bash
# Package by layer — layers are top-level directories
ls -1 | grep -E "^(controllers|services|models|repositories|dto|config)$"

# Package by feature — features are top-level directories
ls -1 | grep -E "^(users|orders|billing|auth)$" | wc -l

# Both? (dangerous — typically indicates inconsistent evolution)
ls -1 | grep -E "^(controllers|services|models|repositories|dto|config|users|orders)$"
```

**Decision Point:** package-by-layer = thinking in architecture terms. package-by-feature = thinking in business terms. Feature usually wins for large systems.

### Detect: Existing Boundary Patterns

```bash
# Look for explicit interfaces/ports (markers of architectural intent)
find . -name "*Port.java" -o -name "*Boundary.ts" -o -name "*Gateway.py"

# Look for dependency inversion patterns
grep -r "interface.*Repository" --include="*.java" --include="*.ts" | wc -l

# Look for presentation models / DTOs (boundaries)
find . -name "*DTO*" -o -name "*Request*" -o -name "*Response*"
```

**Signal strength:** Strong = system already thinks about boundaries. Weak = will need to introduce them.

### Detect: Deployment Model

```bash
# Monolith deployed as single unit
test -f Dockerfile && grep -c "^FROM" && test $(grep -c "^FROM") -eq 1

# Microservices or modular monolith (separate containers)
find . -path "**/docker-compose.yml" -o -path "**/kubernetes/**/*.yml"

# Serverless (Lambda functions, Cloud Functions)
find . -name "serverless.yml" -o -name "sam.yml"
```

---

## Step 1: Generate Context-Specific Rules

Map Clean Architecture principles to PHP backend + TypeScript frontend:

### PHP (Backend)

- **Plain domain entities** — NOT coupled to any framework. True entities are simple PHP classes in the Domain layer.
- **Business logic in Service classes or Use Cases** — NOT in ORM models or Controllers.
- **Controllers are thin adapters** — parse request, call service/use case, return response. No business logic.
- **Validation separated** — keep validation concerns separate from business logic.
- **Repository pattern** — define interfaces in use case layer, implement in adapter layer.
- **Dependency injection** — inject dependencies via constructor, enable swapping implementations.

**Structure:**
```
app/
  Domain/              # Pure entities, value objects, business rules (no framework code)
  UseCases/           # Application logic, interactors (orchestrate domain + gateways)
  Repositories/       # Gateway interfaces (NOT implementations)
  Http/
    Controllers/      # Thin adapters, parse request, call use case, return response
    Resources/        # DTO/response formatters
  Services/           # Domain services, shared business logic
  Adapters/
    Persistence/      # Database repositories (implement gateway interfaces)
  Providers/          # DI container wiring
```

### TypeScript (Frontend)

- **Classes and services for business logic** — NOT in UI components. Extract logic to service classes.
- **Service classes** — encapsulate API calls, domain logic, and state management.
- **Components are presentation-only** — handle rendering, user interaction, delegate to services.
- **State management isolated** — use service classes or modules for business state.
- **TypeScript interfaces** for domain models — `Order`, `User`, `CartItem` live in a domain layer, not scattered in components.

**Structure:**
```
src/
  domain/           # TypeScript types/interfaces, business rules (Order, User, validation)
  services/         # Service classes (API, domain logic, business operations)
  components/       # UI components (presentation-only)
  pages/            # Page components (thin adapters, compose components + services)
  models/           # Domain models and entities
  utils/            # Pure utility functions
```

### Microservices

- **Each service IS a complete architecture** — not a layer. Each has its own domain model, use cases, persistence.
- **Internal architecture still matters** — dependency rule applies within each service.
- **Service boundaries == business boundaries** — organize by business capability, not technical layer.
- **Database per service** — no shared databases across services. No joins between services.

---

## Step 2: Apply Decision Rules

Convert architecture principles to testable, verifiable decision rules.

### The Dependency Rule (WHEN/WHEN NOT/Verification)

**WHEN to enforce:** Every file/class you write.

**WHEN NOT to enforce:** Application bootstrap / wiring only (DI container bindings, known violations acceptable).

**Verification:**

```bash
# PHP: No framework imports in domain layer
find app/Domain app/UseCases -name "*.php" | while read f; do
  grep -l "use PDO\|use Doctrine\|use Database" "$f" && echo "VIOLATION: Framework in domain: $f"
done

# PHP: No DB queries in controllers
grep -rn "DB::\|->where(\|->find(\|->get()" app/Http/Controllers/ | grep -v "// " && echo "Query in controller"

# TypeScript: No API calls in components (should be in services)
find src/components -name "*.tsx" -o -name "*.ts" | while read f; do
  grep -l "fetch\|axios\|fetch\|api\." "$f" && echo "VIOLATION: Direct API call in component: $f"
done

# TypeScript: No framework code in domain/
find src/domain -name "*.ts" | while read f; do
  grep -l "import.*express\|import.*axios\|import.*prisma" "$f" && echo "VIOLATION: Framework in domain: $f"
done
```

### Boundary Placement (WHEN to create vs keep together)

**WHEN to create a new boundary:** When two subsystems change for different reasons (different actors, different deployment cycles, different teams).

**WHEN to keep together:** When subsystems always change together, share data intimately, have high-frequency calls.

**Test it:**
```bash
# Git blame: do these two files change together?
git log --name-only --oneline -- app/Domain/Order.php app/Http/Controllers/OrderController.php | grep "^app" | sort | uniq -c | sort -rn

# If Order.php appears in 30 commits and OrderController appears in 28 of those 30,
# they're changing together — maybe they're not separate enough yet.
```

### Database Independence (WHEN to abstract vs direct access)

**WHEN to use a gateway interface:** Always, for persistent data.

**WHEN direct access is fine:** Reading configuration files, caches, temporary data not part of the domain model.

**Pattern:**
```
// In use_cases layer
interface OrderRepository:
    findById(orderId)
    save(order)

// In adapters layer — implemented multiple ways
class PostgresOrderRepository implements OrderRepository
class MockOrderRepository implements OrderRepository  (for testing)
class InMemoryOrderRepository implements OrderRepository
```

### Framework Independence (WHEN to isolate vs embrace)

**WHEN to isolate:** Business entities, domain logic, use case orchestration. The system should work without the framework (testable in pure code).

**WHEN to embrace:** Controllers, presenters, models that inherit from framework base classes. These are adapter code; let the framework be itself.

**Verification:**

```bash
# Can you test all business logic without starting the framework?
# Run: mvn test -Dtest=OrderServiceTest (no @SpringBootTest, no @WebMvcTest)

# If you need @SpringBootTest, the logic belongs in the use case, not the controller.
```

### Screaming Architecture (structure reveals intent)

**Test:** Ask someone unfamiliar with the codebase to guess the business purpose from directory names alone.

**Good:** app/Domain, app/UseCases, src/domain, src/services (reveals intent)
**Bad:** app/models, app/views, app/controllers, src/components, src/utils (screams framework, not business)

---

## Step 3: Review Checklist

Use this table for code review. For each item, mark yes/no/na. Critical items are show-stoppers.

| Item | WHEN to check | How | Severity |
|------|--------------|-----|----------|
| **Dependency direction** | Every class | No inner layer imports outer framework code | CRITICAL |
| **Boundary integrity** | New class/module | Does it cross a boundary? If so, use DTO, not entity | CRITICAL |
| **Entity purity** | Domain classes | Free of framework annotations, database queries | CRITICAL |
| **Use case isolation** | Interactor classes | No knowledge of UI, database, external API details | HIGH |
| **Framework leakage** | Controllers, presenters | Spring/@Service/@Autowired lives here only, not in domain | HIGH |
| **Screaming test** | Directory structure | Can you name the business purpose from top-level dirs? | MEDIUM |
| **Humble objects at I/O** | Gateways, controllers, presenters | Minimal logic, delegates to domain, testable without framework | MEDIUM |
| **No circular dependencies** | Module wiring | A depends on B depends on A? Use interface inversion to break | HIGH |

---

## Step 4: Refactoring Patterns

### Invert Dependency Direction (DIP & Extract Use Case)

**Problem:** Use case/service depends directly on concrete implementation, or business logic buried in controller.

**PHP:**
```php
// Before: concrete dependency + logic in controller
class OrderController {
    public function store(Request $req) {
        $order = DB::find('orders', $req->id); // direct DB call
    }
}

// After: interface in use case, inject concrete implementation
interface OrderRepository { public function findById($id); }
class CreateOrderUseCase {
    public function __construct(private OrderRepository $repo) {}
    public function execute($req) { return $this->repo->findById($req->id); }
}
class DatabaseOrderRepository implements OrderRepository {
    public function findById($id) { return DB::find('orders', $id); }
}
```

**TypeScript:**
```typescript
// Before: direct fetch in service
class OrderService {
    async get(id: string) { return (await fetch(`/api/orders/${id}`)).json(); }
}

// After: inject repository interface
interface OrderRepository { findById(id: string): Promise<Order>; }
class OrderService {
    constructor(private repo: OrderRepository) {}
    async get(id: string) { return this.repo.findById(id); }
}
class HttpOrderRepository implements OrderRepository {
    async findById(id: string) { return (await fetch(`/api/orders/${id}`)).json(); }
}
```

**Verification:** Delete the concrete implementation; does your use case still compile with just the interface?

### Push Framework to Outer Layer

**Problem:** Framework code leaks into domain entities.

**PHP:** Domain order is pure (no ORM, no DB), persistence moves to adapters.
```php
// Domain: pure
class Order {
    public function calculateDiscount(): Money { return $this->amount->multiply(0.1); }
}
// Adapter: persistence
class OrderPersister { public function save(Order $o) { /* DB here */ } }
```

**TypeScript:** Domain order is pure, service calls handle API.
```typescript
// Domain: pure
export class Order {
    calculateDiscount(): number { return this.amount * 0.1; }
}
// Service: API layer
class OrderService { async save(o: Order) { await fetch('/api/orders', {...}); } }
```

### Package by Feature

**Problem:** Feature's controller, service, repository scattered across layer folders.

**Before (by layer):** Hard to see what belongs to "orders"
```
app/Http/Controllers/OrderController.php
app/Services/OrderService.php
app/Domain/Order.php
app/Repositories/OrderRepository.php
```

**After (by feature):** Feature boundary is clear
```
app/Features/Orders/
  Http/OrderController.php
  UseCases/CreateOrderUseCase.php
  Repositories/OrderRepository.php
  Domain/Order.php
```

---

## When NOT to Apply

- **Small CRUD apps** — if your app is "read form, write database, display result," don't force architectural layers. The framework IS your architecture.
- **Prototypes** — exploring unknowns faster than architecture precision.
- **Framework-heavy projects** — if fighting the framework costs more than the boundary benefit (e.g., Rails single-table inheritance), embrace it.
- **Single-developer projects with no change pressure** — architecture is insurance against the cost of change. If change pressure is low, the premium isn't worth it.
- **Scripts and utilities** — a 50-line CLI tool doesn't need use case interactors.

**Rule of thumb:** Apply architecture in proportion to change pressure. Greenfield systems: full architecture. Stable systems: minimal structure. Evolving systems: introduce structure as needed.

---

## K-Line History

- 2025-Q1: PHP + TypeScript stack focus. Added detection commands and domain separation patterns.
- 2024-Q1: Restructured around "detect then apply" — detect context before prescribing rules.

---

## Communication Style

- **Be skeptical of pure architecture.** Framework reality wins. Design with the grain, not against it.
- **Draw lines proportional to change pressure.** Premature abstraction is overhead; late abstraction is pain. Both are real costs.
- **Test the architecture by removing pieces.** Can you test domain logic without the framework? If no, the boundary is wrong.
- **Every boundary has a cost.** More abstraction = more interfaces, more indirection, more files. Worth it when it isolates change. Not worth it when it isolates nothing.
- **Dependencies move more slowly than code.** You can refactor a function in a day; breaking a dependency cycle takes weeks. Protect dependencies carefully.

---

## Related Skills

- `/solid` — SOLID principles for class/module design within boundaries
- `/components` — Component cohesion, coupling metrics, stability
- `/patterns` — Design patterns that implement architectural concepts
