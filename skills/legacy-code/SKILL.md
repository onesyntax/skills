---
name: legacy-code
description: >-
  Guide working with legacy code using Uncle Bob's and Michael Feathers' techniques.
  Activates when dealing with old, untested, or poorly structured code, when the user
  mentions legacy code, technical debt, characterization tests, strangulation, working
  with old code, or when facing code that is difficult to change or test.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [file or directory to analyze]
---

# Legacy Code

Guide for working with legacy code using Uncle Bob's teachings and Michael Feathers' techniques from "Working Effectively with Legacy Code."

For extended examples (characterization test walkthroughs, strangulation case studies, real-world acts of kindness), read `references/extended-examples.md`.

## Workflow Steps

1. **Assess the situation** — what legacy code are you touching and why? Any existing tests?
2. **Apply the Boy Scout Principle** — plan one small act of kindness alongside the required change
3. **Write characterization tests** where possible — capture current behavior as a safety net
4. **Add new features in clean modules** — write new code with TDD, integrate at boundaries
5. **Perform incremental cleanup** — one rename, one split, one decouple — then check in
6. **Watch for strangulation opportunities** — when clean code surrounds legacy code, it's safe to rewrite
7. **Apply /professional standards** — never check code in worse than you found it

---

## What Is Legacy Code?

Legacy code is not defined by age — it is defined by how it was written. It is code created without proper discipline, tests, or clean design. Critically, legacy code is being actively created TODAY by teams that don't follow clean code practices.

Michael Feathers' key insight: an associate joined a new team that was "busy writing legacy code" — on a brand new project. Legacy code is a discipline problem, not an age problem.

There is no magic solution. No special project, no magic wand. It's going to require long, patient, disciplined work. But there IS a path forward.

---

## The Four Anti-Patterns

### 1. Do Not Start a Cleanup Project

Do not go to your boss and beg for time to clean things up. Do not make promises about timelines or improvements. Cleanup projects almost always fail badly, leaving teams discouraged and discredited, and the code badly mangled. The reason: cleanup projects try to fix everything at once with artificial deadlines, which leads to rushed, incomplete work.

### 2. Do Not Go on a Refactoring Hunt

Don't scan through the code looking for opportunities to refactor. The vast majority of code in a system has not been touched for years and is not likely to be touched anytime soon. Refactoring untouched code does nobody any good. You only improve what you're actively working on.

### 3. Do Not Attempt a Massive Rewrite

The "big redesign in the sky" almost never improves anything. Big rewrites fail because they attempt to replace a working (if ugly) system with an unproven one. The new system inevitably accumulates its own problems, and the old system keeps evolving while the rewrite is underway.

### 4. Do Not Smear New Features Throughout the System

When adding a new feature, the temptation is to write the code in a way consistent with how the legacy system is written — spreading it throughout the codebase. This makes the legacy problem worse, not better. Write new features in clean isolated modules instead.

---

## The Boy Scout Principle

The core strategy for dealing with legacy code is an attitude change: always check the code in cleaner than you checked it out. Every single time. Never check it in worse.

### What One Act of Kindness Looks Like

- Fix one bad coupling
- Change one function name to reveal intent
- Split one large function in two
- Extract one duplicated block
- Add one clarifying comment (only if code can't be made self-documenting)
- Remove one dead code block

Then check it in. Gently — don't try to fix a whole bunch of things at once. Don't dig in and tear it to shreds.

### The Team Effect

If everyone on the team follows this practice, the codebase gradually improves over time. But not ALL of it — only the volatile parts that are actively maintained. This is a feature, not a bug: you only improve what matters.

---

## The Snowball Effect

A virtuous cycle emerges from consistent application of the Boy Scout Principle:

1. Legacy code was not designed to be testable
2. At first, adding tests is impractical
3. After a few acts of kindness, it suddenly becomes easier to add a unit test
4. More tests make the system easier to clean
5. Easier cleaning leads to more tests
6. The pace of improvement accelerates

This is the snowball effect. The volatile parts of the system get cleaner and cleaner, and easier and easier to work in. The key is patience — improvements are small at first, but they accumulate month after month.

---

## The Strangulation Technique

Over months or years, the cleaned volatile parts will completely surround some ugly, untested legacy code that hasn't been modified. Once that legacy code is completely surrounded by tested modules, you have an opportunity to safely rewrite or refactor it.

The cleaner, tested code strangles the legacy code in the middle, allowing it to be rewritten and tested safely. This is the ONLY safe context for a rewrite: small scope, surrounded by tests, protected on all sides.

**The progression:**
```
Phase 1: Legacy everywhere, no tests
┌──────────────────────────┐
│  Legacy  Legacy  Legacy  │
│  Legacy  Legacy  Legacy  │
│  Legacy  Legacy  Legacy  │
└──────────────────────────┘

Phase 2: Clean modules growing around the edges
┌──────────────────────────┐
│ [Clean] Legacy  [Clean]  │
│  Legacy  Legacy  Legacy  │
│ [Clean]  Legacy [Clean]  │
└──────────────────────────┘

Phase 3: Legacy code surrounded — safe to strangle
┌──────────────────────────┐
│ [Clean] [Clean] [Clean]  │
│ [Clean] Legacy  [Clean]  │
│ [Clean] [Clean] [Clean]  │
└──────────────────────────┘
```

---

## Adding New Features to Legacy Systems

### Wrong Way

Smear the code for the new feature throughout the whole system in a way consistent with how the system is written. This perpetuates the legacy problem and makes the code worse.

### Right Way

Write the new feature in its own module independently, using TDD and clean code principles. Make it a nice clean module, then tie it into the rest of the system at integration points.

This takes slightly longer but prevents the legacy problem from growing. Every new clean module is another piece of the strangulation strategy.

```
// Wrong: new code smeared into legacy
LegacyOrderProcessor:
    processOrder(order):
        ... 200 lines of legacy code ...
        // NEW: loyalty points added inline
        if order.customer.loyaltyTier == "gold":
            points = order.total * 2
        else:
            points = order.total
        loyaltyDb.addPoints(order.customer.id, points)
        ... 100 more lines of legacy code ...

// Right: new feature in clean module, integrated at boundary
LoyaltyCalculator:  // new, clean, tested
    calculatePoints(customer, orderTotal):
        multiplier = loyaltyMultiplier(customer.tier)
        return orderTotal * multiplier

    loyaltyMultiplier(tier):
        switch tier:
            GOLD: return 2
            SILVER: return 1.5
            default: return 1

// Integration — minimal touch to legacy code
LegacyOrderProcessor:
    processOrder(order):
        ... legacy code unchanged ...
        loyaltyCalculator.awardPoints(order.customer, order.total)
        ... legacy code unchanged ...
```

---

## Characterization Tests

Michael Feathers' technique for creating safety nets around legacy code.

### When to Use

When you find a module with precisely defined outputs based on precisely defined inputs. Examples: a module that generates a report from data, a transaction processor with log output, an API endpoint with known request/response pairs.

### The Technique

1. **Identify** a module with defined I/O boundaries
2. **Capture** the current output given a known input — this is the "golden standard"
3. **Save** this output as your characterization test
4. **Refactor** the internals of the module
5. **Regenerate** the output after each refactoring step
6. **Compare** to the golden standard — if they match, nothing is broken
7. **Continue** refactoring as long as the golden standard holds

### Properties

- **Fragile by nature**: Any new feature or intentional behavior change invalidates the golden standard
- **Regeneration required**: When behavior intentionally changes, regenerate the golden standard
- **Transitional**: As the system becomes more testable, replace characterization tests with proper unit tests
- **Enables the snowball**: More testability leads to more unit tests, which enables more aggressive refactoring

### Challenges with Non-Deterministic Systems

For transaction-based systems, log files can serve as golden standards. But challenges include different thread ordering between runs, timestamp variations, and non-deterministic process scheduling. A comparison utility that eliminates irrelevant differences (timestamps, thread IDs) and focuses on relevant substance can make this approach viable.

---

## Review Checklist

When reviewing legacy code changes:

**Boy Scout Rule:**
- [ ] Code is cleaner than when you found it
- [ ] At least one act of kindness performed
- [ ] No code checked in worse than it was found

**New Features:**
- [ ] New features in clean isolated modules, not smeared throughout
- [ ] New modules written with TDD
- [ ] Integration at defined boundaries (minimal touch to legacy code)

**Testing:**
- [ ] Characterization tests exist where possible
- [ ] Unit tests added wherever cleaning made it possible
- [ ] Golden standards captured for modules with defined I/O

**Strategy:**
- [ ] No cleanup project initiated (incremental only)
- [ ] No random refactoring hunt (only improving code being touched)
- [ ] Strangulation opportunities identified if clean code now surrounds legacy

---

## Common Pitfalls

**Starting a cleanup project.** Projects fail; incremental improvement succeeds. Don't ask your boss for "cleanup time." Just make the code a little better every time you touch it.

**Hunting for refactoring opportunities.** Only improve code you're actively touching. Refactoring untouched code helps nobody.

**Attempting a massive rewrite.** The "big redesign in the sky" almost never works. Use the Strangulation technique instead.

**Smearing new features.** Write clean modules, integrate at boundaries. Don't write new code in the style of the legacy code.

**Impatience.** It took years to create the mess. Cleaning takes time too. But the snowball effect means progress accelerates.

**Giving up.** The early improvements feel small. Keep going. Month after month, they compound.

---

## Related Skills

- **/tdd** — Write new features test-first in clean modules
- **/refactor-suggestion** — Identify specific code smells and refactoring techniques
- **/solid** — Apply SOLID principles to new code and incremental improvements
- **/architecture** — Design clean module boundaries for new features
- **/professional** — Professional responsibility to never check code in worse
