# API Stats Tool

Claude Code API 使用统计工具，从本地 session 文件中提取和分析 API 使用情况。

## 功能特性

- 📊 按模型统计 API 请求次数和 token 消耗
- 📅 支持日期范围筛选（今天、最近 N 天、全部）
- 🔍 支持按模型名称过滤
- 💾 支持 JSON 格式输出
- 🚀 快速扫描本地 session 文件，无需远程 API

## 安装

```bash
# 创建符号链接到 ~/.claude/skills
ln -sf "$(pwd)/api-stats" ~/.claude/skills/api-stats
```

## 使用方法

### 作为 Skill 使用

```bash
# 查看今天的统计（默认）
/api-stats

# 查看最近 7 天
/api-stats --days 7

# 查看所有时间
/api-stats --all

# 按模型筛选
/api-stats --model opus

# JSON 格式输出
/api-stats --json
```

### 直接运行 Python 脚本

```bash
python3 stats.py --days 1
python3 stats.py --all --json
python3 stats.py --model sonnet --days 7
```

## 输出示例

```
API Usage Statistics (Last 7 days)

====================================================================================================
Model                            Requests    Input Tokens   Output Tokens      Cache Read
====================================================================================================
kimi-for-coding                     19793   1,260,658,361       1,488,379     471,387,904
claude-opus-4-6                     17565      32,837,921       1,069,758   1,011,839,834
claude-haiku-4-5-20251001            6672       3,944,709          16,916     213,522,304
glm-5                                1378       7,974,943         392,372     129,085,184
====================================================================================================
TOTAL                               50671   1,483,309,653       3,660,945   2,022,952,956
====================================================================================================
```

## 数据来源

工具从以下位置读取数据：
- `~/.claude/projects/*/*.jsonl` - 所有 session 的历史记录
- 提取 `type="assistant"` 且包含 `usage` 字段的记录
- 只统计 `input_tokens > 0` 的有效请求

## 统计指标

- **Requests**: API 请求次数
- **Input Tokens**: 输入 token 总数
- **Output Tokens**: 输出 token 总数
- **Cache Read**: 缓存读取 token 总数

## 技术实现

- 纯 Python 实现，无外部依赖
- 使用 JSONL 流式解析，内存占用低
- 支持大量 session 文件的快速扫描

## 限制

- 不包含 baseUrl 信息（session 文件中未存储）
- 只统计成功的 API 请求
- 依赖本地 session 文件的完整性
