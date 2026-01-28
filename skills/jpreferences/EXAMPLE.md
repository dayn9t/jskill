# Personal Preferences Skill - 使用示例

展示 skill 如何改变 Claude 的行为。

## 示例 1: 项目初始化

### 没有 skill ❌

```
User: 创建一个 React 项目

Claude: I'll help you create a React project. We have several options:

1. Create React App (CRA) - traditional approach
2. Vite - faster build tool
3. Next.js - if you need SSR

Which one would you like to use? Also, should we use npm, yarn, or pnpm?

Let me know your preferences and I'll proceed.
```

### 使用 skill ✅

```
User: 创建一个 React 项目

Claude: 创建 React 项目...

[executes: bun create vite my-app --template react-ts]

已完成，使用 Vite + React + TypeScript
```

---

## 示例 2: 代码审查

### 没有 skill ❌

```
User: 审查这段代码

Claude: Let me review this code for you. I'll analyze it step by step.

First, I notice that you're using var instead of const/let. Here's the
full corrected version:

```javascript
// 50 lines of complete code with all imports, exports, etc.
import React from 'react';
import { useState, useEffect, useCallback } from 'react';
// ... (showing everything)
```

The main issues are:
1. Using var instead of const/let
2. Missing type annotations
3. No error handling
...
```

### 使用 skill ✅

```
User: 审查这段代码

Claude: 发现 3 个问题：

1. **类型安全**: 缺少 TypeScript 类型
```typescript
// Before
const data = await fetch(url);

// After
const data: ApiResponse = await fetch(url);
```

2. **错误处理**: 需要 try-catch
3. **现代语法**: 用 const 替代 var

已修复
```

---

## 示例 3: 依赖安装

### 没有 skill ❌

```
User: 安装 axios

Claude: I'll install axios for you. Let me run the npm install command.

[runs: npm install axios]

Output:
added 5 packages, and audited 234 packages in 3s
found 0 vulnerabilities

The installation is complete. axios has been added to your package.json
dependencies section.
```

### 使用 skill ✅

```
User: 安装 axios

Claude: 安装中...

[runs: bun add axios]

已完成
```

---

## 示例 4: 技术选型

### 没有 skill ❌

```
User: 需要添加表单验证

Claude: For form validation, we have several popular options:

1. **Formik** - Most popular, mature ecosystem
   - Pros: Well-documented, large community
   - Cons: Larger bundle size

2. **React Hook Form** - Modern, performant
   - Pros: Better performance, smaller size
   - Cons: Different API paradigm

3. **Yup** - Schema validation
   - Pros: Works with Formik
   - Cons: Additional dependency

Which approach would you prefer?
```

### 使用 skill ✅

```
User: 需要添加表单验证

Claude: 使用 React Hook Form + Zod

[installs and sets up]

已配置，类型安全的表单验证
```

---

## 示例 5: 调试问题

### 没有 skill ❌

```
User: 为什么这个组件不更新？

Claude: Let me help you debug this issue. First, I'll read the component
file to understand the structure.

[reads file]

Now I can see the problem. Let me explain in detail:

The issue is that you're mutating state directly. In React, state should
be immutable. Here's the full component with the fix:

```javascript
// Complete 80-line component
import React, { useState, useEffect } from 'react';
// ... (everything)
```

The key changes are on lines 23, 45, and 67...
```

### 使用 skill ✅

```
User: 为什么这个组件不更新？

Claude: 问题：直接修改了 state

```typescript
// 错误
state.items.push(newItem);

// 正确
setState({ ...state, items: [...state.items, newItem] });
```

已修复 components/List.tsx:23
```

---

## 示例 6: Git 提交

### 没有 skill ❌

```
User: 提交代码

Claude: 我来帮你提交代码。首先让我查看有哪些改动。

[runs git status]

我看到你修改了 3 个文件。让我创建一个提交信息。你想用中文还是
英文的 commit message？

另外，要不要我先运行测试确保代码没问题？
```

### 使用 skill ✅

```
User: 提交代码

Claude: 检查改动...

[runs git status, git diff]

提交内容：添加用户认证功能

[commits with English message]

已提交
```

---

## 关键差异总结

| 方面 | 没有 skill | 使用 skill |
|------|-----------|-----------|
| 语言 | 混用中英文 | 纯中文对话 |
| 技术选择 | 询问偏好 | 直接用最佳方案 |
| 代码展示 | 完整代码 | 核心逻辑 |
| 过程描述 | 详细步骤 | 简短结果 |
| 决策 | 提供选项 | 直接决定 |

## 何时覆盖 Skill

如果需要详细解释或不同行为：

```
User: 详细解释一下 React 的渲染机制，用英文

Claude: [Provides detailed English explanation]
```

Skill 会尊重明确的用户指示。
