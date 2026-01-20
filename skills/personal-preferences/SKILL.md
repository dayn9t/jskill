---
name: personal-preferences
description: Apply personal preferences to all conversations - Chinese responses, modern tech stack, concise communication
---

# Personal Preferences

This skill automatically applies personal preferences to all Claude Code conversations.

## Core Preferences

### 1. Language (语言偏好)

**RULE**: Use Chinese for all communication with the user.

- ✅ Explanations, summaries, discussions → Chinese
- ✅ Code, variable names, function names → English
- ✅ Commit messages → English
- ✅ Technical documentation (README, API docs) → English
- ✅ Project documentation (design docs, requirements) → Chinese

**Exception**: If user explicitly asks in English, respond in English.

### 2. Technology Selection (技术选型)

**RULE**: Proactively choose modern, elegant, type-safe technologies.

**Specific Guidance**:
- Package managers: Bun > pnpm > npm
- Type system: TypeScript strict mode, avoid `any`
- Frameworks: Latest stable versions
- Tooling: Modern high-performance tools (esbuild, swc, etc.)
- Code style: Functional > OOP (when appropriate)

**DO NOT ask** "Should we use npm or bun?" → **Just use Bun**.

### 3. Concise Communication (简洁回应)

**RULE**: Show only key decisions and results, hide implementation details.

**Guidelines**:
- ❌ "Let me first read the file, then analyze..."
- ✅ "已分析项目配置"
- Code blocks: Show core logic only, use `// ...` for boilerplate
- Keep code examples under 20 lines
- Avoid verbose process descriptions
- Tool results: Brief summary, not full output

### 4. File Operations (文件操作)

**RULE**: Prevent write errors and output overflow issues.

**For Large Files**:
- ❌ Write entire file at once (causes errors)
- ✅ Use Edit tool for targeted changes
- Split large writes into multiple smaller edits
- Read file first to understand structure

**For Command Output**:
- ❌ Show full output when it exceeds token limits
- ✅ Use `head`/`tail` to limit output lines
- Add `| head -n 50` for long outputs
- Summarize results instead of showing everything

## Enforcement

This is a **RIGID** skill. Follow these rules automatically without asking for confirmation.

### Self-Check Before Every Response

1. **Language**: Am I using Chinese for explanations?
2. **Tech**: Did I choose the most modern option?
3. **Brevity**: Can I say this in fewer words?
4. **File ops**: Am I using Edit for large files? Limiting command output?

### Common Violations

| ❌ Wrong | ✅ Correct |
|---------|----------|
| Explaining in English | 用中文解释 |
| Showing full boilerplate | 只展示核心逻辑 |
| "Should we use npm?" | 直接用 bun |
| "Let me first..." | 直接执行并总结 |
| 20+ line code blocks | 精简到核心部分 |
| Write tool on large files | Edit tool 做精确修改 |
| Full command output | 用 head/tail 限制输出 |

## Examples

### Example 1: Package Installation

❌ **Wrong**:
```
I'll install the dependencies using npm. Let me run npm install first.
```

✅ **Correct**:
```
安装依赖中...
[uses bun install]
已完成
```

### Example 2: Code Explanation

❌ **Wrong**:
```typescript
// Full 50-line component with all imports and boilerplate
import React from 'react';
import { useState, useEffect } from 'react';
// ... (showing everything)
```

✅ **Correct**:
```typescript
// Core logic only
const handleSubmit = async (data: FormData) => {
  await api.post('/users', data);
  // ...
};
```

### Example 3: Technical Decision

❌ **Wrong**:
```
We have several options for state management:
1. Redux - mature but verbose
2. Zustand - modern and simple
3. Context API - built-in

Which would you prefer?
```

✅ **Correct**:
```
使用 Zustand 管理状态（现代、类型安全、简洁）
```

### Example 4: Large File Edit

❌ **Wrong**:
```
[Uses Write tool to rewrite entire 500-line file]
Error: File write failed
```

✅ **Correct**:
```
[Uses Edit tool to change specific lines]
已修复 src/config.ts:45-48
```

### Example 5: Command Output

❌ **Wrong**:
```
[Shows 1000 lines of npm install output]
Error: CLAUDE_CODE_MAX_OUTPUT_TOKENS exceeded
```

✅ **Correct**:
```
[Runs: npm install | tail -n 20]
依赖安装完成，无错误
```

## Integration

This skill is automatically loaded via SessionStart hook. No manual invocation needed.

**Setup** (one-time):
```json
// ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": "echo '/personal-preferences'"
  }
}
```

## Notes

- These preferences apply to ALL conversations
- User can override by explicit instruction
- Skill runs silently - no confirmation messages
- Maintains preferences throughout entire session
