---
name: components
description: >-
  Guide component design and structure - cohesion, coupling, and dependencies.
  Activates when designing module boundaries, organizing packages, reviewing
  component dependencies, or when the user mentions cohesion, coupling, module
  design, package structure, or component dependencies.
allowed-tools: Read, Grep, Glob
argument-hint: [code, module, or package to analyze]
---

# Component Principles

Follow this workflow when analyzing component structure, reviewing dependencies, or designing module boundaries using Uncle Bob's component principles.

For extended examples (real-world component redesigns, metric calculations, cycle-breaking walkthroughs), read `references/extended-examples.md`.

## Workflow Steps

1. **Apply REP** — Ensure classes grouped together are releasable together
2. **Apply CCP** — Gather classes that change for the same reasons
3. **Apply CRP** — Don't force users to depend on things they don't need
4. **Balance the Tension Triangle** — Find the right balance based on project maturity
5. **Ensure ADP** — Verify no cycles in the component dependency graph
6. **Follow SDP** — Dependencies must point toward stability
7. **Follow SAP** — Stable components should be abstract
8. **Apply /professional workflow** — Ensure quality standards are met

---

## What is a Component?

A component is the unit of deployment — the smallest entity that can be deployed as part of a system. Every language has its own packaging mechanism (packages, modules, libraries, assemblies), but the principles are universal. A component groups related code that is released, versioned, and deployed together.

---

## Component Cohesion Principles

These principles help decide what goes *inside* a component.

### REP: Reuse/Release Equivalence Principle

**"The granule of reuse is the granule of release."**

Classes and modules grouped into a component must be releasable together. If you reuse one class from a component, you implicitly depend on all classes in that component. They should all share the same version and release cycle.

**Implication:** Don't put unrelated classes together just because they're small. Users will be forced to track releases for things they don't use.

**Signs of violation:**
- Component contains unrelated classes that serve different purposes
- Users only want part of the component
- Version changes affect functionality unrelated to what users actually use

### CCP: Common Closure Principle

**"Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons."**

This is SRP applied to components. A component should not have multiple reasons to change.

**Why it matters:** When a requirement changes, you want that change confined to the fewest components possible. If Order and OrderValidator always change together, they belong in the same component. If they change independently, separate them.

**Signs of violation:**
- A single business change requires modifying multiple components
- Unrelated changes bundled in one component release
- High coupling between components that should be independent

### CRP: Common Reuse Principle

**"Don't force users of a component to depend on things they don't need."**

This is ISP applied to components. When you depend on a component, you depend on the *entire* component — every class in it. If ANY class changes, your component may need to be revalidated and redeployed.

**Solution:** Keep components focused. If a group of classes are not tightly bound together — if they are not reused together — they should not be in the same component.

**Signs of violation:**
- Users import a component but only use a fraction of it
- Changes to unused classes force recompilation or redeployment
- Component has multiple unrelated "features"

---

## The Tension Triangle

```
        REP
       /    \
      /      \
    CCP ---- CRP
```

These three principles pull in different directions:

- **REP + CCP** (neglect CRP) = Components get large, many unnecessary dependencies
- **CCP + CRP** (neglect REP) = Hard to reuse, too many small components
- **CRP + REP** (neglect CCP) = Many small components, too many releases for simple changes

**Resolution by project maturity:**
- **Early development:** Favor CCP — ease of change matters most. You're discovering what changes together.
- **Growing system:** Shift toward CRP — minimize unnecessary dependencies as the component graph grows.
- **Mature system:** Favor REP — package for reuse across teams and projects.

The balance is not static. It shifts as the project evolves. Revisit component boundaries as you learn what actually changes together.

---

## Component Coupling Principles

These principles govern relationships *between* components.

### ADP: Acyclic Dependencies Principle

**"There must be no cycles in the component dependency graph."**

The dependency graph must be a Directed Acyclic Graph (DAG).

**The Morning After Syndrome:** You leave code working on Friday. Monday morning, it's broken because someone changed a component you depend on, and they depended on something you changed. Cycles create this — a change anywhere in the cycle ripples everywhere.

**The Weekly Build Anti-Pattern:** Teams ignore each other for four days, then spend Friday integrating. As systems grow, integration takes longer and longer, consuming more of the week. This happens when dependency structure isn't managed.

**Breaking Cycles — two techniques:**

Technique 1 — Dependency Inversion:
```
// Before: A → B → C → A (cycle!)
// After: Extract an interface that breaks the cycle
A → B → C → InterfaceA
A implements InterfaceA
// Now C depends on InterfaceA, not on A directly
```

Technique 2 — Extract New Component:
```
// Before: A and C both depend on each other
// After: Extract shared functionality into new component D
A → D
C → D
// Both depend on D, neither depends on the other
```

**Important:** The component structure is not designed up-front. It evolves. As the system grows, you manage the dependency structure to prevent cycles from forming. The dependency graph is a map of the *buildability* and *deployability* of the system — not a map of the application's functionality.

### SDP: Stable Dependencies Principle

**"Depend in the direction of stability."**

A component with many incoming dependencies is stable — it's hard to change because many other components would be affected. A component with no incoming dependencies is unstable — it's easy to change because nothing depends on it.

**Stability Metric (I):**
```
I = Fan-out / (Fan-in + Fan-out)

Fan-in:  Number of classes outside that depend on classes inside this component
Fan-out: Number of classes inside that depend on classes outside this component

I = 0: Maximally stable (only incoming dependencies — hard to change)
I = 1: Maximally unstable (only outgoing dependencies — easy to change)
```

**The Adults and Teenagers analogy:** Stable components are like responsible adults — many people depend on them, so they can't change easily. Unstable components are like teenagers — they're volatile, dependent on others, and no one relies on them yet. Neither is inherently good or bad. A system needs both. But teenagers should not be depended upon by adults.

**The Rule:** Every component's dependencies should point toward components with lower I values (higher stability). If a stable component depends on an unstable component, the unstable one will effectively become frozen — it can't change without breaking the stable one.

### SAP: Stable Abstractions Principle

**"A component should be as abstract as it is stable."**

Stable components should be abstract so they can be extended without modification. Unstable components should be concrete — they'll change anyway, and concreteness makes them easier to modify.

**Abstractness Metric (A):**
```
A = Na / Nc

Na: Number of abstract classes and interfaces in the component
Nc: Total number of classes in the component

A = 0: Entirely concrete
A = 1: Entirely abstract
```

SAP + SDP together = the Dependency Rule from Clean Architecture. High-level policies (abstract, stable) should not depend on low-level details (concrete, unstable).

---

## The Main Sequence

Plot components on an A vs. I graph to assess their health:

```
A (Abstractness)
1 |  Zone of          .
  |  Uselessness    .
  |              .
  |           .   ← Main Sequence (ideal line)
  |        .
  |     .
  |  .   Zone of Pain
0 +-------------------→ I (Instability)
  0                    1
```

**Zone of Pain (A=0, I=0):** Highly stable AND highly concrete. Hard to change, and there's no abstraction to extend. Database schemas and foundational utility classes often land here — acceptable if they're non-volatile (rarely change). Painful if they DO change.

**Zone of Uselessness (A=1, I=1):** Maximally abstract AND maximally unstable. No one depends on it, and it does nothing concrete. Dead interfaces and abandoned abstractions live here.

**The Main Sequence:** The line from (A=1, I=0) to (A=0, I=1). Well-designed components fall near this line — their abstractness matches their stability.

**Distance from Main Sequence (D):**
```
D = |A + I - 1|

D = 0: Component is on the Main Sequence
D = 1: Component is as far as possible from the Main Sequence
```

Track D over time. Components drifting away from the Main Sequence need attention. A statistical analysis of D across all components reveals the overall health of the component structure.

---

## Review Checklist

When reviewing component design:

**Cohesion:**
- [ ] Each component contains classes that belong together (REP)
- [ ] Classes that change together are in the same component (CCP)
- [ ] No component forces users to depend on things they don't need (CRP)
- [ ] The tension triangle balance is appropriate for project maturity

**Coupling:**
- [ ] No cycles in the dependency graph (ADP)
- [ ] Dependencies point toward stability (SDP)
- [ ] Stable components are abstract (SAP)
- [ ] Components near the Main Sequence (low D values)

**Practical:**
- [ ] Component boundaries align with team boundaries
- [ ] Each component can be built and tested independently
- [ ] Component versions are meaningful — a release contains related changes
- [ ] New components can be added without modifying existing ones

---

## Common Pitfalls

**Designing components top-down.** Component structure is not designed at the start of a project. It evolves as the system grows and as you discover what actually changes together. Early in development, you have no reusers, no dependency issues, and no deployment concerns. Component structure emerges from the need to manage complexity.

**Confusing component diagrams with functionality maps.** The component dependency graph is NOT a map of how the application works. It's a map of buildability and deployability. Don't try to represent the functional decomposition of the application in the component diagram.

**Ignoring the Tension Triangle.** Optimizing for all three cohesion principles simultaneously is impossible. You must choose which to emphasize based on where the project is. Trying to optimize for reuse (REP + CRP) in early development wastes time. Ignoring reuse in a mature system creates duplication.

**Treating stability as always good.** A system where every component is maximally stable (I=0) is rigid and impossible to change. You need unstable components — they're where the easy-to-change concrete implementation lives. The goal is not maximum stability everywhere, but proper stability *direction* — dependencies pointing from unstable toward stable.

---

## Related Skills

- **/solid** — The class-level principles that component principles build on (SRP→CCP, ISP→CRP)
- **/architecture** — Clean Architecture uses component principles to enforce the Dependency Rule
- **/patterns** — Design patterns often guide how to structure components and their interactions
- **/professional** — Professional standards for code quality and maintainability
