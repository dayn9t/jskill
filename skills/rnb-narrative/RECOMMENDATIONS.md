# RNB 项目剧本创作工具推荐

**文档版本**: v1.0
**更新日期**: 2026-02-09
**适用项目**: rnb-engine (演艺圈模拟游戏)

---

## 一、项目需求分析

### RNB 项目的特殊挑战

| 挑战 | 说明 | 工具需求 |
|-----|------|---------|
| **20年时间跨度** | 2000-2020，~21,900个时间点 | 长期一致性维护 |
| **ES事件系统** | WorldLog + Arbiter + Effect | 事件链因果验证 |
| **复杂角色网络** | 多角色关系动态演化 | 关系建模与冲突生成 |
| **AI驱动** | 无硬编码规则 | 涌现式叙事能力 |
| **双客户端** | Godot + UE5 | 跨平台叙事同步 |

---

## 二、工具分层架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      叙事生成层 (Generation)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Claude 4.5   │  │ DeepSeek-V3  │  │ GPT-5.2      │          │
│  │ (情感深度)    │  │ (快速原型)   │  │ (对话自然)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                      结构管理层 (Management)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ WhatELSE     │  │ 量子探险      │  │ 易笔AI       │          │
│  │ (大纲-实例)   │  │ (长文本记忆)  │  │ (投喂学习)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                      游戏集成层 (Integration)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ rnb-narrative│  │ Inworld AI   │  │ Convai       │          │
│  │ (本项目Skill)│  │ (NPC记忆)    │  │ (对话系统)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、核心工具推荐

### 3.1 大语言模型层

#### 🥇 Claude Opus 4.5 (Anthropic)

**适用场景**:
- 复杂角色弧线设计
- 情感深度场景
- 多角色互动剧情
- 长期因果链维护

**优势**:
- ✅ 200K 上下文，适合长期叙事
- ✅ 角色一致性最佳
- ✅ 避免AI陈词滥调
- ✅ 因果推理能力强

**劣势**:
- ❌ 价格最高 ($25/MTok)
- ❌ API 响应较慢

**RNB 集成方式**:
```python
# 用于 FateNode (叙事重力) 设计
# 用于关键剧情节点生成
# 用于情感高潮场景
```

---

#### 🥈 DeepSeek-V3 (深度求索)

**适用场景**:
- 大纲快速生成
- 批量事件原型
- 日常对话填充
- 成本敏感任务

**优势**:
- ✅ 性价比高
- ✅ 中文语境优秀
- ✅ 长文本能力强
- ✅ 生成速度快

**劣势**:
- ❌ 情感深度略逊
- ❌ 创意上限不如 Claude

**RNB 集成方式**:
```python
# 用于 TickOrchestrator 批量生成事件候选
# 用于日常 NPC 对话
# 用于背景事件填充
```

---

#### 🥉 GPT-5.2 (OpenAI)

**适用场景**:
- 自然对话生成
- 特定风格模仿
- 类型片结构
- 多语言支持

**优势**:
- ✅ 对话自然度最高
- ✅ 风格匹配能力强
- ✅ 生态工具丰富

**劣势**:
- ❌ 400K 上下文 (介于 Claude 和 Gemini 之间)
- ❌ 情感细腻度不如 Claude

**RNB 集成方式**:
```python
# 用于角色对话生成
# 用于特定类型剧情（悬疑、喜剧）
# 用于多语言版本
```

---

### 3.2 专业叙事工具层

#### WhatELSE (Autodesk Research 2025)

**核心能力**:
- 大纲 ↔ 实例 双向转换
- LLM-Modulo 因果规划
- 玩家行为建模
- Play-Time 动态响应

**RNB 适配性**: ⭐⭐⭐⭐⭐

**为什么适合 RNB**:
- 原生支持事件系统架构
- 与 rnb-engine 的 ES 设计理念一致
- 支持长期叙事一致性

**集成建议**:
```rust
// rnb-engine 可借鉴其架构
// 将 WhatELSE 作为外部叙事服务
// 通过 Cap'n Proto 协议通信
```

---

#### 量子探险 (国产)

**核心能力**:
- 200万字长文本记忆
- 120种基础诡计变体
- 罗生门架构 (6-8角色视角)
- 小说→剧本→分镜一体化

**RNB 适配性**: ⭐⭐⭐⭐☆

**为什么适合 RNB**:
- 中文原生，符合项目语境
- 长文本记忆解决 20 年时间跨度问题
- 多角色视角适合复杂关系网络

**使用建议**:
- 用于生成复杂丑闻事件链
- 用于多角色冲突场景
- 用于媒体舆论事件

---

#### 易笔AI (国产)

**核心能力**:
- 30秒生成完整大纲
- MBTI 角色设定支持
- 投喂学习经典语料
- 50万字+小说支持

**RNB 适配性**: ⭐⭐⭐⭐☆

**使用建议**:
- 快速原型验证
- 角色性格设计
- 批量生成事件候选

---

### 3.3 游戏集成中间件

#### Inworld AI

**核心能力**:
- NPC 长期记忆
- 跨平台角色一致性
- 情感计算集成
- 90% 玩家情感依附度提升

**RNB 适配性**: ⭐⭐⭐⭐⭐

**集成方案**:
```
rnb-engine NPC
    ↓
Inworld AI (对话生成 + 记忆)
    ↓
返回 GameEvents
    ↓
WorldLog 存储
```

---

#### Convai

**核心能力**:
- UE/Godot 插件
- AI 叙事设计集成
- 语音/文本双模态
- 行为树集成

**RNB 适配性**: ⭐⭐⭐⭐☆

**集成方案**:
- Godot 客户端直接使用 Convai 插件
- 与 CognitiveEngine 桥接

---

## 四、工具组合方案

### 方案 A: 精品路线 (推荐)

| 层级 | 工具 | 成本 | 效果 |
|-----|------|------|------|
| 核心剧情 | Claude 4.5 | 高 | 最佳 |
| 批量生成 | DeepSeek-V3 | 低 | 良好 |
| 对话润色 | GPT-5.2 | 中 | 优秀 |
| 结构管理 | WhatELSE | 中 | 专业 |
| NPC 集成 | Inworld AI | 中 | 沉浸 |

**适用**: 有充足预算，追求最佳叙事品质

---

### 方案 B: 性价比路线

| 层级 | 工具 | 成本 | 效果 |
|-----|------|------|------|
| 核心剧情 | DeepSeek-V3 | 低 | 良好 |
| 批量生成 | 本地 LLaMA | 极低 | 一般 |
| 对话润色 | 量子探险 | 低 | 良好 |
| 结构管理 | 自研简化版 | 开发成本 | 定制 |
| NPC 集成 | 本地方案 | 低 | 可控 |

**适用**: 预算有限，技术团队强

---

### 方案 C: 混合路线 (推荐平衡)

| 层级 | 工具 | 使用策略 |
|-----|------|---------|
| 关键剧情 | Claude 4.5 | 仅用于 20% 核心内容 |
| 日常生成 | DeepSeek-V3 | 80% 批量内容 |
| 对话优化 | GPT-5.2 | 按需调用 |
| 中文特化 | 量子探险 | 丑闻/媒体事件 |
| 原型快速 | 易笔AI | 前期验证 |

**适用**: 大多数项目，平衡成本与效果

---

## 五、与 rnb-engine 的深度集成

### 5.1 与 ES 架构集成

```
叙事生成器
    ↓ (生成)
GameEvents (JSON)
    ↓ (序列化)
Cap'n Proto Message
    ↓ (网络)
rnb-engine WorldLog.append()
    ↓ (验证)
Arbiter.arbitrate()
    ↓ (应用)
EffectApplicator.apply()
    ↓ (分发)
PerceptionNetwork.process()
```

### 5.2 与 AI Model Traits 集成

| Trait | 叙事工具对应 |
|-------|-------------|
| `CognitiveModel` | Inworld AI / Convai |
| `WorldModel` | WhatELSE / 量子探险 |
| `LanguageModel` | Claude 4.5 / GPT-5.2 |

### 5.3 数据流设计

```rust
// rnb-engine 定义
struct NarrativeRequest {
    trigger: String,
    participants: Vec<CharacterId>,
    current_world_state: WorldSnapshot,
    constraints: NarrativeConstraints,
}

struct NarrativeResponse {
    events: Vec<GameEvent>,
    fate_node_impulses: Vec<FateNodeImpulse>,
    tension_delta: f32,
}

// 叙事服务接口
#[async_trait]
trait NarrativeService {
    async fn generate_event_chain(&self, req: NarrativeRequest) -> NarrativeResponse;
}

// 实现可以是外部 AI 服务
struct ExternalNarrativeService {
    client: ClaudeClient, // 或 DeepSeekClient
}
```

---

## 六、实施路线图

### Phase 1: 基础设施 (2周)
- [ ] 搭建叙事生成 Pipeline
- [ ] 实现与 rnb-engine 的协议接口
- [ ] 配置 API 密钥和速率限制
- [ ] 建立评估基准

### Phase 2: 核心集成 (4周)
- [ ] 实现 Event Chain 生成
- [ ] 集成 Claude 4.5 用于关键剧情
- [ ] 集成 DeepSeek-V3 用于批量生成
- [ ] 因果一致性验证

### Phase 3: 高级功能 (4周)
- [ ] 角色弧线设计工具
- [ ] 关系驱动剧情生成
- [ ] 与 FateNode 系统集成
- [ ] 长期记忆维护

### Phase 4: 优化迭代 (持续)
- [ ] A/B 测试不同模型效果
- [ ] 收集反馈优化 Prompt
- [ ] 成本优化
- [ ] 本地化支持

---

## 七、成本估算

### 月度成本预估 (100万 Token/天)

| 方案 | Claude | DeepSeek | GPT | 其他 | 总计 |
|-----|--------|----------|-----|------|------|
| A-精品 | $750 | $100 | $300 | $200 | $1,350 |
| B-性价比 | $0 | $300 | $0 | $100 | $400 |
| C-混合 | $150 | $200 | $100 | $100 | $550 |

*注: 实际成本取决于使用量和优化程度*

---

## 八、参考资源

### 学术论文
- [WhatELSE: Shaping Narrative Spaces](https://www.research.autodesk.com/app/uploads/2025/02/WhatELSE.pdf) - Autodesk Research
- [Emergent Minds: AI in Video Game NPCs](https://www.ijfmr.com/papers/2025/3/42387.pdf)

### 行业工具
- [Inworld AI](https://www.inworld.ai/)
- [Convai](https://www.convai.com/)
- [量子探险](https://www.68aixie.com/)

### 开源项目
- [Concordia Framework](https://github.com/google-deepmind/concordia) - Google DeepMind

---

**维护**: rnb-engine 开发团队
**更新**: 随技术和需求变化定期更新
