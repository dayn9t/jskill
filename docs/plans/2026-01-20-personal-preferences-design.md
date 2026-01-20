# Personal Preferences Skill - Design Document

**Date**: 2026-01-20
**Status**: Design Complete, Ready for Implementation

## Overview

A global personal preferences skill that automatically applies user preferences to all Claude Code conversations without manual invocation.

## User Requirements

1. **Chinese responses** - Improve reading efficiency
2. **Modern tech stack** - Prefer advanced, elegant, type-safe technologies
3. **Concise communication** - Reduce technical detail display
4. **Auto-load** - Apply to all projects automatically

## Design Decisions

### 1. Scope: Global Skill

**Decision**: Create a global skill in `~/.claude/skills/` that auto-loads via SessionStart hook

**Rationale**:
- User wants "all projects automatically"
- Personal preferences are consistent across projects
- Simple to maintain - one configuration for everything

**Alternatives Considered**:
- Project-level config: Rejected (requires per-project setup)
- Mixed approach: Rejected (over-engineering for this use case)

### 2. Language Rules

**Decision**: Chinese for dialogue, English for code/commits

**Rationale**:
- Improves user's reading efficiency (primary goal)
- Maintains industry standards (English code/commits)
- Aligns with international collaboration practices

**Specific Rules**:
- Dialogue/explanations → Chinese
- Code/variables/functions → English
- Commit messages → English
- Technical docs (README, API) → English
- Project docs (design, requirements) → Chinese

### 3. Technology Selection Strategy

**Decision**: Proactively choose modern tech, don't ask

**Rationale**:
- User wants "prefer advanced, elegant technologies"
- Asking defeats the purpose of having preferences
- Faster workflow - no decision paralysis

**Guidance**:
- Bun > pnpm > npm
- TypeScript strict mode
- Latest stable framework versions
- Modern tooling (esbuild, swc)
- Functional style when appropriate

### 4. Conciseness Level

**Decision**: Extreme minimalism - results only, hide process

**Rationale**:
- User selected "极简模式" (extreme minimalism)
- Show what was done, not how it was done
- Code examples: core logic only, omit boilerplate

**Implementation**:
- Avoid "Let me first..." phrases
- Tool results: brief summary, not full output
- Code blocks: <20 lines, use `// ...` for omissions
- Direct execution, minimal narration

### 5. Auto-Loading Mechanism

**Decision**: Use SessionStart hook in `~/.claude/settings.json`

**Rationale**:
- Automatic - no manual invocation needed
- Silent - doesn't interrupt workflow
- Persistent - applies to entire session

**Configuration**:
```json
{
  "hooks": {
    "SessionStart": "echo '/personal-preferences'"
  }
}
```

## Architecture

### Skill Type
**Rigid** - Must be followed exactly, not guidelines

### Token Budget
~400 words for main skill content (well within limits)

### Components

```
skills/personal-preferences/
├── SKILL.md          # Core skill (rigid rules + examples)
├── README.md         # Installation and usage guide
└── EXAMPLE.md        # Before/after comparisons
```

## Enforcement Mechanisms

### 1. Self-Check Table
Before every response, Claude checks:
- Language: Using Chinese for dialogue?
- Tech: Chose most modern option?
- Brevity: Can this be shorter?

### 2. Violation Table
Common mistakes and corrections:

| ❌ Wrong | ✅ Correct |
|---------|----------|
| English explanations | 中文解释 |
| Full boilerplate code | 核心逻辑 |
| "Should we use npm?" | 直接用 bun |
| "Let me first..." | 直接执行 |

### 3. Examples in Skill
Concrete before/after examples to guide behavior

## User Experience

### Installation
```bash
# One-time setup
cp -r skills/personal-preferences ~/.claude/skills/
# Edit ~/.claude/settings.json to add SessionStart hook
```

### Usage
- No manual invocation needed
- Automatically applies to all conversations
- User can override with explicit instructions

### Override Mechanism
```
User: 这次用英文详细解释
Claude: [follows user instruction, overrides preferences]
```

## Success Criteria

### Language
- ✅ 100% Chinese dialogue (unless user requests English)
- ✅ 100% English code/commits
- ✅ Appropriate mix in documentation

### Technology
- ✅ Always recommends modern stack
- ✅ No unnecessary option-asking
- ✅ Proactive decisions

### Conciseness
- ✅ No verbose process descriptions
- ✅ Code examples <20 lines
- ✅ Results-focused communication

## Implementation Plan

### Phase 1: Core Skill ✅
- [x] Create SKILL.md with rules and examples
- [x] Define enforcement mechanisms
- [x] Add self-check table

### Phase 2: Documentation ✅
- [x] Write README.md with installation guide
- [x] Create EXAMPLE.md with before/after comparisons
- [x] Document override mechanism

### Phase 3: Deployment (Next)
- [ ] Copy to ~/.claude/skills/
- [ ] Configure SessionStart hook
- [ ] Test in real conversations
- [ ] Iterate based on usage

## Testing Strategy

### Manual Testing
Test conversations covering:
1. Project initialization
2. Code review
3. Dependency installation
4. Technical decisions
5. Debugging
6. Git operations

### Validation Criteria
- Responses in Chinese ✓
- Modern tech choices ✓
- Concise communication ✓
- No unnecessary questions ✓

## Lessons from requirements-organizer

Applied learnings:
1. **Clear enforcement** - Rigid skill type, explicit rules
2. **Concrete examples** - Before/after comparisons
3. **Self-check mechanisms** - Violation table
4. **Token efficiency** - ~400 words, focused content

## Future Enhancements

Potential v2.0 features:
1. **Project-specific overrides** - `.claude/preferences.json` in project
2. **Preference profiles** - Switch between "work" and "personal" modes
3. **Learning mode** - Track which preferences are most useful
4. **Team preferences** - Share preferences with team members

## Conclusion

The personal-preferences skill provides:
- ✅ Automatic Chinese responses
- ✅ Proactive modern tech selection
- ✅ Concise, results-focused communication
- ✅ Zero-friction auto-loading

**Design Status**: Complete and validated
**Ready for**: Implementation and deployment
