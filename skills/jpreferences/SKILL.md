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

**For Command Output**:
- ❌ Show full output when it exceeds token limits
- ✅ Use `head`/`tail` to limit output lines
- Add `| head -n 50` for long outputs
- Summarize results instead of showing everything

## 大文档生成协议

**强制要求**：生成任何文档前必须执行此协议。此协议优先级高于其他 skill（包括 writing-plans）的单文件要求。

### 决策流程

```
生成文档前 → 估算内容大小
    │
    ├─ < 200 行 ────→ 单文件生成
    ├─ 200-300 行 ──→ 尝试单文件，失败则分文件
    └─ > 300 行 ────→ 直接分文件
```

### 估算方法

取以下较大值：
- 任务数 × 50 行
- 代码块数 × 25 行

| 任务数 | 估算行数 | 策略 |
|--------|----------|------|
| 3 | ~150 | 单文件 |
| 5 | ~250 | 尝试单文件 |
| 6+ | >300 | 直接分文件 |

### 分文件结构

```
docs/plans/YYYY-MM-DD-<topic>-overview.md
docs/plans/YYYY-MM-DD-<topic>-tasks/
  ├── 01-<task-name>.md    (< 250 行)
  ├── 02-<task-name>.md    (< 250 行)
  └── ...
```

**overview.md 内容**：目标、架构、技术栈、任务列表（带链接）

**task 文件内容**：完整单个任务 + 返回 overview 链接

### 失败回退

遇到 "Error writing file" 时：
1. 不要重试相同方法
2. 立即切换分文件策略
3. 告知用户："内容较多，已切换分文件生成"

### 适用范围

- ✅ 使用 writing-plans 等 skill 生成计划
- ✅ 直接创建设计文档、需求文档
- ❌ 代码文件（用 Edit 工具修改）
- ❌ 已存在大文件的小修改

## 输出 Token 限制协议

**问题**：Claude 响应超过 64000 token 限制时会报错：
```
API Error: Claude's response exceeded the 64000 output token maximum
```

### 预防策略

**生成代码前估算**：
| 内容类型 | 估算 tokens | 策略 |
|----------|-------------|------|
| < 500 行代码 | ~10K | 正常生成 |
| 500-1000 行 | ~20K | 分批生成 |
| > 1000 行 | >40K | 必须分批 |

**分批生成方法**：
1. 先生成核心文件（models、ports）
2. 等待用户确认后继续
3. 再生成实现文件（services、adapters）
4. 最后生成测试文件

### 响应时自检

每次响应前检查：
- 是否要生成多个完整文件？→ 分批
- 是否要展示大量代码？→ 只展示核心部分
- 是否要输出长命令结果？→ 用 `| head -50` 限制

### 遇到错误时

如果收到 `exceeded the 64000 output token maximum` 错误：
1. **不要重试相同内容**
2. 告知用户："响应过长，分批处理"
3. 只生成第一部分，询问是否继续

### 示例

❌ **错误**：一次性生成 10 个文件
```
[生成 models.py]
[生成 ports.py]
[生成 services.py]
[生成 adapters.py]
[生成 5 个测试文件]
→ API Error: exceeded 64000 token maximum
```

✅ **正确**：分批生成
```
第一批：生成核心模型
- models.py ✅
- ports.py ✅

继续生成实现层？(y/n)
```

## Enforcement

This is a **RIGID** skill. Follow these rules automatically without asking for confirmation.

### Self-Check Before Every Response

1. **Language**: Am I using Chinese for explanations?
2. **Tech**: Did I choose the most modern option?
3. **Brevity**: Can I say this in fewer words?
4. **File ops**: Am I using Edit for large files? Limiting command output?
5. **Doc protocol**: 生成文档前是否执行了大文档生成协议？
6. **Output tokens**: 响应是否可能超过 64K tokens？需要分批吗？

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
| 6+ 任务的计划写单文件 | 执行大文档生成协议，直接分文件 |
| Retry same approach on error | 识别 token 限制，切换策略 |
| 一次生成 10+ 个文件 | 分批生成，每批 3-4 个文件 |
| 响应超 64K tokens | 分批处理，询问是否继续 |

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
[Uses writing-plans skill with 8 tasks]
[Tries to write single file]
Error writing file
Error writing file
[Keeps retrying]
```

✅ **Correct**:
```
估算：8 任务 × 50 = 400 行 > 300，执行分文件策略

已创建：
- docs/plans/2026-02-04-feature-overview.md
- docs/plans/2026-02-04-feature-tasks/01-setup.md
- docs/plans/2026-02-04-feature-tasks/02-api.md
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
