---
name: requirements-organizer
description: Manual tool for consolidating scattered requirements into structured, modular documentation with automatic file splitting - invoke explicitly when organizing requirements
version: 1.1.0
---

# Requirements Organizer

## Overview

Consolidates scattered requirement changes into structured, modular documentation. Combines existing requirements with new changes from conversation, organizes by functional modules, and automatically splits large files to prevent context overload.

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

Use this skill when:
- Requirements have changed and need to be updated in documentation
- Multiple requirement changes are scattered across conversation history
- Existing requirement docs need to be merged with new changes
- Requirements are growing too large and need modular organization
- You need to prevent single files from becoming too large (>1000 lines)

Do NOT use when:
- Just starting a new project with no existing requirements
- Only making trivial wording changes to existing docs
- Requirements are already well-organized and no changes occurred

## The Iron Law

**ALWAYS create modular structure. NEVER update monolithic files in place.**

Violating this rule creates context overload and write failures. No exceptions.

## The Process

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

### Phase 1: Discovery

1. **Locate existing requirements**
   - Search for common requirement file patterns: `requirements/`, `docs/requirements/`, `REQUIREMENTS.md`, `specs/`
   - Check project root and common documentation directories
   - If found, read and analyze existing structure
   - **DO NOT modify existing files in place** - you will create new modular structure

2. **Extract conversation changes**
   - Review recent conversation history for requirement changes
   - Identify: new features, modifications, removals, clarifications
   - Note any explicit user statements about requirements

### Phase 2: Analysis

3. **Merge and deduplicate**
   - Combine existing requirements with new changes
   - Remove duplicates and contradictions (new changes take precedence)
   - Identify functional modules (user management, payment, reporting, etc.)

4. **Organize by modules**
   - Group requirements by functional area
   - Maintain clear boundaries between modules
   - Identify cross-module dependencies

**After identifying modules, COUNT them and report:**
- "Identified X functional modules: [list names]"
- Add X todo items to your TodoWrite checklist (one per module)
- This count will be verified in Phase 4

### Phase 3: Documentation

5. **Structure each module**
   - **EVERY module MUST use this exact template. No exceptions.**
     ```markdown
     # [Module Name]

     ## Overview
     Brief description and core objectives

     ## Requirements

     ### Functional Requirements
     - **REQ-[ID]**: [Requirement description]
       - Acceptance: [How to verify]
       - Priority: [High/Medium/Low]

     ## Implementation Notes
     Technical constraints, architecture decisions, key considerations

     ## Acceptance Criteria
     - [ ] [Testable criterion 1]
     - [ ] [Testable criterion 2]

     ## Dependencies
     Other modules or external systems this depends on
     ```

6. **Check file sizes BEFORE writing**
   - Count lines in your prepared content
   - Target: Keep files under 1000 lines or ~4000 tokens
   - **If approaching 900 lines, MUST split before writing**
   - Use `wc -l` or count manually to verify

7. **Intelligent splitting (when needed)**
   - Analyze logical boundaries within the module
   - Split strategies (in priority order):
     a. **By sub-feature** - Natural functional subdivisions (e.g., "User Management" → "Registration", "Authentication", "Profile")
     b. **By section** - If sub-features aren't clear, split by major sections (Overview+Requirements in part 1, Implementation+Criteria in part 2)
     c. **By logical groups** - Group related requirements that form coherent units

   - Naming convention: `module-name-subfeature.md` or `module-name-part1.md`
   - Create index file: `module-name-index.md` linking to all parts

8. **Write documentation**
   - **FIRST: Create requirements/README.md with module overview and navigation**
   - Create directory structure: `requirements/[module-name]/`
   - Write each file with clear, concise content
   - Add cross-references between related modules
   - Mark each module as completed in your TodoWrite checklist as you finish it

### Phase 4: Validation

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

10. **Handle old files**
    - If old monolithic requirement files exist (e.g., docs/requirements.md)
    - Add a note at the top: "⚠️ This file has been reorganized. See requirements/ directory for current documentation."
    - Report to user which old files exist and suggest they can be archived

11. **Report to user**

    **MANDATORY: Include these metrics in your report:**
    - Modules identified: X
    - Modules created: X (must match)
    - Files written: Y
    - Completion rate: 100% (anything less means you're not done)

    Then include:
    - Summarize what was organized
    - List all created/updated files (count them)
    - Highlight any ambiguities or decisions made
    - Suggest archiving old files if they exist

## File Size Guidelines

**Target limits per file:**
- Maximum: 1000 lines
- Maximum: ~4000 tokens
- Ideal: 500-800 lines for frequently-accessed modules

**Why these limits:**
- Reduces write failures
- Improves maintainability
- Minimizes context window pressure
- Forces better modularization

## Document Structure Template

```markdown
# [Module Name]

## Overview
[2-3 sentences describing the module's purpose and scope]

## Requirements

### Functional Requirements
- **REQ-[ID]**: [Requirement description]
  - Acceptance: [How to verify]
  - Priority: [High/Medium/Low]

### Non-Functional Requirements
- **NFR-[ID]**: [Performance, security, scalability requirements]

## Implementation Notes

### Architecture Decisions
- [Key technical decisions and rationale]

### Technical Constraints
- [Limitations, dependencies, technology choices]

### Data Models
- [Key entities and relationships if applicable]

## Acceptance Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## Dependencies

### Internal Dependencies
- [Other modules this depends on]

### External Dependencies
- [Third-party services, APIs, libraries]

## Change History

- [Date]: [Summary of changes]
```

## Intelligent Splitting Example

**Before splitting** (1500 lines):
```
requirements/user-management.md
```

**After intelligent splitting**:
```
requirements/user-management/
  ├── index.md                    # Overview and navigation
  ├── registration.md             # User registration sub-feature
  ├── authentication.md           # Login, logout, session management
  ├── profile-management.md       # User profile CRUD operations
  └── permissions.md              # Role-based access control
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **Updating existing files in place** | **ALWAYS create new modular structure** |
| **Omitting acceptance criteria** | **EVERY requirement MUST have acceptance criteria** |
| **Skipping the template** | **EVERY module MUST use the standard template** |
| **Not checking file size before writing** | **Count lines BEFORE writing, split at 900 lines** |
| Splitting too early | Only split when approaching 1000 lines, not preemptively |
| Arbitrary splits | Always split at logical boundaries, never mid-requirement |
| Losing context | Always create index files when splitting |
| Ignoring existing docs | Always read and merge with existing requirements |
| Over-engineering structure | Keep it simple - only add complexity when needed |
| Missing cross-references | Link related modules explicitly |
| **No navigation README** | **ALWAYS create README.md with module overview** |

## Red Flags

These thoughts mean STOP - you're doing it wrong:

| Thought | Reality |
|---------|---------|
| "I'll just update the existing file" | Monolithic files cause context overload and write failures |
| "I'll create one big file" | Large files fail to write and overload context |
| "Single file is more cohesive" | Modular structure provides BETTER cohesion and maintainability |
| "I'll maintain the existing format" | Consistency with poor structure perpetuates problems |
| "Single pass is more efficient" | Proper structure saves MORE time long-term |
| "Moderate detail is enough" | Missing acceptance criteria makes requirements incomplete |
| "I'll split alphabetically" | Split by logical boundaries, not arbitrary rules |
| "I don't need to read existing docs" | Always merge with existing requirements |
| "This module is too small to document" | Even small modules need structure for consistency |
| "I'll organize this my own way" | Follow the template for consistency |
| "I've created the main modules" | ALL modules must be created, not just main ones |
| "I'll create the rest later" | Complete ALL modules now, not later |
| "The user can create remaining modules" | Your job is to create ALL modules |
| "I've done enough for now" | Check TodoWrite - all items must be completed |

**All of these mean: Follow the process. Create modular structure. Use the template.**

## Rationalization Table

Common excuses and why they're wrong:

| Rationalization | Reality |
|----------------|---------|
| "Update existing files for continuity" | Monolithic files cause context overload and write failures |
| "Single file is more cohesive" | Modular structure provides better cohesion and maintainability |
| "Maintain existing format for consistency" | Consistency with poor structure perpetuates problems |
| "Single pass is efficient" | Proper structure saves more time long-term |
| "Moderate detail is enough" | Missing acceptance criteria makes requirements incomplete |
| "Manual process is straightforward" | Systematic process ensures completeness and prevents errors |

## Key Principles

1. **Merge, don't replace** - Preserve existing requirements unless explicitly superseded
2. **Modular by function** - Organize by what the system does, not how it's built
3. **Size matters** - Keep files small to prevent failures and context overload
4. **Logical boundaries** - Split at natural seams, never arbitrarily
5. **Navigable structure** - Always provide clear navigation between modules
6. **Executable documentation** - Write requirements that can guide implementation
7. **Change tracking** - Document what changed and why

## Success Criteria

You've succeeded when:
- ✅ All requirement changes from conversation are captured
- ✅ Existing requirements are merged and updated appropriately
- ✅ Requirements are organized into clear functional modules
- ✅ **EVERY module uses the standard template (no exceptions)**
- ✅ No single file exceeds 1000 lines or 4000 tokens
- ✅ All splits maintain logical coherence
- ✅ Navigation between modules is clear (README.md exists)
- ✅ **Modular directory structure created (requirements/[module-name]/)**
- ✅ User can immediately understand what changed and where to find it

## Mandatory Checklist

**Create this checklist with TodoWrite before starting:**

- [ ] Search for existing requirements in multiple locations
- [ ] Read and analyze all existing requirement files
- [ ] Extract all requirement changes from conversation
- [ ] Identify functional modules
- [ ] Create `requirements/` directory structure
- [ ] Apply standard template to EVERY module
- [ ] Add acceptance criteria to EVERY requirement
- [ ] Document dependencies between modules
- [ ] Check file sizes (must be < 1000 lines) BEFORE writing
- [ ] Split any files approaching 900 lines
- [ ] Create navigation README.md
- [ ] Verify all conversation changes are captured
- [ ] Report summary to user
