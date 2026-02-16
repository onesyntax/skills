---
name: agile
description: >-
  Guide Agile software development practices using Uncle Bob's teachings from the Clean
  Code series. Operational procedure for assessing team maturity, diagnosing Agile health,
  and fixing common anti-patterns. Activates when discussing Agile methodology, iteration planning,
  velocity, estimation, continuous integration, Definition of Done, or when user mentions Scrum,
  XP, sprint, velocity, planning game, or professional expectations.
model: opus
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
delegates-to:
  - tdd                 # technical practices foundation
  - professional        # professional expectations
  - acceptance-testing  # collaboration artifact
  - clean-code-review   # quality verification
argument-hint: [team context or practice to assess]
---

# Agile Skill — Operational Procedure

Core principle: **Technical practices first, ceremonies second.** Agile was created by programmers, not project managers. Its soul lives in engineering discipline — TDD, CI, refactoring. Without these, all ceremonies are theater.

---

## Step 0: Detect Context

Before assessing or recommending, detect the team's current state:

### Methodology
- **Current framework:** Scrum, Kanban, XP, Lean, hybrid, or ad-hoc?
- **Iteration length:** If using iterations, how long? (1 week, 2 weeks, continuous flow?)
- **Cadence:** Do ceremonies happen on a predictable schedule?

### Technical Practices
- **TDD:** Are developers writing tests before code? What percentage of code has unit test coverage?
- **CI/CD:** Is the build automated? Do developers commit at least daily? Is the main branch always deployable?
- **Code review:** Pair programming, pull request review, or no review?
- **Refactoring:** Is refactoring part of every task, or deferred to "tech debt sprints"?
- **Deployment:** How often does code reach production? (hourly, daily, weekly, quarterly?)

### Iteration Health
- **Velocity tracking:** Is velocity measured? Is it stable or declining?
- **Velocity gaming:** Are estimates inflated? Are partially-done stories counted as complete?
- **Definition of Done:** Does the team have a written Definition of Done? Is it enforced?
- **Cycle time:** How long from "in progress" to "done"? (Hours, days, weeks?)

### Ceremonies
- **Planning:** How long do planning meetings take? Is scope negotiated or predetermined?
- **Standup:** 5-15 minutes or 30+ minutes? Status reports or problem-solving?
- **Demo:** Only truly done stories shown, or half-finished work?
- **Retrospective:** Are action items identified? Are they followed up in next iteration?

### Pain Points
- **What is the team complaining about?**
  - Velocity declining?
  - Unpredictable releases?
  - Too many bugs in production?
  - Changes are risky and slow?
  - Can't hire or retain developers?
  - Manager pressure to do more with less?

---

## Step 1: Diagnose Agile Health

Rate each category. Use the assessment to identify root causes, not to shame the team.

### Technical Practices Assessment

| Practice | Status | Evidence (PHP/TypeScript) | Severity if Missing |
|----------|--------|----------|-------------------|
| Unit tests exist | ☐ Yes ☐ No ☐ Partial | `tests/` directories populated (PHP), `*.test.ts` files exist (TypeScript), >50% coverage | 🔴 Critical |
| TDD as workflow | ☐ Yes ☐ No ☐ Partial | Developers write tests before code; use `./vendor/bin/phpunit` / `npm test` in dev loop | 🔴 Critical |
| CI/CD automated | ☐ Yes ☐ No ☐ Partial | GitHub Actions/pipeline runs `./vendor/bin/phpunit` and `npm run build` on every commit | 🔴 Critical |
| Main branch stable | ☐ Yes ☐ No ☐ Partial | Failed test or build blocks merges; fixed within hours | 🟡 High |
| Code review mandatory | ☐ Yes ☐ No ☐ Partial | Every commit reviewed before merge (pair or PR) | 🟡 High |
| Refactoring continuous | ☐ Yes ☐ No ☐ Partial | Refactoring happens as part of tasks; tests enable safe changes | 🟡 High |
| Daily commits | ☐ Yes ☐ No ☐ Partial | Developers integrate at least once per day | 🟢 Medium |

**RED flags (all critical):**
- No automated tests
- No CI/CD pipeline
- Build breaks are tolerated for days
- Code review is skipped under "time pressure"

### Ceremony Quality Assessment

| Ceremony | Status | Questions |
|----------|--------|-----------|
| Planning | ☐ Valuable ☐ Theater ☐ None | Do stories have clear acceptance criteria? Is scope negotiable? Does team commit based on velocity? |
| Standup | ☐ Valuable ☐ Theater ☐ None | Blocked immediately surfaced and solved? Or is it a status report? |
| Demo | ☐ Valuable ☐ Theater ☐ None | Only done stories shown? Do stakeholders give feedback? |
| Retro | ☐ Valuable ☐ Theater ☐ None | Action items identified and tracked? Changes made next iteration? |

### Velocity Integrity Assessment

| Question | Status |
|----------|--------|
| Is velocity measured consistently? | ☐ Yes ☐ No ☐ Inconsistent |
| Are only truly done stories counted? | ☐ Yes ☐ No ☐ Sometimes |
| Is velocity stable or trending? | ☐ Stable ☐ Declining ☐ Erratic |
| Are estimates adjusted after completion to look better? | ☐ Never ☐ Rarely ☐ Often |
| Is velocity used for planning only, not evaluation? | ☐ Yes ☐ No |

**RED flag:** Velocity gaming. If estimates are adjusted backward or partial stories are counted, velocity is fiction.

### Definition of Done Assessment

Ask: **"Is a story truly done when all of these are true?"**

1. ☐ All acceptance tests pass (integration tests or service-level tests)
2. ☐ All unit tests pass (PHPUnit for PHP, Jest for TypeScript)
3. ☐ Code has been reviewed (pair programming or PR review)
4. ☐ Code meets clean code standards (readable, no obvious tech debt; passes linting and type checks)
5. ☐ Code integrated into main branch (not sitting in a feature branch)
6. ☐ No known defects (QA found nothing or issues logged for next iteration)
7. ☐ System is deployable (`npm run build` succeeds, type checks pass, tests pass)

**Count:**
- 7/7 = Solid
- 5-6/7 = Gaps exist; find which ones are causing problems
- <5/7 = Definition of Done is broken; velocity is unreliable

---

## Step 2: Apply Decision Rules

### Rule 1: Technical Practices First

**WHEN:** Assessing any Agile process. Ceremonies are useless without engineering discipline.

**WHEN NOT:** Never skip this assessment.

**CHECK:**
1. Does TDD exist? If no, it's the blocker. Inject TDD first (delegate to `/tdd`).
2. Does CI/CD exist? If no, it's the second blocker. Set up automated build and deploy.
3. Is code review happening? If no, establish pair programming or PR reviews.
4. Is refactoring part of the workflow? If no, teach developers refactoring discipline (delegate to `/refactor-suggestion`).

**ACTION:** If technical practices are missing, no Agile framework will work. Start here.

---

### Rule 2: Definition of Done Completeness

**WHEN:** Reviewing any "done" claim. Planning next iteration. Velocity seems suspicious.

**WHEN NOT:** Pure research/spike tasks (those are explicitly "not done" by definition).

**CHECK:** Apply the 7-point checklist above. Each missing point is corruption:
- No tests → Velocity lies
- No review → Defects in production
- Not integrated → Merge conflicts pile up
- Not deployable → Hardening sprint needed (Definition of Done is broken)

**ACTION:**
1. Write the 7-point checklist on a card and post it
2. In retrospective, ask: "Which items do we always skip?"
3. Prioritize fixing the most-skipped item first
4. Enforce it strictly for one full iteration

---

### Rule 3: Velocity Integrity

**WHEN:** Planning next iteration. Investigating why velocity declined. Responding to management pressure.

**WHEN NOT:** First 2-3 iterations (insufficient data). Team composition just changed significantly.

**CHECK:**
1. Are estimates adjusted after completion? If yes, velocity is fiction.
2. Are partially-done stories counted as complete? If yes, velocity is fiction.
3. Is velocity stable or declining? Declining = accumulating technical debt.
4. Is velocity used for performance evaluation? If yes, it's gamed. Use it for planning only.

**CALCULATION (Yesterday's Weather):**
```
next_iteration_velocity = average(last_3_to_5_iterations_actual_velocity)
```
**Not** best-case. **Not** management-desired. **Actual.**

**ACTION:**
1. Count only truly done stories for 3 iterations to establish baseline
2. Refuse to use velocity for performance evaluation
3. If velocity is declining, diagnose technical debt (delegate to `/refactor-suggestion`)

---

### Rule 4: Iteration Scope — Variable Scope, Fixed Time

**WHEN:** Facing scope pressure or deadline pressure. Starting iteration planning.

**WHEN NOT:** Critical deadline with fixed scope (be honest about what won't fit, delegate to `/professional`).

**THE IRON TRIANGLE:**
```
You cannot fix all three:
  Scope — Schedule — Resources
Pick two. Agile picks Scope and Schedule (flexible Scope, fixed Schedule).
```

**DECISION:**
- **Fixed iteration length** (1-2 weeks) ← Never negotiate
- **Variable scope** (stories that fit yesterday's velocity) ← Always negotiate
- **Resources** (team size) ← Adjust if possible, but adding people often slows you down

**ACTION:**
1. If manager says "we need feature X, Y, Z in 2 weeks": calculate velocity, show what fits, ask which features to defer
2. If team says "we can do more": remind them velocity is measured, not promised
3. Never extend iteration length to "fit in" more scope

---

### Rule 5: Estimation — PERT or Reference Comparison

**WHEN:** Estimating any story or task.

**WHEN NOT:** Trivial tasks (<1 hour). Pure research (estimate as "unknown").

**PERT ESTIMATION:**
For each story, provide three points:
- **Best (B):** Everything goes right, 1% chance of being this fast
- **Normal (N):** Realistic expectation, 50% chance
- **Worst (W):** Murphy's Law, 99% chance done by this time

```
Expected = ((B + W) / 2 + N) / 3
Std Dev  = (W - B) / 6
```

**REFERENCE COMPARISON:**
If PERT feels too heavyweight, compare to stories already completed:
- "This is like story #23 (5 points) but with more edge cases, so 8 points"
- Relative sizing is more reliable than absolute estimates

**ACTION:**
1. Show team the PERT formula, let them choose (PERT or reference)
2. Collect estimates from multiple people, discuss outliers
3. Always provide ranges, never single-point estimates to management

---

### Rule 6: Iteration Rhythm — Synchronization, Not Status Reports

**WHEN:** Designing or fixing ceremonies.

**WHEN NOT:** Never skip ceremonies; instead, make them valuable.

**THE RHYTHM:**

| Ceremony | Duration | Purpose | Output |
|----------|----------|---------|--------|
| **Planning** (start) | 30-60 min | Prioritize backlog, estimate unknowns, team commits | Stories with criteria, commitment |
| **Standup** (daily) | 5-15 min | "What will I do? What blocked me?" Solve offline. | Blockers surfaced, problems solved |
| **Development** (all week) | — | TDD, CI, code review, refactoring, acceptance tests | Shippable software |
| **Demo** (end) | 30-45 min | Show DONE stories to stakeholders | Feedback for next iteration |
| **Retro** (end) | 30-45 min | "What went well? What could improve? One action item." | Committed improvements |

**ANTI-PATTERNS:**
- **Standup Theater:** 30-minute status reports → should be 5 minutes
- **Planning Marathon:** 4-hour planning session → should be 1 hour, just-in-time details
- **Demo of Half-Done Work:** → only show truly done stories
- **Retro Without Action:** Complaints but no follow-through → identify ONE concrete change

**ACTION:** If a ceremony takes >budget, it's broken. Fix it in retrospective.

---

### Rule 7: Anti-Pattern Detection & Recovery

**WHEN:** Team shows symptoms. Velocity declining. Bugs increasing. Morale dropping.

**WHEN NOT:** Never use anti-patterns to shame; use them to diagnose.

**IDENTIFY THE ANTI-PATTERN:**

| Anti-Pattern | Symptoms | Fix |
|--------------|----------|-----|
| **Flaccid Scrum** | Ceremonies yes, practices no. Velocity collapses. | Enforce 7-point DoD. Inject TDD. Set up CI/CD. |
| **PM Takeover** | Ceremonies but waterfall planning. Team estimates ignored. | Restore team ownership of pace. Educate on TDD. |
| **Velocity Gaming** | Inflated estimates. Partial stories counted as done. | Count only truly done stories. Never use velocity for evaluation. |
| **Hardening Sprint** | Dev sprint + separate QA sprint. Bugs pile up. | Add "deployable" to DoD. QA in every sprint, not after. |
| **Sprint Zero** | Months of planning before first delivery. | Deliver in iteration one. Architecture emerges iteratively. |
| **Standup Theater** | 30-60 minute status reports. Management attends. | 5-15 minutes. Blockers only. Keep managers out. |
| **Certification Illusion** | Playbook-following without discipline. | Real learning: pair, read Clean Code, do `/tdd` properly. |

---

## Step 3: Review Checklist — Agile Health Scan

**Run this checklist on a team to identify quick wins and critical gaps.**

### Technical Practices (Foundation)
- 🔴 **TDD in place:** Are >50% of stories tested first (PHPUnit or Jest)? Or are tests an afterthought?
- 🔴 **CI/CD automated:** Can you deploy without manual steps? Does `./vendor/bin/phpunit` and `npm run build` run on every commit? Is main always green?
- 🔴 **Code review mandatory:** Does every commit get eyes before merge?
- 🟡 **Refactoring continuous:** Is refactoring part of stories, or deferred?

### Definition of Done (Velocity Reliability)
- 🔴 **All 7 points defined and enforced:** Tests, review, integration, deployment-ready?
- 🔴 **No partial stories counted:** Only fully done stories in velocity calculation?
- 🟡 **No hardening sprints:** Every iteration produces deployable software?

### Velocity (Planning Accuracy)
- 🔴 **Velocity measured honestly:** Inflated estimates? Undone stories? Trend declining?
- 🟡 **Yesterday's Weather used:** Planning based on actual past velocity, not wishes?
- 🟡 **Not used for evaluation:** Velocity a planning tool, not a judgment tool?

### Ceremonies (Value Delivered)
- 🟡 **Planning <1 hour:** Or does it drag on into planning marathons?
- 🟡 **Standup <15 minutes:** Or is it status reports?
- 🟢 **Demo shows only done work:** Or half-finished features?
- 🟢 **Retro has follow-through:** Or are complaints logged and forgotten?

### Professional Expectations (Sustainable Pace)
- 🟢 **Honest estimates:** Or are dates promised without certainty?
- 🟢 **No crunch mode:** Or is overtime normalized?
- 🟢 **Continuous readiness:** Or are releases chaotic?

**Severity:**
- 🔴 **RED:** Blocks everything. Fix first.
- 🟡 **YELLOW:** Limits velocity or quality. Fix in next iteration.
- 🟢 **GREEN:** Nice to have. Improve gradually.

---

## Step 4: Fix Patterns — Refactoring Agile

### Pattern 1: Inject Technical Practices

**When:** No TDD, no CI, or code review missing.

**Order (spend one iteration per step):**
1. **CI/CD first** — Automated build on every commit. `./vendor/bin/phpunit` and `npm run build` in pipeline. Main branch always green.
2. **TDD second** — New code tested first. Retrofit old code with characterization tests. Pair experienced dev with skeptic.
3. **Code review third** — Pair programming or PR review. Every commit reviewed before merge.
4. **Refactoring fourth** — Refactoring part of every story. Tests enable safe changes.

**Action:** Pick one, spend one iteration making it real, measure improvement.

---

### Pattern 2: Fix Definition of Done

**When:** Velocity unreliable, bugs in production, or partial stories getting counted.

**The 7-point checklist:**
```
Done means ALL of these:
1. Acceptance tests pass | 2. Unit tests pass | 3. Code reviewed
4. Clean code standards | 5. Integrated into main | 6. No known defects
7. System deployable
```

**Steps:**
1. Post the checklist visibly (wall, workflow tool)
2. Audit: Which items do teams skip? Which cause most bugs?
3. Enforce for one iteration: Stories don't move to done until all 7 pass
4. In retro: "Which item helped most? Which was hardest?" Adjust, but maintain rigor

**Result:** Velocity becomes reliable. Bugs decrease. Deployment predictable.

---

### Pattern 3: Restore Velocity Integrity

**When:** Velocity is inflated, declining, or gamed.

**Steps:**
1. **Reset 3 iterations:** Count only truly done stories. Expect drop (you're being honest). Ignore old numbers.
2. **Track trend:**
   ```
   Iteration 1: 20 points (honest count, tests passing)
   Iteration 2: 22 points (stabilizing)
   Iteration 3: 21 points (average = 21, use for planning)
   ```
3. **If declining:** Technical debt accumulating. Allocate 20% of capacity to refactoring.
4. **Never use velocity for evaluation:** Removes incentive to game. Planning only.

**Result:** Reliable forecasting tool.

---

### Pattern 4: Convert Ceremonies to Substance

**When:** Standup is 30 minutes, planning is a marathon, retro is complaining.

| Ceremony | Fix |
|----------|-----|
| **Standup** | 5-15 min, hard stop. "What will I do? What's blocking?" Blockers resolved offline. No managers. |
| **Planning** | 30-60 min. Prioritize, estimate, team commits based on yesterday's velocity. Criteria written when picked up. |
| **Demo** | Show only done work. Stakeholder feedback shapes next iteration. |
| **Retro** | Three questions: went well? improve? one concrete change? Track it next iteration. |

---

### Pattern 5: Descale — Return Autonomy to Teams

**When:** Too many layers of coordination. Story can't start without BA meeting. Code can't merge without architectural council. Deployment needs PM sign-off.

**Fix:** Small autonomous teams (5-9) make decisions. Own estimation, DoD, velocity. Commit to iteration, not managers. Managers set constraints (security, compliance), teams figure out how.

**Result:** Faster feedback, faster decisions, higher morale.

---

### Pattern 6: Kill Hardening Sprint

**When:** Dev sprint + separate stabilization sprint. Bugs pile up.

**Fix:**
1. Add "System is deployable" to Definition of Done
2. QA in every sprint, not after
3. Acceptance tests with stories, not in separate phase
4. Deploy from every sprint; if you can't, DoD is broken

**Result:** No hardening sprint. Quality improves because bugs caught earlier.

---

## When NOT to Apply

1. **Fixed scope + deadline + resources.** Agile needs flexibility in one. Be honest (delegate to `/professional`).
2. **Single-person team.** Use simple task board. Still apply TDD, CI.
3. **Non-software.** Hardware, construction don't iterate fast. Borrow mindset, not ceremonies.
4. **Compliance-heavy.** Layer in audit trail and docs. Don't drop Agile.

**Red flags:** No technical discipline (unwilling). Manager treats Agile as faster waterfall. Team burned out (needs rest, not Agile). Organization plays politics (Agile exposes it).

---

## Communication Style

### When Diagnosing
- **Not:** "Your team is doing Scrum wrong"
- **Yes:** "Your Definition of Done is missing integration tests. That's why bugs reach production. Let's fix that."

### When Recommending
- **Not:** "Agile best practice says..."
- **Yes:** "Your velocity is declining because technical debt is slowing you down. Adding TDD and refactoring time will fix it."

### When Pushing Back
- **Not:** "Agile doesn't allow hardening sprints"
- **Yes:** "Every day you spend in hardening is a day you're not delivering value. Let's fix Definition of Done so you don't need hardening."

### To Managers
- **Not:** "Agile requires you to let go"
- **Yes:** "Agile gives you visibility into actual capacity and honest forecasts. You can plan better because we're not lying about velocity."

---

## K-Line History

**TDD:** Reduces defects. Only safe way to refactor.

**CI/CD:** Painless integration. Reduces surprises.

**Definition of Done:** Without it, velocity is fiction. Planning is guessing.

**Velocity (honest):** The only reliable forecast. Gaming destroys it.

**Ceremonies:** Valuable when they surface blockers, not status reports.

**Fixed short iteration:** Enables accurate velocity.

**Autonomous teams:** Better, faster decisions. Fewer coordination layers.

---

## Related Skills

- **/tdd** — Enables fearless competence, honest velocity, and clean code
- **/professional** — Professional expectations Agile demands of developers
- **/acceptance-testing** — Collaboration artifact with customers, ATDD
- **/clean-code-review** — Quality verification before marking done
- **/refactor-suggestion** — Diagnosing and fixing technical debt
- **/legacy-code** — Boy Scout Rule for continuous improvement
- **/solid** — Keeps designs simple and changeable
- **/architecture** — Enables inexpensive adaptability across iterations
