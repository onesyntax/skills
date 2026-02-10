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

# Legacy Code Workflow

This workflow guides AI agents through working with legacy code using Uncle Bob's teachings from the Clean Code series (Episode 68) and Michael Feathers' techniques from "Working Effectively with Legacy Code." Follow these steps when dealing with old, untested, or poorly structured code.

## Workflow Steps

### Step 1: Assess the Legacy Code Situation
- Identify the scope of the legacy code being touched
- Determine if the code has any existing tests
- Identify inputs and outputs for potential characterization tests
- Understand what change is actually needed (bug fix, new feature, refactor)

### Step 2: Apply the Boy Scout Principle
- Plan one small act of kindness alongside any required change
- Do NOT start a cleanup project or hunt for refactoring opportunities
- Focus only on the code you are actively touching

### Step 3: Write Characterization Tests Where Possible
- Find modules with defined inputs and outputs
- Capture current behavior as the "golden standard"
- Use these tests as safety nets for refactoring

### Step 4: Add New Features in Clean Modules
- Write new functionality in isolated, clean modules using TDD
- Integrate the clean module into the legacy system at boundaries
- Do NOT smear new code throughout the existing system

### Step 5: Perform Incremental Cleanup
- Fix one bad coupling, rename one function, split one function
- Run existing tests to verify nothing broke
- Check in the code cleaner than you found it

### Step 6: Watch for Strangulation Opportunities
- As clean code accumulates around legacy code, look for safe rewrite opportunities
- Only rewrite code that is completely surrounded by tested modules

### Step 7: Apply /professional Standards
- Ensure all changes meet professional quality standards
- Never check code in worse than you found it

---

## Core Philosophy

### What Is Legacy Code?

Legacy code is not defined by age alone -- it is defined by how it was written. It is code created without proper discipline, tests, or clean design. Critically, legacy code is being actively created today by teams that don't follow clean code practices.

> "Just about every programmer in the world is embroiled in the midst of some old crufty poorly designed, badly maintained, tangled, and tortured mass of ugly legacy code."

Michael Feathers' key insight came from an associate who joined a new team that was "busy writing legacy code" -- on a brand new project. This reframes legacy code as a discipline problem, not an age problem.

### The Legacy Code Dilemma

There is no magic solution:

> "There is no simple solution to solve this problem. There's no magic wand. There's no special beans. There's no miracles you can perform. It's just going to require a lot of long hard work."

But there is hope. The techniques below provide a disciplined, incremental path forward.

---

## The Four Anti-Patterns: What NOT To Do

### Anti-Pattern 1: Do Not Start a Cleanup Project

> "Do not start a project to clean up the legacy code."

Do not go to your boss and beg for time to clean things up. Do not make promises about timelines or improvements. Cleanup projects almost always fail badly, leaving teams discouraged and discredited, and the code badly mangled.

> "Clean up projects never work, and when they're tried, they usually do more damage than good."

### Anti-Pattern 2: Do Not Go on a Refactoring Hunt

> "Don't go scanning through the code, looking for opportunities to refactor things."

Any effort put into random refactoring will be entirely wasted because the vast majority of code in a system has not been touched for years and is not likely to be touched anytime soon. Refactoring untouched code does nobody any good.

### Anti-Pattern 3: Do Not Attempt a Massive Rewrite

> "Don't convince yourself that the only solution is a massive rewrite."

The "big redesign in the sky" almost never improves anything. Big rewrites fail because they attempt to replace a working (if ugly) system with an unproven one, and the new system inevitably accumulates its own problems.

### Anti-Pattern 4: Do Not Smear New Features Throughout the System

When adding a new feature, the temptation is to write the code in a way consistent with how the legacy system is written -- spreading it throughout the codebase. This makes the legacy problem worse, not better.

---

## The Boy Scout Principle: The Correct Approach

The core strategy for dealing with legacy code is an attitude change:

> "Always check the code in cleaner than you checked it out every single time."

> "Never ever check it in worse than it was. Always make it better."

### What One Random Act of Kindness Looks Like

- Fix one bad coupling
- Change one function name to reveal intent
- Split one large function in two
- Extract one duplicated block
- Add one clarifying comment (only if code can't be made self-documenting)

Then check it in.

> "Do some random act of kindness to the code... Gently, gently don't do too much. Don't try to fix a whole bunch of things. Don't dig in and tear it to shreds. Do it gently. Do it evenly."

### The Team Effect

If everyone on the team follows this practice, the codebase will gradually improve over time. But not ALL of it will improve -- only the volatile parts that are actively maintained. This is a feature, not a bug: you only improve what matters.

---

## The Snowball Effect

A virtuous cycle emerges from consistent application of the Boy Scout Principle:

1. Legacy code generally was not designed to be testable
2. At first, adding tests is impractical
3. After a few acts of kindness, it suddenly becomes easier to add a unit test
4. More tests make the system easier to clean
5. Easier cleaning leads to more tests
6. The pace of improvement accelerates

> "And now you've got a rolling snowball."

The volatile parts of the system get cleaner and cleaner, and easier and easier to work in.

---

## The Strangulation Technique

Over months or even years, the cleaned volatile parts will completely surround some ugly, untested legacy code that hasn't been modified. Once that legacy code is completely surrounded by tested modules, you have an opportunity to safely rewrite or refactor it.

> "Rewriting code that's surrounded by tested modules is a safe operation, and it's safe because of all those modules that are tested. We call this technique strangulation."

> "The cleaner tested code strangles that bad yuck in the middle there, and allows it to be rewritten, and refactored, and tested."

This is the ONLY safe context for a rewrite: small, surrounded, and protected by tests.

---

## Adding New Features to Legacy Systems

When asked to add a new feature to a legacy system:

### Wrong Way
Smear the code for the new feature throughout the whole system in a way consistent with how the system is written. This perpetuates the legacy problem.

### Right Way
Write the new feature in its own module independently, using test-driven development and clean code principles. Make it a nice clean module, then tie it into the rest of the system at integration points.

This takes slightly longer but prevents the legacy problem from growing. Every new clean module is another piece of the strangulation strategy.

---

## Characterization Tests (Golden Standard)

Michael Feathers' technique for creating safety nets around legacy code:

### When to Use
- Find a module with precisely defined outputs based on precisely defined inputs
- Examples: a module that prints a report from a database, a transaction processor with log output

### The Technique

1. **Identify** a module with defined I/O boundaries
2. **Capture** the current output given a known input -- this is the "golden standard"
3. **Save** this output as your characterization test
4. **Refactor** the internals of the module
5. **Regenerate** the output after each refactoring step
6. **Compare** to the golden standard -- if they match, nothing is broken
7. **Continue** refactoring as long as the golden standard holds

### Properties of Characterization Tests

- **Fragile by nature**: Any new feature or behavior change can invalidate the golden standard
- **Regeneration required**: When behavior intentionally changes, regenerate the golden standard
- **Transitional**: As the system becomes more testable, replace characterization tests with proper unit tests
- **Enables the snowball**: More testability leads to more unit tests, which enables more aggressive refactoring

### Beyond Reports: Log Files as Golden Standards

For transaction-based systems, log files can potentially serve as golden standards. However, challenges include:
- Different thread ordering between runs
- Timestamp variations from system clocks
- Non-deterministic process scheduling

A comparison utility that eliminates irrelevant differences and focuses on relevant substance can make this approach viable.

---

## Prevention: How to Avoid Creating Legacy Code

The entire 67-episode Clean Code series teaches how to avoid creating legacy code in the first place. The key practices:

1. **Test-Driven Development** (`/tdd`): Write tests first, always
2. **SOLID Principles** (`/solid`): Design classes with proper responsibilities and dependencies
3. **Clean Functions** (`/functions`): Keep functions small and focused
4. **Clean Names** (`/naming`): Use intention-revealing names
5. **Clean Architecture** (`/architecture`): Separate concerns, invert dependencies
6. **Boy Scout Rule**: Always leave code cleaner than you found it
7. **Professional Discipline** (`/professional`): Take responsibility for code quality

> "We programmers built an awful lot of systems in the past before we knew how systems ought to be built."

The problem is not just historical -- many programmers today still create legacy code due to the same misconceptions and lack of discipline.

---

## Step-by-Step Workflow for Legacy Code

### Assessment Phase
1. **Identify the scope** -- What legacy code are you touching and why?
2. **Check for existing tests** -- Any tests at all? Integration tests? Manual test scripts?
3. **Map the I/O boundaries** -- Can you identify inputs and outputs for characterization tests?
4. **Understand the change** -- Is this a bug fix, new feature, or required refactoring?

### Preparation Phase
5. **Create characterization tests** where possible for modules you'll be modifying
6. **Establish golden standards** for output comparison
7. **Identify integration points** where new clean code will connect to legacy code

### Implementation Phase
8. **Write new features in clean isolated modules** using TDD
9. **Perform one small act of kindness** for each check-in (rename, split, decouple)
10. **Add unit tests** wherever the cleaning makes it possible
11. **Integrate clean modules** at defined boundaries

### Ongoing Phase
12. **Watch for strangulation opportunities** as clean code surrounds legacy code
13. **Never revert** to old habits or check code in worse than you found it
14. **Be patient** -- improvements accumulate over months and years

---

## Patience and Determination

> "Whatever happens, nothing is going to happen quickly."

> "It took a long time to make the mess. It's gonna take a long time to clean it up, but it can be cleaned up. It just takes determination and patience."

The trajectory:
- Improvements will be small at first
- Month after month, they accumulate
- The pace of cleaning accelerates as testability improves
- Don't give up and don't revert to old habits

---

## Output Format

When analyzing legacy code, present findings as:

```
## Legacy Code Assessment

**Scope:** [What legacy code is being touched]
**Existing Tests:** [Any existing test coverage]
**Characterization Test Opportunities:** [Modules with defined I/O]
**Recommended Acts of Kindness:** [Specific small improvements]
**New Feature Strategy:** [How to add features cleanly]
**Strangulation Status:** [Progress toward surrounding legacy code with tested modules]
```

For each recommended change:
```
### Act of Kindness: [Description]
**Location:** file:line
**Type:** [rename/split/decouple/extract/test]
**Current State:** [What the code looks like now]
**Proposed Change:** [What it should look like]
**Risk Level:** [low/medium - legacy changes should always be low risk]
**Test Coverage:** [How this change is protected]
```

---

## Memorable Quotes

> "Just about every programmer in the world is embroiled in the midst of some old crufty poorly designed, badly maintained, tangled, and tortured mass of ugly legacy code."

> "There is no simple solution to solve this problem. There's no magic wand. There's no special beans."

> "Do not start a project to clean up the legacy code."

> "Clean up projects never work, and when they're tried, they usually do more damage than good."

> "Big rewrites almost never improve anything."

> "Always check the code in cleaner than you checked it out every single time."

> "Never ever check it in worse than it was. Always make it better."

> "Do some random act of kindness to the code."

> "Gently, gently don't do too much."

> "And now you've got a rolling snowball."

> "We call this technique strangulation."

> "The cleaner tested code strangles that bad yuck in the middle there, and allows it to be rewritten, and refactored, and tested."

> "It took a long time to make the mess. It's gonna take a long time to clean it up, but it can be cleaned up. It just takes determination and patience."

---

## Common Pitfalls

- **Starting a cleanup project** - Projects fail; incremental improvement succeeds
- **Random refactoring hunts** - Only improve code you're actively touching
- **Big rewrites** - Almost never improve anything
- **Smearing new features** - Write clean modules, integrate at boundaries
- **Impatience** - Legacy code took years to create; cleaning takes time too
- **Giving up** - The snowball effect means progress accelerates over time
- **Checking in worse code** - Never, under any circumstances

---

## Self-Review (Back Pressure)

After working with legacy code, ALWAYS perform this self-review:

### Self-Review Steps
1. **Boy Scout Check**: Is this code cleaner than when I found it?
2. **Smearing Check**: Did I add new features in clean isolated modules, or smear them throughout the system?
3. **Test Check**: Did I add characterization tests or unit tests where possible?
4. **Kindness Check**: Did I perform at least one small act of kindness?
5. **Integration Check**: Are new modules integrated at clean boundaries?

### If Violations Found
- Fix the violations immediately
- Ensure no code is checked in worse than it was found
- Re-run self-review

### Mandatory Quality Gate
Legacy code changes are NOT complete until:
- [ ] Code is cleaner than when you found it (Boy Scout Rule)
- [ ] New features are in clean isolated modules
- [ ] Characterization tests exist where possible
- [ ] At least one act of kindness performed per change
- [ ] No code smeared throughout the legacy system

---

## Code to Analyze

$ARGUMENTS

---

## Related Skills

Working with legacy code integrates with all Clean Code practices:

- **/tdd** - Write new features test-first in clean modules
- **/solid** - Apply SOLID principles to new code and incremental improvements
- **/naming** - Rename unclear functions and variables as acts of kindness
- **/functions** - Split large functions as acts of kindness
- **/architecture** - Design clean module boundaries for new features
- **/patterns** - Apply appropriate patterns when refactoring legacy code
- **/professional** - Take professional responsibility for code quality
- **/clean-code-review** - Review changes before checking in
