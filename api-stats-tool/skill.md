---
name: api-stats
description: 查看 Claude Code API 使用统计，支持按模型和 URL 统计 token 使用量
---

# api-stats

查看 Claude Code API 使用统计

## 用法

```bash
# 查看今天的统计
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

## Proxy 模式（按 URL 统计）

```bash
# 启动代理
/api-stats proxy --start --port 8080

# 设置环境变量
export HTTPS_PROXY=http://127.0.0.1:8080

# 查看代理统计
/api-stats proxy --stats --hours 24
```

## 功能

- 从本地 session 文件提取 API 使用记录
- 按模型统计请求次数和 token 消耗
- 支持日期范围筛选
- 显示输入/输出 tokens 和缓存读取量
- TCP proxy 模式按 URL 统计

## 数据来源

- 本地日志：`~/.claude/projects/*/*.jsonl`
- Proxy 数据：`~/.claude/proxy_stats.db`
