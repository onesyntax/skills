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

# Agile Software Development Workflow

This workflow guides AI agents through evaluating and improving Agile software development practices using Uncle Bob's teachings from the Clean Code series (Episodes 46-52). Follow this workflow when discussing Agile methodology, assessing team practices, or when professional Agile expectations are relevant.

## Workflow Steps

### Step 1: Assess Current Agile Practices
- Identify which Agile practices are in place and which are missing
- Determine if the team is practicing "real" Agile or ceremony-only Agile
- Look for signs of Flaccid Scrum (ceremonies without technical disciplines)

### Step 2: Evaluate Technical Practices
- Is TDD being practiced for all new code?
- Is continuous integration in place with automated tests?
- Is refactoring happening regularly (not deferred)?
- Is pair programming or code review practiced?
- Is simple design a guiding principle?

### Step 3: Check Definition of Done Rigor
- Does "done" mean truly done -- tested, integrated, deployable?
- Are stories counted as done before QA verification?
- Is the Definition of Done written down and enforced?
- Would QA find nothing (or close to it) when reviewing completed stories?

### Step 4: Verify Estimation and Planning Discipline
- Are estimates honest ranges, not single-point commitments?
- Is velocity measured honestly using only truly done stories?
- Is yesterday's weather used for iteration planning?
- Are planning meetings short and focused on prioritization?

### Step 5: Apply Professional Standards
- Are professional expectations being met (quality, readiness, adaptability)?
- Is technical debt being tracked and addressed?
- Is the system deployable at any time?
- Is productivity stable or improving, not declining?

### Step 6: Identify Where Agile Has Gone Wrong
- Has project management taken over from technical leadership?
- Have technical practices been abandoned in favor of ceremonies?
- Is velocity being gamed or inflated?
- Are large-scale frameworks adding bureaucracy without value?

---

## Core Philosophy

### What Agile Really Is

Agile was born at Snowbird, Utah in February 2001 when 17 software practitioners created the Agile Manifesto. It was NOT about project management -- it was about technical excellence and professional discipline. The signatories were programmers and technical leaders, not project managers.

> "Agile is a set of disciplines, a way of thinking about software development. It is not a process. It is not a methodology."

Uncle Bob's key insight: Agile has been largely taken over by project management, losing its technical soul. The ceremonies (standups, sprints, retrospectives) are the LEAST important parts. The technical practices (TDD, refactoring, simple design, pair programming) are what actually make Agile work.

The Agile Manifesto was never intended to be a project management framework. It was a statement of values by technical practitioners who had discovered that certain disciplines produced better software. When project managers adopted Agile, they kept the parts they understood (ceremonies, roles, artifacts) and dropped the parts they did not (TDD, refactoring, continuous integration, simple design).

### The Iron Triangle (Scope, Schedule, Resources)

The fundamental constraint of all projects:

```
        Scope
       /     \
      /       \
     /  Pick   \
    /   Two     \
   /             \
  Schedule --- Resources
```

- You CANNOT fix all three variables
- Something must be flexible
- Agile makes SCOPE the flexible variable
- Fixed iterations with variable scope is the core Agile mechanism
- Management often tries to fix all three, which is a recipe for failure
- When scope is flexible, teams can deliver the highest-value work within fixed time and budget

### The Agile Manifesto Values (Applied)

The four values, properly understood through Uncle Bob's lens:

**Individuals and Interactions over Processes and Tools**
- The technical practices matter more than the ceremonies
- A talented team with discipline will outperform a mediocre team with perfect process
- Tools serve people, not the other way around
- Standups, retrospectives, and planning meetings are tools -- not the point

**Working Software over Comprehensive Documentation**
- Tested, deployed software is the measure of progress
- Working means WORKING -- tested, integrated, deployable
- Documentation that nobody reads is waste
- Tests are the best low-level documentation

**Customer Collaboration over Contract Negotiation**
- Acceptance tests are the collaboration artifact
- The customer defines what "done" means through acceptance criteria
- Negotiating scope within iterations replaces contract renegotiation
- The Planning Game is the collaboration mechanism

**Responding to Change over Following a Plan**
- Variable scope within fixed iterations is how you respond to change
- Clean code and simple design make change inexpensive
- SOLID principles keep designs isolated so changes don't cascade
- The architecture must accommodate change without undue turmoil

---

## How Agile Goes Wrong

Uncle Bob's diagnosis of how Agile has been corrupted:

### 1. Certification Programs

Scrum Master certifications that can be earned in two days create the illusion of competence. A two-day course teaches ceremonies and vocabulary, not the deep technical discipline that makes Agile work.

> "You cannot learn Agile in two days."

The certification industry has produced thousands of "Scrum Masters" who understand the ceremonies but not the engineering practices. They can facilitate a standup but cannot explain why TDD matters. They can run a retrospective but cannot identify technical debt.

### 2. Project Management Takeover

Agile was created by technical people. When project managers adopted it, they kept the ceremonies and dropped the technical practices. The result: Scrum without engineering discipline.

Project managers understood iterations, velocity charts, and burndown reports. They did not understand TDD, refactoring, or continuous integration. So they kept what they understood and discarded what they did not. This is like keeping the dashboard of a car and discarding the engine.

### 3. Flaccid Scrum

A term coined by Martin Fowler. Scrum practiced without technical practices -- no TDD, no refactoring, no continuous integration -- is empty ceremony. Velocity looks good initially but collapses as technical debt accumulates.

**The Pattern of Flaccid Scrum:**
1. Early iterations show high velocity (easy features, no debt yet)
2. Team counts partially-done stories to maintain velocity numbers
3. Technical debt accumulates silently
4. Velocity begins to decline as debt creates drag
5. Management pressure increases to maintain velocity
6. Quality corners are cut further
7. System becomes progressively harder to change
8. Productivity collapses

### 4. Large-Scale Agile Frameworks

SAFe, LeSS, Nexus, and similar frameworks attempt to scale Agile to large organizations. Uncle Bob is blunt about this:

> "Agile is not a technique for large teams. It never was and it never will be. Agile is a technique for small teams."

You build large systems the way we have always built large things:

> "The way we've always built big things -- by building lots of small things."

Large-scale frameworks add layers of ceremony, coordination meetings, and management overhead that contradict the simplicity Agile was designed to provide. They turn Agile into exactly the kind of heavyweight process Agile was created to escape.

### 5. Abandoning Technical Practices

Teams drop TDD because it "slows them down." They skip refactoring because there's "no time." They avoid pair programming because it "wastes resources." These are exactly the practices that make Agile sustainable.

Without TDD, you have no safety net for refactoring. Without refactoring, code degrades. Without clean code, velocity declines. Without velocity, deadlines are missed. Without meeting deadlines, pressure increases. Without relief from pressure, more corners are cut. The death spiral accelerates.

---

## The Planning Game

How estimation and planning should work in Agile:

### Story Estimation

- Stories are estimated using relative sizing (story points)
- Estimates are "gut feel" -- NOT precise commitments
- The law of large numbers: individual inaccuracies average out over many stories
- Relative sizing is more reliable than absolute time estimates
- Compare stories to each other: "Is this bigger or smaller than that?"
- Planning Poker or similar techniques create consensus quickly

### Velocity

Velocity is the MOST IMPORTANT metric in Agile. It is the number of story points actually completed per iteration.

- It must be HONEST -- only count truly DONE stories
- Inflate velocity and you destroy your ability to plan
- Management pressure to increase velocity is destructive
- Velocity should stabilize after a few iterations
- Declining velocity is a signal that technical debt is accumulating

> "The only way to go fast is to go well."

**Velocity Rules:**
1. Only count stories that meet the full Definition of Done
2. Never count partially-completed stories
3. Never inflate point estimates to make velocity look better
4. Use velocity for planning, not for performance evaluation
5. Track velocity over time to spot trends

**Yesterday's Weather:**
The best predictor of next iteration's velocity is last iteration's velocity. Use the average of the last 3-5 iterations for planning. Do not use best-case velocity. Do not use management-desired velocity. Use ACTUAL velocity.

### Planning Meetings

- Should be SHORT -- focus on prioritization and rough sizing
- Product owner presents highest-priority stories
- Team estimates stories relative to each other
- Team commits to what they believe they can complete
- Detailed acceptance criteria written "just in time" when story is picked up
- Do not plan more than one iteration ahead in detail
- Keep a rough roadmap, but accept that it will change

---

## Definition of Done

A story is DONE when ALL of the following are true:

1. All acceptance tests pass
2. All unit tests pass
3. Code has been reviewed (pair programming or code review)
4. Code meets coding standards (clean code principles)
5. Code has been integrated into the main branch
6. No known defects remain
7. System is deployable with this change included

> "Done means done. Not sort-of done. Not almost done. DONE."

### Why Definition of Done Matters

- Demonstrated but not QA'd work corrupts velocity
- "Almost done" stories that carry over create planning uncertainty
- Undone work accumulates as hidden technical debt
- If QA routinely finds defects, the Definition of Done is too loose
- Every story that passes through "done" without truly being done is a lie told to the planning process

### Common Definition of Done Failures

- "Done" means code is written but not tested
- "Done" means it works on the developer's machine but is not integrated
- "Done" means it passes developer testing but not QA
- "Done" means it is demonstrated but not deployable
- Each of these corrupts velocity and destroys planning reliability

---

## Continuous Integration

### The Discipline

- Integrate frequently -- at LEAST daily, preferably continuously
- The build must NEVER be broken
- If the build breaks, fixing it is the TOP PRIORITY for the team
- Automated build and test pipeline is non-negotiable
- Every commit triggers a full build and test cycle

> "If you can't build and deploy at any time, you're not doing CI."

### What CI Requires

1. **Automated Build**: One command or trigger builds the entire system
2. **Automated Tests**: Unit tests, integration tests run on every build
3. **Fast Feedback**: Developers know within minutes if they broke something
4. **Main Branch Always Green**: The build is always in a deployable state
5. **Frequent Commits**: Small, frequent integrations reduce merge conflicts

### CI and the Green Button

> "If you have a button that when you push it, everything goes green -- you'd never stop pushing it."

The goal is to have a system where deploying is so safe and routine that you would be comfortable doing it at any time. This requires:
- Comprehensive automated test coverage
- TDD as a standard practice
- Clean, well-structured code
- Automated deployment pipeline

---

## Iteration Structure

### Fixed-Length Iterations

- 1-2 weeks is typical (Uncle Bob favors shorter iterations)
- Each iteration produces shippable software
- The iteration length is fixed -- scope varies to fit
- Consistency enables reliable velocity measurement

### Iteration Rhythm

**Iteration Planning (beginning of iteration):**
- Select stories from the backlog based on priority
- Estimate stories the team has not yet estimated
- Team commits to stories they believe they can complete
- Commitment is based on yesterday's weather (past velocity)

**Daily Standup (every day):**
- Brief synchronization -- not a status report
- Three questions: What did I do? What will I do? What is blocking me?
- Should take 5-15 minutes, not more
- Standing up keeps it short
- Not a problem-solving meeting -- take issues offline

**Development (throughout iteration):**
- TDD for all new code
- Continuous integration
- Pair programming or code review
- Refactoring as part of every task
- Acceptance test writing alongside development

**Iteration Demo (end of iteration):**
- Show working software to stakeholders
- Only demonstrate truly DONE stories
- Collect feedback for future iterations
- This is the primary measure of progress

**Retrospective (end of iteration):**
- Inspect and adapt the process
- What went well? What could improve?
- Identify one or two concrete improvements for next iteration
- Keep it short and actionable

---

## Expecting Professionalism

Uncle Bob frames Agile as a set of professional EXPECTATIONS that customers and managers have every right to demand of software teams:

### 1. We Will Not Ship Defective Products

> "QA should find nothing. That should be the goal."

- Customers expect extreme quality
- Bug tracking systems are an ADMISSION that defects are too numerous to track manually
- Professional goal: the bug count should be LOW ENOUGH to track on a sticky note
- QA should find NOTHING -- that should be the goal every iteration
- If QA routinely finds defects, the development process is broken

> "Do you use a bug reporting system? Explain to your users why the number of defects is so large it requires an automated system."

### 2. Continuous Technical Readiness

The system should be deployable at any time. Not "after the hardening sprint." Not "after the stabilization phase." At ANY time.

> "If you have a button... that makes everything green... you'd never stop pushing it."

- TDD provides the suite of tests you trust with your life
- Continuous integration keeps the system in a deployable state
- No "code freeze" periods should be necessary
- No "hardening sprints" should be needed

### 3. Stable Productivity

Customers expect that adding features does not get progressively more expensive. The cost of the 100th feature should be similar to the cost of the 10th feature.

- The mess creates quicksand -- more programmers producing less code per person
- Clean code is the ONLY way to maintain velocity over time
- Productivity should remain stable or improve, never decline
- If each iteration delivers less than the previous one, something is wrong
- That something is almost always technical debt

### 4. Inexpensive Adaptability

Customers have the right to change requirements without paying through the nose. That is the entire point of the word "soft" in software.

- Simple designs are the easiest to change
- SOLID principles keep designs simple and isolated
- The architecture must accommodate changes without undue turmoil
- If changing a requirement requires modifying dozens of files, the design has failed
- Agile without clean code makes change increasingly expensive

### 5. Continuous Improvement

Software systems should get BETTER over time, not worse. This is a professional expectation, not a nice-to-have.

- Boy Scout Rule: always leave code cleaner than you found it
- Refactoring is the primary mechanism for continuous improvement
- TDD enables fearless refactoring
- Each iteration should leave the codebase in better shape than the previous one
- Technical debt should decrease over time, not increase

### 6. Fearless Competence

The opposite of "fearful incompetence" -- being afraid to clean messy code because you might break it.

> "Fearful incompetence: you see the mess, you should clean it, but you're not touching it."

**With a trusted test suite:**
- See mess, clean it, run tests, green, move on
- Confidence to make changes
- Code gets better with every touch

**Without tests:**
- See mess, avoid it
- Code rots further
- Everyone slows down
- Fear breeds more fear

### 7. We Will Not Dump On QA

QA should find nothing. Professionals do not knowingly ship defects to QA and hope they catch them.

- Manual testing creates a bottleneck; automate everything possible
- QA's role shifts from "finding bugs" to exploratory testing and writing acceptance criteria
- Developers take ownership of quality -- QA is a safety net, not the primary quality mechanism
- If QA routinely finds defects, the development team has failed

### 8. Honest Estimates

- Never promise what you cannot deliver
- Use ranges, not point estimates
- Say "I don't know" when you don't know
- Saying NO is sometimes the most professional thing to do
- Estimates are not commitments -- they are probability distributions
- Management deserves honest forecasts, not comfortable lies

### 9. Automation Over Manual Process

- Automate everything that can be automated
- Manual processes are error-prone and expensive
- Build, test, and deploy should all be automated
- Manual regression testing does not scale
- If a human has to do it every iteration, automate it

### 10. Cover For Each Other

- Teams should be able to continue if any member is unavailable
- No single points of knowledge failure
- Share code ownership -- no one "owns" a module exclusively
- Share knowledge through pair programming, code review, and documentation
- If only one person understands a critical system, the team has a bus-factor problem

---

## Anti-Patterns

### 1. Flaccid Scrum
Ceremonies without technical practices. Standups and sprints without TDD, refactoring, or CI. The most common corruption of Agile.

### 2. Velocity Gaming
Inflating story points, counting undone stories as done, or adjusting estimates after the fact to make velocity numbers look better. Destroys planning reliability.

### 3. Certification Worship
Believing that a two-day certification course makes someone qualified to lead Agile adoption. Confuses vocabulary with understanding.

### 4. Project Management Takeover
Keeping ceremonies and roles while dropping engineering practices. The technical soul of Agile is replaced with management theater.

### 5. SAFe and Large-Scale Frameworks
Attempting to scale Agile through bureaucracy. Adding layers of coordination, Program Increment planning, and management roles contradicts Agile simplicity. Build big things from lots of small things.

### 6. Abandoning TDD
Dropping TDD because it "slows development down." This is the excuse that guarantees you will have even less time in the future. Without TDD, refactoring is dangerous, code rots, and velocity collapses.

### 7. Hardening Sprints
If you need a dedicated sprint to fix bugs and stabilize the system, your Definition of Done is broken. Every iteration should produce shippable software. Hardening sprints are an admission that "done" does not mean done.

### 8. Sprint Zero
Extensive upfront planning, architecture, and setup before the first "real" sprint contradicts Agile principles. Start delivering working software from iteration one. Architecture emerges through iterative development, not upfront design.

### 9. Velocity as Performance Metric
Using velocity to compare teams or evaluate individual performance. Velocity is a PLANNING tool, not a performance measure. Using it as a performance metric incentivizes inflation and gaming.

### 10. Standup Theater
Daily standups that become long status reports, problem-solving sessions, or management checkpoints. Standups should be brief team synchronization -- 5-15 minutes maximum, focused on coordination, not control.

---

## Agile Practice Assessment

$ARGUMENTS

---

## Output Format

When assessing Agile practices, present findings as:

```
## Agile Practice Assessment

**Practice:** [What practice is being evaluated]
**Current State:** [How it's currently done]
**Expected State:** [What Uncle Bob would expect]
**Technical Practices:** [TDD, CI, refactoring status]
**Definition of Done:** [How rigorous is it?]
**Velocity Honesty:** [Is velocity inflated?]
**Recommendations:** [Specific improvements]
```

For each identified issue:
```
### Issue: [Description]
**Category:** [ceremony-without-discipline / velocity-gaming / missing-practice / anti-pattern]
**Impact:** [How this affects the team's ability to deliver]
**Root Cause:** [Why this is happening]
**Recommendation:** [Specific corrective action]
**Related Principle:** [Which Agile/Clean Code principle applies]
```

---

## Memorable Quotes

> "Agile is a set of disciplines, not a process or methodology."

> "The only way to go fast is to go well."

> "Done means done. Not sort-of done. Not almost done. DONE."

> "You cannot learn Agile in two days."

> "Agile is not a technique for large teams. It never was and it never will be."

> "The way we've always built big things -- by building lots of small things."

> "If you have a button... that makes everything green... you'd never stop pushing it."

> "Fearful incompetence: you see the mess, you should clean it, but you're not touching it."

> "Do you use a bug reporting system? Explain to your users why the number of defects is so large it requires an automated system."

> "We programmers are the ones who actively do the damage."

> "QA should find nothing. That should be the goal."

---

## Common Pitfalls

- **Ceremonies without discipline** -- Doing standups and sprints but skipping TDD and CI
- **Velocity inflation** -- Counting stories as done when they are not truly done
- **Ignoring technical debt** -- Treating refactoring as optional instead of continuous
- **Blaming the process** -- When velocity declines, the problem is almost always code quality, not the process
- **Scaling prematurely** -- Adopting SAFe or similar frameworks before mastering Agile fundamentals with small teams
- **Dropping pair programming** -- Viewing it as "two people doing one job" rather than knowledge sharing and quality improvement
- **Skipping retrospectives** -- Or holding retrospectives that produce no concrete improvements
- **Confusing estimation with commitment** -- Treating estimates as promises and punishing misses

---

## Self-Review (Back Pressure)

After assessing or recommending Agile practices, ALWAYS perform this self-review:

### Self-Review Steps

1. **Technical Practice Check**: Are TDD, CI, and refactoring in place? If not, this is the most critical gap to address. No amount of ceremony can compensate for missing technical discipline.

2. **Definition of Done Check**: Is "done" truly done? If stories are counted as done before they meet all criteria, velocity is a lie and planning is impossible.

3. **Velocity Check**: Is velocity honest and sustainable? If velocity is inflated, declining, or unstable, identify the root cause (usually technical debt or dishonest Definition of Done).

4. **Quality Check**: Would QA find nothing? If QA routinely finds defects, the development process needs improvement, not more QA resources.

5. **Professionalism Check**: Are the team meeting the professional expectations outlined in this document? Continuous readiness, stable productivity, inexpensive adaptability, fearless competence?

### If Violations Found
- Prioritize technical practices over ceremonies
- Address Definition of Done before velocity
- Fix quality at the source, not through more testing
- Re-run self-review after corrections

### Mandatory Quality Gate

Agile practice assessment is NOT complete until:
- [ ] TDD practiced for all new code
- [ ] Continuous integration with automated tests
- [ ] Definition of Done is rigorous and honest
- [ ] Velocity is not inflated
- [ ] Code gets cleaner over time (Boy Scout Rule)
- [ ] QA finds nothing (or close to it)
- [ ] System is deployable at any time

---

## Related Skills

Agile development integrates deeply with all Clean Code practices:

- **/tdd** - The technical practice that enables fearless competence and honest velocity
- **/professional** - Professional expectations that Agile demands of every team member
- **/architecture** - Clean Architecture enables inexpensive adaptability and continuous readiness
- **/solid** - SOLID principles keep designs simple, isolated, and changeable
- **/components** - Component design principles for independent deployability
- **/naming** - Clear naming supports simple design and code quality
- **/functions** - Small, focused functions support refactoring and continuous improvement
- **/patterns** - Design patterns applied during refactoring phases
- **/legacy-code** - Boy Scout Rule for improving existing code incrementally
- **/clean-code-review** - Quality verification before marking stories as done
