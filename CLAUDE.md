# Clean Code Documentation Project

This project contains comprehensive Clean Code documentation based on Uncle Bob's teachings.

## TDD Workflow (Mandatory)

When implementing new features or fixing bugs, **you MUST use TDD (Test-Driven Development)**:

1. **RED**: Write a failing test for the next small increment
2. **GREEN**: Write minimum code to make the test pass
3. **REFACTOR**: Clean up using `/naming`, `/functions`, `/patterns`, `/solid`, `/component` principles
4. **REPEAT**: Continue the cycle until feature is complete

TDD ensures:
- Code is testable by design
- Quick, sure, repeatable proof that code works
- Confidence to refactor without fear
- Clean code emerges naturally through the refactor step

**Use `/tdd` skill** for ALL feature implementations and bug fixes.

## Quality Gates (Mandatory)

Before completing any code task, the AI MUST:

1. **Apply /tdd workflow** for implementing new features (Red-Green-Refactor)
2. **Apply /naming principles** to all new/modified names
3. **Apply /functions principles** to all new/modified functions
4. **Apply /patterns principles** to all new/modified functions
5. **Apply /solid principles** to all new/modified classes
6. **Apply /component principles** to all new/modified classes
7. **Apply /architecture principles** to all new/modified classes
8. **Run /clean-code-review** on all modified code
9. **Report any Clean Code violations found**
10. **Fix violations before marking task complete**

These gates are NOT optional. Code that doesn't meet Clean Code standards must be refactored.

## Self-Review Loop

After writing any code, automatically perform a self-review:

1. Verify tests exist and pass (TDD compliance)
2. Review code against `/naming` principles
3. Review code against `/functions` principles
4. Review code against `/patterns` principles 
5. Review code against `/solid` principles 
6. Review code against `/components` principles 
7. Review code against `/architecture` principles 
8. Review code against `/professional` standards 
9. If violations found:
   a. Fix violations
   b. Re-run self-review 
10. Present clean code to user

## Available Skills (Workflows)

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/naming` | Naming analysis | Writing/reviewing names |
| `/functions` | Function analysis | Writing/refactoring functions |
| `/solid` | SOLID principles | Designing classes/modules |
| `/tdd` | Test-Driven Development | ALL feature implementations (mandatory) |
| `/architecture` | Clean Architecture | Designing system structure |
| `/patterns` | Design Patterns | Identifying/applying patterns |
| `/professional` | Professional standards | Ethics, estimates, commitments |
| `/components` | Component design | Module boundaries, cohesion, coupling |
| `/acceptance-testing` | Acceptance testing | ATDD, testing pyramid, BDD, fixtures |
| `/agile` | Agile practices | Velocity, planning, CI, Definition of Done |
| `/functional-programming` | Functional programming | Pure functions, immutability, FP patterns |
| `/legacy-code` | Legacy code | Boy Scout Rule, characterization tests, strangulation |
| `/clean-code-review` | Comprehensive review | Before commit/merge |
| `/refactor-suggestion` | Refactoring guidance | Improving existing code |
| `/teach-concept` | Teaching concepts | Learning Clean Code principles |

## Back Pressure Workflow

```
User Request: "Implement feature X" or "Fix bug Y"
    │
    ▼
/tdd workflow activates (mandatory)
    │
    ├── RED: Write failing test
    │     │
    │     ▼
    ├── GREEN: Write minimum code to pass
    │     │
    │     ▼
    ├── REFACTOR: Clean up code
    │     ├── Apply /naming principles
    │     ├── Apply /functions principles
    │     ├── Apply /patterns principles
    │     ├── Apply /solid principles
    │     ├── Apply /components principles
    │     │
    │     ▼
    └── REPEAT until feature complete
    │
    ▼
Self-Review Loop activates
    ├── Check /naming principles
    ├── Check /functions principles
    ├── Check /patterns principles
    ├── Check /solid principles
    ├── Check /architecture principles
    ├── Check /professional standards
    │
    ▼
If violations found → Fix and re-review
    │
    ▼
/clean-code-review activates (mandatory)
    ├── Comprehensive review against ALL skills
    │
    ▼
If passes → Present to user as "done"
If fails → Fix and re-review
```

## Project Structure

- `.claude/skills/` - Comprehensive workflow guides for AI agents
- `.claude/agents/` - Thin wrappers that invoke skills

Each skill contains comprehensive Clean Code content from Uncle Bob's teachings that AI agents follow automatically when writing code.
