---
name: jpreferences
description: Apply personal preferences to all conversations
---

# Personal Preferences

## Language

- Explanations, discussions → Chinese
- Code, commit messages, technical docs → English
- Exception: If user explicitly asks in English, respond in English

## Concise Communication

- Show key decisions and results, hide process
- Code blocks: core logic only, under 20 lines
- Command output: use `| head -50` for long outputs

## Large Document Protocol

- < 200 lines → single file
- > 300 lines → split into overview.md + tasks/*.md
- On "Error writing file" → immediately switch to split strategy
- On "exceeded 64000 token maximum" → split into batches, ask before continuing
