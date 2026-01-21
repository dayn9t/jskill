# Requirements Organizer Improvements - Design Document

## Design Date
2026-01-21

## Overview
This document outlines improvements to the requirements-organizer skill to address two critical issues identified through testing and user feedback:
1. Unwanted automatic triggering
2. Incomplete execution (only 15% of modules completed in tests)

## Problem Statement

### Problem 1: Automatic Triggering
**Current behavior**: The skill automatically triggers when users discuss requirement changes, even when they don't want to organize requirements yet.

**Root cause**: The description field contains trigger phrases like "when requirements change" that cause Claude to automatically invoke the skill.

**User impact**: Interrupts natural conversation flow, forces premature organization.

### Problem 2: Incomplete Execution
**Current behavior**: In testing, only 2 out of 13 identified modules were created (15% completion rate).

**Root cause**:
- Weak enforcement of TodoWrite checklist creation
- No verification that all identified modules are created
- Agent can rationalize stopping early without consequences

**User impact**: Incomplete documentation, missing modules, wasted effort.

## Design Goals

1. **Manual-only triggering**: Skill should only activate when explicitly invoked
2. **100% completion rate**: All identified modules must be created
3. **Maintain existing quality**: Keep all current quality improvements (templates, acceptance criteria, etc.)
4. **Minimal token overhead**: Keep skill concise and efficient

## Proposed Solution

### Solution 1: Modify Trigger Mechanism

#### Change 1.1: Update Description Field

**Current**:
```yaml
description: Use when requirements change and need to be consolidated, restructured, and documented in a clear format with automatic file splitting to prevent context overload
```

**Proposed**:
```yaml
description: Manual tool for consolidating scattered requirements into structured, modular documentation with automatic file splitting - invoke explicitly when organizing requirements
```

**Rationale**:
- Removes trigger phrase "when requirements change"
- Adds "Manual tool" to signal explicit invocation needed
- Adds "invoke explicitly" to reinforce manual nature
- Maintains clarity about what the tool does

#### Change 1.2: Update "When to Use" Section

Add explicit statement at the beginning:

```markdown
## When to Use

**This is a MANUAL tool. Only use when explicitly requested by the user.**

Invoke this skill when the user says:
- "Use requirements-organizer"
- "/requirements-organizer"
- "Organize our requirements"
- Similar explicit requests

Do NOT auto-invoke when:
- User mentions requirement changes in passing
- Requirements are discussed but not ready to organize
- User hasn't explicitly asked for organization
```

### Solution 2: Fix Completeness Issues

#### Change 2.1: Strengthen TodoWrite Enforcement

**Location**: "The Process" section, before Phase 1

**Current**:
```markdown
**MANDATORY: Use TodoWrite to create a checklist from Phase 1-4 before starting.**

**Include one todo item for EACH module you identify:**
- [ ] Create [module-name] module
- [ ] Create [module-name] module
... (one per module)

Mark each as completed as you write it. This ensures you don't skip modules.
```

**Proposed**:
```markdown
**MANDATORY FIRST STEP: Use TodoWrite BEFORE doing anything else.**

You MUST create a checklist with:
1. Phase markers (Discovery, Analysis, Documentation, Validation)
2. ONE item for EACH module (add after Phase 2 when modules are identified)

Example structure:
- [ ] Phase 1: Discovery - locate existing requirements
- [ ] Phase 2: Analysis - identify modules
- [ ] Create [module-1] module
- [ ] Create [module-2] module
- [ ] Create [module-3] module
... (one per module)
- [ ] Phase 3: Create README.md
- [ ] Phase 4: Validation - verify completeness

**CRITICAL**: Mark each module as completed IMMEDIATELY after writing it.
**CRITICAL**: You are NOT done until ALL module items are marked completed.
```

**Rationale**:
- More explicit about when to create checklist (BEFORE anything else)
- Shows concrete example structure
- Emphasizes marking items completed immediately
- Adds explicit "NOT done until ALL completed" statement

#### Change 2.2: Add Module Counting Requirement

**Location**: Phase 2, step 4 "Organize by modules"

**Add after existing content**:
```markdown
**After identifying modules, COUNT them and report:**
- "Identified X functional modules: [list names]"
- Add X todo items to your TodoWrite checklist (one per module)
- This count will be verified in Phase 4
```

#### Change 2.3: Strengthen Phase 4 Validation

**Location**: Phase 4, step 9 "Verify completeness"

**Current** (first bullet):
```markdown
- **CRITICAL: Check that EVERY identified module has a file**
```

**Proposed** (replace entire step 9):
```markdown
9. **Verify completeness (MANDATORY)**

   **Step 1: Count verification**
   - Count modules identified in Phase 2: X modules
   - Count module files created in Phase 3: Y files
   - Count completed module todos in TodoWrite: Z items
   - **If X ≠ Y ≠ Z, you are NOT done**

   **Step 2: List missing modules**
   - If any counts don't match, list missing modules by name
   - Create each missing module immediately
   - Mark each as completed in TodoWrite

   **Step 3: Content verification**
   - Verify all conversation changes are captured
   - All existing requirements are preserved or explicitly updated
   - No contradictions remain
   - All modules are properly linked
   - README.md exists and lists all modules

   **Step 4: TodoWrite verification**
   - Check your TodoWrite checklist
   - ALL module items must show "completed" status
   - If any are not completed, you are NOT done

   **You can only proceed to step 10 when all counts match and all todos are completed.**
```

**Rationale**:
- Triple verification: module count, file count, todo count
- Explicit "NOT done" language
- Step-by-step verification process
- Blocks progression until complete

#### Change 2.4: Add Completion Report Requirement

**Location**: Phase 4, step 11 "Report to user"

**Current**:
```markdown
11. **Report to user**
    - Summarize what was organized
    - List all created/updated files (count them)
    - Report: "Created X modules out of X identified" (must be 100%)
    - Highlight any ambiguities or decisions made
    - Suggest archiving old files if they exist
```

**Proposed** (add at the beginning):
```markdown
11. **Report to user**

    **MANDATORY: Include these metrics in your report:**
    - Modules identified: X
    - Modules created: X (must match)
    - Files written: Y
    - Completion rate: 100% (anything less means you're not done)

    Then include:
    - Summary of what was organized
    - List all created/updated files
    - Highlight any ambiguities or decisions made
    - Suggest archiving old files if they exist
```

#### Change 2.5: Update Red Flags Table

**Location**: "Red Flags" section

**Add new entries**:
```markdown
| Thought | Reality |
|---------|---------|
| "I've created the main modules" | ALL modules must be created, not just main ones |
| "I'll create the rest later" | Complete ALL modules now, not later |
| "The user can create remaining modules" | Your job is to create ALL modules |
| "I've done enough for now" | Check TodoWrite - all items must be completed |
```

## Implementation Changes Summary

### Files to Modify

**1. skills/requirements-organizer/SKILL.md**
- Line 3: Update description field
- Line 13-26: Update "When to Use" section
- Line 35-42: Strengthen TodoWrite requirement
- Line 64: Add module counting requirement
- Line 122-131: Replace step 9 with enhanced verification
- Line 138-143: Add metrics to step 11
- Line 244-255: Add new red flag entries

**2. skills/requirements-organizer/README.md**
- Line 3: Update description to match SKILL.md
- Line 39-51: Update "Usage" section to emphasize manual invocation

**3. skills/requirements-organizer/EXAMPLE.md**
- Line 155-161: Update "How to Invoke" section to emphasize explicit invocation

### Estimated Changes
- Total lines modified: ~50 lines
- Total lines added: ~40 lines
- Token impact: +150 tokens (still well under 500 word target for main content)

## Testing Strategy

### Test 1: Trigger Mechanism
**Objective**: Verify skill doesn't auto-trigger

**Scenario**:
1. Start conversation about adding new features
2. Mention "we need to add authentication and payment processing"
3. Discuss requirements without explicitly invoking skill

**Expected**: Skill should NOT trigger automatically

**Success criteria**: Agent discusses requirements but doesn't invoke requirements-organizer

### Test 2: Completeness Enforcement
**Objective**: Verify 100% module completion

**Scenario**: Use existing test-pressure.md scenario (13 modules)

**Expected**:
- TodoWrite checklist created with 13 module items
- All 13 modules created
- All 13 todos marked completed
- Verification report shows 13/13 completion

**Success criteria**:
- 13 module files exist
- README.md lists all 13 modules
- Report shows "Modules identified: 13, Modules created: 13, Completion rate: 100%"

### Test 3: Manual Invocation
**Objective**: Verify skill works when explicitly invoked

**Scenario**: Say "Use requirements-organizer to organize our requirements"

**Expected**: Skill triggers and executes normally

**Success criteria**: Skill activates and completes successfully

## Rollout Plan

### Phase 1: Implementation
1. Update SKILL.md with all changes
2. Update README.md with trigger mechanism changes
3. Update EXAMPLE.md with invocation guidance

### Phase 2: Testing
1. Run Test 1 (no auto-trigger)
2. Run Test 2 (completeness enforcement)
3. Run Test 3 (manual invocation)

### Phase 3: Documentation
1. Update PROJECT-SUMMARY.md with v1.1.0 changes
2. Create test-results-v1.1.0.md documenting improvements
3. Update version number in SKILL.md to 1.1.0

## Success Metrics

### Trigger Mechanism
- ✅ Skill does NOT auto-trigger in casual requirement discussions
- ✅ Skill DOES trigger when explicitly invoked
- ✅ Description clearly indicates manual tool

### Completeness
- ✅ 100% module completion rate (was 15%)
- ✅ TodoWrite checklist created before starting
- ✅ All todos marked completed
- ✅ Verification report shows matching counts

### Quality Maintenance
- ✅ All existing quality features preserved (templates, acceptance criteria, etc.)
- ✅ Token usage remains under target (<500 words main content)
- ✅ No regression in file size management or splitting logic

## Risks and Mitigations

### Risk 1: Over-enforcement
**Risk**: Too many verification steps might make skill feel bureaucratic

**Mitigation**: Verification steps are quick checks, not complex operations. Total overhead: ~30 seconds

### Risk 2: Token Overhead
**Risk**: Additional enforcement text increases token usage

**Mitigation**: Changes add ~150 tokens, still well under budget. Main skill content remains ~600 words (target: <500 for core, but enforcement is critical)

### Risk 3: User Confusion
**Risk**: Users might not know how to invoke skill

**Mitigation**:
- Clear documentation in README
- Examples in EXAMPLE.md
- Description field explains invocation

## Future Enhancements (Out of Scope)

These improvements focus on trigger mechanism and completeness. Future versions could add:
- Automatic requirement ID generation
- Requirement traceability matrix
- Progress indicators during execution
- Incremental organization (add to existing structure)

## Conclusion

These improvements address the two critical issues identified in testing:
1. **Unwanted auto-triggering** → Manual-only invocation
2. **Incomplete execution (15%)** → 100% completion enforcement

The changes are focused, minimal, and maintain all existing quality improvements while adding strong completeness guarantees.

**Estimated implementation time**: Changes are straightforward text edits to existing files.

**Expected outcome**:
- Zero auto-trigger incidents
- 100% module completion rate
- Maintained quality and user satisfaction
