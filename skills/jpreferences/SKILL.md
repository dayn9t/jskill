---
name: jpreferences
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

**For Planning Documents**:

**识别"详细计划"场景**（容易触发输出 token 限制）：
- 包含 5+ 个大型代码块（每个 >20 行）
- 包含完整的 Schema 定义、API 设计、多个任务详情
- 用户明确要求"详细的"、"完整的"、"包含代码示例"

**应对策略 - 分文件生成**：
- ❌ 一次性生成包含所有细节的单个文件
- ✅ 拆分成多个文件（混合拆分策略）：
  ```
  docs/plans/YYYY-MM-DD-topic-overview.md       # 总览（目标、架构概要、文件导航）
  docs/plans/YYYY-MM-DD-topic-design.md         # 技术设计（Schema、API、数据流）
  docs/plans/YYYY-MM-DD-topic-tasks/            # 任务目录
    ├── task1-xxx.md                            # 任务1详情（< 300 行）
    ├── task2-xxx.md                            # 任务2详情（< 300 行）
    └── ...
  ```
- ✅ 每个文件控制在 300 行以内
- ✅ overview.md 作为入口，包含到其他文件的链接

**失败后的应对**：
- 如果遇到 "Error writing file" 且重试多次失败
- 识别为 token 限制问题
- 立即切换到分文件策略
- 告知用户："检测到内容较多，已切换为分文件生成"

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
| Detailed plan in one file | 分文件生成（overview + design + tasks/） |
| Retry same approach on error | 识别 token 限制，切换策略 |

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

### Example 6: Large Planning Document

❌ **Wrong**:
```
现在让我创建 Phase 2 的详细实施计划...
[Tries to write 1500-line plan with 10+ code blocks in one file]
Error writing file
Error writing file
Error writing file
[Keeps retrying the same approach]
```

✅ **Correct**:
```
检测到这是详细实施计划（包含 Schema、API 设计、8 个任务），将分文件生成：

已创建：
- docs/plans/2026-01-21-phase2-overview.md (总览)
- docs/plans/2026-01-21-phase2-design.md (技术设计)
- docs/plans/2026-01-21-phase2-tasks/task1-init.md
- docs/plans/2026-01-21-phase2-tasks/task2-crud.md
...

从 overview.md 开始查看。
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
