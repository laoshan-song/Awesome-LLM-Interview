"""Generate RoPE visualization PNG."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Circle
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor('#0f1117')

positions = [0, 3, 7]
titles = ['位置 m=0', '位置 m=3', '位置 m=7']
colors = ['#7c6af7', '#5eead4', '#f472b6']

base_vec = np.array([1.0, 0.5])
theta = 0.5

for ax, m, title, c in zip(axes, positions, titles, colors):
    ax.set_facecolor('#1a1d2e')
    ax.spines[:].set_color('#94a3b8')
    ax.tick_params(colors='#e2e8f0')

    rotation = m * theta
    rot_matrix = np.array([[np.cos(rotation), -np.sin(rotation)],
                           [np.sin(rotation), np.cos(rotation)]])
    rotated = rot_matrix @ base_vec

    ax.arrow(0, 0, base_vec[0], base_vec[1],
             head_width=0.08, head_length=0.1, fc='#94a3b8', ec='#94a3b8', alpha=0.4,
             length_includes_head=True, label='原始向量')
    ax.arrow(0, 0, rotated[0], rotated[1],
             head_width=0.08, head_length=0.1, fc=c, ec=c,
             length_includes_head=True, linewidth=2.2)

    if m > 0:
        arc_t = np.linspace(0, rotation, 50)
        r = 0.35
        ax.plot(r*np.cos(arc_t), r*np.sin(arc_t), color=c, alpha=0.6, linewidth=1.5)
        mid_t = rotation / 2
        ax.text(0.5*np.cos(mid_t), 0.5*np.sin(mid_t), f'{m}θ',
                color=c, fontsize=12, ha='center', fontweight='bold')

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15, color='#94a3b8')
    ax.axhline(y=0, color='#94a3b8', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='#94a3b8', linewidth=0.5, alpha=0.3)
    ax.set_title(title, color='#e2e8f0', fontsize=14, pad=12, fontweight='bold')

fig.suptitle('RoPE 旋转位置编码：q 向量在不同位置 m 被旋转 m·θ 角度',
             color='#5eead4', fontsize=15, fontweight='bold', y=0.98)
fig.text(0.5, 0.02, '相对距离 (m-n) 决定了 q_m·k_n 的内积，与绝对位置无关',
         color='#94a3b8', fontsize=11, ha='center', style='italic')

plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.12)
plt.savefig('D:/vscode/VSCode.C/llm面试准备日志/notes/assets/rope_rotation.png',
            dpi=120, facecolor='#0f1117', bbox_inches='tight')
print("Saved rope_rotation.png")
