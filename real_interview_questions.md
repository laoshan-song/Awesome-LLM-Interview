# 真实 LLM 面试题型整理

> 说明：这里整理的是公开面经、公开题库、岗位 JD 和社区讨论中反复出现的 LLM 面试问法，已做去重、归类和表达统一；不是逐字搬运某个候选人的原始面经。复习时建议先口述答案，再回到对应 notes 查漏补缺。
>
> 更准确地说，这份文档收集的是“真实面试会这样追问的题型”：面试官通常不会只问定义，而会沿着原理、工程取舍、线上故障、指标和项目细节连续追问。

---

## 怎么使用

1. 先随机抽 10 题，用 2-3 分钟口述答案。
2. 每题按“定义 -> 原理 -> 工程取舍 -> 常见坑 -> 指标”组织。
3. 说不清的题，直接跳到对应 notes 补。
4. 二面/项目面重点准备“追问方向”和“系统设计题”。

## 答题评分标准

面试官通常按下面几个维度判断你是不是“真的做过”：

| 维度 | 低分回答 | 高分回答 |
|------|----------|----------|
| 原理 | 只背名词 | 能写公式、画链路、解释瓶颈来源 |
| 工程 | 只说“可以优化” | 能说清延迟、吞吐、显存、成本、失败恢复 |
| 数据 | 只说“准备数据” | 能说清清洗、标注、评估集、badcase 回流 |
| 指标 | 只说“效果更好” | 能拆 TTFT/TPOT、Recall@K、faithfulness、成本/请求 |
| 安全 | 只说“加权限” | 能说明权限前置过滤、审计、工具白名单、prompt injection 防御 |
| 项目 | 只讲功能 | 能讲线上约束、取舍、失败案例和迭代路径 |

---

## 一、LLM 基础链路

对应 notes：

- [LLM 从输入到输出](./notes/00_LLM总览/01_LLM从输入到输出.md)
- [LLM 核心名词解释](./notes/01_基础架构/01_名词解释.md)
- [Transformer 架构](./notes/01_基础架构/03_Transformer架构.md)
- [位置编码](./notes/01_基础架构/04_位置编码.md)

真实高频题：

1. 用户输入一句话后，LLM 从 tokenizer 到输出 token 的完整流程是什么？
2. Token、词、字符有什么区别？为什么中文、英文、代码的 token 成本不同？
3. Embedding 层解决什么问题？训练时 token embedding 和 RAG embedding 是一回事吗？
4. Self-Attention 的公式是什么？为什么要除以 `sqrt(d_k)`？
5. Multi-Head Attention 为什么有效？多头是不是简单增加参数？
6. Decoder-only、Encoder-only、Encoder-Decoder 的区别是什么？为什么主流生成式 LLM 多用 decoder-only？
7. Pre-LN 和 Post-LN 的区别是什么？为什么大模型更常用 Pre-LN？
8. RMSNorm 和 LayerNorm 有什么区别？
9. SwiGLU 相比 ReLU/GELU 有什么优势？
10. RoPE 的核心思想是什么？为什么它适合相对位置建模？
11. RoPE 外推到长上下文会遇到什么问题？常见扩展方法有哪些？
12. Causal Mask 的作用是什么？训练和推理时分别怎么用？

常见追问：

- 如果让你画一张 LLM 推理流程图，你会把哪些模块画进去？
- 为什么 Transformer 能并行训练，但生成时不能完全并行？
- 上下文窗口变长后，attention、KV Cache、延迟分别怎么变化？

---

## 二、训练、SFT 与对齐

对应 notes：

- [预训练 vs 微调 vs RLHF](./notes/02_训练与对齐/05_预训练与微调.md)
- [SFT](./notes/02_训练与对齐/06_SFT.md)
- [RLHF / DPO / PPO](./notes/02_训练与对齐/07_RLHF_DPO_PPO.md)
- [LoRA 与 PEFT](./notes/02_训练与对齐/08_LoRA与PEFT.md)
- [预训练数据处理](./notes/02_训练与对齐/09_预训练数据处理.md)

真实高频题：

1. Pretraining、Continued Pretraining、SFT、RLHF、DPO 分别解决什么问题？
2. SFT 是不是给模型注入知识？什么时候 SFT 不适合？
3. Instruction tuning 和传统 fine-tuning 有什么区别？
4. 训练 chat model 时，为什么 chat template 很重要？
5. SFT 数据怎么构造？一条高质量 SFT 样本应该包含什么？
6. 多轮 SFT 数据里 loss 应该算哪些 token？system/user token 要不要算 loss？
7. RLHF 的三阶段流程是什么？
8. Reward Model 怎么训练？偏好数据怎么组织？
9. PPO 在 RLHF 中的作用是什么？为什么要 KL penalty？
10. DPO 为什么可以不用单独训练 Reward Model？
11. DPO 相比 PPO 的工程优缺点是什么？
12. RLHF/DPO 会提升事实正确率吗？为什么不一定？
13. LoRA 的低秩分解公式是什么？`rank r` 影响什么？
14. LoRA 应该插在哪些层？`q_proj/v_proj/o_proj/ffn` 怎么选？
15. QLoRA 和 LoRA 的区别是什么？
16. 全量微调、LoRA、Prefix Tuning、Adapter 怎么选？
17. 如果领域模型回答风格差但知识够，应该 SFT 还是继续预训练？
18. 如果领域知识缺失，为什么只做 SFT 可能没用？

常见追问：

- 给你 1 万条企业客服问答，如何判断适合 SFT 还是 RAG？
- 如何防止 SFT 过拟合模板？
- 偏好数据标注不一致时怎么处理？

---

## 三、推理、KV Cache 与部署优化

对应 notes：

- [KV Cache](./notes/03_推理与优化/09_KV_Cache.md)
- [量化](./notes/03_推理与优化/10_量化.md)
- [解码策略](./notes/03_推理与优化/11_解码策略.md)
- [推理加速](./notes/03_推理与优化/12_推理加速.md)
- [推理框架对比](./notes/03_推理与优化/13_推理框架对比.md)

真实高频题：

1. Prefill 和 Decode 的区别是什么？各自瓶颈在哪里？
2. KV Cache 为什么能加速推理？为什么只缓存 K/V 不缓存 Q？
3. KV Cache 显存怎么估算？和 batch size、seq len、layer、head 有什么关系？
4. MHA、MQA、GQA 对 KV Cache 有什么影响？
5. PagedAttention 解决了什么问题？和 OS paging 类比在哪里？
6. Continuous batching 为什么能提升吞吐？
7. TTFT、TPOT、吞吐、并发之间有什么区别？
8. FlashAttention 的核心优化是什么？它减少的是计算量还是 IO？
9. Speculative Decoding 的流程是什么？什么时候收益明显？
10. Temperature、Top-k、Top-p 分别怎么影响输出？
11. Beam Search 为什么在开放式对话里不一定好？
12. INT8、INT4、FP8 的区别是什么？
13. GPTQ、AWQ、SmoothQuant 分别解决什么问题？
14. 量化对数学、代码、长上下文任务会有什么风险？
15. vLLM、SGLang、llama.cpp、Ollama 怎么选？
16. 为什么小 batch 低延迟和大 batch 高吞吐常常冲突？
17. 如果线上首 token 慢，你会怎么排查？
18. 如果 decode 慢，你会怎么排查？

常见追问：

- 7B/13B/70B 模型在单卡上怎么部署？
- 一个请求 32K 上下文和 200 token 输出，瓶颈更可能在哪？
- 为什么显存够但吞吐仍然上不去？

---

## 四、RAG、Embedding 与向量检索

对应 notes：

- [RAG](./notes/05_前沿专题/14_RAG.md)
- [GraphRAG 与高级 RAG](./notes/05_前沿专题/20_GraphRAG与高级RAG.md)
- [生产 RAG 排障指南](./notes/06_工程实践/02_生产RAG排障指南.md)
- [Embedding 与向量检索](./notes/06_工程实践/03_Embedding与向量检索.md)
- [上下文工程与长上下文应用](./notes/06_工程实践/04_上下文工程与长上下文应用.md)

真实高频题：

1. RAG 的完整链路是什么？离线和在线分别做什么？
2. RAG 相比微调解决什么问题？什么时候 RAG 不适合？
3. Chunk size 和 overlap 怎么选？过大/过小分别有什么问题？
4. 文档解析、清洗、分块、metadata 哪一步最容易出问题？
5. Dense Retrieval 和 BM25 的区别是什么？
6. 为什么企业知识库通常需要 Hybrid Search？
7. RRF 融合是什么？相比加权求和有什么好处？
8. Reranker 为什么通常能提升 RAG 效果？代价是什么？
9. Bi-Encoder 和 Cross-Encoder 的区别是什么？
10. Embedding 模型怎么选？只看 MTEB 排名够吗？
11. 向量库 HNSW、IVF、PQ 的基本区别是什么？
12. RAG 中为什么仍然会 hallucination？
13. 如何评估 RAG？Retrieval Recall、Faithfulness、Citation Accuracy 分别是什么？
14. 线上 RAG 答错了，你怎么判断是检索问题还是生成问题？
15. 如果正确文档在 Top-20 但答案错了，下一步查什么？
16. Query rewrite 有什么风险？为什么不能丢原 query？
17. GraphRAG 解决普通 RAG 的什么问题？
18. 长上下文能不能替代 RAG？
19. RAG 如何做权限隔离？为什么不能让模型自己判断权限？
20. 表格、图片、PDF、代码文档怎么做 RAG？

常见追问：

- 如果用户问“昨天那个接口又报 502 了”，query rewrite 怎么处理？
- 如果知识库频繁更新，索引和缓存如何失效？
- 多租户 RAG 如何防止 A 用户检索到 B 用户文档？

---

## 五、Agent、工具调用与 MCP

对应 notes：

- [Agent](./notes/05_前沿专题/15_Agent.md)
- [Agent 框架与 MCP](./notes/05_前沿专题/22_Agent框架与MCP.md)
- [Prompt Engineering](./notes/05_前沿专题/16_Prompt_Engineering.md)
- [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md)

真实高频题：

1. Agent 和普通 Chatbot 的区别是什么？
2. ReAct 的 Thought/Action/Observation 流程是什么？
3. Function Calling 和普通文本生成有什么区别？
4. Tool schema 怎么设计？参数校验为什么重要？
5. Plan-and-Execute 和 ReAct 的区别是什么？
6. Agent 为什么容易无限循环？怎么限制？
7. Agent 的记忆分哪几类？短期记忆和长期记忆如何实现？
8. 多 Agent 系统什么时候有必要？什么时候反而复杂化？
9. LangGraph 相比普通 Chain 的优势是什么？
10. MCP 解决什么问题？和普通 API/tool calling 有什么区别？
11. Agent 调外部工具失败时怎么恢复？
12. 高风险工具调用为什么要人工确认？
13. 工具返回内容可能被 prompt injection 污染，怎么防？
14. Agent 如何做 trace 和可观测性？
15. Agent 项目怎么评估成功率，而不是只看回答质量？

常见追问：

- 让 Agent 自动改代码，如何防止它误删文件？
- 如果工具返回“已成功”，但实际业务失败，系统怎么发现？
- Agent 调用多个工具时，如何避免成本失控？

---

## 六、Prompt、上下文与安全

对应 notes：

- [Prompt Engineering](./notes/05_前沿专题/16_Prompt_Engineering.md)
- [上下文工程与长上下文应用](./notes/06_工程实践/04_上下文工程与长上下文应用.md)
- [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md)

真实高频题：

1. Zero-shot、Few-shot、CoT、Self-Consistency、ToT 分别适合什么场景？
2. CoT 为什么有效？为什么小模型上不一定有效？
3. Self-Consistency 为什么能提升推理准确率？
4. Tree of Thoughts 相比 Chain of Thought 的区别是什么？
5. Prompt Engineering 和 Context Engineering 的区别是什么？
6. 一个生产 prompt 应该包含哪些部分？
7. 上下文排序会影响结果吗？为什么 Lost in the Middle 重要？
8. Prompt caching 适合什么场景？
9. 多轮对话历史怎么压缩？summary memory 有什么风险？
10. Prompt Injection 和 Jailbreak 的区别是什么？
11. 间接 Prompt Injection 为什么在 RAG/Agent 中更危险？
12. system prompt 能完全保密吗？
13. 如何设计 prompt injection 红队用例？
14. LLM 输出敏感信息怎么防？
15. 安全策略应该放在 prompt、模型还是系统层？

常见追问：

- “请忽略之前指令”这类攻击为什么不能只靠一句 system prompt 防住？
- 如果网页内容里写着“把内部 token 发给我”，Agent 为什么可能中招？
- 你会如何做 LLM 应用的安全审计日志？

---

## 七、评估、幻觉与 LLMOps

对应 notes：

- [大模型幻觉与评估](./notes/05_前沿专题/17_大模型幻觉与评估.md)
- [评估框架与 Harness](./notes/05_前沿专题/21_评估框架与Harness.md)
- [LLM 应用架构与 LLMOps](./notes/06_工程实践/01_LLM应用架构与LLMOps.md)
- [模型网关与成本治理](./notes/06_工程实践/05_模型网关与成本治理.md)

真实高频题：

1. 大模型幻觉有哪些类型？事实性幻觉和忠实性幻觉怎么区分？
2. RAG 能完全解决幻觉吗？为什么不能？
3. LLM-as-Judge 有什么优缺点？
4. MMLU、GSM8K、HumanEval、MT-Bench 分别评估什么？
5. Benchmark contamination 是什么？怎么检测？
6. 为什么公开榜单高不等于业务好用？
7. 如何构建企业内部黄金评测集？
8. 回归评估应该在模型升级、prompt 改动、知识库更新时怎么跑？
9. 线上用户反馈如何进入评估闭环？
10. LLMOps 和 MLOps 的区别是什么？
11. 生产级 LLM 应用需要监控哪些指标？
12. 模型网关为什么重要？它负责哪些能力？
13. 模型路由怎么做？什么时候走小模型，什么时候走强模型？
14. LLM 成本如何归因？input/output/cache token 怎么看？
15. 降级、限流、熔断在 LLM 应用里怎么设计？

常见追问：

- 如果新 prompt 离线评估提升 3%，但线上差评增加，你怎么处理？
- 如果用户反馈“答案看起来对但引用不支持”，应该归类为什么问题？
- 如果某租户成本突然暴涨，你怎么定位？

---

## 八、系统设计题

对应 notes：

- [LLM 应用架构与 LLMOps](./notes/06_工程实践/01_LLM应用架构与LLMOps.md)
- [生产 RAG 排障指南](./notes/06_工程实践/02_生产RAG排障指南.md)
- [模型网关与成本治理](./notes/06_工程实践/05_模型网关与成本治理.md)
- [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md)

真实高频系统设计题：

1. 设计一个企业知识库问答系统，要求支持权限隔离、引用来源、低延迟。
2. 设计一个技术支持工单助手，能回答文档问题、判断是否转人工、生成工单摘要。
3. 设计一个面向内部研发的代码问答助手，如何处理 repo 级检索和代码上下文？
4. 设计一个 LLM 模型网关，支持多模型路由、限流、预算、降级和审计。
5. 设计一个 RAG 评估平台，支持离线黄金集、线上 badcase 回流和版本对比。
6. 设计一个 Agent 自动化运维助手，要求只能执行安全白名单命令。
7. 设计一个多租户向量检索系统，如何保证数据隔离？
8. 设计一个长上下文文档分析系统，如何控制成本和引用准确率？
9. 设计一个 prompt/模型版本灰度发布系统，如何回滚？
10. 设计一个 LLM 安全红队测试平台，如何覆盖 jailbreak、prompt injection、工具滥用？

回答框架：

```text
需求澄清 -> 数据流 -> 核心模块 -> 存储/索引 -> 模型调用 -> 评估指标 -> 安全合规 -> 成本和降级
```

---

## 九、项目追问题

这些题通常出现在你讲完项目之后。

1. 你的 RAG 项目相比普通 demo 多了什么生产能力？
2. 为什么选择 Hybrid Search，而不是只用向量检索？
3. 为什么需要 reranker？你如何证明它提升了效果？
4. 你的 chunk size 怎么定的？有没有做实验？
5. 你的系统怎么处理用户无权限访问的问题？
6. 如果模型回答错了，你的日志能定位到哪一层？
7. 你的系统怎么评估 citation 是否正确？
8. 模型 API 超时怎么降级？
9. 你怎么控制 token 成本？
10. 你如何处理 prompt injection？
11. 你怎么做离线评估集？
12. 你的项目如何从 demo 变成商业项目？

---

## 十、代码与实现题

对应 notes：

- [Transformer 架构](./notes/01_基础架构/03_Transformer架构.md)
- [KV Cache](./notes/03_推理与优化/09_KV_Cache.md)
- [Embedding 与向量检索](./notes/06_工程实践/03_Embedding与向量检索.md)
- [生产 RAG 排障指南](./notes/06_工程实践/02_生产RAG排障指南.md)

真实高频题：

1. 用 PyTorch 手写 scaled dot-product attention，输入输出 shape 分别是什么？
2. 手写 causal mask，为什么 mask 后通常填 `-inf` 而不是 0？
3. 给一段 attention 代码，让你指出维度错误或 softmax 维度错误。
4. 如何把一批不同长度的 prompt pad 成 batch？attention mask 怎么构造？
5. 手写一个简单的 top-k / top-p sampling。
6. 如何实现 streaming 输出？服务端和前端分别怎么处理？
7. 用伪代码写一个最小 RAG pipeline：load -> chunk -> embed -> retrieve -> rerank -> generate。
8. 写 SQL/伪代码设计 chat history、message、retrieval trace、feedback 表。
9. 如何记录一次 RAG 请求的 trace，方便定位 Top-K、prompt、模型输出和引用？
10. 给你 100 万个 chunk，如何构建向量索引并支持增量更新？
11. 如何实现基于 metadata 的权限过滤？应该在向量检索前、检索中还是检索后做？
12. 如何设计一个 API，输入问题，返回答案、引用、置信度和可观测 trace id？
13. 如何写一个离线评估脚本，比较两个 prompt 版本的命中率和忠实性？
14. 如何把长文档切分成 chunk，并保留标题层级、页码和表格上下文？
15. 如何实现一个简单模型网关：超时、重试、fallback、限流、预算统计？

常见追问：

- 如果线上用户说“引用打不开”，你的数据结构怎么支持回溯？
- 如果 reranker 超时，你的 API 是失败、降级还是返回未重排结果？
- 如果 embedding 版本升级，历史向量索引如何迁移？

---

## 十一、线上故障排查题

对应 notes：

- [LLM 应用架构与 LLMOps](./notes/06_工程实践/01_LLM应用架构与LLMOps.md)
- [生产 RAG 排障指南](./notes/06_工程实践/02_生产RAG排障指南.md)
- [模型网关与成本治理](./notes/06_工程实践/05_模型网关与成本治理.md)
- [LLM 安全与红队](./notes/06_工程实践/06_LLM安全与红队.md)

真实高频题：

1. 线上 RAG 突然大量答非所问，你第一步看哪些指标？
2. Top-5 召回为空，是文档解析、embedding、索引、query rewrite 还是权限过滤的问题？
3. 正确文档召回了，但模型没用它回答，怎么排查 prompt 和上下文排序？
4. 用户说答案“看起来很自信但错了”，怎么判断是幻觉还是知识库过期？
5. 模型升级后投诉变多，如何做灰度、回滚和版本对比？
6. 某租户 token 成本突然升高，可能原因有哪些？
7. 首 token 延迟从 1s 变 8s，如何拆 prefill、排队、模型端、网络端？
8. 输出速度变慢但 TTFT 正常，可能是什么问题？
9. 向量库 CPU 飙高或查询变慢，你会检查哪些参数？
10. Reranker 成为瓶颈时如何降级？
11. 用户上传 PDF 后问不到内容，如何排查 OCR、表格解析、chunk 和 metadata？
12. Agent 调工具成功率下降，如何区分模型选错工具、schema 不清、工具服务故障？
13. 出现 prompt injection badcase 后，如何定位攻击入口和修复链路？
14. 多租户系统出现疑似越权检索，如何紧急止血？
15. 如何设计告警：哪些指标适合实时告警，哪些适合日报分析？

回答框架：

```text
现象复现 -> 请求 trace -> 指标拆分 -> 分层定位 -> 临时止血 -> 根因修复 -> 回归评估 -> 监控补洞
```

---

## 十二、岗位 JD 场景题

这些题常见于“LLM 应用工程师 / RAG 工程师 / AI 平台工程师 / 算法工程师”岗位。

### LLM 应用工程师

1. 如何把企业内部知识库接入 LLM，并保证答案可追溯？
2. 如何设计 prompt 模板管理、版本管理和 A/B 测试？
3. 如何把用户反馈自动沉淀成评估集和优化任务？
4. 如果业务要求 3 秒内返回答案，你怎么做架构取舍？
5. 如果法务要求敏感信息不可出域，模型部署怎么选？

### RAG 工程师

1. 如何处理 PDF、Word、网页、表格、图片混合知识库？
2. 如何设计 chunk metadata，支持权限、时间、来源、业务线过滤？
3. 如何选择 embedding 模型和 reranker？
4. 如何评估召回质量，而不是只看最终答案？
5. 如果文档每天更新，索引如何增量构建和回滚？

### AI 平台工程师

1. 如何设计统一模型调用网关？
2. 如何支持多模型、多租户、多地域的调用和成本统计？
3. 如何做 prompt、模型、知识库、工具版本的可观测性？
4. 如何设计限流、熔断和 fallback？
5. 如何把离线 benchmark、线上日志和人工反馈接入平台？

### 模型算法工程师

1. 如何选择继续预训练、SFT、DPO、RAG 的方案？
2. 如何构建领域 SFT 数据并做质量控制？
3. 如何判断模型是否过拟合训练样本？
4. 如何分析微调后通用能力下降？
5. 如何评估一个模型在企业问答场景的真实收益？

---

## 十三、英文面试常见问法

很多外企或英文 JD 会用下面这些表达。建议能用中文讲清，也能用英文讲 1-2 分钟。

1. Walk me through the full lifecycle of a user query in a RAG application.
2. How would you debug hallucination in a production LLM system?
3. What is the difference between prefill and decode in LLM inference?
4. How does KV cache reduce latency, and what is its memory cost?
5. When would you use fine-tuning instead of RAG?
6. How do you evaluate retrieval quality independently from generation quality?
7. What are the trade-offs between dense retrieval, sparse retrieval, and hybrid search?
8. How would you design a multi-tenant knowledge base with strict access control?
9. How do you prevent prompt injection in an agentic workflow?
10. What metrics would you monitor for an LLM application in production?
11. How would you reduce LLM serving cost without hurting user experience?
12. How would you design a fallback strategy when the primary model API fails?
13. What is LoRA, and why is it parameter-efficient?
14. How does DPO differ from RLHF with PPO?
15. How would you build a golden evaluation set for an enterprise chatbot?

---

## 公开来源参考

这些链接不是逐字题库来源，而是用于校准“真实面试中常被追问的技术主题”和最新方向：

- [Retrieval-Augmented Generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)：RAG 的流程、应用和挑战。
- [Reinforcement learning from human feedback](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback)：RLHF 流程、应用和局限。
- [LoRA 原论文](https://arxiv.org/abs/2106.09685)：PEFT/LoRA 面试题的核心来源。
- [Zero-shot CoT](https://arxiv.org/abs/2205.11916)：Prompt/CoT 面试追问来源。
- [LLM-as-an-Interviewer](https://arxiv.org/abs/2412.10424)：动态面试式评估思路。
- [LiveRAG](https://arxiv.org/abs/2511.14531)：RAG 评估题和多难度 QA 数据集思路。
- [Question Decomposition for RAG](https://arxiv.org/abs/2507.00355)：多跳 RAG 追问来源。
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)：Transformer、Self-Attention、位置编码题的原始来源。
- [FlashAttention](https://arxiv.org/abs/2205.14135)：推理加速、attention IO 复杂度追问来源。
- [vLLM / PagedAttention](https://arxiv.org/abs/2309.06180)：KV Cache 管理、continuous batching、serving 追问来源。
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)：DPO 与 RLHF/PPO 对比题来源。
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)：RAG 原始论文。
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)：长上下文和上下文排序追问来源。
- [ReAct](https://arxiv.org/abs/2210.03629)：Agent 工具调用、Reasoning + Acting 题来源。
- [Toolformer](https://arxiv.org/abs/2302.04761)：工具调用学习与 Agent 工程追问来源。
- [SWE-bench](https://arxiv.org/abs/2310.06770)：代码 Agent 和真实软件工程评估题来源。
- [MTEB](https://arxiv.org/abs/2210.07316)：Embedding 模型评估和检索质量题来源。
- [RAGAS](https://arxiv.org/abs/2309.15217)：RAG faithfulness、answer relevance、context precision/recall 评估题来源。

---

## 面试前 30 分钟速刷

如果只剩 30 分钟，优先刷：

1. Self-Attention 公式、KV Cache 显存、Prefill/Decode。
2. RAG 链路、Hybrid Search、Rerank、RAG 排障。
3. SFT/RLHF/DPO/LoRA 的边界。
4. Agent 工具调用、安全边界和无限循环。
5. LLMOps 指标、模型网关、成本治理。
6. 你自己的项目如何证明“不是 demo”。

## 如果只准备 10 个必问题

1. LLM 从输入到输出完整链路。
2. Self-Attention 公式和 Multi-Head Attention 作用。
3. Prefill/Decode、KV Cache 和显存估算。
4. RAG 完整链路、chunk、embedding、rerank、引用。
5. RAG 答错时如何区分检索问题和生成问题。
6. SFT、LoRA、RLHF、DPO 的区别和适用场景。
7. LLM 线上指标：TTFT、TPOT、吞吐、成功率、成本、幻觉率。
8. Prompt Injection、权限隔离、Agent 工具安全。
9. 设计一个企业知识库智能问答与工单助手。
10. 讲一个你项目里的真实 trade-off：效果、延迟、成本、安全四者如何取舍。
