# Personal Preferences Skill

个人偏好 skill，自动应用到所有 Claude Code 对话。

## 功能

### 1. 中文优先
- 所有对话和解释使用中文
- 代码和技术文档保持英文（符合行业惯例）

### 2. 现代技术栈
- 自动选择最先进、最优雅的技术
- Bun > npm, TypeScript strict mode, 最新框架版本

### 3. 简洁回应
- 只展示关键决策和结果
- 隐藏实现细节和冗长过程
- 代码示例精简到核心逻辑

## 安装

### 方法 1: 全局安装（推荐）

```bash
# 复制到 Claude Code skills 目录
cp -r skills/personal-preferences ~/.claude/skills/

# 配置自动加载
# 编辑 ~/.claude/settings.json，添加：
{
  "hooks": {
    "SessionStart": "echo '/personal-preferences'"
  }
}
```

### 方法 2: 符号链接

```bash
ln -s $(pwd)/skills/personal-preferences ~/.claude/skills/personal-preferences
```

## 使用

安装后自动生效，无需手动调用。

每次启动 Claude Code 会话时，这些偏好会自动应用：
- ✅ Claude 用中文回应
- ✅ 自动选择现代技术栈
- ✅ 保持回应简洁

## 效果对比

### 没有 skill

```
User: 帮我初始化一个新项目
Claude: I'll help you initialize a new project. First, let me create
a package.json file. We can use npm or yarn. Which one would you prefer?
```

### 使用 skill

```
User: 帮我初始化一个新项目
Claude: 创建项目中...
[uses bun init]
已完成，使用 TypeScript + Bun
```

## 自定义

如果需要修改偏好，编辑 `SKILL.md` 文件：
- 调整语言规则
- 修改技术选型偏好
- 改变简洁程度

## 临时覆盖

如果某次对话需要不同设置：
```
User: 这次用英文回应，并详细解释
Claude: [follows user instruction]
```

## 文件结构

```
skills/personal-preferences/
├── SKILL.md          # 核心 skill 文件
├── README.md         # 本文件
└── EXAMPLE.md        # 使用示例
```

## 兼容性

- ✅ Claude Code CLI
- ✅ 所有 Claude 模型（Haiku, Sonnet, Opus）
- ✅ 所有项目类型

## 注意事项

1. **全局生效**: 这个 skill 会影响所有项目
2. **可覆盖**: 用户明确指示可以覆盖偏好
3. **静默运行**: 不会显示加载消息，不打断工作流
