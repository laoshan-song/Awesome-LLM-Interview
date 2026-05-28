"""LLM evolution timeline."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

events = [
    (2017.5, '2017.6', 'Transformer', 'Attention is All You Need', '#7c6af7'),
    (2018.7, '2018.10', 'BERT', 'Encoder-only 双向预训练', '#5eead4'),
    (2018.4, '2018.6', 'GPT-1', 'Decoder-only 路线起点', '#f472b6'),
    (2020.5, '2020.5', 'GPT-3', '175B 涌现 In-Context Learning', '#fbbf24'),
    (2022.2, '2022.3', 'InstructGPT', 'RLHF 对齐范式确立', '#4ade80'),
    (2022.11, '2022.11', 'ChatGPT', '改变历史', '#f87171'),
    (2023.2, '2023.2', 'LLaMA', '开源生态起飞', '#a78bfa'),
    (2023.7, '2023.7', 'LLaMA 2', 'GQA + RLHF 开源', '#60a5fa'),
    (2024.4, '2024.4', 'LLaMA 3', '15T tokens 训练', '#34d399'),
    (2024.5, '2024.5', 'DeepSeek-V2', 'MLA + 细粒度 MoE', '#fb923c'),
    (2024.12, '2024.12', 'DeepSeek-V3', 'FP8 训练 + 671B MoE', '#e879f9'),
    (2025.1, '2025.1', 'DeepSeek-R1', '纯 RL 涌现推理能力', '#22d3ee'),
    (2025.3, '2025.3', 'Qwen3 系列', '混合推理模式', '#f59e0b'),
    (2025.10, '2025.10', 'GPT-5', '统一推理模型范式', '#ec4899'),
]

y_levels = [0.6, -0.7, 0.45, -0.55, 0.7, -0.6, 0.5, -0.5, 0.65, -0.6, 0.55, -0.55, 0.65, -0.65]

ax.axhline(y=0, color='#7c6af7', linewidth=2.5, alpha=0.7, zorder=1)

for (year, date_str, name, desc, color), y in zip(events, y_levels):
    ax.plot(year, 0, 'o', markersize=14, color=color, zorder=3,
            markeredgecolor='#0f1117', markeredgewidth=2)
    ax.plot([year, year], [0, y], color=color, linewidth=1.5, alpha=0.5, zorder=2)

    box = FancyBboxPatch((year - 0.55, y - 0.18 if y > 0 else y - 0.04),
                          1.1, 0.22,
                          boxstyle="round,pad=0.02",
                          facecolor='#1a1d2e', edgecolor=color, linewidth=1.5, zorder=4)
    ax.add_patch(box)

    text_y = y - 0.07 if y > 0 else y + 0.06
    ax.text(year, text_y, name, ha='center', va='center',
            color=color, fontsize=10, fontweight='bold', zorder=5)
    ax.text(year, text_y - 0.075 if y > 0 else text_y - 0.075, desc, ha='center', va='center',
            color='#94a3b8', fontsize=7.5, zorder=5)
    ax.text(year, 0.07 if y > 0 else -0.09, date_str, ha='center', va='center',
            color='#e2e8f0', fontsize=7, fontweight='bold', zorder=5)

ax.set_xlim(2016.8, 2026)
ax.set_ylim(-1.1, 1.1)
ax.set_xticks(range(2017, 2026))
ax.set_xticklabels([str(y) for y in range(2017, 2026)], color='#e2e8f0', fontsize=11)
ax.set_yticks([])
ax.spines[:].set_visible(False)
ax.tick_params(colors='#e2e8f0', length=0)

ax.set_title('LLM 发展时间轴：从 Transformer 到 GPT-5 (2017-2025)',
             color='#5eead4', fontsize=15, fontweight='bold', pad=18)

# 添加几个分期标签
for x_pos, label, c in [(2018.5, '架构奠基期', '#7c6af7'),
                          (2022, '范式确立期', '#fbbf24'),
                          (2024.5, '开源繁荣期', '#4ade80')]:
    ax.text(x_pos, 1.02, label, ha='center', color=c, fontsize=11,
            fontweight='bold', alpha=0.8)

plt.tight_layout()
plt.savefig('D:/vscode/VSCode.C/llm面试准备日志/notes/assets/llm_timeline.png',
            dpi=120, facecolor='#0f1117', bbox_inches='tight')
print("Saved llm_timeline.png")
