---
name: professional
description: >-
  Operational guide for professional software development practices — responsibility, ethics, estimates, saying no, commitments.
  Activates when discussing professional conduct, estimation, commitments, ethics, saying no, or when quality standards and
  professional responsibility are relevant.
model: opus
allowed-tools: Read, Grep, Glob
argument-hint: [situation or code to evaluate]
delegates-to: [tdd, agile, clean-code-review]
---

# Professional Software Development

Operational protocol for professional responsibility in software development. Covers nine core commitments, decision rules for estimation and commitments, quality standards, knowledge ownership, and harm prevention.

---

## Step 0: Detect Context

Classify the professional situation you're evaluating:

- **Estimation request** — Someone asking for time/effort estimates for a task or feature
- **Commitment pressure** — Being asked to promise a delivery date or guarantee an outcome
- **Quality shortcut** — Being asked to skip tests, skip review, rush code to production
- **Ethics concern** — Code or decision that could harm users, society, system stability, or business
- **Code ownership** — Code checked in; responsibility for quality, maintainability, and knowledge sharing
- **Team dynamics** — Knowledge silos, single points of failure, need for coverage or knowledge sharing
- **Pressure situation** — Manager, client, or business pressure to compromise on standards

---

## Step 1: Apply Relevant Professional Standards

Based on detected context from Step 0, apply the decision rules in Step 2. Each context maps to specific standards:

| Context | Primary Standards |
|---------|------------------|
| Estimation request | Honest Estimation, PERT formula, range not point |
| Commitment pressure | Saying No, Honest Estimation, Quality Non-Negotiable |
| Quality shortcut | Quality Non-Negotiable, Do No Harm, Best Work |
| Ethics concern | Do No Harm (function, structure, society), Speak Up |
| Code ownership | Best Work, Knowledge Sharing, Boy Scout Rule |
| Team dynamics | Knowledge Sharing, Speak Up, Team Coverage |
| Pressure situation | Professional No, Quality Shield, Speak Up Protocol |

---

## Step 2: Decision Rules (7 Core Standards)

### Rule 1: Do No Harm
**WHEN:** Any code change, any estimate, any commitment, any decision to ship.
**Apply:** Verify that code does not harm users, customers, system function, system structure, or society. This is non-negotiable. It applies even when requirements are written by others — your fingers are on the keyboard.

**WHEN NOT:** Never skip. There are no contexts where harm is acceptable.

---

### Rule 2: Honest Estimation
**WHEN:** Any estimation request. Someone asks "How long will this take?"
**Apply:** Provide three estimates (PERT): Best Case (B), Normal Case (N), Worst Case (W). Calculate expected time as ((B + W)/2 + N) / 3. Present as a range with confidence, not a single point. Include fudge factor (2x–4x) to account for unknown unknowns.

**WHEN NOT:** Trivial tasks where estimation is not needed (e.g., "copy this line"). Even then, err on the side of transparency.

---

### Rule 3: Saying No
**WHEN:** Asked to commit to something you cannot deliver with confidence. Asked to skip tests, skip review, ship broken code, or make a promise without certainty.
**Apply:** Say no. Explain the constraint. Offer alternatives. Be willing to discuss and hunt for ways to say yes — but don't be afraid to say no. Saying yes to an impossible commitment is lying.

**WHEN NOT:** When you genuinely can commit. When you have confidence in the estimate and delivery date.

---

### Rule 4: Quality Non-Negotiable
**WHEN:** Pressure to cut corners, skip tests, skip review, rush code to production, or ship known defects.
**Apply:** Quality is not negotiable. The cost of discipline (TDD, review, refactoring) is always less than the cost of harm (defects, rework, downtime, loss of trust). Explain this tradeoff clearly.

**WHEN NOT:** Never. Quality is always required.

---

### Rule 5: Best Work
**WHEN:** Every check-in. Every release. Every piece of code goes to production under your name.
**Apply:** Code represents your best work at this moment. Leave code better than you found it (Boy Scout Rule). Remove dead code. Fix quick patches. If a spike or prototype is thrown away, label it clearly as throwaway.

**WHEN NOT:** Throwaway spike code (but mark it explicitly so it doesn't accidentally ship).

---

### Rule 6: Knowledge Sharing
**WHEN:** Code ownership concern, critical system knowledge, risk of single point of failure.
**Apply:** No single points of knowledge failure. Others can cover for you, you can cover for them. Ensure that at least two people understand critical code paths. Document, pair, review, teach.

**WHEN NOT:** Temporary solo work on isolated prototype (but only temporary).

---

### Rule 7: Speak Up
**WHEN:** You see something wrong — deployment risk, security issue, harmful code, quality concern, ethics violation.
**Apply:** Speak up early, constructively, with evidence. Frame concerns as risks to deliver value, not as personal attacks. Escalate if ignored. You were hired because you know how to identify trouble before it happens.

**WHEN NOT:** Stylistic preferences (those go through code review and team discussion, not emergency escalation).

---

## Step 3: Review Checklist — The Programmer's Oath

Check each item. Mark severity: 🔴 (critical — must fix before shipping), 🟡 (warning — address this cycle), 🟢 (opportunity — address when convenient).

1. 🔴 **Harm to users/society** — Does this code do harm? Could it harm anyone? Does it conceal truth or deceive?

2. 🔴 **Undisclosed defects** — Are there known defects being shipped without disclosure? Is quality hiding harm?

3. 🔴 **No proof of correctness** — Is there test coverage (PHPUnit, Jest)? Can you prove this code works as intended? Do the test suites pass?

4. 🔴 **Commitment without confidence** — Was a date promised without real confidence? Does the estimate have evidence behind it (based on past velocity, story pointing)?

5. 🟡 **Code worse than found** — Is code harder to read, change, or understand than before? Did you leave it worse?

6. 🟡 **Point estimate as commitment** — Was an estimate presented as a date? Should it be a range instead?

7. 🟡 **Knowledge silo** — Does only one person understand this code? Is there single-point-of-failure risk?

8. 🟢 **Opportunity missed** — Could this code be made more expressive, more maintainable, more testable?

9. 🟢 **Learning stagnated** — Did you learn something new? Did you grow your craft with this work?

---

## Step 4: Response Patterns (5 Named Responses)

Use these patterns to respond to professional situations:

### Pattern 1: The Honest Estimate

**Situation:** "How long will this take?"

**Response:**
1. Break the work into small tasks
2. For each task, estimate three points: Best (B), Normal (N), Worst (W)
3. Calculate: Expected time = ((B + W)/2 + N) / 3
4. Sum across all tasks
5. Apply fudge factor (multiply by 2–4 for unknown unknowns)
6. Present as a range: "Between X and Y, most likely Z"
7. Communicate the uncertainty level: "High confidence" or "Moderate confidence" or "Low confidence"

**Do NOT:**
- Present a single point as if it's certain
- Reverse-engineer estimates from a known deadline
- Leave out the fudge factor
- Skip communicating uncertainty

---

### Pattern 2: The Professional No

**Situation:** Pressure to commit to something impossible.

**Response:**
1. Acknowledge the request and its business importance
2. Explain why you cannot commit: "I don't have confidence I can deliver by [date] because [specific reason]"
3. Offer alternatives:
   - A later date you can commit to with confidence
   - A reduced scope you can deliver on the requested date
   - A range instead of a point date
4. Propose next steps: "Here's what I can do: [option A] or [option B]"

**Do NOT:**
- Say "yes" to an impossible commitment
- Say "I'll try" (it's a lie — you're already trying)
- Be passive-aggressive (deploy broken code as a protest)
- Apologize for being professional

---

### Pattern 3: The Quality Shield

**Situation:** "Just skip the tests and ship it" or "We need to cut corners to hit the deadline."

**Response:**
1. Acknowledge the deadline pressure and business need
2. Explain the tradeoff clearly with language-specific evidence:
   - "Skipping PHPUnit/Jest tests saves us X hours now"
   - "But defects in production will cost us [hours of rework + downtime + reputation damage + potential harm]"
   - "Our test suite gives us confidence in changes"
3. Show the math: Cost of discipline (running tests) << Cost of harm (production bugs)
4. Offer alternatives to speed delivery:
   - Reduce scope instead of quality (remove features, keep tests)
   - Deploy early and iterate (but PHPUnit/Jest tests must pass on each release)
   - Add resources to work in parallel (larger team can test faster)
   - Run tests in parallel (speed up feedback loop)
5. Make the call clear: "The answer is no to cutting quality. Here's how we deliver on time anyway."

**Do NOT:**
- Compromise on test suite (PHPUnit for PHP, Jest for TypeScript) or proof of correctness
- Frame quality as optional or nice-to-have
- Skip the math on cost of defects
- Skip deployment validation (`npm run build`, type checking)

---

### Pattern 4: The Speak Up Protocol

**Situation:** You see a risk, ethics concern, or quality problem.

**Response:**
1. **Gather evidence** — Get specifics: what could go wrong, what's the impact, what's the risk level
2. **Frame constructively** — "I see a risk to [outcome we care about]: [specific risk]. Here's why it matters: [impact]. I suggest: [alternative approach]"
3. **Escalate appropriately**:
   - First: Tell the person directly (your teammate, code reviewer)
   - Second: Escalate to lead/manager if not addressed
   - Third: Escalate to senior leadership if still not addressed
4. **Document** — If ignored, document your concern (email, ticket comment, meeting notes)
5. **Own the outcome** — You did your part by speaking up. The decision becomes a team decision once escalated.

**Do NOT:**
- Stay silent when you know something is wrong
- Frame concerns as personal attacks
- Escalate stylistic preferences as emergencies
- Give up after one attempt to communicate

---

### Pattern 5: The Boy Scout Commit

**Situation:** Every check-in, every PR, every piece of code.

**Response:**
1. **Before shipping:** Run the quality checklist (Step 3)
2. **Leave code better:**
   - Remove dead code
   - Fix naming issues you see
   - Extract a function if one is too long
   - Add a test for an untested path
3. **Don't accumulate mess:** If you see a quick patch, clean it up now or add a ticket to clean it later (and do it)
4. **Document knowledge:** If you're the only one who understands something, document it or pair with someone
5. **Verify tests pass:** Don't commit failing tests

**Do NOT:**
- Leave code worse than you found it
- Accumulate technical debt by ignoring quick wins
- Create knowledge silos
- Ship code with failures

---

## When NOT to Apply This Skill

This skill is always relevant when:
- Discussing estimation, commitments, deadlines
- Evaluating code quality or professional standards
- Considering whether to ship or deploy
- Facing pressure to compromise on quality or ethics
- Making decisions about code ownership or knowledge sharing

This skill is **not relevant** when:
- Discussing pure technical architecture (use `/architecture`)
- Debugging a specific code defect (use language-specific tools)
- Refactoring for style (use `/naming` or `/functions`)
- Learning a new technology (use `/teach-concept`)

---

## K-Line History

This skill encodes the accumulated knowledge of:

- **The Programmer's Oath** — Uncle Bob Martin's nine commitments (Clean Coder)
- **Do No Harm Framework** — Preventing harm to users, function, structure, and society
- **Two Values of Software** — Behavior and structure; structure enables change
- **PERT Estimation** — Beta distribution for three-point estimates
- **Professional Responsibility** — Ownership, saying no, saying yes, the danger of "try"
- **Quality as Risk Management** — Cost of discipline vs cost of harm
- **The Coming Reckoning** — Self-regulation before external regulation

---

## Communication Style

When applying this skill:

- **Be direct** — Use clear language: "This is a critical risk because..." not "It might be..."
- **Use evidence** — Point to specific defects, specific risks, specific harms
- **Respect business context** — Acknowledge deadline pressure and business needs
- **Offer alternatives** — Don't just say no; say no and offer a path forward
- **Calm and professional** — Never passive-aggressive, never "I told you so"
- **Document decisions** — When you escalate, document your recommendation and the decision
- **Own your part** — You control your code quality, your estimates, your willingness to speak up

---

## Related Skills

- **/tdd** — Proof of correctness; TDD as professional standard
- **/agile** — Professional expectations that Agile teams demand
- **/clean-code-review** — Quality gate before shipping; harm verification
- **/solid** — Preventing structural harm between modules
- **/architecture** — Preventing harm at the highest level; system design
- **/legacy-code** — Professional responsibility toward existing code; characterization tests
