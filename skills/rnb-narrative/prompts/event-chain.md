# Event Chain Generation Prompt

## 用途
生成因果一致的游戏事件链，与 rnb-engine 的 ES 架构兼容。

## Input Schema
```json
{
  "start_state": {
    "date": "2005-03-15",
    "characters": ["char_001", "char_005"],
    "world_state": {
      "char_001_fame": 45,
      "char_005_fame": 60,
      "company_standing": 0.7
    }
  },
  "trigger_event": "主角获得重要角色试镜机会",
  "target_state": {
    "description": "主角与导演产生矛盾",
    "metrics": {
      "char_001_fame": 50,
      "tension_with_director": 0.8
    }
  },
  "constraints": {
    "max_events": 5,
    "time_span_days": 30,
    "drama_intensity": "medium"
  }
}
```

## Prompt Template

```markdown
你是一位资深的娱乐圈题材游戏编剧，熟悉演艺圈生态和人情世故。

请为以下游戏场景生成一个事件链：

## 起始状态
- 日期: {date}
- 涉及角色:
{character_descriptions}
- 世界状态:
{world_state}

## 触发事件
{trigger_event}

## 目标状态
{target_state}

## 约束条件
- 最多 {max_events} 个事件
- 时间跨度: {time_span_days} 天
- 戏剧强度: {drama_intensity}

## 输出格式
请以 JSON 格式输出事件链，每个事件包含:

```json
{
  "events": [
    {
      "id": "evt_001",
      "timestamp": "2005-03-15T09:00:00",
      "type": "dialogue|action|decision|consequence",
      "title": "事件标题",
      "description": "详细描述",
      "participants": ["char_001", "char_005"],
      "location": "地点",
      "prerequisites": ["evt_000"],
      "consequences": {
        "character_states": {
          "char_001": {"fame": +5, "stress": +10}
        },
        "relationship_changes": [
          {"from": "char_001", "to": "char_005", "delta": -5}
        ],
        "world_flags": ["audition_scheduled"]
      },
      "dialogue_key_lines": [
        {"speaker": "char_005", "line": "关键台词", "emotion": "condescending"}
      ]
    }
  ]
}
```

## 要求
1. 每个事件必须有明确的因果关系
2. 角色行为必须符合其性格和当前状态
3. 事件之间的时间间隔合理
4. 包含关键的决策点和转折点
5. 体现娱乐圈的特定生态（竞争、人情、机会）
```

## 模型选择
- **Claude Opus 4.5**: 复杂因果链、多角色互动
- **DeepSeek-V3**: 快速原型、批量生成

## 后处理
生成后需要通过 Arbiter 检查:
- 时间冲突检测
- 角色状态一致性
- 世界规则合规性
