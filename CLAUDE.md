# Clean Code Guidelines

Clean Code principles from Uncle Bob's teachings, organized as operational skills for AI agents. Examples use PHP and TypeScript.

## The TDD Workflow

When implementing features or fixing bugs, use TDD:

1. **RED** — Write a failing test for the next small increment
2. **GREEN** — Write the minimum code to make the test pass
3. **REFACTOR** — Clean up using the relevant skills below
4. **REPEAT** — Continue until the feature is complete

TDD is not optional for feature work. Use `/tdd` for the methodology and the three laws.

## Quality Gate

Before marking code as done, run `/clean-code-review`. This is the comprehensive 10-dimension review that checks naming, functions, classes, error handling, comments, formatting, tests, architecture, patterns, and professional standards. It delegates to specialized skills for deep analysis.

Code is NOT done until the review passes with no critical issues.

## Skills

### When Writing Code

| Skill | Use When |
|-------|----------|
| `/tdd` | Implementing any feature or fix (mandatory) |
| `/naming` | Naming variables, functions, classes, modules |
| `/functions` | Writing or refactoring functions |
| `/solid` | Designing classes, checking SOLID compliance |
| `/patterns` | Applying or evaluating design patterns |
| `/architecture` | Designing system structure, boundaries, layers |
| `/components` | Module boundaries, cohesion, coupling, dependency management |
| `/functional-programming` | Pure functions, immutability, side effect isolation |

### When Reviewing Code

| Skill | Use When |
|-------|----------|
| `/clean-code-review` | Final quality gate before marking done (mandatory) |
| `/refactor-suggestion` | Analyzing code smells, planning refactoring |
| `/legacy-code` | Working with old untested code, characterization tests |
| `/acceptance-testing` | Writing acceptance tests, ATDD, testing pyramid |

### When Discussing Process or Teaching

| Skill | Use When |
|-------|----------|
| `/agile` | Velocity, planning, CI, Definition of Done, Scrum |
| `/professional` | Ethics, estimation, commitments, saying no |
| `/teach-concept` | Explaining any Clean Code concept to a learner |

## How Skills Work

Each skill is an operational procedure with context detection (Step 0), decision rules (WHEN/WHEN NOT), severity-rated checklists, and named refactoring patterns. Skills follow a runtime procedure structure — they change agent behavior, not just provide reference material.

- **SKILL.md** — Operational procedure loaded when the skill activates (<500 lines)
- **agents/** — Optional subagent definitions for delegation (analyzer/refactorer pairs)

Skills delegate to each other via `delegates-to` in frontmatter. For example, `/clean-code-review` delegates to `/naming`, `/functions`, `/solid`, etc. for deep analysis of each dimension.

## Applying Skills Proportionally

Not every change requires every skill. Match the depth of review to the scope of the change:

**Small change** (rename, fix typo, one-line bug fix): Apply `/naming` if names changed. No full review needed.

**Medium change** (new function, refactor a class, add a test): Apply `/tdd` for the workflow. Check `/naming` and `/functions` on modified code. Run `/clean-code-review` focused on the changed files.

**Large change** (new feature, new module, architectural change): Full `/tdd` workflow. Apply `/solid`, `/architecture`, `/components` as relevant. Run `/clean-code-review` comprehensively. Check `/acceptance-testing` if user-facing behavior changed.

**Legacy code work**: Start with `/legacy-code` for the approach (characterization tests, Boy Scout Rule, strangulation). Then apply other skills during the refactoring step.
