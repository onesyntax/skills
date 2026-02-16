---
name: components
description: >-
  Module boundaries, package organization, monorepo structure, dependency management,
  composer/npm/pip/cargo package design. Activate when defining package structure,
  managing coupling across module boundaries, or when the user mentions monorepo,
  package.json, composer.json, coupling, cohesion, circular dependency, or module design.
model: opus
allowed-tools: [bash, read, grep, write]
delegates-to: [architecture, solid]
argument-hint: "[--detect-only] [--stack=npm|python|rust|go] [--show-metrics]"
---

## Step 0: Detect Context

Identify your component model and dependency tooling:

```bash
# Composer (PHP): list package boundaries
find . -name "composer.json" -not -path "*/vendor/*" | head -20

# npm (TypeScript): list package boundaries
find . -name "package.json" -not -path "*/node_modules/*" | head -20

# Dependency graph detection
# Composer (PHP): composer show --direct | grep -E "packages|requires"
# npm (TypeScript): npm ls --depth=0
```

Detect: package manager, monorepo structure, module system, existing dependency graph.

## Step 1: Generate Context-Specific Rules

Map principles to detected stack:

| Stack | Component Boundary | Visibility Control | Dependency Expression |
|-------|-------------------|-------------------|----------------------|
| **Composer/PHP** | Package (PSR-4 namespace) | public/protected/private, internal dirs | composer.json require |
| **npm/TypeScript** | Package (package.json) | exports field, barrel files | package.json dependencies |
| **Monorepo** | Workspace package | Same as native, plus workspace rules | workspace field enforces CRP |

Apply immediately:
- **REP (Reuse/Release):** Split when components have different release cadences or version lifecycles
- **CCP (Common Closure):** Merge when changes to one package require changes to another
- **CRP (Common Reuse):** Isolate unnecessary coupling; remove dependents that import only one symbol
- **ADP (Acyclic):** Detect cycles with madge/pipdeptree/go mod graph; use Dependency Inversion to break
- **SDP (Stable Dependencies):** Measure stability (I = Fan-out/(Fan-in+Fan-out)); abstract should flow left, dependencies should flow right
- **SAP (Stable Abstractions):** When I is high (stable), A must be high (abstract); when I is low (volatile), A must be low (concrete)

**Tension Triangle:** Early stage (prototype) → favor CCP. Mature codebase → balance all three. High-velocity teams → favor REP (loose coupling).

## Step 2: Apply Decision Rules

For each package boundary or cycle:

| Decision | Rule | Action |
|----------|------|--------|
| **Split now?** | CCP: unrelated changes trigger updates in different directions | Yes if: changes in A never co-occur with B; REP applies |
| **Merge now?** | CCP: every change to A requires change to B and vice versa | Yes if: <5 symbols exported; <10% external dependents |
| **Remove dependency?** | CRP: A imports only one symbol from B; or import is for test only | Yes if: can create minimal wrapper or inline; else refactor B |
| **Break cycle?** | ADP: A→B→A or longer ring detected | Use DIP: introduce abstraction C; both A and B depend on C |
| **Fix direction?** | SDP: dependency points from stable to volatile | Invert: abstract the stable component; volatile depends upward |
| **Add abstraction?** | SAP: I > 0.7 (stable) but A ≈ 0 (no interfaces) | Add abstract base; make concrete impl depend on it |

## Step 3: Review Checklist

Before merging or shipping:

| Check | Command | Pass Criteria |
|-------|---------|---------------|
| **No cycles** | `composer check-platform-reqs` OR manual inspection of composer.json | Empty output |
| **Stability direction** | Compute I for each pkg; graph should flow up | Dependents have lower I than dependencies |
| **Abstraction-stability** | For each pkg: A=(abstractions/total classes), I, compute D=\|A+I-1\| | D < 0.5 (Zone of Pain) only for foundation; D > 0.3 (Zone of Uselessness) only for experimental |
| **Release granularity** | Can each package release independently? | No cross-version pinning within monorepo |
| **Unnecessary coupling** | Find imports of >1 symbol, <5 used | Move only necessary symbols; rest stays in source |
| **Pain zones** | Identify (I, A) pairs: Pain=(I>0.8, A<0.3), Useless=(I<0.2, A>0.8) | Pain components are candidates for split or stabilization; Useless are dead code or too abstract |

## Step 4: Refactoring Patterns

### Break Dependency Cycle
Detect: Inspect composer.json or package.json dependencies manually for circular references
Apply DIP: Create shared abstraction; both sides depend on it, not each other.

### Split Overloaded Package
Measure: >500 lines, >15 exported symbols, multiple release cadences. Action: Partition exports by feature; move to separate packages.

### Merge Under-loaded Packages
Measure: <100 lines, <3 exported symbols, high co-change. Action: Move to parent package; update imports.

### Stabilize Foundation Component
Identify: High fan-in (>5 dependents), High fan-out (>5 dependencies), Low abstraction. Action: Extract abstract interface; make concrete impl detail; refactor dependents.

### Abstract Stable Component
Identify: I > 0.7, A ≈ 0. Action: Define interface/trait/abstract base; move concrete impl to separate internal package; adjust visibility.

## When NOT to Apply

- Single-package projects: Skip until splitting is justified by size or release cycles
- Early prototypes (< 3 months): Favor CCP; delay splitting
- Tiny teams (<3 engineers): Fewer components = less coordination cost
- Internal tools, single consumer: Defer until multi-consumer demand appears

## K-Line History

**I (Instability) = Fan-out / (Fan-in + Fan-out)**
- I = 1: no dependents, isolated
- I = 0: all dependents, stable foundation
- Optimal: I increases as you go up the dependency graph

**A (Abstractness) = (Abstract Classes | Interfaces | Traits) / Total Classes**
- A = 1: pure abstraction
- A = 0: pure concrete
- Optimal: A ≈ 1 - I (main sequence)

**D (Distance from Main Sequence) = |A + I - 1|**
- D ≈ 0: healthy
- D > 0.3 (Zone of Uselessness): too abstract, not used
- D > 0.5 (Zone of Pain): too concrete, too depended-on; refactor

---

## Communication Style

- Use metrics as operational diagnostics, not teaching moments
- Pair each rule with a concrete bash/CLI command
- Frame decisions as tradeoffs in the Tension Triangle
- Focus on: Can we release this independently? Does it have too many jobs? Are we stable enough to abstract?
- Keep refactoring patterns small and named; pair with one metric check each
