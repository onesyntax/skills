---
name: refactor-suggestion
description: >-
  Analyze code and provide specific, actionable refactoring suggestions based on
  Clean Code principles. Activates when code feels messy or hard to change, after
  implementation to improve code quality, or when the user mentions refactor,
  improve code, clean up, technical debt, or code smells.
allowed-tools: Read, Grep, Glob
argument-hint: [file path to analyze]
---

# Refactoring Suggestions

Analyze the code and provide specific, actionable refactoring suggestions.

## Refactoring Workflow

Follow this workflow when analyzing code for refactoring:

1. **Identify Code Smells** - Scan for common issues (long methods, large classes, duplication, etc.)
2. **Determine Refactoring Type** - Classify what kind of refactoring is needed
3. **Use Specialized Skill** - Apply the appropriate skill for detailed guidance
4. **Apply Refactoring** - Make changes following Clean Code principles
5. **Verify Quality** - Run /clean-code-review to ensure improvements

## Analysis Focus

1. **Extract Method** - Long functions that should be broken down
2. **Rename** - Names that don't reveal intent
3. **Extract Class** - Classes with multiple responsibilities
4. **Replace Conditional with Polymorphism** - Complex switch/if chains
5. **Remove Duplication** - Repeated code patterns
6. **Simplify** - Unnecessary complexity
7. **Improve Error Handling** - Better exception usage

## Related Skills by Refactoring Type

When you identify a refactoring opportunity, use the appropriate specialized skill for detailed guidance:

| Refactoring Type | Skill to Use | When to Apply |
|------------------|--------------|---------------|
| **Naming Issues** | `/naming` | Variables, functions, classes, or modules with unclear, misleading, or non-descriptive names |
| **Function Problems** | `/functions` | Long functions, too many parameters, mixed abstraction levels, side effects |
| **SOLID Violations** | `/solid` | Single responsibility issues, dependency problems, interface segregation concerns |
| **Test-Related** | `/tdd` | Missing tests, untestable code, test refactoring, improving test coverage |
| **Architectural Issues** | `/architecture` | Module boundaries, layer violations, coupling/cohesion problems |
| **Pattern Opportunities** | `/patterns` | Repeated structures that could use design patterns, anti-patterns to remove |
| **Component Structure** | `/components` | UI component organization, prop drilling, state management issues |
| **Comprehensive Review** | `/clean-code-review` | After completing refactoring to verify overall code quality |

### Skill Usage Guidelines

- **For naming refactoring**: Use `/naming` skill to get guidance on intention-revealing names, consistent conventions, and avoiding misleading names
- **For function refactoring**: Use `/functions` skill for breaking down long methods, reducing parameters, and ensuring functions do one thing
- **For SOLID-related refactoring**: Use `/solid` skill when addressing single responsibility, open/closed, Liskov substitution, interface segregation, or dependency inversion issues
- **For test-related refactoring**: Use `/tdd` skill when tests need improvement or when making code more testable
- **For architectural refactoring**: Use `/architecture` skill for module reorganization, layer restructuring, or dependency management
- **For pattern-based refactoring**: Use `/patterns` skill when introducing design patterns or removing anti-patterns
- **For component restructuring**: Use `/components` skill when reorganizing UI components, props, or component hierarchies
- **For comprehensive review after refactoring**: Use `/clean-code-review` skill to verify the refactoring improved overall code quality

## Output Format

For each refactoring opportunity:

```

## Refactoring: [Name of Refactoring]

**Location:** file:line_range
**Current Code:**
```[language]
// The problematic code
```

**Problem:** Why this needs refactoring

**Recommended Skill:** /[skill-name] for detailed guidance

**Suggested Refactoring:**
```[language]
// The improved code
```

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Steps:**
1. [Step to perform the refactoring]
2. [Next step]
```

## Priority Order

Present refactorings in order of impact:
1. Critical - Bugs or significant maintainability issues
2. High - Clear violations of Clean Code principles
3. Medium - Improvements that would help readability
4. Low - Nice-to-have polish

## Guiding Principles

- **Boy Scout Rule**: Leave the code cleaner than you found it
- **Small Steps**: Each refactoring should be a small, safe change
- **Tests First**: Ensure tests exist before refactoring
- **One Thing**: Each refactoring addresses one concern

## Related Skills

For comprehensive Clean Code guidance, combine this skill with:

- `/professional` - Professional software craftsmanship principles
- `/naming` - Intention-revealing names and naming conventions
- `/functions` - Function design and organization
- `/solid` - SOLID principles for object-oriented design
- `/tdd` - Test-Driven Development practices
- `/architecture` - System architecture and module organization
- `/patterns` - Design patterns and best practices
- `/components` - UI component structure and organization
- `/clean-code-review` - Comprehensive code quality review

## Target Code

$ARGUMENTS
