# RLHF / DPO / PPO 对比

## 面试高频考点
- RLHF 的完整流程是什么？
- DPO 和 RLHF 的区别？
- PPO 为什么训练不稳定？四个模型各做什么？
- KL 惩罚的作用？β 怎么设？
- GRPO 相比 PPO 的改进？

---

## 一、RLHF 完整流程

RLHF（Reinforcement Learning from Human Feedback）是 InstructGPT / ChatGPT 背后的对齐技术，分为三个阶段：

### Stage 1: SFT（Supervised Fine-Tuning）

```
预训练模型 → 用高质量人工编写的 (指令, 回复) 对做微调 → SFT 模型

目的：让模型学会"遵循指令"的基本格式
数据量：通常 10K-100K 条高质量标注
```

### Stage 2: RM（Reward Model）训练

```
对同一个 prompt，SFT 模型生成多个回复（如 K=4）
标注人员对这些回复排序（y₁ > y₂ > y₃ > y₄）

用 Bradley-Terry 模型训练 RM：
  P(y_w > y_l | x) = σ(r(x, y_w) - r(x, y_l))  ← 好回复比差回复得分高的概率

  Loss = -E[log σ(r(x, y_w) - r(x, y_l))]
  直觉：让好回复和差回复的得分差距尽可能大

RM 通常是去掉最后 LM head 的 SFT 模型 + 一个标量输出头
```

### Stage 3: PPO 强化学习

```
优化目标：
  max E[r(x, y) - β · KL(π_θ(y|x) || π_ref(y|x))]

  第一项：奖励模型打分（越高越好）
  第二项：KL 惩罚（生成分布不能偏离 SFT 参考模型太远）

四个模型同时存在于显存中（这是 RLHF 显存开销大的根本原因）：

┌────────────────────────────────────────────────────┐
│  Actor (策略模型)     ← 被训练，初始化自 SFT          │
│  Critic (价值模型)    ← 被训练，估计状态价值 V(s)      │
│  Reference (参考)     ← 冻结，SFT 模型，计算 KL 惩罚   │
│  Reward Model (奖励)  ← 冻结，为每个回复打分           │
└────────────────────────────────────────────────────┘
```

---

## 二、PPO 的核心机制

### 为什么需要 PPO（而不是普通的策略梯度）？

在标准 RL 中，策略梯度更新可能导致策略突变（一次更新后策略"跳"太远），训练崩溃。PPO 的核心是 **Trust Region（信任域）**：限制每次更新的幅度。

### PPO-Clip 的核心公式

```
PPO-Clip 目标（简化版）：

L = min(
    r_t(θ) · A_t,                        ← 正常策略梯度
    clip(r_t(θ), 1-ε, 1+ε) · A_t        ← 裁剪版本
)

其中 r_t(θ) = π_θ(a_t|s_t) / π_old(a_t|s_t)   ← 新旧策略概率比
      A_t = 优势函数（实际奖励 - 基线）

如果概率比超出 [1-ε, 1+ε] 范围，梯度被裁剪 → 防止一次更新过大
```

### PPO 在 LLM 中的特殊性

```
标准 RL：每个 step 都有奖励
LLM RLHF：整个回复结束后才有一个奖励（稀疏奖励）

解决方案：
  - 用 Critic（价值网络）估计每个 token 的"未来累积奖励"
  - GAE (Generalized Advantage Estimation) 方法计算每个 token 的优势值
  - 在 token 级别做 PPO 更新（每个 token 是一个"动作"）

实现细节：
  - 对同一 prompt 生成多条回复（如 4 条），构成 mini-batch
  - 用这些回复更新 PPO（Experience Buffer）
```

---

## 三、DPO（Direct Preference Optimization）

### 核心思想：绕过 RM，直接优化

DPO 的数学洞察：RLHF 的最优策略有**解析解**：

```
RLHF 的最优策略 π* 满足：

π*(y|x) ∝ π_ref(y|x) · exp(r(x,y) / β)

反解出奖励函数：
r(x,y) = β · log(π*(y|x) / π_ref(y|x)) + β · log Z(x)
```

将这个表达式代入 Bradley-Terry 模型的损失函数，Z(x) 项会消掉，得到：

```
L_DPO = -E[log σ(
    β · log(π_θ(y_w|x) / π_ref(y_w|x))   ← 好回复的"隐式奖励"
  - β · log(π_θ(y_l|x) / π_ref(y_l|x))   ← 差回复的"隐式奖励"
)]

直觉：
  - π_θ(y_w|x) 越大越好 → 好回复的概率被提升
  - π_θ(y_l|x) 越小越好 → 差回复的概率被压制
  - π_ref 作为"锚点" → 防止偏离太远（等同于 KL 惩罚的效果）
  - β 控制偏离参考模型的程度
```

### DPO 的数学推导（简化）

```
Step 1: 写出 RLHF 的优化目标（带 KL 惩罚）

  max_π E_{y~π}[r(x,y)] - β · KL(π || π_ref)

Step 2: 这个约束优化问题有闭合解

  π*(y|x) = π_ref(y|x) · exp(r(x,y)/β) / Z(x)
  其中 Z(x) = Σ_y π_ref(y|x) · exp(r(x,y)/β)

Step 3: 反解出 r(x,y)

  r(x,y) = β · log(π*(y|x) / π_ref(y|x)) + β · log Z(x)

Step 4: 将 r 代入 Bradley-Terry 损失

  L = -E[log σ(r(x, y_w) - r(x, y_l))]
  代入 r 的表达式，log Z(x) 相消
  → 得到 DPO 损失
```

### DPO vs RLHF

| 维度 | PPO/RLHF | DPO |
|------|---------|-----|
| 需要 RM | 是（需额外训练） | **否**（隐式 RM 在损失函数中） |
| 模型数量 | 4 个（Actor + Critic + Ref + RM） | **2 个**（策略 + 参考） |
| 训练方式 | 在线 RL（需要持续采样新数据） | **离线**有监督学习 |
| 训练稳定性 | 差（RL 天然不稳定） | **好**（交叉熵 + 梯度下降） |
| 实现复杂度 | 高 | **低** |
| 在线数据利用 | ✅ 可以 | ❌ 无法利用（只训练一次） |
| 迭代改进 | ✅ 可以 | 需重复收集偏好数据 |
| 前沿模型 | ChatGPT, Claude 早期 | Llama 3, Qwen 对齐 |

---

## 四、其他对齐方法

### SimPO（Simple Preference Optimization）

```
比 DPO 更简化的方案：
  - 去掉参考模型 π_ref（减少推理时的模型数量）
  - 用生成长度做归一化：reward = log π(y|x) / |y|
  - 加入 Margin：要求好回复的归一化概率 > 差回复 + γ

优点：不需要参考模型，训练和推理都更快
```

### ORPO（Odds Ratio Preference Optimization）

```
一步完成 SFT + 对齐：

  L_ORPO = L_SFT + λ · L_OR

  其中 L_OR 是 Odds Ratio 损失，同时优化"生成好回复"和"抑制差回复"

优点：不需要单独的 SFT 阶段，一步训练完成对齐
```

### KTO（Kahneman-Tversky Optimization）

```
不需要成对偏好数据（只需单条回复的好/差标签）：

  "这条回复好" → 提升概率
  "这条回复差" → 降低概率

优点：数据标注更简单（不需要 pairwise 比较）
适合：从用户点赞/踩等隐式反馈中学习
```

---

## 五、Reward Hacking 与对策

### Reward Hacking 的典型表现

```
RLHF 训练中常见的"Cheating"模式：

① 长度偏见：RM 偏好长回复 → 模型学会"水字数"
② 礼貌偏见：RM 偏好礼貌语气 → 回复全是"当然！很棒的问题！"
③ 格式偏见：RM 偏好列表格式 → 所有回复都是 bullet points
④ 知识回避：模型拒绝回答难的题（RM 给"安全拒答"打高分）
⑤ 重复短语：RM 给某些高频短语打高分 → 模型频繁重复
```

### 检测与缓解

| 阶段 | 方法 |
|------|------|
| **数据** | 确保 RM 训练数据中好回复和差回复长度接近；加入反偏见的样本 |
| **RM 训练** | RM 集成（取多个 RM 的最低分）；RM 模型架构加入长度惩罚 |
| **PPO 训练** | KL 惩罚（核心防线）；在线标注（定期让人评估最新生成，补充进训练集） |
| **方法选择** | GRPO 用规则奖励（数学直接验证答案）→ 彻底消除 RM hacking |

---

## 六、面试延伸

**Q：为什么 RLHF 需要 KL 惩罚？β 设多少合适？**

> 没有 KL 惩罚，策略模型会"奖励黑客"——找到让 RM 打高分但实际质量差的捷径（如输出超长文本、重复正面短语等）。KL 惩罚将模型"锚定"在 SFT 参考模型附近，保证生成质量不会剧烈恶化。
>
> β 通常设为 0.01-0.5。β 太大：模型几乎不更新，学习不到偏好。β 太小：约束失效。实践中常通过监控 KL 散度来动态调整 β——如果 KL 增长过快，增大 β；如果 KL 几乎不变，减小 β。

**Q：DPO 的局限性是什么？**

> ① 离线训练：只能学习标注时的偏好分布，无法探索新策略空间（on-policy exploration）；② 分布偏移：训练时用的是 SFT 模型生成的偏好数据，但 DPO 训练过程中模型本身也在变，数据分布和当前策略不匹配；③ 对偏好数据的噪声更敏感（因为没有 RM 的平滑作用）。

**Q：为什么 PPO 在 RLHF 中训练不稳定？**

> ① 稀疏奖励（整个回复只有一个分数），价值估计的方差大；② 四个模型同时在显存中，显存压力大 → 只能用小 batch → 梯度噪声大；③ 策略和 RM 的非平稳交互（RM 的评分空间在 PPO 过程中被探索到了训练未见过的区域）；④ 超参敏感（KL 系数、学习率、clip 范围等任何一个不对都可能导致崩溃）。

**Q：GRPO 相比 PPO 有什么改进？**

> GRPO（DeepSeek-R1 使用）去掉了 Critic 网络（不需要价值函数估计），对同一 prompt 采样 G 条输出，用组内相对奖励替代绝对奖励：Advantage = (r_i - mean(r_1...r_G)) / std(r_1...r_G)。这省去了训练 Critic 的显存和时间，且对于数学/代码等可自动验证的任务尤为有效（直接用规则判断答案对错，不需要 RM）。详见 [10_前沿对齐技术.md](./10_前沿对齐技术.md)。

---

## 原始论文

| 论文 | 链接 |
|------|------|
| Training Language Models to Follow Instructions (InstructGPT / RLHF) (Ouyang et al., NeurIPS 2022) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) |
| Proximal Policy Optimization Algorithms (Schulman et al., 2017) | [arxiv.org/abs/1707.06347](https://arxiv.org/abs/1707.06347) |
| Direct Preference Optimization (Rafailov et al., NeurIPS 2023) | [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290) |
| SimPO: Simple Preference Optimization (Meng et al., ICML 2024) | [arxiv.org/abs/2405.14734](https://arxiv.org/abs/2405.14734) |
| ORPO: Monolithic Preference Optimization (Hong et al., 2024) | [arxiv.org/abs/2403.07691](https://arxiv.org/abs/2403.07691) |
| KTO: Model Alignment as Prospect Theoretic Optimization (Ethayarajh et al., ICML 2024) | [arxiv.org/abs/2402.01306](https://arxiv.org/abs/2402.01306) |
| DeepSeekMath: Pushing the Limits of Mathematical Reasoning (GRPO) (Shao et al., 2024) | [arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300) |

## 延伸阅读与视频

| 平台 | 标题 | 说明 |
|------|------|------|
| 📺 YouTube | [RLHF Explained (AssemblyAI)](https://www.youtube.com/watch?v=Im6ZwnEOy38) | 完整 RLHF 流程讲解 |
| 📺 B站 | [跟李沐学AI - InstructGPT 论文精读](https://www.bilibili.com/video/BV1hd4y187CR) | 李沐 InstructGPT 精读 |
