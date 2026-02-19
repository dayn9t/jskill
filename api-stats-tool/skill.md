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

## 功能

- 从本地 session 文件提取 API 使用记录
- 按模型统计请求次数和 token 消耗
- 支持日期范围筛选
- 显示输入/输出 tokens 和缓存读取量

## 数据来源

`~/.claude/projects/*/*.jsonl` - 本地 session 历史记录
