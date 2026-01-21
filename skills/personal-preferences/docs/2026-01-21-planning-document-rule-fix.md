# Planning Document Rule Fix - 设计文档

**日期**: 2026-01-21
**问题**: "Error writing file" 在生成详细计划文档时反复出现
**状态**: ✅ 已解决

---

## 问题分析

### 原始错误信息

```
● 现在让我创建 Phase 2 的详细实施计划...
  ⎿  Error writing file
  ⎿  Error writing file
  ⎿  Error writing file
  ⎿  Error writing file

● 让我创建 Phase 2 的实施计划文档。
  ⎿  Error writing file
  ⎿  Error writing file
  ⎿  Error writing file

[... 重复多次 ...]

● 让我重新开始，正确创建 Phase 2 计划文档：
● Write(docs/plans/2026-01-21-phase2-duckdb-metadata-layer.md)
  ⎿  Wrote 482 lines to docs/plans/2026-01-21-phase2-duckdb-metadata-layer.md
```

### 关键发现

1. **文件最终成功写入**：481 行，12,374 字节
2. **前 4 次尝试失败**：每次都有多个 "Error writing file"
3. **第 5 次成功**：只有 1 次 Write 调用

### 错误的假设（v1.0 规则）

```markdown
**For Planning Documents**:
- ❌ Write 1000+ line implementation plans in one file
- ✅ Split into multiple smaller files (< 500 lines each)
```

**为什么这是错的**：
- ❌ 481 行的文件最终成功了，说明不是行数限制
- ❌ 12KB 的文件很小，说明不是文件大小限制
- ✅ 真正的问题是**生成过程中的输出 token 限制**

---

## 根本原因

### Token 限制问题

Claude 在生成详细计划时：
1. 尝试一次性生成包含大量代码块、表格、详细说明的内容
2. 生成过程中超出单次响应的 token 限制
3. 触发 "Error writing file"
4. 自动重试，但每次都在同样的地方失败
5. 最后一次"重新开始"时，可能调整了生成策略（更简洁的描述），才成功

### 详细计划的特征

容易触发 token 限制的内容：
- 5+ 个大型代码块（每个 >20 行）
- 完整的 Schema 定义（SQL DDL）
- 完整的 API 设计（Rust 接口定义）
- 8+ 个详细任务分解（每个包含子任务、验收标准）
- 大量表格（性能目标、风险矩阵等）

---

## 解决方案

### 新规则设计（v2.0）

#### 1. 识别"详细计划"场景

**触发条件**（满足任一即可）：
- 包含 5+ 个大型代码块（每个 >20 行）
- 包含完整的 Schema 定义、API 设计、多个任务详情
- 用户明确要求"详细的"、"完整的"、"包含代码示例"

#### 2. 应对策略 - 分文件生成

**文件结构**（混合拆分）：
```
docs/plans/YYYY-MM-DD-topic-overview.md       # 总览（目标、架构概要、文件导航）
docs/plans/YYYY-MM-DD-topic-design.md         # 技术设计（Schema、API、数据流）
docs/plans/YYYY-MM-DD-topic-tasks/            # 任务目录
  ├── task1-xxx.md                            # 任务1详情（< 300 行）
  ├── task2-xxx.md                            # 任务2详情（< 300 行）
  └── ...
```

**关键原则**：
- 每个文件 < 300 行（远低于 token 限制）
- overview.md 作为入口，包含导航链接
- design.md 包含技术细节（Schema、API）
- tasks/ 目录包含独立的任务文档

#### 3. 失败后的应对

如果遇到 "Error writing file" 且重试多次失败：
1. 识别为 token 限制问题
2. 立即切换到分文件策略
3. 告知用户："检测到内容较多，已切换为分文件生成"

---

## 设计决策

### 为什么选择 300 行限制？

- ❌ 500 行：仍可能触发 token 限制（如果包含大量代码块）
- ✅ 300 行：安全边界，即使包含代码块也不会超限
- ✅ 更小的文件更易维护和导航

### 为什么选择混合拆分？

**对比其他方案**：

**方案 A - 按任务拆分**：
```
task1.md, task2.md, task3.md, ...
```
- ❌ 缺少架构设计的集中展示
- ❌ Schema 和 API 分散在各个任务中

**方案 B - 按章节拆分**：
```
overview.md, design.md, tasks.md, testing.md
```
- ❌ tasks.md 仍可能很大（8+ 个任务）
- ❌ 没有解决根本问题

**方案 C - 混合拆分**（✅ 选中）：
```
overview.md, design.md, tasks/task1.md, tasks/task2.md, ...
```
- ✅ overview 提供清晰导航
- ✅ design 集中展示技术设计
- ✅ tasks/ 目录便于任务管理
- ✅ 每个文件都很小，不会触发限制

---

## 实施效果

### 预期改进

**预防性**：
- Claude 识别到"详细计划"场景
- 主动使用分文件策略
- 避免浪费时间在注定失败的尝试上

**响应性**：
- 检测到重复的 "Error writing file"
- 立即切换策略
- 不再无限重试同样的方法

### 成功标准

- ✅ 不再出现连续多次 "Error writing file"
- ✅ 详细计划能够一次性成功生成
- ✅ 文件结构清晰，易于导航
- ✅ 每个文件大小合理（< 300 行）

---

## 测试计划

### 测试场景 1：详细实施计划

**输入**：
```
用户：创建 Phase 3 的详细实施计划，包含完整的 API 设计和 10 个任务
```

**期望输出**：
```
检测到这是详细实施计划，将分文件生成：

已创建：
- docs/plans/2026-01-21-phase3-overview.md
- docs/plans/2026-01-21-phase3-design.md
- docs/plans/2026-01-21-phase3-tasks/task1-xxx.md
- docs/plans/2026-01-21-phase3-tasks/task2-xxx.md
...

从 overview.md 开始查看。
```

### 测试场景 2：简单计划

**输入**：
```
用户：创建一个简单的重构计划
```

**期望输出**：
```
已创建：docs/plans/2026-01-21-refactoring-plan.md
```

（不触发分文件策略）

### 测试场景 3：失败后恢复

**输入**：
```
[Claude 尝试写入大文件]
Error writing file
Error writing file
```

**期望输出**：
```
检测到内容较多，已切换为分文件生成：
[生成多个小文件]
```

---

## 版本历史

### v1.0 (2026-01-21 早期)
- 错误假设：文件行数限制
- 规则：拆分 1000+ 行文件为 < 500 行

### v2.0 (2026-01-21)
- 正确识别：输出 token 限制
- 规则：识别详细计划，分文件生成（< 300 行）
- 新增：失败后的应对策略

---

## 相关文件

- `SKILL.md` - 主规则文件
- `docs/plans/2026-01-21-phase2-duckdb-metadata-layer.md` - 触发问题的原始文件
- Git commit: `2f6f91f` - 规则修复提交

---

## 总结

**问题**：详细计划生成时反复出现 "Error writing file"

**根本原因**：输出 token 限制，而非文件大小限制

**解决方案**：
1. 识别详细计划场景（5+ 代码块、Schema/API 设计）
2. 分文件生成（overview + design + tasks/）
3. 每个文件 < 300 行
4. 失败后立即切换策略

**效果**：避免 token 限制，提高成功率，改善文件组织
