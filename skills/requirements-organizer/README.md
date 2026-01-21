# Requirements Organizer Skill

A Claude Code skill for organizing and structuring software requirements documentation with automatic modularization and file splitting.

## Overview

This skill helps consolidate scattered requirement changes into structured, modular documentation. It combines existing requirements with new changes from conversation, organizes by functional modules, and automatically splits large files to prevent context overload.

**This is a MANUAL tool** - it must be explicitly invoked and will not trigger automatically.

## When to Use

Use this skill when:
- Requirements have changed and need to be updated in documentation
- Multiple requirement changes are scattered across conversation history
- Existing requirement docs need to be merged with new changes
- Requirements are growing too large and need modular organization
- You need to prevent single files from becoming too large (>1000 lines)

## Installation

### For Claude Code CLI

1. Copy the `requirements-organizer` directory to your skills location:
   ```bash
   cp -r requirements-organizer ~/.claude/skills/
   ```

2. Or symlink it:
   ```bash
   ln -s /path/to/requirements-organizer ~/.claude/skills/requirements-organizer
   ```

3. Restart Claude Code or reload skills

### For Claude Code in IDE

1. Copy the skill to your project's `.claude/skills/` directory
2. The skill will be automatically available

## Usage

**This skill must be explicitly invoked - it will not trigger automatically.**

To use the skill, explicitly request it:

```
User: Use requirements-organizer to organize our requirements
```

Or:

```
User: /requirements-organizer
```

Or:

```
User: Organize our requirements with the requirements-organizer skill
```

The skill will NOT auto-trigger when you simply discuss requirements. You must explicitly invoke it.

## What It Does

1. **Discovers existing requirements** - Searches for and reads existing requirement files
2. **Extracts changes** - Identifies new requirements from conversation history
3. **Merges and organizes** - Combines existing + new requirements into functional modules
4. **Creates modular structure** - Generates `requirements/[module-name]/` directories
5. **Applies standard template** - Every module follows consistent structure
6. **Manages file sizes** - Keeps files under 1000 lines, splits intelligently if needed
7. **Adds navigation** - Creates README with module overview
8. **Verifies completeness** - Ensures all requirements are captured

## Output Structure

```
requirements/
├── README.md                           # Module overview and navigation
├── authentication/
│   └── authentication.md               # Auth requirements
├── payment/
│   └── payment.md                      # Payment requirements
├── shopping-cart/
│   └── shopping-cart.md                # Cart requirements
└── ...
```

Each module file contains:
- Overview
- Requirements (with IDs and acceptance criteria)
- Implementation Notes
- Acceptance Criteria checklist
- Dependencies
- Change History

## Key Features

- **Modular by default** - Never creates monolithic files
- **Size-aware** - Automatically splits files exceeding 1000 lines
- **Template-driven** - Consistent structure across all modules
- **Acceptance criteria** - Every requirement has testable criteria
- **Dependency tracking** - Documents inter-module dependencies
- **Change tracking** - Records what changed and when

## Testing

The skill includes comprehensive tests:
- `test-pressure.md` - Pressure test scenario
- `baseline-analysis.md` - Analysis of behavior without skill
- `test-results-analysis.md` - Comparison of baseline vs with-skill

To run tests:
```bash
cd skills/requirements-organizer
# Follow instructions in test-pressure.md
```

## Development

This skill was developed using TDD (Test-Driven Development) following the superpowers:writing-skills methodology:

1. **RED phase** - Created pressure test, ran baseline without skill
2. **GREEN phase** - Implemented skill to address violations
3. **REFACTOR phase** - Refined skill based on test results

## Version History

- **1.1.0** (2026-01-21) - Trigger mechanism and completeness improvements
  - Changed to manual-only triggering (no auto-invoke)
  - Strengthened TodoWrite enforcement
  - Added triple verification (module count, file count, todo count)
  - Enhanced Phase 4 validation with step-by-step checks
  - Added completion metrics to user reports
  - Updated red flags table with completeness checks
- **1.0.0** (2026-01-20) - Initial release
  - Modular structure creation
  - Standard template enforcement
  - File size management
  - Intelligent splitting
  - Completeness verification

## License

MIT

## Contributing

Improvements welcome! Please:
1. Add tests for new features
2. Follow the existing template structure
3. Keep token usage minimal
4. Test with multiple models (Haiku, Sonnet, Opus)

## Support

For issues or questions:
- Check the test files for examples
- Review the SKILL.md for detailed process
- Open an issue in the repository
