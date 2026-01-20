---
name: requirements-organizer
description: Use when requirements change and need to be consolidated, restructured, and documented in a clear format with automatic file splitting to prevent context overload
version: 1.0.0
---

# Requirements Organizer

## Overview

Consolidates scattered requirement changes into structured, modular documentation. Combines existing requirements with new changes from conversation, organizes by functional modules, and automatically splits large files to prevent context overload.

## When to Use

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

**MANDATORY: Use TodoWrite to create a checklist from Phase 1-4 before starting.**

**Include one todo item for EACH module you identify:**
- [ ] Create [module-name] module
- [ ] Create [module-name] module
... (one per module)

Mark each as completed as you write it. This ensures you don't skip modules.

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

9. **Verify completeness**
   - **CRITICAL: Check that EVERY identified module has a file**
   - Count modules identified in Phase 2
   - Count files created in Phase 3
   - **If counts don't match, you're NOT done - create missing modules**
   - Verify all conversation changes are captured
   - All existing requirements are preserved or explicitly updated
   - No contradictions remain
   - All modules are properly linked
   - **Check your TodoWrite checklist - all module items must be completed**

10. **Handle old files**
    - If old monolithic requirement files exist (e.g., docs/requirements.md)
    - Add a note at the top: "⚠️ This file has been reorganized. See requirements/ directory for current documentation."
    - Report to user which old files exist and suggest they can be archived

11. **Report to user**
    - Summarize what was organized
    - List all created/updated files (count them)
    - Report: "Created X modules out of X identified" (must be 100%)
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
