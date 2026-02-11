# RNB 叙事生成 Skill

专为 **rnb-engine**（演艺圈模拟游戏）设计的 AI 剧本创作 Skill。

## 功能

- 结合 ES 事件系统生成分支叙事
- 长期时间线（20年）因果一致性维护
- 角色关系网络驱动的剧情生成
- 与 rnb-engine 数据模型深度集成

## 使用

```
/rnb-narrative <任务类型> [参数]
```

## 任务类型

- `event-chain`: 生成事件链（给定起始事件和目标状态）
- `character-arc`: 生成角色成长弧线
- `relationship-drama`: 基于角色关系生成冲突/合作剧情
- `scene-dialogue`: 生成场景对话
- `plot-review`: 审查剧情因果一致性

## 依赖

- rnb-engine ES 架构（WorldLog + Arbiter + Effect）
- Claude Opus 4.5 / DeepSeek / GPT-5.2 API
