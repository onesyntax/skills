---
name: teach-concept
description: >-
  Operational framework for teaching Clean Code concepts. Activates when explaining
  or learning about Clean Code principles. Routes to specialized skills and applies
  learner-level-appropriate teaching strategies.
allowed-tools: Read, Grep, Glob, Skill
argument-hint: [concept name - e.g., "SOLID", "TDD", "naming", "functions"]
model: opus
delegates-to: [naming, functions, solid, tdd, architecture, patterns, components, functional-programming, acceptance-testing, agile, professional, legacy-code, refactor-suggestion, clean-code-review]
---

# Teach Clean Code Concept

Operational framework for teaching Clean Code concepts to learners at different levels. This is a meta-skill that detects context, routes to specialized skills, applies decision rules, and executes teaching patterns.

---

## Step 0: Detect Context

Before teaching anything, assess the learner's situation. The same concept needs different treatment at different levels.

### Learner Level Detection

**Beginner** — First exposure to the concept. May not have encountered the problem it solves. Needs problem framing before principle framing.
- Indicator: "What is X?" or "How do I use X?"
- Signal: Limited vocabulary around the concept
- Approach: Problem first, then solution, then name

**Intermediate** — Knows some concepts, wants to understand depth or connections. Already solving related problems, needs bridge from familiar to new.
- Indicator: "How does this relate to..." or "When should I use..."
- Signal: References other concepts, discusses tradeoffs
- Approach: Connect to known concepts, show patterns, discuss when to apply

**Advanced** — Wants tradeoffs, tensions, limits, and when NOT to apply. Already practiced with the concept, seeking mastery nuance.
- Indicator: "What are the limitations?" or "When does this conflict with..."
- Signal: Discusses edge cases, exceptions, philosophy
- Approach: Tensions and tradeoffs, show where principles collide

### Context Assessment

| Factor | Question | Impact |
|--------|----------|--------|
| **Language/Framework** | What stack are they coding in? | Use concrete examples in their language |
| **Codebase Access** | Do they have code to work with? | Use their code vs generic examples |
| **Problem Type** | Are they learning theory or solving a problem? | Theory=conceptual; Problem=applied teaching |
| **Concept Familiarity** | What related concepts do they already know? | Build bridges from known to new |
| **Time Available** | Teaching session or quick question? | Session=go deep; Quick=focused answer |

---

## Step 1: Route to Specialized Skill

Look up the concept in the routing table. Load the specialized skill to get decision rules, patterns, checklist, and concrete examples.

### Skill Routing Table

| Concept | Skill | Use When (with PHP/TypeScript examples) |
|---------|-------|----------|
| Intent-revealing names, vocabulary, naming patterns | `/naming` | Learner asks about naming (PHP class/method names, TypeScript interface/function names, variable clarity) |
| Function size, arguments, side effects, step-down rule | `/functions` | Learner asks about function design (PHP service methods, TypeScript utility functions, parameter counts) |
| SRP, OCP, LSP, ISP, DIP, SOLID violations | `/solid` | Learner asks about class design (PHP Service/Repository classes, TypeScript interfaces and classes) |
| Three laws of TDD, test-driven workflow, test design | `/tdd` | Learner asks about testing with PHPUnit (PHP) or Jest (TypeScript), test-first development |
| Architecture layers, boundaries, Dependency Rule, use cases | `/architecture` | Learner asks about system design (PHP layers: Controller→Service→Repository, TypeScript module boundaries) |
| GOF patterns, when to apply, anti-patterns | `/patterns` | Learner asks about design patterns (PHP service locator, TypeScript dependency injection, factory patterns) |
| Component cohesion (REP, CCP, CRP), coupling (ADP, SDP, SAP), Main Sequence | `/components` | Learner asks about module organization (PHP namespace organization, TypeScript module organization) |
| Acceptance testing, ATDD, testing pyramid, BDD, fixtures | `/acceptance-testing` | Learner asks about acceptance criteria (PHP integration tests, TypeScript service tests, test pyramid) |
| Agile velocity, planning, CI/CD, Definition of Done | `/agile` | Learner asks about process (velocity, test runner in CI, build gates, Definition of Done) |
| Pure functions, immutability, composition, functional SOLID | `/functional-programming` | Learner asks about functional techniques (TypeScript pure functions, PHP array functions, immutability) |
| Boy Scout Rule, characterization tests, strangulation | `/legacy-code` | Learner works with untested PHP/TypeScript code, needs refactoring safety patterns |
| Programmer's Oath, estimation, saying no, ethics | `/professional` | Learner asks about professional responsibility, estimation with uncertainty, shipping confidence |
| 10-dimension review, severity classification, quality gates | `/clean-code-review` | Learner asks about code quality (PHPUnit coverage, Jest coverage, code review standards) |
| Code smells, safe refactoring, transformation techniques | `/refactor-suggestion` | Learner asks about improving PHP/TypeScript code, recognizing smells, safe refactoring paths |

**Delegation rule:** Once routed, load the skill's SKILL.md (core principles) and reference extended-examples.md (detailed walkthroughs) as teaching source material.

---

## Step 2: Apply Teaching Decision Rules

These rules determine HOW to deliver the teaching at the detected learner level.

### Rule 1: Concrete First (ALWAYS apply)

**WHEN:** Teaching any concept at any level.

**WHEN NOT:** Advanced learner explicitly asks "Give me the theoretical definition" (rare).

**Action:** Start with a code example or problem, not the principle name.
- Bad: "The Single Responsibility Principle states that a class should have one reason to change."
- Good: "This UserManager class does authentication, database persistence, and logging. When auth rules change, you risk breaking persistence. That's the problem SRP solves."

---

### Rule 2: Use Their Code (when available)

**WHEN:** Learner has provided code, described their codebase, or works in a specific domain.

**WHEN NOT:** Learner asking about a concept before encountering it in their codebase. They're learning theory.

**Action:** Use their code as the teaching example, not generic pseudocode.
- Generic: "A long function can be split by extracting helper methods."
- Specific: "Your payment-processing function is 240 lines. Let me show you how to extract the validation logic, then the calculation logic, as separate functions."

---

### Rule 3: One Concept Deep

**WHEN:** Teaching session or learner wants to understand a concept thoroughly.

**WHEN NOT:** Learner asks for a survey ("What are all the SOLID principles?") or has limited time.

**Action:** Go deep on ONE concept per session. Mention related concepts but don't teach them simultaneously.
- Bad: Teaching SRP, OCP, and LSP in one go (firehose).
- Good: "Let's focus on SRP today. Here's how it connects to OCP (we'll cover that next time)."

---

### Rule 4: Level-Appropriate Framing

**WHEN:** Always. Adapt the framing to the detected learner level.

**Action:**
- **Beginner:** Problem → Solution → Principle name. "You have this pain. Here's the cure. It's called X."
- **Intermediate:** Bridge from known concept. "You already do this with functions. SOLID is the same thinking at the class level."
- **Advanced:** Tensions and tradeoffs. "SRP and OCP can conflict. Here's when and how to navigate that."

---

### Rule 5: End with Action

**WHEN:** Teaching session concludes or learner is ready to apply the concept.

**WHEN NOT:** Quick clarification question in the middle of implementation.

**Action:** Give a concrete exercise.
- "Take your longest function and extract three methods using the step-down rule."
- "Find a class that has more than one reason to change and sketch how you'd split it."
- "Write a test first for the next small feature."

---

### Rule 6: Avoid Anti-Patterns

**WHEN:** Always. These mistakes undo the teaching.

**Action:** Avoid these:
- **Definition dump:** Listing all principles with formal definitions (teaches vocabulary, not understanding)
- **Perfection framing:** Implying clean code is absolute standard (wrong—it's directional)
- **Authority argument:** "Uncle Bob says" instead of evidence (creates compliance, not conviction)
- **Firehose:** Teaching 10 concepts in one session (learners absorb 1-2 per session)
- **Generic examples:** Using textbook examples when learner's code is available (makes it abstract, not applicable)

---

## Step 3: Teaching Quality Checklist

Verify teaching quality before concluding. Use severity markers to identify critical failures.

### Quality Verification (8 items)

| # | Checkpoint | Severity | Pass Criteria |
|---|-----------|----------|---------------|
| 1 | Started with code example, not definition | 🔴 Critical | First element is a concrete problem or code snippet, not "X means..." |
| 2 | Framing matched learner level | 🔴 Critical | Beginner got problem framing; Intermediate got connections; Advanced got tensions |
| 3 | Named the principle/pattern AFTER showing it working | 🔴 Critical | Learner saw the benefit before learning the name |
| 4 | Used learner's code when available | 🟡 Medium | If learner provided code, teaching example came from it, not generic pseudocode |
| 5 | Connected to at least one related concept | 🟡 Medium | Mentioned how this concept reinforces or relates to one they already know |
| 6 | Avoided authority arguments | 🔴 Critical | No "Uncle Bob says" or "Best practice says"—used evidence instead |
| 7 | Ended with concrete action/exercise | 🟡 Medium | Learner has a specific task they can do right now to practice |
| 8 | Kept to 1-2 concepts max | 🔴 Critical | Didn't firehose; focused depth on one concept |

**Decision rule:** If any 🔴 critical fails, the teaching needs rework. 🟡 medium items improve quality but don't block completion.

---

## Step 4: Teaching Patterns

Named patterns for delivering teaching at different levels and situations.

### Pattern 1: Problem-First (Beginner default)

**When:** Learner has no prior exposure to the concept or is struggling with "why should I care."

**Structure:**
1. **Paint the Pain** — Describe a real problem (broken features, hard refactors, fear of change).
2. **Show the Cure** — Walk through a code transformation that solves the problem.
3. **Name the Principle** — "What we just did is called X."
4. **Show the Benefit** — "Now when we change this, we don't risk breaking unrelated features."

**Example:** Teaching SRP with PHP
- Pain: "This UserManager class handles authentication, database persistence, and notification sending. When auth changes, persistence tests fail."
- Cure: Extract UserService for auth, create UserRepository for persistence, create NotificationService.
- Name: "This is the Single Responsibility Principle."
- Benefit: "Now each class changes for one reason. Safer refactoring. Tests are faster and more focused."

---

### Pattern 2: Code Transform (All levels)

**When:** Teaching HOW to apply a principle through concrete transformation.

**Structure:**
1. **Before code** — Messy or problematic PHP/TypeScript code (often from their codebase).
2. **Step-by-step walkthrough** — Show each transformation incrementally (service extraction, function extraction, etc.).
3. **After code** — Clean result with improved test suite testability.
4. **Reflection** — "Notice what changed? That's the principle in action. Watch how tests become simpler."

**Guidance:** Show intermediate steps, not just before/after. The journey is where understanding lives.

---

### Pattern 3: Concept Bridge (Intermediate default)

**When:** Learner knows related concepts and needs to connect the dots.

**Structure:**
1. **Known concept** — Start with something they already practice.
2. **Parallel principle** — "You do this at level X. The same pattern applies at level Y."
3. **Concrete example** — Show the parallel in code.
4. **New insight** — "This is why you already intuitively apply this principle."

**Example:** Teaching SOLID via PHP/TypeScript functions
- Known: "You extract PHP service methods to avoid duplication. You extract TypeScript utility functions to share logic."
- Parallel: "SOLID applies the same thinking at the class and module level."
- Example: "You name functions well (PHP: `validateEmail()`, TypeScript: `authenticateUser()`) so readers understand intent. SRP does the same for classes and interfaces."
- Insight: "You've been following SOLID without knowing it. Now apply it consciously to Service classes and module boundaries."

---

### Pattern 4: Tension Exploration (Advanced default)

**When:** Advanced learner wants to understand limits, conflicts, and tradeoffs.

**Structure:**
1. **Principle A** — State the principle clearly.
2. **Principle B** — State a potentially conflicting principle.
3. **Show the tension** — Code example where applying both creates conflict.
4. **Navigation strategies** — Discuss when to prioritize A vs B, or how to balance.
5. **Judgment call** — "This requires experience and context to decide."

**Example:** SRP vs OCP tension
- SRP: "Split classes by reason to change."
- OCP: "Extend behavior without modifying existing classes."
- Tension: "Splitting a class for SRP might force all callers to change (violates OCP)."
- Navigation: "Prefer SRP in hot-change areas. Prefer OCP in stable interfaces."

---

### Pattern 5: Guided Discovery (All levels, when time permits)

**When:** Teaching session with time, or learner benefits from thinking through the principle themselves.

**Structure:**
1. **Ask the problem question** — "What happens when this class has five reasons to change?"
2. **Let them think** — Don't answer immediately.
3. **Guide with observations** — "Notice that changes to auth break persistence tests. Why?"
4. **They name the principle** — "We could split the class so changes are isolated."
5. **Confirm and extend** — "Exactly. That's SRP. Here's how to name the resulting classes..."

**Benefit:** Learners who discover principles themselves retain them better than those told.

---

## Step 5: Communication Style

Operational guidance for tone, language, and delivery.

### Tone Rules

| Element | Rule | Example |
|---------|------|---------|
| **Authority** | Evidence-based, not authoritarian | Not: "You must do TDD." Better: "Here's what happens without tests..." |
| **Confidence** | Confident about principles, humble about application | "SRP is a universal principle. How you apply it depends on your domain." |
| **Precision** | Use precise language; avoid "always/never" | Not: "Functions should always be small." Better: "Small functions are easier to test and reason about." |
| **Concreteness** | Prefer specific examples over generalizations | Not: "Clean code is important." Better: "This function has 200 lines; let's extract three methods." |

### Language

- **Use their vocabulary** — If they say "refactoring," use that term. If they say "cleaning up," bridge to "refactoring."
- **Name the thing after showing it** — The principle becomes a label for something they've seen, not an abstract concept.
- **Pseudocode for language independence** — Show examples in pseudocode so they translate to their stack, not translated examples that might be clunky.

### Timing

- **Patience with process** — Don't rush to the principle. Spend time on the problem.
- **Chunk for absorption** — Teaching 1-2 concepts per session. After that, learners tune out.
- **Feedback loops** — "Does this make sense?" "How would you apply this in your code?"

---

## K-Line History

Knowledge dependencies and conceptual prerequisites:

- **Naming** — Foundation. Hard to teach anything else without clear naming examples.
- **Functions** — Built on naming. Small, focused functions are the first clean code skill.
- **SOLID** — Built on naming and functions. Class-level application of function principles.
- **TDD** — Built on testing mindset. Prerequisite for refactoring confidence.
- **Refactoring** — Built on TDD (tests enable fearless refactoring). Prerequisite for architecture discussion.
- **Architecture** — Built on SOLID and component thinking. Applies principles at system scale.
- **Agile/Professional** — Cross-cutting. Context for WHEN and WHETHER to apply technical practices.

**Teaching order:** Naming → Functions → SOLID → TDD → Refactoring → Architecture. Agile/Professional can be woven in at any point.

---

## When NOT to Apply

This skill is NOT appropriate when:

1. **Learner is in production crisis** — Defer teaching. Get the fire out first. Then use it as a teaching moment.
2. **Learner explicitly rejects the premise** — "I don't care about clean code" is a signal to address assumptions, not teach technique. Ask "What's driving that? Cost/schedule pressure? Bad previous experience?"
3. **Learner lacks basic language/framework competence** — Teaching SRP to someone who doesn't understand class syntax is premature. Build foundation first.
4. **Learner is cognitively overloaded** — Already learning a new language, new framework, new domain. Defer. Cognitive load is finite.
5. **Teaching would delay critical delivery** — Time-box the teaching. A 5-minute explanation is appropriate; a 30-minute deep dive is not when deadlines loom.

**In all cases:** Document the deferral reason so teaching can happen later when conditions improve.

---

## Operational Procedure: Step 0 → 1 → 2 → 3 → 4

**Step 0: Detect Context**
- Identify learner level (beginner/intermediate/advanced) from their questions and vocabulary
- Assess language/framework, codebase access, problem type
- Determine if this is theoretical learning or applied problem-solving

**Step 1: Route to Specialized Skill**
- Look up the concept in the skill routing table
- Load the specialized skill's SKILL.md
- Extract decision rules, patterns, and concrete examples as teaching source material

**Step 2: Apply Teaching Decision Rules**
- Apply Rules 1-6 in order: Concrete First, Use Their Code, One Concept Deep, Level-Appropriate Framing, End with Action, Avoid Anti-Patterns
- Check WHEN/WHEN NOT conditions for each rule
- Adapt explanation structure based on detected level

**Step 3: Teaching Quality Checklist**
- Verify 8 quality checkpoints before concluding
- Identify severity of any gaps (🔴 critical must be fixed; 🟡 medium improves quality)
- If critical items fail, rework the explanation

**Step 4: Teaching Patterns**
- Select the pattern matching the learner level and situation
- Deliver using the pattern's structure
- Adjust pacing and detail based on learner response

---

## Handling Common Objections

When learners push back, address the underlying assumption, not the surface objection.

**Objection:** "Isn't this over-engineering?"

**Underlying:** Fear that clean code means unnecessary complexity.

**Response:** "Clean code is about simplicity, not complexity. If applying a principle makes the code harder to understand, you've misapplied it. The goal is code that reads like well-written prose — controllers that are thin, services that are focused, functions that are small and composable. What part feels over-engineered to you?"

---

**Objection:** "We don't have time for this."

**Underlying:** Schedule pressure or past experience where "best practices" slowed things down.

**Response:** "The mess is what slows you down. Every shortcut creates drag that compounds. Let me show you a specific example from your codebase: [point to a slow refactor caused by tight coupling in a controller or service]. That cost you Y hours of testing and debugging. Investing in clean code structure — well-separated Services, testable modules with clear interfaces — prevents that and makes tests faster."

---

**Objection:** "This doesn't apply to our language/framework."

**Underlying:** Skepticism that principles are universal.

**Response:** "Clean Code principles are language-independent. The syntax changes, but the reasoning is universal: small functions/methods, clear names, single responsibility, dependency inversion. In PHP, we extract Service classes and use dependency injection. In TypeScript, we use interfaces and module exports for clear boundaries. Let me show you how to translate this pattern to your PHP/TypeScript stack."

---

**Objection:** "My team won't adopt this."

**Underlying:** Doubt about change capacity or buy-in.

**Response:** "Start small. The Boy Scout Rule — leave code cleaner than you found it — requires no team buy-in. Apply it to your own code in small ways. When others see the improvement, they'll ask what you're doing differently. That's how culture shifts."