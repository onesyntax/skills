# Agile Software Development — Extended Examples

Detailed case studies and assessment walkthroughs showing Agile principles applied and misapplied.

---

## Example: Diagnosing Flaccid Scrum

### The Situation

A team of 8 developers has been doing "Scrum" for 18 months. They have all the ceremonies — daily standups, two-week sprints, sprint planning, retrospectives, demos. The Scrum Master is certified. The product owner maintains a groomed backlog. Burndown charts are posted on the wall.

But velocity has been declining for the last 6 sprints. Management is alarmed. The team's response: "We need more developers."

### The Assessment

**Ceremonies: Present**
- Daily standup: yes (but takes 30 minutes)
- Sprint planning: yes
- Retrospective: yes (but produces no concrete changes)
- Demo: yes (but includes "almost done" stories)

**Technical Practices: Absent**
- TDD: No. "We write tests after, when there's time." (There's never time.)
- Continuous integration: Partial. Build runs nightly, not on every commit. Build has been red for 3 days — nobody is alarmed.
- Refactoring: No. "We don't have time to refactor." Code quality has visibly degraded.
- Pair programming: No. "That's wasting two people on one task."
- Code review: Sporadic. Reviews are rubber-stamped because reviewers are overloaded.

**Definition of Done: Weak**
- "Done" means developer says it works on their machine
- No acceptance tests — stories are manually tested by the developer
- QA finds 15-25 defects per sprint
- Stories are counted as done before QA finishes

**Velocity: Dishonest**
- Team counts stories as done when they demo, not when QA signs off
- 30% of "done" stories have open defects
- Actual velocity (truly done stories) is about 60% of reported velocity

### The Diagnosis

This is textbook Flaccid Scrum. The team has the skin of Agile (ceremonies, roles, artifacts) without the skeleton (technical practices). The velocity decline is predictable — technical debt accumulated from month one because there was no TDD, no refactoring, and a weak Definition of Done.

### The Prescription

**Phase 1 — Stop the bleeding (Sprint 1-2):**
- Fix the Definition of Done immediately. Nothing counts as done until QA signs off and code is on main branch
- Accept that reported velocity will drop 40% — this is honesty, not failure
- Start CI: build on every commit, broken build is top priority

**Phase 2 — Add the skeleton (Sprint 3-6):**
- Introduce TDD for all new code. Expect a 2-sprint learning curve
- Begin refactoring the worst code modules during each sprint
- Move standups back to 10 minutes — three questions only
- Retrospective must produce exactly one concrete change per sprint

**Phase 3 — Stabilize (Sprint 7-12):**
- Velocity should stabilize at a lower but honest number
- QA defect count should drop below 5 per sprint
- Begin pair programming on complex stories
- Technical debt decreasing visibly each sprint

---

## Example: Velocity Gaming Diagnosis

### The Data

A team reports this velocity over 8 sprints:

```
Sprint 1:  32 points
Sprint 2:  35 points
Sprint 3:  38 points
Sprint 4:  41 points
Sprint 5:  44 points
Sprint 6:  47 points  ← Management sets target: 50
Sprint 7:  52 points  ← "We hit the target!"
Sprint 8:  55 points
```

Management is thrilled — velocity is increasing every sprint. But the system is getting harder to change, bugs are increasing, and developers are working overtime.

### Red Flags

**Steady increase is suspicious.** Real velocity fluctuates. A smooth upward trend almost always indicates gaming, not genuine improvement.

**Point inflation.** Compare Sprint 1 and Sprint 8 stories. A story that would have been 3 points in Sprint 1 is now estimated at 5 points. The work hasn't changed — the numbers have.

**Partial counting.** "80% complete" stories are counted as done. Three stories that were 80% done were counted at full points in Sprint 7. That's 60% of their value counted for 0% deliverable.

**Definition of Done erosion.** Sprint 1's Definition of Done required QA sign-off and integration testing. By Sprint 7, "done" means "developer tested on local machine." The bar dropped to make the numbers work.

### The Real Velocity

Adjusting for inflation and partial counting:

```
Sprint 1:  32 points (honest)
Sprint 2:  33 points (slight inflation started)
Sprint 3:  31 points (adjusted for inflation)
Sprint 4:  29 points (debt beginning to slow work)
Sprint 5:  27 points (more debt)
Sprint 6:  25 points (declining)
Sprint 7:  22 points (significant decline masked by gaming)
Sprint 8:  20 points (the real number)
```

Real velocity has been declining since Sprint 3. The team is producing LESS, not more. Gaming hid the decline for 5 sprints, during which technical debt compounded unchecked.

### The Fix

- Reset point baseline: re-estimate 5 reference stories at original scale
- Enforce original Definition of Done — accept the velocity drop
- Stop using velocity as a performance target
- Track honest velocity for 3 sprints before making any plans
- Address the technical debt that caused the real decline

---

## Example: Assessing a Team's Agile Maturity

### Assessment Framework

Rate each practice on a scale:

**Level 0 — Absent:** Practice is not done at all.
**Level 1 — Attempted:** Practice exists on paper but is not consistently followed.
**Level 2 — Practiced:** Practice is done consistently but without full rigor.
**Level 3 — Disciplined:** Practice is done consistently with full rigor and produces results.

### Sample Assessment

```
Practice                    Level   Notes
─────────────────────────── ─────   ─────────────────────────────
TDD                         0       No tests written first
Unit Testing (after)        2       Tests exist but patchy coverage
Continuous Integration      1       Nightly build, often red
Refactoring                 0       "No time"
Pair Programming            0       "Too expensive"
Code Review                 1       Done but rubber-stamped
Definition of Done          1       Written down but not enforced
Velocity Tracking           2       Tracked but partially inflated
Sprint Planning             3       Well-run, focused meetings
Daily Standup               2       Runs but takes too long (25 min)
Sprint Demo                 2       Done but includes partial work
Retrospective               1       Held but no concrete outcomes
Acceptance Testing          0       No automated acceptance tests
Simple Design               1       Discussed but not enforced
```

### Diagnosis Pattern

This team scores well on ceremonies (planning, standup, demo) and poorly on technical practices (TDD, refactoring, pair programming, acceptance testing). This is the classic Flaccid Scrum pattern — the parts project managers understand are present, the parts programmers drive are absent.

### Priority Order for Improvement

1. **TDD** — This is the foundation. Everything else depends on having a trusted test suite.
2. **Definition of Done enforcement** — Make velocity honest immediately.
3. **CI discipline** — Build on every commit, never tolerate a red build.
4. **Refactoring** — Start small. Boy Scout Rule: leave code cleaner than you found it.
5. **Acceptance testing** — Automate the Definition of Done criteria.
6. **Pair programming** — Start with complex stories only, expand as team sees value.

---

## Example: The Death Spiral in Action

### Month 1-3: The Honeymoon

New project, green field. Team of 6 picks up Scrum. Velocity is 40 points per sprint. Features are easy — minimal complexity, no legacy constraints. Everyone is excited.

Management projects: at 40 points/sprint, we'll finish the 800-point backlog in 20 sprints (40 weeks).

### Month 4-6: The Cracks

Velocity drops to 35. Team explains: "Features are getting more complex." True — but the real cause is accumulating technical debt. No TDD means no refactoring safety net. Code is getting tangled but nobody notices yet.

Management adjusts: 23 sprints. Still acceptable.

### Month 7-9: The Pressure

Velocity drops to 25. Management is concerned. Team is working overtime. Every change seems to break something else. Bug count is rising. QA is overwhelmed.

Management response: "Can we add developers?" Brooks' Law: adding people to a late project makes it later. But they add 2 developers anyway.

### Month 10-12: The Spiral

New developers spend 3 sprints learning the codebase (which has no tests to explain behavior). Velocity drops to 18 during onboarding. Existing developers spend time mentoring instead of coding.

Once new developers are productive, velocity recovers to 22 — but now with 8 developers instead of 6. Per-developer productivity has dropped by 45%.

### Month 13-15: The Crisis

Management adds 4 more developers. 12 people, velocity of 25. Same output as 6 people 9 months ago. Merge conflicts are constant. Communication overhead is enormous. Every change breaks something.

Someone suggests: "We should rewrite it."

### The Alternative Timeline

Same team, same project. But with TDD from day one:

- Month 1-3: Velocity 35 (slightly lower due to TDD learning curve)
- Month 4-6: Velocity 37 (improving as test suite grows)
- Month 7-9: Velocity 38 (refactoring keeps code clean, changes stay local)
- Month 10-12: Velocity 40 (team has confidence, code is maintainable)

No death spiral. No overtime. No emergency hires. The disciplined approach is slower at first and faster forever after.
