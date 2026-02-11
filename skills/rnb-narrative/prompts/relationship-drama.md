# Relationship-Driven Drama Generation Prompt

## 用途
基于角色关系生成冲突或合作剧情。

## Input Schema
```json
{
  "characters": [
    {"id": "char_001", "name": "林小雨", "traits": ["理想主义", "敏感"]},
    {"id": "char_003", "name": "王制片", "traits": ["现实", "圆滑", "有权势"]}
  ],
  "relationship": {
    "type": "mentor-student|rivalry|romance|family|colleague",
    "current_state": "表面和谐，暗流涌动",
    "tension_level": 0.4,
    "history": "王制片发掘了林小雨，但开始要求回报"
  },
  "trigger": "王制片暗示林小雨需要参加'应酬'",
  "setting": {
    "location": "高级餐厅包厢",
    "occasion": "'庆功'晚宴",
    "power_dynamic": "王制片主导"
  }
}
```

## Prompt Template

```markdown
请为以下角色关系生成一个戏剧性场景：

## 角色信息
{character_details}

## 关系现状
- 类型: {relationship_type}
- 当前状态: {current_state}
- 紧张度: {tension_level}/1.0
- 历史背景: {history}

## 触发事件
{trigger}

## 场景设定
{setting}

## 输出格式

```json
{
  "scene": {
    "title": "场景标题",
    "dramatic_beats": [
      {
        "beat": 1,
        "type": "setup|rising_action|climax|fallout",
        "description": "节拍描述",
        "character_emotions": {
          "char_001": "emotion",
          "char_003": "emotion"
        },
        "dialogue": [
          {"speaker": "char_003", "line": "台词", "subtext": "潜台词"}
        ],
        "stage_directions": "动作/表情指示",
        "tension_delta": +0.2
      }
    ],
    "relationship_changes": {
      "char_001_to_char_003": {
        "trust": -15,
        "respect": -10,
        "dependence": +5
      }
    },
    "potential_outcomes": [
      {
        "choice": "林小雨的选择",
        "consequences": "后果描述",
        "next_scene_hint": "暗示"
      }
    ],
    "themes": ["权力", "理想与现实的冲突", "女性困境"],
    "symbolism": ["酒杯", "灯光", "窗外的雨"]
  }
}
```

## 要求
1. 对话要有潜台词，体现娱乐圈的人情世故
2. 权力动态要清晰但不直白
3. 情感变化要细腻、渐进
4. 提供2-3个有意义的选择分支
5. 体现特定时代背景（2000-2020）的娱乐圈生态

## 风格参考
- 电影:《霸王别姬》《花样年华》《爱乐之城》
- 剧集:《甄嬛传》《琅琊榜》《沉默的真相》
```

## 模型选择
- **Claude Opus 4.5**: 微妙的人际关系、潜台词
- **GPT-5.2**: 对话自然度

## 集成说明
- 生成的场景可直接转换为 GameEvents
- relationship_changes 数据更新 RelationshipRepository
- dramatic_beats 可与 TickOrchestrator 配合
