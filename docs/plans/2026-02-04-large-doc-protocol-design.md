# 大文档生成协议设计

> **For Claude:** 使用 superpowers:executing-plans 实现此计划。

**目标**：防止文档生成时因 token 限制导致 "Error writing file"

**架构**：在 jpreferences 中添加通用协议，覆盖所有文档生成场景

**技术栈**：Claude Code skill (Markdown)

---

## 背景

### 问题
- 使用 writing-plans skill 生成详细计划时频繁出现 "Error writing file"
- 原因：单文件内容超出 output token 限制

### 现状
- jpreferences 已有分文件规则，但不够系统化
- writing-plans 要求单文件输出，与 jpreferences 冲突

### 解决方案
- 创建通用的"大文档生成协议"
- 协议优先级高于其他 skill 的单文件要求

---

## 协议参数

| 参数 | 值 |
|------|-----|
| 阈值 | 250 行 |
| 目录结构 | 嵌套（overview + tasks/） |
| 触发方式 | 预判 + 失败回退 |

---

## 决策流程

```
生成文档前
    │
    ▼
估算内容大小
    │
    ├─ 明显 < 200 行 ──→ 单文件生成
    │
    ├─ 200-300 行 ──→ 尝试单文件
    │                    │
    │                    ├─ 成功 → 完成
    │                    └─ 失败 → 切换分文件
    │
    └─ 明显 > 300 行 ──→ 直接分文件
```

### 估算方法
- 任务数 × 50 行（每任务含代码块）
- 或：代码块数 × 25 行
- 取较大值

### 示例
- 3 个任务 → ~150 行 → 单文件
- 6 个任务 → ~300 行 → 边界，尝试后回退
- 10 个任务 → ~500 行 → 直接分文件

---

## 分文件结构

### 目录命名
```
docs/plans/YYYY-MM-DD-<topic>-overview.md
docs/plans/YYYY-MM-DD-<topic>-tasks/
  ├── 01-<task-name>.md
  ├── 02-<task-name>.md
  └── ...
```

### overview.md 内容
- 目标（1 句话）
- 架构概要（2-3 句）
- 技术栈
- 任务列表（带链接）
- 执行说明

### task 文件内容
- 完整的单个任务（Files、Steps、代码块）
- 控制在 250 行以内
- 包含返回 overview 的链接

---

## 适用范围

### 适用
- 使用 writing-plans 等 skill 生成计划
- 直接创建大型文档
- 编辑导致文件超过阈值

### 不适用
- 代码文件（有其他拆分标准）
- 已存在的大文件的小修改

---

## 实现任务

### Task 1: 更新 jpreferences SKILL.md

**Files:**
- Modify: `skills/jpreferences/SKILL.md`

**步骤:**
1. 将 "For Planning Documents" 部分替换为"大文档生成协议"
2. 添加决策流程图
3. 添加估算方法
4. 添加分文件结构说明
5. 添加与 writing-plans 的集成说明

**验收标准:**
- [ ] 协议作为独立章节存在
- [ ] 包含完整决策流程
- [ ] 包含估算方法和示例
- [ ] 明确说明与 writing-plans 的关系
