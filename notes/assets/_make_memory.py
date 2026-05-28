"""Memory consumption breakdown for LLM training."""
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(15, 6))
fig.patch.set_facecolor('#0f1117')

# 左图：训练时显存饼图
ax1 = plt.subplot(1, 2, 1)
ax1.set_facecolor('#1a1d2e')
labels = ['模型权重\n(FP16, 2Φ)', '梯度\n(FP16, 2Φ)', 'Adam m\n(FP32, 4Φ)',
          'Adam v\n(FP32, 4Φ)', 'FP32 主权重\n(4Φ)']
sizes = [2, 2, 4, 4, 4]
colors = ['#7c6af7', '#5eead4', '#f472b6', '#fbbf24', '#4ade80']
explode = (0.04, 0.04, 0.04, 0.04, 0.04)

wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                     startangle=90, explode=explode,
                                     textprops={'color': '#e2e8f0', 'fontsize': 10, 'fontweight': 'bold'})
for autotext in autotexts:
    autotext.set_color('#0f1117')
    autotext.set_fontweight('bold')

ax1.set_title('混合精度训练显存占比 (Φ 为参数量)\n总计 16Φ bytes/参数',
              color='#5eead4', fontsize=13, fontweight='bold', pad=14)

# 右图：ZeRO 三阶段显存柱状图
ax2 = plt.subplot(1, 2, 2)
ax2.set_facecolor('#1a1d2e')

stages = ['Baseline\n(DDP)', 'ZeRO-1\n(优化器分片)', 'ZeRO-2\n(+ 梯度分片)', 'ZeRO-3\n(+ 参数分片)']
memory_per_gpu = [16, 4, 2, 0.5]  # 假设 N=8 卡的相对显存
colors_bar = ['#f87171', '#fbbf24', '#5eead4', '#4ade80']

bars = ax2.bar(stages, memory_per_gpu, color=colors_bar, edgecolor='#0f1117', linewidth=2.5)
for bar, val in zip(bars, memory_per_gpu):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
             f'{val}Φ', ha='center', va='bottom',
             color='#e2e8f0', fontsize=12, fontweight='bold')

ax2.set_ylabel('单卡显存 (相对 Φ)', color='#e2e8f0', fontsize=11)
ax2.set_title('ZeRO 三阶段：单卡显存随分片粒度递减\n(假设 N=8 张卡)',
              color='#5eead4', fontsize=13, fontweight='bold', pad=14)
ax2.tick_params(colors='#e2e8f0')
ax2.spines[:].set_color('#94a3b8')
ax2.grid(axis='y', alpha=0.15, color='#94a3b8')
ax2.set_ylim(0, 18)

plt.tight_layout()
plt.savefig('D:/vscode/VSCode.C/llm面试准备日志/notes/assets/memory_breakdown.png',
            dpi=120, facecolor='#0f1117', bbox_inches='tight')
print("Saved memory_breakdown.png")
