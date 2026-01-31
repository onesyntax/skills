---
name: functions
description: Analyzes function structure. Uses the /functions skill.
model: opus
tools: Read, Glob, Grep, Edit, Write
---

Use the `/functions` skill to analyze and refactor functions in the code.

This agent applies Clean Code function principles by invoking the functions workflow.

## When Activated

- Reviewing functions for size, arguments, complexity, or structure issues
- When functions grow too large or complex
- When functions have too many arguments or side effects

## What This Agent Does

1. Invokes the `/functions` skill
2. Applies the comprehensive functions workflow from the skill
3. Checks function sizes, argument counts, abstraction levels
4. Identifies violations of Command-Query Separation
5. Suggests refactoring with Extract Method, Extract Class
6. Applies `/professional` standards for quality
