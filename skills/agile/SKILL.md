---
name: agile
description: >-
  Guide Agile software development practices using Uncle Bob's teachings from the Clean
  Code series. Activates when discussing Agile methodology, iteration planning, velocity,
  estimation, continuous integration, or when the user mentions Agile, Scrum, XP, iteration,
  sprint, velocity, planning game, Definition of Done, or professional expectations.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: [process or practice to analyze]
---

# Agile Software Development

Agile practices through Uncle Bob's lens — technical excellence first, ceremonies second. Agile was created by programmers, not project managers, and its soul lives in engineering discipline.

For detailed case studies and assessment walkthroughs, read `references/extended-examples.md`.

---

## What Agile Really Is

Agile was born at Snowbird, Utah in February 2001 when 17 software practitioners — programmers and technical leaders, not project managers — created the Agile Manifesto. It was a statement of values by people who had discovered that certain disciplines produced better software.

The technical practices (TDD, refactoring, simple design, pair programming, continuous integration) are what actually make Agile work. The ceremonies (standups, sprints, retrospectives) are coordination tools — useful, but not the point.

### The Agile Manifesto Values (Applied)

**Individuals and Interactions over Processes and Tools.** The technical practices matter more than the ceremonies. A disciplined team with minimal process outperforms a mediocre team with perfect ceremony. Tools serve people, not the reverse.

**Working Software over Comprehensive Documentation.** Tested, integrated, deployable software is the measure of progress. Not "demonstrated." Not "mostly works." Deployed and running. Tests are the best low-level documentation.

**Customer Collaboration over Contract Negotiation.** Acceptance tests are the collaboration artifact. The customer defines "done" through acceptance criteria. The Planning Game is the collaboration mechanism — negotiating scope within iterations replaces contract renegotiation.

**Responding to Change over Following a Plan.** Variable scope within fixed iterations is how you respond to change. Clean code and SOLID principles make change inexpensive. If changing a requirement requires modifying dozens of files, the design has failed — and Agile without clean code makes change increasingly expensive.

### The Iron Triangle

```
        Scope
       /     \
      /       \
     /  Pick   \
    /   Two     \
   /             \
  Schedule --- Resources
```

You cannot fix all three. Agile makes SCOPE the flexible variable — fixed iterations with variable scope. Management often tries to fix all three, which guarantees failure.

---

## The Planning Game

### Story Estimation

Stories are estimated using relative sizing (story points) — gut-feel comparisons, not precise commitments. "Is this bigger or smaller than that?" The law of large numbers means individual inaccuracies average out over many stories. Relative sizing is more reliable than absolute time estimates.

### Velocity

Velocity is the number of story points actually completed per iteration. It is the most important Agile metric — and the most commonly corrupted.

**The rules are non-negotiable:**
- Only count stories that meet the FULL Definition of Done
- Never count partially-completed stories
- Never inflate point estimates to look better
- Use velocity for PLANNING, never for performance evaluation
- Track trends — declining velocity signals accumulating technical debt

**Yesterday's Weather:** The best predictor of next iteration's velocity is last iteration's velocity. Use the average of the last 3-5 iterations. Not best-case. Not management-desired. ACTUAL.

### Planning Meetings

Keep them short — focus on prioritization and rough sizing. Product owner presents highest-priority stories, team estimates relative to each other, team commits to what they believe they can complete based on yesterday's weather. Write detailed acceptance criteria just-in-time when a story is picked up. Do not plan more than one iteration ahead in detail.

---

## Definition of Done

A story is DONE when ALL of the following are true:

1. All acceptance tests pass
2. All unit tests pass
3. Code has been reviewed (pair programming or code review)
4. Code meets clean code standards
5. Code has been integrated into the main branch
6. No known defects remain
7. System is deployable with this change included

"Done" means done. Not sort-of done. Not almost done. Not "works on my machine." Every story that passes through "done" without truly being done is a lie told to the planning process — it corrupts velocity, creates hidden debt, and destroys planning reliability.

**Common failures:** "Done" means written but not tested. "Done" means works locally but not integrated. "Done" means demonstrated but not deployable. Each corrupts velocity and makes future planning impossible.

---

## Continuous Integration

Integrate frequently — at LEAST daily, preferably continuously. The build must never be broken. If it breaks, fixing it is the team's top priority.

**What CI requires:**
- Automated build: one command builds the entire system
- Automated tests: unit and integration tests run on every commit
- Fast feedback: developers know within minutes if something broke
- Main branch always green: the system is always deployable
- Frequent commits: small, frequent integrations reduce merge conflicts

The goal: deploying is so safe and routine that you would do it at any time. This requires comprehensive test coverage, TDD as standard practice, and an automated deployment pipeline. No "hardening sprints." No "code freeze." If you need those, your Definition of Done is broken.

---

## Iteration Structure

### Fixed-Length Iterations

1-2 weeks is typical (shorter is better). Each iteration produces shippable software. The iteration length is fixed — scope varies to fit. Consistency enables reliable velocity measurement.

### Iteration Rhythm

**Planning (start):** Select stories from backlog by priority, estimate unestimated stories, team commits based on yesterday's weather.

**Daily Standup:** Brief synchronization — not a status report. What did I do? What will I do? What's blocking me? 5-15 minutes maximum. Take problem-solving offline.

**Development (throughout):** TDD for all new code, continuous integration, pair programming or code review, refactoring as part of every task, acceptance tests alongside development.

**Demo (end):** Show working software to stakeholders. Only demonstrate truly done stories. Collect feedback for future iterations.

**Retrospective (end):** Inspect and adapt. What went well? What could improve? Identify one or two concrete, actionable improvements. Not a blame session.

---

## Professional Expectations

Agile frames these as expectations that customers and managers have every right to demand:

### Quality

QA should find nothing. That should be the goal every iteration. Bug tracking systems are an admission that defects are too numerous to track manually. The professional goal: a bug count low enough to track on a sticky note.

### Continuous Readiness

The system should be deployable at any time. Not after the hardening sprint. Not after the stabilization phase. At any time. TDD provides the test suite. CI keeps the system deployable.

### Stable Productivity

Adding features should not get progressively more expensive. The cost of the 100th feature should be similar to the 10th. If each iteration delivers less, something is wrong — almost always technical debt. Clean code is the only way to maintain velocity over time.

### Inexpensive Adaptability

Customers have the right to change requirements without paying through the nose. That is the entire point of "soft" in software. Simple designs and SOLID principles keep changes local. If a requirement change cascades through dozens of files, the design has failed.

### Fearless Competence

With a trusted test suite: see mess, clean it, run tests, green, move on. Code gets better with every touch. Without tests: see mess, avoid it, code rots, everyone slows down, fear breeds more fear. TDD is what separates fearless competence from fearful incompetence.

### Honest Estimates

Never promise what you cannot deliver. Use ranges, not point estimates. Say "I don't know" when you don't know. Estimates are probability distributions, not commitments. Management deserves honest forecasts, not comfortable lies.

### Cover for Each Other

No single points of knowledge failure. Share code ownership — no one "owns" a module exclusively. If only one person understands a critical system, the team has a bus-factor problem. Pair programming, code review, and knowledge sharing are professional responsibilities.

---

## How Agile Goes Wrong

### Flaccid Scrum

The most common corruption. Ceremonies without technical practices — standups and sprints without TDD, refactoring, or CI. The pattern is predictable: early iterations show high velocity (easy features, no debt), team counts partially-done stories to maintain numbers, debt accumulates silently, velocity begins to decline, management pressure increases, quality corners are cut further, system becomes progressively harder to change, productivity collapses.

### Project Management Takeover

Agile was created by technical people. When project managers adopted it, they kept the ceremonies and dropped the engineering practices. They understood iterations and burndown charts but not TDD or refactoring. Keeping the dashboard and discarding the engine.

### Certification Illusion

Two-day certification courses create the illusion of competence. They teach ceremonies and vocabulary, not the deep technical discipline that makes Agile work. Thousands of "Scrum Masters" can facilitate a standup but cannot explain why TDD matters.

### Velocity Gaming

Inflating story points, counting undone stories, adjusting estimates after the fact — all to make velocity numbers look better. Every instance destroys planning reliability. When velocity is a lie, planning is impossible.

### Scaling Through Bureaucracy

Large-scale frameworks (SAFe, LeSS, etc.) attempt to scale Agile through layers of coordination meetings and management overhead. Agile was designed for small teams. You build large systems the way we have always built large things — by building lots of small things with small teams.

### Abandoning Technical Practices

Teams drop TDD because it "slows them down." They skip refactoring because there's "no time." These are the practices that make Agile sustainable. Without TDD, no safety net for refactoring. Without refactoring, code degrades. Without clean code, velocity collapses. The death spiral accelerates.

### Anti-Pattern Ceremonies

**Hardening Sprints:** If you need a sprint to fix bugs and stabilize, your Definition of Done is broken. Every iteration should produce shippable software.

**Sprint Zero:** Extensive upfront planning before the first "real" sprint. Start delivering from iteration one. Architecture emerges iteratively.

**Standup Theater:** Daily standups that become long status reports or management checkpoints instead of brief team synchronization.

---

## Related Skills

- **/tdd** — Enables fearless competence and honest velocity
- **/professional** — Professional expectations Agile demands
- **/architecture** — Enables inexpensive adaptability
- **/solid** — Keeps designs simple and changeable
- **/components** — Independent deployability
- **/acceptance-testing** — Collaboration artifact with customers
- **/clean-code-review** — Quality verification before marking done
- **/legacy-code** — Boy Scout Rule for continuous improvement
