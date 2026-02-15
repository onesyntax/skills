# Functional Programming — Extended Examples

Deep dives, category theory foundations, and architecture examples for functional programming.

---

## Category Theory Foundations

### Categories

A category is a collection of objects connected by arrows (morphisms) that compose. Programming types form a category where types are objects and functions are arrows.

```
Category rules:
1. Composition: If f: A→B and g: B→C, then g∘f: A→C exists
2. Associativity: h∘(g∘f) = (h∘g)∘f
3. Identity: For every object A, there exists id_A such that f∘id_A = f and id_A∘g = g
```

Why this matters for programming: Function composition is guaranteed to work. If `parse: String→Data` and `validate: Data→Result`, then `validate∘parse: String→Result` is automatically valid. This is why FP pipelines are reliable — they're backed by mathematical law, not convention.

### Monoids

A monoid is a type with an associative binary operation and an identity element:

```
Monoid laws:
1. Closure: combine(a, b) produces same type
2. Associativity: combine(a, combine(b, c)) = combine(combine(a, b), c)
3. Identity: combine(a, identity) = combine(identity, a) = a

Examples:
- (Integer, +, 0)     — numbers under addition
- (Integer, ×, 1)     — numbers under multiplication
- (String, concat, "") — strings under concatenation
- (List, append, [])   — lists under append
- (Boolean, AND, true) — booleans under AND
- (Boolean, OR, false) — booleans under OR
```

Why this matters for programming: Monoids enable safe parallel reduction. Because `combine` is associative, you can split a list across cores, reduce each chunk independently, then combine the results. `reduce(add, 0, numbers)` works in parallel precisely because `(Integer, +, 0)` is a monoid.

```
Sequential:  reduce(add, 0, [1, 2, 3, 4, 5, 6, 7, 8]) = 36

Parallel:
  Core 1: reduce(add, 0, [1, 2, 3, 4]) = 10
  Core 2: reduce(add, 0, [5, 6, 7, 8]) = 26
  Combine: add(10, 26) = 36  ✓ Same result!
```

This ONLY works because addition is associative. Subtraction is NOT a monoid — parallel subtraction gives wrong results.

### Functors

A functor is a mapping between categories that preserves structure — it maps both objects and arrows while preserving composition and identity:

```
Functor laws:
1. map(id, container) = container                    — preserves identity
2. map(g∘f, container) = map(g, map(f, container))  — preserves composition

Examples:
- List is a functor: map(f, [a, b, c]) = [f(a), f(b), f(c)]
- Maybe is a functor: map(f, Just(x)) = Just(f(x)), map(f, Nothing) = Nothing
- Tree is a functor: map(f, tree) applies f to every node
```

Why this matters: `map` is not just "apply function to list." It's a universal pattern for applying transformations inside any container while preserving the container's structure. Once you recognize a type as a functor, you know `map` works correctly on it — the functor laws guarantee it.

### Monads

A monad is a functor with additional structure — it supports `flatMap` (also called `bind` or `>>=`) which handles nested containers:

```
Monad operations:
- unit(value): Wrap a value in the monad (also called return, pure, of)
- flatMap(f, monad): Apply f (which returns a monad) and flatten the result

Monad laws:
1. Left identity:  flatMap(f, unit(x)) = f(x)
2. Right identity: flatMap(unit, m) = m
3. Associativity:  flatMap(g, flatMap(f, m)) = flatMap(x -> flatMap(g, f(x)), m)

The problem monads solve — nested containers:
  map(parse, Just("42"))        = Just(Just(42))   — nested Maybe!
  flatMap(parse, Just("42"))    = Just(42)          — flattened!

  map(getOrders, [user1, user2])     = [[order1, order2], [order3]]  — nested lists!
  flatMap(getOrders, [user1, user2]) = [order1, order2, order3]      — flattened!
```

Common monads in practice: Maybe/Option (nullable values), Either/Result (error handling), List (multiple results), IO (side effects), Promise/Future (async operations).

---

## Functional Web Architecture

Web request handling is inherently functional — a request comes in, a function processes it, a response goes out.

### HTTP as Data

Represent HTTP as plain data structures — maps, not objects:

```
request = {
    method: GET,
    uri: "/users/42",
    headers: {"content-type": "application/json"},
    body: nil
}

response = {
    status: 200,
    headers: {"content-type": "application/json"},
    body: "{\"name\": \"Alice\"}"
}

// A handler is just a function: Request → Response
handler(request):
    user = findUser(request.uri.id)
    return {status: 200, body: toJson(user)}
```

No class hierarchy. No response builder pattern. Just data in, data out.

### Middleware as Function Composition

Each middleware is a higher-order function that wraps a handler:

```
wrapLogging(handler):
    return (request) ->
        log("-->", request.method, request.uri)
        response = handler(request)
        log("<--", response.status)
        return response

wrapAuthentication(handler):
    return (request) ->
        user = authenticate(request.headers.authorization)
        if user == nil: return {status: 401, body: "Unauthorized"}
        return handler(request.with(user: user))

wrapContentType(handler):
    return (request) ->
        response = handler(request)
        return response.with(headers: response.headers.merge({"content-type": "application/json"}))

// Compose middleware — order matters (outermost wraps first)
app = compose(wrapLogging, wrapAuthentication, wrapContentType, routeHandler)
```

Each middleware is independently testable, reusable, and composable. The full app is built entirely from composed functions.

### Routing as Data

Routes are data structures, not annotations or configuration files:

```
routes = [
    {method: GET,  path: "/users",     handler: listUsers},
    {method: GET,  path: "/users/:id", handler: getUser},
    {method: POST, path: "/users",     handler: createUser},
    {method: PUT,  path: "/users/:id", handler: updateUser}
]
```

### Clean Architecture with FP

Functional Clean Architecture enforces the dependency rule through function arguments, not class hierarchies:

```
// Entities — pure data + pure functions
User = {name, email, role}
validateUser(user): return user.name != "" and isValidEmail(user.email)

// Use Cases — pure functions (interactors)
createUser(userGateway, user):
    if not validateUser(user): return {error: "Invalid user data"}
    if userGateway.findByEmail(user.email): return {error: "Email taken"}
    return userGateway.save(user)

// Interface Adapters — translate between use cases and external format
handleCreateUser(request):
    userData = parseJson(request.body)
    result = createUser(gateway, userData)
    if result.error: return {status: 400, body: toJson(result)}
    return {status: 201, body: toJson(result)}

// Frameworks — HTTP library, database driver (outermost layer, all side effects here)
```

`createUser` takes a `userGateway` as an argument — it doesn't import one. The dependency rule is enforced through function parameters.

---

## Extended Architecture Examples

### The Object Mother Pattern — Functional Test Fixtures

Test fixtures through builder functions — pure functions that produce test data:

```
// Base factory — returns valid default
makeUser():
    return {
        name: "Test User",
        email: "test@example.com",
        role: MEMBER,
        active: true,
        createdAt: epoch(0)
    }

// Derived factories — override specific fields
makeAdmin(): return makeUser().with(role: ADMIN)
makeInactive(): return makeUser().with(active: false)
makeUserWithName(name): return makeUser().with(name: name)

// Composable — combine overrides
makeInactiveAdmin(): return makeUser().with(role: ADMIN, active: false)

// In tests
test "admin can delete users":
    admin = makeAdmin()
    target = makeUser()
    result = deleteUser(admin, target)
    assert result.success == true

test "member cannot delete users":
    member = makeUser()
    target = makeUser()
    result = deleteUser(member, target)
    assert result.error == "Insufficient permissions"
```

Each factory is a pure function. No shared mutable state between tests. No test database to set up and tear down.

### State Machine as Pure Function

A state machine is naturally a pure function: `(CurrentState, Event) → NewState`

```
// Turnstile state machine — functional implementation
transition(state, event):
    return cond:
        state == LOCKED and event == COIN:   {state: UNLOCKED, action: UNLOCK}
        state == LOCKED and event == PUSH:   {state: LOCKED, action: ALARM}
        state == UNLOCKED and event == COIN: {state: UNLOCKED, action: THANKYOU}
        state == UNLOCKED and event == PUSH: {state: LOCKED, action: LOCK}

// Process sequence of events — reduce!
processEvents(initialState, events):
    return reduce(
        (result, event) ->
            next = transition(result.state, event)
            {state: next.state, actions: result.actions.append(next.action)},
        {state: initialState, actions: []},
        events
    )

// Completely testable, deterministic, no side effects
test "coin then push unlocks then locks":
    result = processEvents(LOCKED, [COIN, PUSH])
    assert result.state == LOCKED
    assert result.actions == [UNLOCK, LOCK]
```

### Memoization — Caching as a Pure Function Optimization

Because pure functions always return the same output for the same input, their results can be cached safely:

```
memoize(f):
    cache = {}
    return (args...) ->
        key = hash(args)
        if key not in cache:
            cache[key] = f(args...)
        return cache[key]

// Usage
slowFibonacci(n):
    if n <= 1: return n
    return slowFibonacci(n - 1) + slowFibonacci(n - 2)

fibonacci = memoize(slowFibonacci)
fibonacci(40)  // Fast — each value computed only once

// This is ONLY safe for pure functions!
// Memoizing an impure function caches stale results
```

Memoization is impossible to do safely with impure functions — if the function's result depends on external state, the cache becomes a source of bugs.

---

## TDD and Algorithmic Thinking

Ron Jeffries attempted to solve Sudoku using pure TDD — writing the simplest failing test, making it pass, refactoring, repeating. After many iterations, he never produced a working solver. He approached it mechanically, letting the tests "drive" the design without understanding the underlying algorithm.

Peter Norvig wrote a Sudoku solver in a single sitting using constraint propagation and backtracking search — he understood the algorithm before writing the code.

**The lesson:** TDD is the inner development loop. Algorithmic thinking is the outer development loop. You need both. TDD tells you WHEN your code works. It doesn't tell you WHAT algorithm to implement. Start with understanding, then use TDD to build it incrementally.

The Red-Green-Refactor cycle works brilliantly when you understand the data transformations your pipeline needs to perform.
