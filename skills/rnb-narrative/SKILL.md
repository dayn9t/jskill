# RNB Narrative Generation Skill

## Metadata
- **Name**: rnb-narrative
- **Version**: 1.0.0
- **Target**: rnb-engine (演艺圈模拟游戏)
- **Models**: Claude Opus 4.5, DeepSeek-V3, GPT-5.2

## Description
为 rnb-engine 生成 AI 驱动的游戏剧本、事件链和角色叙事，深度集成 ES（Event Sourcing）架构。

## Usage

```
/rnb-narrative <cOMMAND> [OPTIONS]

Commands:
  event-chain      生成因果一致的事件链
  character-arc    设计角色成长弧线
  relationship     生成关系驱动的剧情
  scene            生成具体场景和对话
  review           审查叙事因果一致性

Options:
  --model MODEL    选择模型 (claude/deepseek/gpt)
  --year YEAR      指定游戏年份 (2000-2020)
  --characters ID  指定角色ID列表
  --save PATH      保存到指定路径
```

## Architecture Integration

### 与 ES 系统协作
```
叙事生成器
    ↓
生成 GameEvents
    ↓
提交到 WorldLog (Append-only)
    ↓
Arbiter 冲突检测
    ↓
EffectApplicator 更新状态
    ↓
PerceptionNetwork 分发感知
```

### 与 AI Model Traits 集成
- **CognitiveModel**: 角色决策生成
- **WorldModel**: 世界判断、冲突仲裁
- **LanguageModel**: 对话变体生成

## Workflow Examples

### 1. 生成事件链
```
/rnb-narrative event-chain \
  --start "主角获得重要角色试镜机会" \
  --end "主角与导演产生矛盾" \
  --characters char_001,char_005 \
  --year 2005
```

### 2. 设计角色弧线
```
/rnb-narrative character-arc \
  --character char_001 \
  --arc-type "rise-fall-redemption" \
  --span-years 5
```

### 3. 生成关系剧情
```
/rnb-narrative relationship \
  --characters char_001,char_003 \
  --relationship-type "rivalry" \
  --trigger "资源争夺"
```

## Model Selection Guide

| 任务 | 推荐模型 | 理由 |
|-----|---------|------|
| 事件链架构 | Claude Opus 4.5 | 因果推理、长期一致性 |
| 角色对话 | GPT-5.2 | 自然对话、风格匹配 |
| 大纲初稿 | DeepSeek-V3 | 速度快、成本低 |
| 情感戏 | Claude Opus 4.5 | 情感深度、角色一致性 |
| 批量生成 | DeepSeek-V3 | 高并发、性价比 |

## Best Practices

1. **因果一致性**: 始终检查事件链的因果合理性
2. **角色一致性**: 维护角色 MBTI/性格标签
3. **时间锚定**: 明确事件发生的游戏时间
4. **状态追踪**: 记录每次生成的世界状态变化
5. **人工审核**: AI 生成后人工审核关键剧情
