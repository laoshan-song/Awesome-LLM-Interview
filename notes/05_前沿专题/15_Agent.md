# Agent 与工具调用

## 面试高频考点
- Agent 和普通 LLM 的区别？
- ReAct 框架的原理？
- 工具调用（Function Calling）如何实现？
- Plan-and-Execute vs ReAct？
- Agent 的常见失败模式？

---

## 一、什么是 Agent？

普通 LLM 是一次性输入输出（无状态、无工具、无规划），而 Agent 是一个具备感知-决策-执行-观察闭环的自主系统。

```
LLM Agent = LLM（大脑） + 工具（双手） + 记忆（笔记本） + 规划（决策链）

┌──────────────────────────────────────────┐
│              Agent 运行循环               │
│                                           │
│   用户目标                                 │
│      ↓                                    │
│   [LLM 思考] ←──────────────┐            │
│      ↓                      │            │
│   决定下一步动作              │            │
│      ↓                      │            │
│   ┌──────┐    ┌──────┐     │            │
│   │调用工具│    │生成回复│    │            │
│   └──┬───┘    └──┬───┘     │            │
│      ↓           ↓          │            │
│   工具返回结果   返回给用户   │            │
│      ↓                      │            │
│   观察结果 ──────────────────┘            │
│                                           │
│   循环终止条件：目标完成 / 超出最大步数     │
└──────────────────────────────────────────┘
```

### Agent 和普通 LLM 的本质区别

| 维度 | 普通 LLM | Agent |
|------|---------|-------|
| 交互方式 | 单轮/多轮对话 | 自主循环决策 |
| 状态 | 只有对话历史 | 有记忆、有任务状态 |
| 能力 | 文本生成 | 文本生成 + 工具调用 + 环境感知 |
| 自主性 | 被动响应 | 主动规划和执行 |
| 失败模式 | 回答错误 | 无限循环、错误行动、状态丢失 |

---

## 二、ReAct（Reasoning + Acting）

### 基本框架

ReAct 是 Agent 最基础的范式，将**推理（Reasoning）**和**行动（Acting）**交织在一起：

```
ReAct 模板：

System: 你可以使用以下工具：
  1. search(query: str) → 搜索结果
  2. calculator(expression: str) → 计算结果

User: 2024年北京GDP占全国GDP的比例是多少？

模型输出：
  Thought: 我需要先查询2024年北京GDP和全国GDP
  Action: search("2024年北京GDP")
  Observation: 2024年北京GDP为4.38万亿元

  Thought: 还需要查询全国GDP
  Action: search("2024年全国GDP")
  Observation: 2024年全国GDP为134.9万亿元

  Thought: 现在可以计算比例了
  Action: calculator("4.38 / 134.9 * 100")
  Observation: 3.25%

  Thought: 已获得所有需要的信息
  Final Answer: 2024年北京GDP约占全国GDP的3.25%
```

### ReAct 的优缺点

**优点**：
- 推理过程透明可解释，出错时容易定位是"想错了"还是"做错了"
- 灵活性高，能处理未见过的任务组合
- 与 LLM 的文本生成能力天然兼容

**缺点**：
- 串行执行，延迟高（每步都要等 LLM 推理）
- 容易陷入无限循环（Thought-Action-Observation 反复，始终不给 Final Answer）
- 长任务时上下文窗口容易溢出

---

## 三、Plan-and-Execute（计划与执行）

与 ReAct 的"边走边想"不同，Plan-and-Execute **先制定完整计划，再逐步执行**：

```
Phase 1 - Planning（计划制定）:

User: 帮我分析特斯拉2024Q4的财务表现

Planner: 
  计划：
  1. 搜索特斯拉2024Q4财报新闻
  2. 提取关键财务指标（营收、利润、毛利率、交付量）
  3. 对比2023Q4数据，计算同比变化
  4. 搜索分析师观点
  5. 综合以上信息，写一份简要分析报告

Phase 2 - Execution（计划执行）:
  Step 1 → 搜索结果：特斯拉Q4营收257亿...
  Step 2 → 提取：营收257亿、利润23亿...
  Step 3 → 同比：营收增长2%，利润下降...
  Step 4 → 分析师观点：...
  Step 5 → 生成报告
```

### ReAct vs Plan-and-Execute

| 维度 | ReAct | Plan-and-Execute |
|------|-------|------------------|
| 规划时机 | 边走边想（在线） | 先规划后执行（离线） |
| 灵活性 | 高（能适应环境变化） | 低（计划可能过时） |
| 全局最优性 | 弱（贪心每一步） | 强（考虑全局） |
| LLM 调用数 | 多（每步都调用） | 少（计划一次 + 执行时可选） |
| 可审查性 | 差（需要追踪全链） | 好（计划可单独审查和修改） |
| 适用场景 | 探索性任务、不确定环境 | 目标明确的复杂任务 |

---

## 四、Function Calling（工具调用）

### 实现原理

Function Calling 本质是让 LLM 输出**结构化的工具调用请求**，而非自由文本。通过 SFT 训练使模型学会：

1. **何时**使用哪个工具
2. **如何**填写工具参数的 JSON
3. **如何**理解工具返回结果并继续推理

### 完整流程

```
┌─────────────────────────────────────────────┐
│         Function Calling 完整流程            │
│                                              │
│  1. 定义工具（JSON Schema）                   │
│  {                                           │
│    "name": "get_weather",                    │
│    "description": "获取指定城市的天气",         │
│    "parameters": {                           │
│      "city": {"type": "string"},             │
│      "date": {"type": "string"}              │
│    }                                         │
│  }                                           │
│                                              │
│  2. 发送给 LLM（system prompt + 工具定义）    │
│     → LLM 决定是否调用工具                    │
│     → 如果是：输出结构化的 function_call      │
│     → 如果否：输出普通文本                     │
│                                              │
│  3. 执行工具调用（由调用方/框架执行）           │
│     result = get_weather("北京", "2024-12-01")│
│                                              │
│  4. 将工具返回结果作为新消息发给 LLM           │
│     → LLM 基于结果生成最终回复                 │
│                                              │
│  5. 可能循环（多轮工具调用）                   │
└─────────────────────────────────────────────┘
```

### OpenAI 风格的 Function Calling 示例

```python
import openai

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
}]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "北京今天多少度？"}],
    tools=tools,
    tool_choice="auto"  # 让模型决定是否调用工具
)

# 模型返回 tool_calls 而非文本
# tool_calls[0].function.name = "get_weather"
# tool_calls[0].function.arguments = '{"city": "北京", "unit": "celsius"}'
```

---

## 五、Agent 记忆系统

```
┌─────────────────────────────────────────┐
│            Agent 的三层记忆              │
│                                          │
│  短期记忆（Working Memory）               │
│  ├── 当前对话历史（上下文窗口内）          │
│  ├── 当前任务状态和中间结果                │
│  └── 容量：~128K tokens（模型窗口限制）   │
│                                          │
│  长期记忆（Long-term Memory）             │
│  ├── 向量数据库存储的会话摘要和历史         │
│  ├── 用户偏好、项目上下文                  │
│  └── 检索 + 注入相关记忆到当前上下文       │
│                                          │
│  工作记忆（Scratchpad）                   │
│  ├── 当前任务的中间推理结果                │
│  ├── 工具调用的返回值缓存                  │
│  └── 通常存在 Agent 框架的状态对象中       │
└─────────────────────────────────────────┘
```

---

## 六、Agent 的主要挑战与应对

| 挑战 | 描述 | 应对方法 |
|------|------|----------|
| **幻觉行动** | 模型编造不存在的工具/参数 | 严格的 JSON Schema 校验 + 工具名模糊匹配 |
| **无限循环** | 反复调用工具不给出最终答案 | max_iterations 限制 + 循环检测 + 重复行为惩罚 |
| **上下文溢出** | 多轮调用后历史超过窗口大小 | 定期摘要压缩 + 滑动窗口 + 只保留关键工具返回 |
| **错误传播** | 一步错误影响后续全部推理 | 每步做 sanity check + 允许回溯 + 并行尝试多个方案 |
| **工具调用幂等性** | 同一操作被执行多次（发两封邮件） | 工具侧保证幂等 + 写操作前二次确认 |
| **权限过大** | Agent 拥有超出需要的工具权限 | 最小权限原则 + 敏感操作需人工审批 |

---

## 七、面试延伸

**Q：如何防止 Agent 进入无限循环？**

> ① 设置最大步数限制（如 max_steps=10），超限强制终止；② 检测连续重复调用模式（连续 3 次调用同一工具且参数相同 → 触发干预）；③ 每步评估任务进度，让 LLM 做 termination check；④ 对循环行为施加额外惩罚（降低 action 的 logit 分数）。

**Q：RAG 和 Agent 的关系是什么？**

> RAG 是 Agent 能力的一个子集——当 Agent 需要查询知识库时，RAG 就是它的"知识检索工具"。Agent 可以调用多种工具（搜索、计算、API、代码执行），RAG 检索只是其中之一。但 RAG 的工程复杂度显著低于 Agent，不需要处理动作规划和多步推理。工程原则：能用 RAG 解决的问题，不要引入 Agent。

**Q：Multi-Agent 系统什么情况下值得投入？**

> 当任务天然需要多个专业角色协作（如软件开发 = 产品经理 + 架构师 + 程序员 + 测试）、或需要并行探索多条路径（如科研文献综述）、或需要多视角交叉验证（如法律合规审查）时，Multi-Agent 有收益。但单 Agent + 好工具往往已经够用，Multi-Agent 引入了通信开销和更复杂的调试难度。

**Q：什么是 Tool Use / Function Calling 的实现原理？**

> 本质上是通过 SFT 训练让模型学会：① 识别用户意图中需要工具的部分；② 输出符合 JSON Schema 的函数调用（而非自由文本）；③ 理解工具的返回结果（文本或 JSON）并整合进后续推理。训练数据通常包含 {用户请求, 工具定义, 模型调用, 工具返回, 最终回复} 的完整链。推理时，框架检测到模型输出 function_call 标记后，提取调用参数，执行工具，将结果注入对话历史，让模型继续推理。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., NeurIPS 2023) | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) |
| Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., NeurIPS 2023) | [arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761) |
| Plan-and-Solve Prompting (Wang et al., ACL 2023) | [arxiv.org/abs/2305.04091](https://arxiv.org/abs/2305.04091) |
| AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (Wu et al., 2023) | [arxiv.org/abs/2308.08155](https://arxiv.org/abs/2308.08155) |
| Magentic-One: A Generalist Multi-Agent System (Fourney et al., 2024) | [arxiv.org/abs/2411.04468](https://arxiv.org/abs/2411.04468) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 B站 | [挑战19分钟搞定LangGraph快速入门与原理剖析](https://search.bilibili.com/all?keyword=%E6%8C%91%E6%88%9819%E5%88%86%E9%92%9F%E6%90%9E%E5%AE%9ALangGraph%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8E%E5%8E%9F%E7%90%86%E5%89%96%E6%9E%90&order=click) | 2万播放，Agent编排框架快速上手 |
| 📺 B站 | [90分钟手撸企业级Agent多智能体（LangGraph+MCP+RAG）](https://search.bilibili.com/all?keyword=90%E5%88%86%E9%92%9F%E6%89%8B%E6%92%B8%E4%BC%81%E4%B8%9A%E7%BA%A7Agent%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%EF%BC%88LangGraph%2BMCP%2BRAG%EF%BC%89&order=click) | 3.7万播放，从0到1的Agent工程实战 |
| 📺 B站 | [【吴恩达】LangChain+LangGraph大模型教程（官方授权）](https://search.bilibili.com/all?keyword=%E3%80%90%E5%90%B4%E6%81%A9%E8%BE%BE%E3%80%91LangChain%2BLangGraph%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%95%99%E7%A8%8B%EF%BC%88%E5%AE%98%E6%96%B9%E6%8E%88%E6%9D%83%EF%BC%89&order=click) | 8万播放，权威Agent开发入门课程 |
