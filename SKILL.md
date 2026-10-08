---
name: sci-figures
description: 科研作图：论点 → 图式 → 成图，含图式库与 mpl_style 工具箱（中文矢量出图、色盲安全配色）。触发词：画图、科研图、论文插图、示意图、对比图、曲线图、图式、配色、矢量导出、PDF 出图、中文字体、matplotlib、画一张图、figure、plot。补充触发词：出图路线、工具链、样式工具箱、色盲安全配色、图式库。
whenToUse: 要为主张/实验**出一张图**（论文插图、汇报图、方法总览）时；想换一种更有说服力的图式时；图里的中文变成方框 / 导出后字体错乱时；要沉淀「哪种图画哪种话」的经验时。
---

> 🕒 v1 · 2026-10-08 20:09 · dsh-agent ｜ 变更：初稿：sci-figures 技能主文件（脱敏版）


# 科研作图（sci-figures）

## 30 秒速览

| | |
|---|---|
| **样式工具箱** | **`scripts/mpl_style.py`** —— **期刊样式（SciencePlots）** / 中文字体 / 矢量导出（含 **pgf**）/ 色盲安全配色 / **四个图式的现成函数** |
| **图式库** | **[`references/图式库.md`](references/图式库.md)** —— 钉子 · 阶梯 · 滑轴 · 魔方串烧 · 横排对照（**append-only，不断更新**） |
| **工具链** | **[`references/工具链.md`](references/工具链.md)** —— **六条出图路线**（SciencePlots · pgf · TikZ · Plotly · Plotnine · Altair）+ Mermaid，**全部实测通过** + 选用判据 + **实测坑** |
| **流程** | ① 先写"这张图要证明的**一句话**" → ② 选图式 → ③ `mpl_style` 出图 → ④ 自检 → ⑤ **归档进图式库** |
| **铁律** | 🔴 **图是论据不是装饰**：写不出一句话的图别画；画完必须能被"图注 + 一句话"讲清 |

### 🚀 默认栈（别再手搓样式）

```
数据图     → mpl_style.use()  # 默认 = SciencePlots 的 science+ieee + 中文字体（一行期刊版式）
           → mpl_style.save() # PDF/SVG + 600dpi PNG，字体已嵌入
LaTeX 论文 → mpl_style.save_pgf()  # 导出 .pgf，字体与正文完全一致（编辑部最认）
探索/交互 → Plotly（选定后用上面复刻成矢量）｜ 分面/多条件 → Plotnine ｜ 结构图/流程 → Mermaid
```

> 六条路线各自的实测产物 / 选用判据 / 实测坑（SciencePlots usetex · CJK 缺 U+2212 · MiKTeX 挂起 · Plotly 大文件）→ [`references/工具链.md`](references/工具链.md)。

---

## 五步流程

```powershell
$env:PYTHONIOENCODING="utf-8"
# 1) 写论点（中文一行）：例如「SmoothL1 让达标步数下降 5%，且不牺牲成功率」
# 2) 选图式（查 references/图式库.md）：这里 → 阶梯（对比两级的跃升差）
# 3) 出图（照 scripts/mpl_style.py 的 docstring 抄）
```

```python
import sys, pathlib
# 把 <技能目录>/scripts 加进 path（改成你自己的安装位置）
sys.path.insert(0, str(pathlib.Path.home() / ".dsh/skills/sci-figures/scripts"))
import matplotlib.pyplot as plt
from mpl_style import use, save, save_pgf, PALETTE, nail, staircase, sliding_axis, cube_skewer

print(use())                            # 默认 = SciencePlots 期刊样式 + 中文字体 + 矢量嵌入
fig, ax = plt.subplots(figsize=(3.5, 2.2))   # A4 单栏宽
ax.plot([1, 2, 3], [4, 5, 6], color=PALETTE[0], label="本文")
save(fig, "figs/fig2_步数下降.pdf")     # 同时出 .pdf/.svg + 600dpi .png
# 若论文是 LaTeX：save_pgf(fig, "figs/fig2.pgf") 然后 \input{fig2.pgf}
```

4) **自检** → 5) **归档**：把这次用的图式、脚本路径、效果追加进图式库（见下"更新协议"）。

---

## 🔴 硬规则（8 条，违反其一就得重画）

1. **矢量优先**：论文插图出 **PDF/SVG**（字体必须嵌入：`pdf.fonttype=42`，`use()` 已设），PNG 只当预览。位图只用于照片/热力快照。
   → **论文是 LaTeX 写的**就再出 `.pgf`（`save_pgf()`），字体与正文完全一致。
2. **中文不出方框**：`use()` 已设 `SimHei → 微软雅黑 → SimSun` 回退链 + 关掉 SciencePlots 的 usetex；**别用默认 DejaVu**。
   ⚠️ 图里**别用真减号 `−`（U+2212）** —— CJK 子集常缺这个字形，用 ASCII `-`。
3. **字号下限**：A4 单栏图 `figsize≈(3.5, 2.2)`，字号 **≥7 pt**（`use()` 设 8），缩到栏宽后仍要能读。
4. **色盲安全 + 灰度可辨**：用 `PALETTE`（Okabe-Ito）；**不要**靠"深浅红绿"区分曲线（打印/色盲会糊）。
5. **共享色标**：多子图比热力图时**同一 `vmin/vmax` + 同一 cmap**，否则对比无效（魔方串烧尤其）。
6. **不截断坐标轴来制造差异**；真有量级差就用**滑轴/断轴**，且**必须画断口符号并标注区间**。
7. **图注自证**：种子、样本数（`20 runs`）、达标阈值、训练轮数 —— 缺一个都算不合格（实验类图全是"口径决定结论"）。
8. **数据可追溯**：画图脚本与数据路径写进图注或代码头注释；**先核对原始数据再画**（汇总文件是二手来源，别直接信）。

---

## 目录与命名约定

```
<论文目录>/figs/
  src/fig2_step_down.py        ← 画图脚本（一图一脚本，可复跑）
  fig2_步数下降.pdf / .svg      ← 投稿用矢量
  fig2_步数下降.png            ← 预览/汇报用
```

命名 = **`figN_一句话.pdf`**（图序 + 图要证明的那句话）。**别叫** `output1.png` / `fig_new2.png`。

---

## 更新协议（"不断更新"就靠这条）

**每画完一张图，做两件事**（30 秒）：

1. **已有图式** → 在 `references/图式库.md` 对应条目下追加一行「**实例**」：
   `日期 · 出处(论文/实验) · 脚本路径 · 一句话效果`。
2. **新图式**（或现有图式的变体）→ **新增一个条目**，照文件里的模板填：
   `一句话用途 / 怎么画 / 代码骨架 / 红线 / 实例`。

> ⚠️ **图式库是 append-only**：看到更好画法就**追加**，别删旧条目 —— 旧图式的坑（比如"断轴不标断口 = 误导"）本身就是资产。

---

## 与其它技能的分工

| 技能 | 管什么 |
|---|---|
| **`sci-figures`**（本技能） | **出图**：图式选择、样式、矢量导出、图式库沉淀 —— 🔴 **图里有中文（中文期刊、毕业论文）默认走这里** |
| `nature-figure`（第三方） | **英文稿 / Nature 系版式**出图 + 出图体检（PDF 真实字号、多面板对齐、元素碰撞）；字体铁律 `Arial/DejaVu Sans`，**不负责中文方框** |
| 日志诊断 / 代码分析类技能 | 出图前的**取数** |

> **一句话选法**：图里有中文 → 本技能（`mpl_style.use()`）；纯英文 + 目标是 Nature/CNS 系版式 → `nature-figure`。

---

## 已知坑（只列主档未重复的；其余见工具链分册）

> 全部实测坑与处置（中文字体/字体嵌入/热力图色标/usetex/MiKTeX 挂起/Plotly 大文件/一批图同一样式）→
> [`references/工具链.md`](references/工具链.md)「坑（实测）」；配套红线见上面「硬规则」1/2/4/5。

- ⚠️ **`figsize` 与字号不匹配**：先定栏宽（单栏 3.5 in / 双栏 7.0 in）再调 `fontsize`，别反过来。
- ⚠️ **中文仍出方框**（`use()` 已设字体仍方框）：`matplotlib.font_manager.findfont("SimHei")` 查字体是否被系统删了。
