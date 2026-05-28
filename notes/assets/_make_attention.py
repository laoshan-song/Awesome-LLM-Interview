"""Attention variants complexity & KV cache visualization."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
fig.patch.set_facecolor('#0f1117')

titles = ['MHA (Multi-Head Attention)', 'GQA (Grouped-Query, G=2)', 'MQA (Multi-Query)']
configs = [
    {'q_heads': 8, 'kv_heads': 8, 'color': '#f87171'},
    {'q_heads': 8, 'kv_heads': 4, 'color': '#5eead4'},
    {'q_heads': 8, 'kv_heads': 1, 'color': '#4ade80'},
]

for ax, title, cfg in zip(axes, titles, configs):
    ax.set_facecolor('#1a1d2e')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title(title, color=cfg['color'], fontsize=12, fontweight='bold', pad=8)

    # Q heads (top row)
    n_q = cfg['q_heads']
    q_width = 8 / n_q
    for i in range(n_q):
        x = 1 + i * q_width
        rect = FancyBboxPatch((x, 7), q_width * 0.85, 1.2,
                                boxstyle="round,pad=0.04",
                                facecolor='#7c6af7', edgecolor='white', linewidth=1, alpha=0.85)
        ax.add_patch(rect)
        ax.text(x + q_width * 0.42, 7.6, f'Q{i+1}', ha='center', va='center',
                color='white', fontsize=8, fontweight='bold')
    ax.text(0.5, 7.6, 'Query', color='#e2e8f0', fontsize=10, fontweight='bold',
            ha='right', va='center')

    # KV heads (bottom row)
    n_kv = cfg['kv_heads']
    kv_width = 8 / n_kv
    for i in range(n_kv):
        x = 1 + i * kv_width
        rect = FancyBboxPatch((x, 1.5), kv_width * 0.92, 1.5,
                                boxstyle="round,pad=0.04",
                                facecolor=cfg['color'], edgecolor='white', linewidth=1, alpha=0.85)
        ax.add_patch(rect)
        ax.text(x + kv_width * 0.46, 2.3, f'K{i+1}V{i+1}', ha='center', va='center',
                color='#0f1117', fontsize=8, fontweight='bold')
    ax.text(0.5, 2.25, 'KV', color='#e2e8f0', fontsize=10, fontweight='bold',
            ha='right', va='center')

    # Mapping arrows from Q to KV
    if n_kv == n_q:  # MHA: 1:1
        for i in range(n_q):
            qx = 1 + i * q_width + q_width * 0.42
            kvx = 1 + i * kv_width + kv_width * 0.46
            ax.annotate('', xy=(kvx, 3), xytext=(qx, 7),
                        arrowprops=dict(arrowstyle='->', color=cfg['color'], alpha=0.4, lw=0.8))
    elif n_kv == 1:  # MQA: all to one
        for i in range(n_q):
            qx = 1 + i * q_width + q_width * 0.42
            ax.annotate('', xy=(5, 3), xytext=(qx, 7),
                        arrowprops=dict(arrowstyle='->', color=cfg['color'], alpha=0.4, lw=0.8))
    else:  # GQA: groups
        group_size = n_q // n_kv
        for i in range(n_q):
            qx = 1 + i * q_width + q_width * 0.42
            kv_idx = i // group_size
            kvx = 1 + kv_idx * kv_width + kv_width * 0.46
            ax.annotate('', xy=(kvx, 3), xytext=(qx, 7),
                        arrowprops=dict(arrowstyle='->', color=cfg['color'], alpha=0.4, lw=0.8))

    # Stats box
    kv_cache_ratio = cfg['kv_heads'] / cfg['q_heads']
    ax.text(5, 0.3, f'KV Cache 大小：{kv_cache_ratio*100:.0f}% (相对 MHA)',
            ha='center', color='#94a3b8', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#252840', edgecolor=cfg['color']))

fig.suptitle('Attention 变体对比：从 MHA → GQA → MQA，KV Cache 逐步压缩',
             color='#5eead4', fontsize=14, fontweight='bold', y=0.97)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig('D:/vscode/VSCode.C/llm面试准备日志/notes/assets/attention_variants.png',
            dpi=120, facecolor='#0f1117', bbox_inches='tight')
print("Saved attention_variants.png")
