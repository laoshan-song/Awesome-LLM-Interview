# 笔记配图资源

本目录存放笔记中嵌入的 PNG 图片以及生成它们的 Python 脚本。

## 图片清单

| 文件 | 用于 | 内容 |
|------|------|------|
| `rope_rotation.png` | [04_位置编码.md](../01_基础架构/04_位置编码.md) | RoPE 旋转位置编码可视化（3 个不同位置） |
| `llm_timeline.png` | [05_主流模型架构对比.md](../01_基础架构/05_主流模型架构对比.md) | LLM 2017-2025 发展时间轴 |
| `attention_variants.png` | [05_主流模型架构对比.md](../01_基础架构/05_主流模型架构对比.md) | MHA / GQA / MQA 注意力变体对比 |
| `memory_breakdown.png` | [02_显存优化技巧.md](../04_分布式训练/02_显存优化技巧.md) | 混合精度训练显存饼图 + ZeRO 阶段对比 |

## 重新生成

所有图片都用 matplotlib 生成。如果需要修改样式或重新生成：

```bash
cd notes/assets
python _make_rope.py       # 生成 rope_rotation.png
python _make_timeline.py   # 生成 llm_timeline.png
python _make_attention.py  # 生成 attention_variants.png
python _make_memory.py     # 生成 memory_breakdown.png
```

依赖：`matplotlib`, `numpy`。

## 配色

所有图片使用统一的暗色主题，与项目网站 `cheatsheet.html` 配色一致：
- 背景：`#0f1117`
- 卡片：`#1a1d2e` / `#252840`
- 主色（紫）：`#7c6af7`
- 辅色（青）：`#5eead4`
- 强调（粉/黄/绿）：`#f472b6` / `#fbbf24` / `#4ade80`
