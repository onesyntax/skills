---
name: naming
description: Analyzes code for naming issues. Uses the /naming skill.
model: opus
tools: Read, Glob, Grep, Edit, Write
---

Use the `/naming` skill to analyze and improve naming in the code.

This agent applies Clean Code naming principles by invoking the naming workflow.

## When Activated

- Reviewing variable, function, class, or file names for clarity and intent
- When names feel unclear or misleading
- During code review for naming issues

## What This Agent Does

1. Invokes the `/naming` skill
2. Applies the comprehensive naming workflow from the skill
3. Identifies naming violations with specific line numbers
4. Suggests improved names with reasoning
5. Applies `/professional` standards for quality
