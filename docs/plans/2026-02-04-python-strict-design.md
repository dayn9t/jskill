# Python Strict Skill Design

## Overview

**Name**: `python-strict`

**Purpose**: Modern Python strict development practices, focusing on type safety, elegant code, and engineering standards. Complements `python-patterns` with emphasis on "strict" and "modern".

**Target**: New project setup with strictest standards from the start.

## Three Pillars

### Pillar 1: Type Safety

- mypy `strict = true` full configuration
- Advanced types: TypeGuard/TypeIs, TypedDict, Literal, Final, @overload
- Pydantic v2 strict mode (`strict=True`, `extra='forbid'`)
- Common type errors and fixes

### Pillar 2: Code Elegance

- SOLID principles in Python
- Protocol over inheritance (duck typing)
- Dependency injection patterns
- Result type error handling (alternative to exceptions)
- Functional programming patterns

### Pillar 3: Engineering Standards

- uv project management (replaces pip/poetry)
- ruff complete rule configuration
- pre-commit hooks
- Project structure template
- CI/CD configuration examples

## Relationship with python-patterns

| Aspect | python-patterns | python-strict |
|--------|-----------------|---------------|
| Type hints | Basic (Optional, List, Dict) | Advanced (TypeGuard, TypedDict, Literal) |
| mypy config | 3 options | Full strict mode |
| Project tools | pip, pyproject.toml basics | uv, ruff, pre-commit |
| Design patterns | Basic patterns | SOLID, DI, Result type |
| Pydantic | Not covered | v2 strict mode |

## File Location

`~/.claude/skills/python-strict/SKILL.md`

## Estimated Length

~400-500 lines (with code examples)
