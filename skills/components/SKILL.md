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

# Components Workflow

Follow this workflow when analyzing component structure, reviewing dependencies, or designing module boundaries using Uncle Bob's component principles.

## Workflow Steps

1. **Apply REP (Reuse/Release Equivalence Principle)** - Ensure classes grouped together are releasable together
2. **Apply CCP (Common Closure Principle)** - Gather classes that change for the same reasons
3. **Apply CRP (Common Reuse Principle)** - Don't force users to depend on things they don't need
4. **Balance the Tension Triangle** - Find the right balance based on project maturity
5. **Ensure ADP (Acyclic Dependencies)** - Verify no cycles exist in the component dependency graph
6. **Follow SDP (Stable Dependencies)** - Dependencies must point toward stability
7. **Follow SAP (Stable Abstractions)** - Stable components should be abstract
8. **Apply /professional workflow** - Ensure quality standards are met

---

## What is a Component?

A component is the unit of deployment - the smallest entity that can be deployed as part of a system. In different languages:
- **Java**: JAR files
- **Ruby**: gem files
- **Node**: npm packages
- **.NET**: DLLs

---

## Component Cohesion Principles

These principles help decide what goes *inside* a component.

### REP: Reuse/Release Equivalence Principle

**"The granule of reuse is the granule of release."**

- Classes and modules grouped into a component should be releasable together
- If you reuse one class, you implicitly reuse all classes in that component
- Components should have a version number and release documentation
- All classes in a component should share the same version

**Implication:** Don't put unrelated classes together just because they're small. Users will be forced to track releases for things they don't use.

**Signs of violation:**
- Component contains unrelated classes
- Users only want part of the component
- Version changes affect unrelated functionality

### CCP: Common Closure Principle

**"Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons."**

This is SRP for components. A component should not have multiple reasons to change.

**Benefits:**
- Limits the number of components that need to be redeployed
- Changes to business rules affect only business rule components
- Changes to reporting affect only reporting components

**Example:** If Order and OrderValidator always change together, put them in the same component. If they change independently, separate them.

**Signs of violation:**
- A single change requires modifying multiple components
- Unrelated changes bundled in one component release
- High coupling between components

### CRP: Common Reuse Principle

**"Don't force users of a component to depend on things they don't need."**

This is ISP for components. When you depend on a component, you depend on the entire component - every class in it.

**Implication:** If you reuse one class from a component, you're coupled to ALL classes. If ANY class changes, your component may need to be redeployed.

**Solution:** Keep components focused. Don't mix unrelated classes.

**Signs of violation:**
- Users import a component but only use a fraction of it
- Changes to unused classes force recompilation/redeployment
- Component has multiple unrelated "features"

---

## The Tension Triangle

```
        REP
       /    \
      /      \
    CCP ---- CRP
```

These three principles are in tension:
- **REP + CCP** = Group for reuse and closure = Components get large
- **CCP + CRP** = Group for closure and minimal coupling = Hard to reuse
- **CRP + REP** = Group for reuse and minimal coupling = Many small components, lots of releases

**Resolution:** Start with CCP (minimize changes), then relax toward CRP (minimize dependencies), then REP (better packaging). The balance shifts as the system matures.

**Balance based on project maturity:**
- **Early development:** Favor CCP (ease of change)
- **Later development:** Favor REP and CRP (ease of reuse)

---

## Component Coupling Principles

These principles govern relationships *between* components.

### ADP: Acyclic Dependencies Principle

**"There must be no cycles in the component dependency graph."**

The dependency graph must be a Directed Acyclic Graph (DAG).

**The Morning After Syndrome:**
You leave code working on Friday. Monday morning, it's broken because someone changed a component you depend on, and they depended on something you changed.

**The Weekly Build Anti-Pattern:**
Everyone ignores each other for four days, then spends Friday integrating. As systems grow, integration takes longer and longer.

**Breaking Cycles:**

Method 1: Dependency Inversion
```
// Before: A -> B -> C -> A (cycle!)
// After: Extract interface, invert dependency
A -> B -> C -> InterfaceA
A implements InterfaceA
```

Method 2: Create New Component
```
// Extract the shared functionality into a new component D
A -> D
B -> D
C -> D
```

### SDP: Stable Dependencies Principle

**"Depend in the direction of stability."**

A component with many incoming dependencies is stable - it's hard to change because many other components would be affected.

**Stability Metric (I):**
```
I = Fan-out / (Fan-in + Fan-out)

Fan-in: Incoming dependencies (classes outside that depend on classes inside)
Fan-out: Outgoing dependencies (classes inside that depend on classes outside)

I = 0: Maximally stable (only incoming, no outgoing)
I = 1: Maximally unstable (only outgoing, no incoming)
```

**Adults vs. Teenagers:**
- **Adults (I = 0):** Responsible, independent, stable. Hard to change. Many depend on them.
- **Teenagers (I = 1):** Irresponsible, dependent, unstable. Easy to change. No one depends on them.

**The Rule:** Depend on components that are MORE stable than you. Unstable components can depend on stable ones, not vice versa.

**Violation Example:**
```
Stable Component (I=0) --> Unstable Component (I=1)
```
This is wrong! The stable component will be hard to change, but it depends on something that changes frequently.

### SAP: Stable Abstractions Principle

**"A component should be as abstract as it is stable."**

Stable components should be abstract so they can be extended. Unstable components should be concrete since they'll change anyway.

**Abstractness Metric (A):**
```
A = Na / Nc

Na: Number of abstract classes and interfaces in component
Nc: Total number of classes in component

A = 0: Component is entirely concrete
A = 1: Component is entirely abstract
```

---

## The Main Sequence

Plot components on an A vs. I graph:
```
A (Abstractness)
1 |  Zone of          .
  |  Uselessness    .
  |              .
  |           .   <-- Main Sequence
  |        .
  |     .
  |  .   Zone of Pain
0 +--------------------> I (Instability)
  0                    1
```

**Zone of Pain (0,0):** Highly stable AND highly concrete. Hard to change, and there's no way to extend it. Painful!
- Example: Database schemas, String class (but non-volatile, so acceptable)

**Zone of Uselessness (1,1):** Maximally abstract AND maximally unstable. No one depends on it, and it does nothing concrete. Useless!

**The Main Sequence:** The line from (0,1) to (1,0). Well-designed components fall near this line.

**Distance Metric (D):**
```
D = |A + I - 1|

D = 0: Component is on the Main Sequence
D = 1: Component is as far as possible from the Main Sequence
```

Track D over time. Components drifting away from the Main Sequence need attention.

---

## Code/Module to Analyze

$ARGUMENTS

## Analysis Process

1. **Identify Components**
   - What are the deployable units?
   - What are the package/module boundaries?

2. **Cohesion Analysis**
   - REP: Can these classes be released together meaningfully?
   - CCP: Do these classes change together?
   - CRP: Do users need all of these classes?

3. **Dependency Analysis**
   - Map component dependencies
   - Check for cycles (ADP)
   - Calculate stability metrics
   - Check abstraction levels

4. **Coupling Evaluation**
   - SDP: Are dependencies pointing toward stability?
   - SAP: Are stable components abstract?

5. **Main Sequence Assessment**
   - Calculate A and I for each component
   - Calculate distance from Main Sequence (D)
   - Identify components in Zone of Pain or Zone of Uselessness

---

## Output Format

```
## Component: [name]

**Cohesion Assessment:**
- REP: [pass/warning/violation] - [explanation]
- CCP: [pass/warning/violation] - [explanation]
- CRP: [pass/warning/violation] - [explanation]

**Stability Metrics:**
- Fan-in: X
- Fan-out: Y
- Instability (I): Z

**Abstractness Metrics:**
- Abstract classes/interfaces: X
- Total classes: Y
- Abstractness (A): Z

**Main Sequence:**
- Distance (D): X
- Position: [On Main Sequence / Zone of Pain / Zone of Uselessness]

**Dependencies:**
- Depends on: [list]
- Depended on by: [list]

**Issues:**
- [List of violations with locations]

**Recommendations:**
- [Specific improvements]
```

---

## Memorable Quotes

> "Stable components should be abstract. Unstable components should be concrete."

> "Adults are responsible and independent. Teenagers are irresponsible and dependent." - On component stability

> "The morning after syndrome - you leave Friday with working code, Monday it's broken." - Why we need acyclic dependencies

> "The granule of reuse is the granule of release." - REP

> "Don't force users of a component to depend on things they don't need." - CRP

---

## Related Skills

- **/professional** - Apply professional standards workflow for code quality, naming conventions, formatting, and maintainability
- **/architecture** - Apply Clean Architecture patterns including the Dependency Rule, boundaries, and component principles in system design
