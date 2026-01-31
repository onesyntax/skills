---
name: teach-concept
description: >-
  Explain Clean Code concepts with examples, quotes, and practical guidance.
  Activates when the user asks to explain or learn about Clean Code concepts,
  wants to understand principles, or mentions teach, explain, what is, how does,
  or why should related to Clean Code topics.
allowed-tools: Read, Grep, Glob, Skill
argument-hint: [concept name - e.g., "SOLID", "TDD", "naming", "functions"]
---

# Teach Clean Code Concept

Explain the requested Clean Code concept using Uncle Bob's teachings.

## Teaching Workflow

1. **Identify the Concept** - Determine which Clean Code concept the user wants to learn
2. **Load Specialized Skill** - Use the appropriate skill for comprehensive content
3. **Teach with Depth** - Provide examples, quotes, and practical guidance from the skill

## Related Skills by Concept

When teaching specific concepts, load the appropriate specialized skill for comprehensive content:

| Concept Category | Skill to Use | When to Load |
|------------------|--------------|--------------|
| Naming | `/naming` | Variables, functions, classes, packages naming conventions |
| Functions | `/functions` | Function design, size, arguments, side effects |
| SOLID | `/solid` | Any SOLID principle (SRP, OCP, LSP, ISP, DIP) |
| Testing | `/tdd` | TDD, three laws, clean tests, test design |
| Architecture | `/architecture` | Clean Architecture, layers, boundaries, use cases |
| Patterns | `/patterns` | Design patterns, state machines, factories |
| Professionalism | `/professional` | Estimates, saying no, ethics, programmer's oath |
| Components | `/components` | Component cohesion, coupling, REP, CCP, CRP |
| Code Review | `/clean-code-review` | Reviewing code for clean code principles |

### How to Use Related Skills

When the user asks about a concept:

1. **Match the concept to a skill category** from the table above
2. **Invoke the skill** using the Skill tool:
   - For naming: `Skill: naming`
   - For functions: `Skill: functions`
   - For SOLID principles: `Skill: solid`
   - For testing/TDD: `Skill: tdd`
   - For architecture: `Skill: architecture`
   - For patterns: `Skill: patterns`
   - For professionalism: `Skill: professional`
   - For components: `Skill: components`
   - For review: `Skill: clean-code-review`
3. **Use the skill's content** to provide comprehensive teaching

## Teaching Approach

1. **Definition** - Clear, concise explanation of the concept
2. **Why It Matters** - The reasoning and benefits
3. **The Rules** - Specific guidelines to follow
4. **Good Examples** - Code that demonstrates the concept well
5. **Bad Examples** - Anti-patterns to avoid
6. **Memorable Quotes** - Uncle Bob's key phrases
7. **Practical Tips** - How to apply it in daily coding

## Available Topics

### Core Concepts

- **naming** - How to name variables, functions, classes
- **functions** - Writing small, focused functions
- **classes** - Designing cohesive classes
- **comments** - When and how to comment
- **formatting** - Code organization and style
- **error-handling** - Exceptions and edge cases

### SOLID Principles

- **srp** - Single Responsibility Principle
- **ocp** - Open-Closed Principle
- **lsp** - Liskov Substitution Principle
- **isp** - Interface Segregation Principle
- **dip** - Dependency Inversion Principle
- **solid** - All five principles together

### Testing

- **tdd** - Test-Driven Development
- **three-laws** - The Three Laws of TDD
- **clean-tests** - Writing maintainable tests
- **mocking** - When and how to use test doubles

### Architecture

- **clean-architecture** - Layers and boundaries
- **use-cases** - Application business rules
- **dependency-rule** - Dependencies point inward
- **components** - Component design principles

### Patterns

- **factory** - Factory patterns
- **strategy** - Strategy pattern
- **observer** - Observer pattern
- **state** - State pattern and FSMs

### Professional

- **estimates** - How to estimate responsibly
- **saying-no** - Professional boundaries
- **programmers-oath** - The commitments we make

## Requested Topic

$ARGUMENTS

## Related Skills

The following skills provide comprehensive content for teaching Clean Code concepts:

| Skill | Command | Purpose |
|-------|---------|---------|
| Naming | `/naming` | Comprehensive naming conventions and guidelines |
| Functions | `/functions` | Function design principles and best practices |
| SOLID | `/solid` | All five SOLID principles with examples |
| TDD | `/tdd` | Test-Driven Development methodology |
| Architecture | `/architecture` | Clean Architecture principles and patterns |
| Patterns | `/patterns` | Design patterns for clean code |
| Professional | `/professional` | Professional ethics and practices |
| Components | `/components` | Component design and cohesion principles |
| Clean Code Review | `/clean-code-review` | Code review using clean code standards |
