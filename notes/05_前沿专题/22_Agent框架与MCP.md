# Agent 框架生态与 MCP 协议（2025）

## 面试高频考点
- LangGraph 和 LangChain 的核心区别是什么？什么时候用图状态机？
- MCP 协议是什么？为什么说它是 AI 的"USB-C"？
- AutoGen 的 GroupChat 和 LangGraph 的多 Agent 有什么设计哲学差异？
- OpenAI Agents SDK 的 Handoffs 机制是如何实现 Agent 间控制转移的？
- 生产级 Agent 系统的核心工程挑战有哪些？

---

## 一、LangGraph

**LangGraph** 是 LangChain 团队开发的有状态多 Agent 编排框架，将 Agent 工作流建模为**有向图（可含环）**，是目前生产环境中最成熟的 Agent 框架。

**GitHub**：[github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

### 核心概念

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 定义状态结构
class AgentState(TypedDict):
    messages: list
    next_action: str
    iteration: int

# 构建图
graph = StateGraph(AgentState)

# 添加节点（每个节点是一个函数）
graph.add_node("researcher", research_agent)
graph.add_node("writer", writing_agent)
graph.add_node("reviewer", review_agent)

# 添加条件边（决定下一步）
graph.add_conditional_edges(
    "reviewer",
    lambda state: "writer" if state["needs_revision"] else END,
    {"writer": "writer", END: END}
)

# 编译并运行
app = graph.compile(checkpointer=MemorySaver())  # 启用持久化
result = app.invoke({"messages": [...]}, config={"thread_id": "session_1"})
```

### 关键特性

**Checkpointing（持久化）**：每个节点执行后自动保存状态，支持断点续跑和 Human-in-the-loop（暂停等待人工审核）：

```python
# 在需要人工审核的节点插入中断
graph.add_node("human_review", interrupt_before=["approve"])

# 外部恢复执行
app.invoke(None, config={"thread_id": "session_1"})  # 从断点继续
```

**适用场景**：复杂多步骤工作流、需要条件分支和循环的任务、需要持久化状态跨会话的应用。

---

## 二、AutoGen（Microsoft）

**AutoGen** 是微软开发的多智能体对话框架，核心模式是让多个 Agent 通过**对话**协作完成任务。

**GitHub**：[github.com/microsoft/autogen](https://github.com/microsoft/autogen)

### GroupChat 机制

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# 定义多个专业 Agent
coder = AssistantAgent("Coder", system_message="你是一个编程专家")
reviewer = AssistantAgent("Reviewer", system_message="你负责代码审查")
user = UserProxyAgent("User", human_input_mode="NEVER")

# 组建群聊
groupchat = GroupChat(
    agents=[user, coder, reviewer],
    messages=[],
    max_round=10,
    speaker_selection_method="auto"  # LLM 自动决定下一个发言者
)
manager = GroupChatManager(groupchat=groupchat)

# 启动对话
user.initiate_chat(manager, message="帮我写一个二分搜索并测试")
```

**Magentic-One**（2024）：AutoGen 的多 Agent 系统，包含 Orchestrator + WebSurfer + FileSurfer + Coder + ComputerTerminal 五个专业 Agent，可以完成复杂的网页操作和文件处理任务。

**AutoGen v0.4（AG2）架构重构**：
- 异步优先（async-first）
- Actor 模型并发
- 更好的模块化和可测试性

---

## 三、OpenAI Agents SDK

**OpenAI Agents SDK**（2025年初发布，从实验性 Swarm 项目演进）是 OpenAI 官方的轻量级 Agent 框架。

**GitHub**：[github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)

### Handoffs 机制

Agent 间控制转移的核心机制，当前 Agent 判断需要专业化处理时，将对话控制权"交接"给另一个 Agent：

```python
from agents import Agent, handoff, Runner

billing_agent = Agent(
    name="Billing",
    instructions="处理所有账单和付款相关问题"
)

tech_agent = Agent(
    name="Tech Support",
    instructions="处理技术故障和产品使用问题"
)

triage_agent = Agent(
    name="Triage",
    instructions="判断用户问题类型并转接给对应专家",
    handoffs=[billing_agent, tech_agent]  # 声明可交接的目标
)

result = Runner.run_sync(triage_agent, "我的账单为什么这个月多了50块？")
```

### Guardrails（输入/输出验证）

```python
from agents import Agent, InputGuardrail, GuardrailFunctionOutput

async def check_safe_input(ctx, agent, input):
    # 检测有害输入
    if "恶意关键词" in input:
        return GuardrailFunctionOutput(
            output_info="检测到不安全内容",
            tripwire_triggered=True  # 阻断执行
        )
    return GuardrailFunctionOutput(tripwire_triggered=False)

agent = Agent(
    name="Safe Agent",
    input_guardrails=[InputGuardrail(guardrail_function=check_safe_input)]
)
```

---

## 四、MCP 协议（Model Context Protocol）

**MCP** 是 Anthropic 主导开发（2024年11月发布）的开放标准，定义了 AI 模型与外部工具/数据源的通信规范。2025 年已被 OpenAI、Google、Microsoft、Cursor 等广泛采纳。

**规范仓库**：[github.com/modelcontextprotocol/specification](https://github.com/modelcontextprotocol/specification)

### 为什么叫"AI 的 USB-C"？

在 MCP 之前，每个 AI 应用需要为每个工具写独立集成代码（N×M 问题）：
```
Claude ←→ 自定义代码 ←→ GitHub
Claude ←→ 自定义代码 ←→ Notion
GPT-4 ←→ 自定义代码 ←→ GitHub（另一套）
GPT-4 ←→ 自定义代码 ←→ Notion（另一套）
```

MCP 统一标准后（N+M 问题）：
```
Claude ←→ MCP Client ←→ MCP 协议 ←→ MCP Server（GitHub）
GPT-4  ←→ MCP Client ←→ MCP 协议 ←→ MCP Server（Notion）
任何AI  ←→              ↑同一套标准
```

### 三层架构

```
┌─────────────────────────────────────────────┐
│  MCP Host（宿主应用）                         │
│  Claude Desktop / Cursor / IDE / 自定义 App  │
│                    ↕                         │
│  MCP Client（协议处理层，内嵌在 Host 中）       │
└─────────────────────────────────────────────┘
                      ↕  MCP 协议（JSON-RPC 2.0）
┌─────────────────────────────────────────────┐
│  MCP Server（工具/数据提供方）                 │
│  GitHub Server / Notion Server / DB Server  │
└─────────────────────────────────────────────┘
```

### 四大原语

| 原语 | 方向 | 描述 | 示例 |
|------|------|------|------|
| **Tools** | Server→Client→Model | 模型可调用的函数 | 搜索代码、发 PR |
| **Resources** | Server→Client | 暴露给模型的数据 | 文件内容、数据库记录 |
| **Prompts** | Server→Client | 预定义的提示模板 | 代码审查模板 |
| **Sampling** | Client→Server | Server 请求 LLM 补全 | 让工具内部调用 LLM |

### 最小 MCP Server 实现

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_code(query: str, repo: str) -> str:
    """在指定仓库中搜索代码"""
    # 实际搜索逻辑
    return f"在 {repo} 中找到关于 {query} 的 3 个结果..."

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path) as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport="stdio")  # 或 "sse" 用于 HTTP
```

### 传输层

| 传输方式 | 适用场景 | 特点 |
|---------|---------|------|
| **stdio** | 本地工具（Claude Desktop、CLI）| 子进程通信，最简单 |
| **HTTP+SSE** | 远程服务、Web 应用 | 服务端推送事件，支持并发 |

---

## 五、A2A 协议（Google，2025）

**A2A（Agent-to-Agent Protocol）** 是 Google 提出的补充协议，专注于 **Agent 之间**的通信标准（MCP 主要解决 Agent 与工具的通信）：

| 维度 | MCP | A2A |
|------|-----|-----|
| 解决问题 | Agent ↔ 工具/数据源 | Agent ↔ Agent |
| 发起方 | Anthropic | Google |
| 成熟度 | 已大规模采纳 | 2025年提出，采纳中 |
| 定位 | 工具接入标准 | 多 Agent 协作标准 |

---

## 六、四框架对比

| 维度 | LangGraph | AutoGen | OpenAI Agents SDK | MCP |
|------|-----------|---------|-------------------|-----|
| 类型 | 编排框架 | 多 Agent 对话 | 轻量 Agent 框架 | 协议标准 |
| 状态管理 | ✅ 图状态 | 有限 | 有限 | N/A |
| 持久化 | ✅ Checkpointing | ❌ | ❌ | N/A |
| 工具集成 | ✅ | ✅ | ✅ | ✅（标准化）|
| 多 Agent | ✅ | ✅（核心特性）| ✅（Handoffs）| N/A |
| 学习曲线 | 高 | 中 | 低 | 低（标准）|
| 适合场景 | 复杂有状态工作流 | 研究/对话协作 | 简单生产 Agent | 工具生态互操作 |

---

## 面试延伸

**Q：LangGraph 相比 LangChain 的 AgentExecutor 有什么本质改进？**
> AgentExecutor 是线性的 Thought→Action→Observation 循环，无法处理条件分支、并行执行和复杂状态。LangGraph 将工作流建模为有向图，支持：① 条件边（根据状态决定下一步）；② 循环（人工审核→修改→再审核）；③ 持久化状态（跨会话记忆）；④ 并行节点执行。本质上是从"固定 ReAct 循环"升级为"可编程状态机"。

**Q：MCP 和 Function Calling（工具调用）的区别是什么？**
> Function Calling 是模型侧的能力（模型输出结构化的函数调用请求），每个 AI 平台有自己的格式（OpenAI/Anthropic/Google 各不同）；MCP 是工具侧的标准协议，定义工具如何暴露自己、如何被发现和调用。两者互补：Function Calling 负责"模型决定调用什么"，MCP 负责"工具如何统一提供能力"。MCP Server 最终也是通过 Function Calling 被模型调用的。

**Q：生产环境中 Agent 最常见的失败模式是什么？**
> ① **无限循环**：Agent 陷入重复动作，需要设置 max_iterations 和循环检测；② **工具调用幂等性**：同一个操作被执行多次（如发送了两封邮件），需要工具侧保证幂等；③ **上下文窗口溢出**：长任务累积的 messages 超过 context length，需要定期压缩/摘要历史；④ **错误传播**：一个子任务失败导致后续全部失败，需要每个节点有 fallback 和错误处理逻辑。

---

## 原始论文与资源

| 资源 | 链接 |
|------|------|
| LangGraph GitHub | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| AutoGen GitHub | [github.com/microsoft/autogen](https://github.com/microsoft/autogen) |
| OpenAI Agents SDK | [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python) |
| MCP 规范 GitHub | [github.com/modelcontextprotocol/specification](https://github.com/modelcontextprotocol/specification) |
| MCP 官网 | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| ReAct 原始论文 (Yao et al., 2022) | [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629) |
| Magentic-One 论文 (2024) | [arxiv.org/abs/2411.04468](https://arxiv.org/abs/2411.04468) |
| MCPAgentBench: Benchmark for LLM Agent MCP Tool Use (2025) | [arxiv.org/abs/2512.24565](https://arxiv.org/abs/2512.24565) |
| Beyond Individual Intelligence: Multi-Agent Survey (2026) | [arxiv.org/abs/2605.14892](https://arxiv.org/abs/2605.14892) |
| Agentic Reasoning for Large Language Models — Survey (2026) | [arxiv.org/abs/2601.12538](https://arxiv.org/abs/2601.12538) |
| Orchard: Open-Source Agentic Modeling Framework (ACL 2026) | [arxiv.org/abs/2605.15040](https://arxiv.org/abs/2605.15040) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 B站 | [挑战19分钟搞定LangGraph快速入门与原理剖析](https://www.bilibili.com/video/BV1HVFLzfEeS/) | 2万播放，LangGraph核心概念快速上手 |
| 📺 B站 | [【吴恩达】LangChain+LangGraph大模型教程（官方授权汉化）](https://search.bilibili.com/all?keyword=%E3%80%90%E5%90%B4%E6%81%A9%E8%BE%BE%E3%80%91LangChain%2BLangGraph%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%95%99%E7%A8%8B%EF%BC%88%E5%AE%98%E6%96%B9%E6%8E%88%E6%9D%83%E6%B1%89%E5%8C%96%EF%BC%89&order=click) | 8万播放，吴恩达课程，权威入门首选 |
| 📺 B站 | [面试官问：LangChain和LangGraph分别适合什么场景？](https://search.bilibili.com/all?keyword=%E9%9D%A2%E8%AF%95%E5%AE%98%E9%97%AE%EF%BC%9ALangChain%E5%92%8CLangGraph%E5%88%86%E5%88%AB%E9%80%82%E5%90%88%E4%BB%80%E4%B9%88%E5%9C%BA%E6%99%AF%EF%BC%9F&order=click) | 1.2万播放，面试向选型对比 |
| 📺 B站 | [LangGraph接入MCP工具：为什么需要？如何接入？](https://www.bilibili.com/video/BV1CsRjYAEXW/) | 1.2万播放，MCP与LangGraph集成实战 |
| 📺 B站 | [90分钟手撸企业级Agent多智能体（LangGraph+MCP+RAG）](https://www.bilibili.com/video/BV1Y4LgzzEeU/) | 3.7万播放，从0到1的多智能体实战 |
