# Agent 与工具调用

## 面试高频考点
- Agent 和普通 LLM 的区别？
- ReAct 框架的原理？
- 工具调用（Function Calling）如何实现？

---

## 什么是 Agent？

LLM Agent = LLM + 工具 + 记忆 + 规划

普通 LLM 是一次性输入输出；Agent 能循环地感知环境、规划、执行动作、观察结果，直到完成目标。

```
目标
 ↓
[思考] → [行动] → [观察]
         ↑_________|
         循环直到完成
```

---

## ReAct（Reasoning + Acting）

将推理（CoT）和行动（工具调用）交织：

```
Thought: 我需要查询今天的天气
Action: search("北京今天天气")
Observation: 北京今天晴，25°C
Thought: 已获得信息，可以回答
Answer: 北京今天晴朗，气温 25°C
```

**优点**：推理过程可解释，出错易定位。
**缺点**：多轮工具调用延迟高，容易陷入循环。

---

## Function Calling（工具调用）

**1. 定义工具（JSON Schema）**

**2. 模型决定是否调用及参数（输出结构化 JSON）**

**3. 执行工具，将结果返回给模型**

**实现原理**：SFT 阶段用大量工具调用数据训练，让模型学会输出结构化调用格式并理解返回结果。

---

## 记忆系统

| 类型 | 实现方式 | 用途 |
|------|----------|------|
| 短期记忆 | 上下文窗口 | 当前对话历史 |
| 长期记忆 | 向量数据库 | 跨会话用户偏好、知识 |
| 工作记忆 | Scratch pad | 中间推理结果 |

---

## Agent 的主要挑战

- **幻觉行动**：模型编造不存在的工具参数
- **循环调用**：陷入无限工具调用循环
- **长序列管理**：多轮调用后上下文过长
- **错误传播**：早期错误影响后续所有步骤

---

## 面试延伸

**Q：如何防止 Agent 进入无限循环？**
> 设置最大步数限制；用 LLM 作为裁判检测循环；每步评估是否已有足够信息回答。

**Q：RAG 和 Agent 的关系？**
> RAG 可以作为 Agent 的一个工具（搜索知识库）。Agent 更通用，可调用任意工具，但复杂度和延迟也更高。


---

## 原始论文

| 论文 | 链接 |
|------|------|
| ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022) | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) |
| Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., 2023) | [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761) |

## 延伸阅读与视频

> 视频链接持续更新中，欢迎 PR 补充优质资源
