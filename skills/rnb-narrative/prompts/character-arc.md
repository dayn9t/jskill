# Character Arc Generation Prompt

## 用途
设计角色在20年游戏时间中的成长弧线。

## Input Schema
```json
{
  "character": {
    "id": "char_001",
    "name": "林小雨",
    "initial_age": 18,
    "mbti": "INFP",
    "initial_traits": ["理想主义", "敏感", "才华横溢", "不善交际"],
    "starting_point": {
      "year": 2000,
      "status": "电影学院新生",
      "fame": 5,
      "wealth": 10
    }
  },
  "arc_type": "rise-fall-redemption",
  "key_milestones": ["获得第一个角色", "陷入丑闻", "重返巅峰"],
  "span_years": 20
}
```

## Prompt Template

```markdown
请为以下角色设计一个{span_years}年的成长弧线：

## 角色基础信息
- 姓名: {name}
- 初始年龄: {initial_age}
- MBTI: {mbti}
- 性格特质: {initial_traits}
- 起点: {starting_point}

## 弧线类型
{arc_type}

## 关键里程碑
{milestones}

## 输出格式

```json
{
  "character_arc": {
    "phases": [
      {
        "name": "阶段名称",
        "years": "2000-2003",
        "age_range": "18-21",
        "theme": "主题",
        "description": "阶段描述",
        "key_events": [
          {
            "year": 2001,
            "event": "事件描述",
            "character_change": "角色心理/能力变化",
            "external_change": "外部地位变化"
          }
        ],
        "relationship_evolution": [
          {"with": "char_002", "change": "从陌生到竞争对手"}
        ],
        "internal_conflict": "内心冲突描述",
        "external_obstacle": "外部障碍描述",
        "transformation": "本阶段结束时的转变"
      }
    ],
    "overall_trajectory": {
      "fame_curve": [5, 15, 45, 80, 60, 90],
      "wealth_curve": [10, 20, 100, 300, 150, 500],
      "happiness_curve": [70, 80, 60, 40, 50, 75],
      "integrity_curve": [90, 85, 60, 30, 50, 80]
    }
  }
}
```

## 要求
1. 弧线必须有清晰的起点、转折点和终点
2. 每个阶段都要有内心冲突和外部冲突
3. 关系演变要自然，符合角色性格
4. 体现娱乐圈的残酷和诱惑
5. 数值曲线要有合理的波动和趋势

## 特殊考虑
- 2000-2010: 互联网兴起对传统娱乐圈的冲击
- 2008: 金融危机对影视行业的影响
- 2015-2020: 流量时代的到来
```

## 模型选择
- **Claude Opus 4.5**: 深度心理描写、复杂弧线
- **GPT-5.2**: 快速生成、对话场景

## 集成说明
生成的弧线数据可用于：
- 预生成角色的 FateNode（叙事重力系统）
- 指导 EventProducer 生成事件
- 与 NarrativeGravity 系统配合调整张力
