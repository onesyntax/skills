---
name: teach-concept
description: >-
  Explain Clean Code concepts with examples and practical guidance.
  Activates when the user asks to explain or learn about Clean Code concepts,
  wants to understand principles, or mentions teach, explain, what is, how does,
  or why should related to Clean Code topics.
allowed-tools: Read, Grep, Glob, Skill
argument-hint: [concept name - e.g., "SOLID", "TDD", "naming", "functions"]
---

# Teach Clean Code Concept

Teaching methodology for Clean Code principles. This is a meta-skill — it defines HOW to teach, then delegates to specialized skills for WHAT to teach.

For lesson plan examples and teaching walkthroughs, read `references/extended-examples.md`.

---

## Teaching Methodology

### 1. Meet Them Where They Are

Before explaining a concept, understand the learner's context. Are they a junior developer hearing about SOLID for the first time, or an experienced developer who wants to understand why their current approach isn't working? The same concept needs different framing at different levels.

**Beginner:** Start with the problem the concept solves. "Have you ever changed one thing and broken something else? That's what SRP prevents." Concrete, relatable, immediate.

**Intermediate:** Connect to concepts they already know. "You already extract functions to avoid duplication. SOLID is the same instinct applied at the class level." Build bridges from familiar to new.

**Advanced:** Go straight to the tension and tradeoffs. "SRP and OCP can conflict — splitting a class for SRP can violate OCP if the split forces changes across callers. Here's how to navigate that."

### 2. Show, Don't Lecture

Every concept needs a code example — ideally a before/after transformation that makes the benefit tangible. Abstract explanations of principles bounce off. Watching messy code become clean sticks.

Use pseudocode (language-independent). Walk through the transformation step by step — don't just show the end state. The journey from bad to good is where understanding lives.

### 3. Use the Concrete-to-Abstract Arc

Start with a concrete problem: "This function is 200 lines long and nobody understands it." Show the fix: extract functions, name them well, apply step-down rule. THEN name the principle: "What we just did is called the Single Responsibility Principle." The principle becomes a label for something they've already seen working.

Never start with the abstract definition. "The Single Responsibility Principle states that a class should have only one reason to change" means nothing until someone has felt the pain of a class with five reasons to change.

### 4. Connect Concepts into a Web

Clean Code principles are not isolated — they form a web where each principle reinforces others. When teaching one concept, show how it connects:

- Naming → Functions: good function names make functions self-documenting
- Functions → SOLID: small functions emerge naturally from SRP classes
- SOLID → Architecture: DIP at the class level becomes the Dependency Rule at the architecture level
- TDD → Refactoring: tests enable fearless refactoring
- Refactoring → Clean Code: refactoring is how messy code becomes clean
- Architecture → Components: Clean Architecture applies component principles at the system level

Always mention at least one connection. Isolated principles feel like rules to memorize. Connected principles feel like a system to understand.

### 5. Address the "Why Should I Care?"

Every concept needs a motivation that goes beyond "Uncle Bob says so." Connect to consequences the learner has experienced or will experience:

- "Without SRP, every feature change risks breaking unrelated features."
- "Without TDD, you're afraid to refactor, and without refactoring, the code rots."
- "Without the Dependency Rule, your business logic is locked inside your framework."

The best motivations are stories of real consequences — Knight Capital ($460M from dead code), Toyota (89 deaths from 10K global variables), the death spiral of Flaccid Scrum. Use them from the relevant skill's references.

### 6. Give Them Something to Do

End every teaching session with a challenge or exercise. "Take your longest function and extract three methods from it using the step-down rule." "Find a class in your codebase that has more than one reason to change and sketch how you'd split it." Learning without practice doesn't stick.

---

## Teaching Anti-Patterns

**The Definition Dump.** Listing all five SOLID principles with their formal definitions. This teaches vocabulary, not understanding. Instead, pick one principle, show it working on real code, and let the others emerge naturally.

**The Perfection Trap.** Implying that clean code is an absolute standard and any deviation is wrong. Clean code is a direction, not a destination. The goal is code that is cleaner than it was, not code that is perfect.

**The Authority Argument.** "Uncle Bob says you must do TDD." This creates compliance, not conviction. Instead: "Here's what happens to a codebase without tests over 12 months" — let the evidence convince, not the authority.

**The Firehose.** Teaching 10 concepts in one session. Learners can absorb 1-2 new ideas per session. Go deep on one concept rather than shallow on many.

**Ignoring Their Codebase.** Teaching with textbook examples when the learner has a real codebase to work with. If they have code, use their code. The concepts become immediately relevant rather than theoretical.

---

## Skill Routing

When teaching a specific concept, delegate to the specialized skill for comprehensive content:

| Concept | Skill | Key Topics |
|---------|-------|------------|
| Naming | `/naming` | Intent-revealing names, parts of speech, vocabulary |
| Functions | `/functions` | Size, arguments, side effects, step-down rule |
| SOLID | `/solid` | SRP, OCP, LSP, ISP, DIP |
| Testing & TDD | `/tdd` | Three laws, clean tests, test design |
| Architecture | `/architecture` | Layers, boundaries, use cases, Dependency Rule |
| Design Patterns | `/patterns` | GOF patterns, when to apply, when to avoid |
| Components | `/components` | REP, CCP, CRP, ADP, SDP, SAP, Main Sequence |
| Acceptance Testing | `/acceptance-testing` | ATDD, testing pyramid, BDD, fixtures |
| Agile | `/agile` | Velocity, planning, CI, Definition of Done |
| Functional Programming | `/functional-programming` | Purity, immutability, composition, functional SOLID |
| Legacy Code | `/legacy-code` | Boy Scout Rule, characterization tests, strangulation |
| Professional Standards | `/professional` | Programmer's Oath, estimation, saying no, ethics |
| Code Review | `/clean-code-review` | 10-dimension review, severity classification |
| Refactoring | `/refactor-suggestion` | Code smells, safe refactoring, techniques |

Each skill has a `references/extended-examples.md` file with detailed walkthroughs — use these for in-depth teaching.

---

## Handling Common Questions

**"Isn't this over-engineering?"** Clean code is about simplicity, not complexity. If applying a principle makes the code harder to understand, you've misapplied it. The goal is code that reads like well-written prose — not code that demonstrates how many patterns you know.

**"We don't have time for this."** The mess is what slows you down. Every shortcut creates drag that compounds over time. The only way to go fast is to go well. Use the Agile death spiral example from `/agile` references.

**"This doesn't apply to our language/framework."** Clean Code principles are language-independent. The specific syntax changes, but the reasoning is universal: small functions, clear names, single responsibility, dependency inversion. Show them the pseudocode examples, then help them translate to their stack.

**"My team won't adopt this."** Start small. The Boy Scout Rule — leave code cleaner than you found it — requires no team buy-in. Apply it to your own code. When others see the improvement, they'll ask what you're doing differently.
