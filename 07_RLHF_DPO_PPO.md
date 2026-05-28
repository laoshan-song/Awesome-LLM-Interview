# RLHF / DPO / PPO 对比

## 面试高频考点
- RLHF 的完整流程是什么？
- DPO 和 RLHF 的区别？
- PPO 为什么训练不稳定？

---

## RLHF 完整流程

**Step 1：收集偏好数据**
对同一 prompt，模型生成多个回复，人工标注哪个更好（y_w > y_l）。

**Step 2：训练奖励模型（RM）**
用 Bradley-Terry 模型拟合人类偏好，RM 输出标量分数表示回复质量。

**Step 3：PPO 优化语言模型**
以 RM 分数为奖励，用 PPO 更新策略，加 KL 惩罚防止偏离 SFT 模型：
```
reward = RM(x,y) - β * KL(π_θ || π_ref)
```

---

## PPO 原理

PPO 通过限制每次更新幅度来稳定训练，将新旧策略的概率比 clip 到 [1-ε, 1+ε] 内。

在 LLM 中，每个 Token 是一个动作，完整回复结束后才有奖励（稀疏奖励问题）。

**RLHF 需要同时维护 4 个模型**：Actor（被训练的 LLM）、Critic（价值网络）、Reference（SFT 模型）、Reward Model。

---

## DPO（Direct Preference Optimization）

**核心**：绕过显式 RM，直接从偏好数据优化语言模型。

RLHF 的最优策略有闭合解，将其代入 Bradley-Terry 损失后，DPO 目标变为：

```
L_DPO = -E[log σ(β * log(π_θ(y_w|x)/π_ref(y_w|x)) - β * log(π_θ(y_l|x)/π_ref(y_l|x)))]
```

**直觉**：增大好回复概率，降低差回复概率，同时与参考模型不偏太远。

---

## RLHF vs DPO 对比

| 维度 | RLHF | DPO |
|------|------|-----|
| 是否需要 RM | 需要 | 不需要 |
| 训练稳定性 | 差（PPO 不稳定）| 好（有监督学习）|
| 实现复杂度 | 高（需要 4 个模型）| 低 |
| 在线 vs 离线 | 在线 | 离线 |
| 性能 | 强 | 接近，有时更好 |

---

## 面试延伸

**Q：为什么 RLHF 需要 KL 惩罚？**
> 没有 KL 惩罚，模型会 reward hacking——找到让 RM 打高分但实际质量差的回复。

**Q：DPO 的局限性？**
> 离线训练，无法利用 on-policy 数据；存在分布偏移问题。改进方案：IPO、SimPO、ORPO。


---

## 原始论文

| 论文 | 链接 |
|------|------|
| InstructGPT / RLHF (Ouyang et al., 2022) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) |
| Direct Preference Optimization (Rafailov et al., 2023) | [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290) |

## 延伸阅读与视频

> 视频链接持续更新中，欢迎 PR 补充优质资源
