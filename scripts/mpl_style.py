#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🕒 v1 · 2026-10-08 20:09 · dsh-agent ｜ 变更：初稿：科研作图工具箱（脱敏版，去个人路径）

r"""
mpl_style.py — 科研作图工具箱（中文字体 / 矢量导出 / 色盲安全配色 / 四个图式）。

用法
----
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path.home() / ".dsh/skills/sci-figures/scripts"))
    import matplotlib.pyplot as plt
    from mpl_style import use, save, PALETTE, nail, staircase, sliding_axis, cube_skewer

    use()                                  # ① 一次搞定字体/字号/矢量嵌入
    fig, ax = plt.subplots(figsize=(3.5, 2.2))     # A4 单栏宽；双栏用 7.0
    ax.plot([1, 2, 3], [4, 5, 6], color=PALETTE[0], label="本文")
    nail(ax, 3, 6, "6.0 @ 20 runs")        # ② 选图式
    save(fig, "figs/fig1_一句话.pdf")       # ③ 出矢量 + 600dpi 预览

设计原则
--------
· 模板只给**骨架**，不替你做学术判断（配色/层级/口径由你定）。
· 四个图式函数都短小、可读、可直接改 —— 图式库(`references/图式库.md`)里写了各自的红线。
· 默认 A4 单栏尺寸与 8pt 字号：缩到栏宽后仍可读（≤6pt 在印刷上会糊）。
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Okabe–Ito 八色：色盲安全，灰度下也可辨（不要用纯红绿对比来表达差异）
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7",
           "#E69F00", "#56B4E9", "#F0E442", "#000000"]

# 中文字体回退链（按可用性挑第一个能用的）
CN_FONTS = ["SimHei", "Microsoft YaHei", "SimSun", "Source Han Sans CN", "Noto Sans CJK SC"]


def use(base_size: float = 8.0, single_column: bool = True, cn: bool = True,
        style: str = "science") -> str:
    """统一 rcParams：期刊样式 + 中文字体 + 字号 + 矢量字体嵌入 + 600dpi 导出。调用一次即可。

    style：
      · `"science"`（默认）—— SciencePlots 的 `['science','ieee']`：期刊级版式（栏宽/字号/线宽/刻度朝内）
      · `"nature"`  —— 上加 `nature`（无衬线、更紧凑）
      · `"cjk"`     —— science + `no-latex` + `cjk-sc-font`（**纯中文图**推荐）
      · `"plain"`   —— 不加载 SciencePlots，用本文件自带的保守 rc（旧行为，向后兼容）
      未安装 SciencePlots 时**自动回退到 plain**，不会报错。

    返回实际生效的样式串（便于日志/图注里写清楚）。
    """
    rc = {
        "figure.dpi": 150,            # 屏幕上看着别太小
        "savefig.dpi": 600,           # 位图预览分辨率
        "savefig.bbox": "tight",
        "font.size": base_size,
        "axes.titlesize": base_size,
        "axes.labelsize": base_size,
        "legend.fontsize": base_size - 1,
        "xtick.labelsize": base_size - 1,
        "ytick.labelsize": base_size - 1,
        "axes.linewidth": 0.8,
        "axes.grid": False,           # 网格默认关：论文图先干净，需要再开
        "legend.frameon": False,
        "lines.linewidth": 1.4,
        "lines.markersize": 4,
        # 🔴 矢量导出必须嵌入 TrueType，否则 PDF/SVG 在编辑部显示错乱
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        # 🔴 防御：SciencePlots 的 `science` 样式**默认开 text.usetex**（它假定你在 LaTeX 里用）。
        # 中文标签 + usetex 会直接失败/出豆腐块 —— 我们一律显式关掉（要真 usetex 自己再开）。
        "text.usetex": False,
    }

    applied = "plain"
    if style != "plain":
        try:
            import scienceplots  # noqa: F401  （必须先 import 才能用样式）
            import matplotlib.pyplot as plt
            # 中文图用 cjk-sc-font；science 默认走 LaTeX，中文场景配 no-latex 更稳
            name_map = {
                "science": ["science", "ieee"],
                "nature": ["science", "nature", "no-latex"],
                "cjk": ["science", "ieee", "no-latex", "cjk-sc-font"],
            }
            names = name_map.get(style, ["science", "ieee"])
            if cn and "cjk-sc-font" not in names:
                names = names + ["no-latex", "cjk-sc-font"]
            plt.style.use(names)
            applied = "+".join(names)
        except Exception:
            applied = "plain(回退：SciencePlots 不可用)"

    matplotlib.rcParams.update(rc)      # 我们自己的关键项**最后覆盖**（字体嵌入选型不能被样式改掉）
    if cn:
        matplotlib.rcParams["font.sans-serif"] = CN_FONTS + ["DejaVu Sans"]
        matplotlib.rcParams["font.family"] = "sans-serif"
        matplotlib.rcParams["axes.unicode_minus"] = False   # 负号不出方框
    if single_column:
        matplotlib.rcParams["figure.figsize"] = (3.5, 2.2)
    return applied


def save_pgf(fig, path: str = "", **kw) -> str:
    """matplotlib 的 **pgf 后端**：导出 .pgf 交给 LaTeX `\\input{}`，字体与论文完全一致。

    适用：论文本身是 LaTeX 写的（这是编辑部最认的做法）。
    前提：本机有 LaTeX（pgf/pgfplots 可用）。
    """
    import matplotlib
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        "pgf.rcfonts": True,
        "text.usetex": False,      # 用 pgf 而非 usetex，避免中文/特殊字符踩 TeX 转义
    })
    fig.savefig(path, **kw)
    return path


def save(fig, path: str) -> list[str]:
    """出矢量（.pdf + .svg）与 600dpi 预览（.png）；返回实际写出的文件列表。"""
    import os
    root, ext = os.path.splitext(path)
    ext = ext.lower()
    written = []
    if ext == ".pdf":
        fig.savefig(path, bbox_inches="tight")
        written.append(path)
    if ext in (".pdf", ".svg") or ext == "":
        svg = root + ".svg"
        fig.savefig(svg, bbox_inches="tight")
        written.append(svg)
    png = root + ".png"
    fig.savefig(png, dpi=600, bbox_inches="tight")
    written.append(png)
    return written


# ---------------------------------------------------------------- 图式 1：钉子
def nail(ax, x, y, text: str = "", base=None, color: str = PALETTE[1],
         marker: str = "v", dx: float = 0.0, dy: float = 0.06, fontsize=None) -> None:
    """在 (x, y) 钉一根钉子：竖杆 + 端点标记 + 一句带口径的标注。

    base=None 时竖杆从轴的 5% 高度处起（避免压住刻度）。
    红线：一张图 ≤3 根钉子；钉的位置必须有真实数据点。
    """
    if base is None:
        lo, hi = ax.get_ylim()
        base = lo + (hi - lo) * 0.05
    ax.plot([x, x], [base, y], color=color, lw=1.0, ls="-", zorder=3)
    ax.plot([x], [y], marker=marker, color=color, ms=6, zorder=4)
    if text:
        ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points",
                    ha="center", va="bottom", fontsize=fontsize, color=color)


# ------------------------------------------------------------ 图式 2：阶梯
def staircase(ax, xs, ys, events=None, label=None, color: str = PALETTE[0],
              marker: str = "o", annotate_events: bool = True):
    """画一条阶梯（step, where='post'），在每个竖直段标出触发事件。

    xs: 阶段边界（轮次）；ys: 每级的值（len(ys) == len(xs)）。
    events: {段索引: "事件名"}，标在该段**上升沿**上（如 {1: "+ SmoothL1"}）。
    红线：台阶必须来自真实离散事件；对比两条阶梯时共享纵轴。
    """
    line, = ax.step(xs, ys, where="post", marker=marker, color=color, label=label)
    if annotate_events and events:
        for idx, text in events.items():
            if 0 <= int(idx) < len(xs):
                ax.annotate(text, xy=(xs[int(idx)], ys[int(idx)]),
                            xytext=(4, 8), textcoords="offset points",
                            fontsize=matplotlib.rcParams["font.size"] - 1,
                            color=color, ha="left", va="bottom")
    return line


# ------------------------------------------------------------ 图式 3：滑轴
def sliding_axis(fig, rect_left=(0.09, 0.15, 0.38, 0.75), rect_right=(0.53, 0.15, 0.38, 0.75),
                 break_marks: bool = True, tick: float = 0.02):
    """断轴/滑轴：左右两个子图，去掉相邻 spine 并画断口斜线。

    🔴 红线：断轴**必须**留断口符号（break_marks=True）并在图注里标注两段区间；
    两段不要各自归一化纵轴。
    返回 (ax_left, ax_right)。
    """
    ax_l = fig.add_axes(rect_left)
    ax_r = fig.add_axes(rect_right)
    ax_l.spines["right"].set_visible(False)
    ax_r.spines["left"].set_visible(False)
    ax_r.tick_params(left=False, labelleft=False)     # 右段共享纵轴刻度
    if break_marks:
        for ax_, x_, flip in ((ax_l, 1.0, 1), (ax_r, 0.0, -1)):
            ax_.plot((x_ - flip * tick, x_ + flip * tick), (-tick, +tick),
                     transform=ax_.transAxes, color="k", lw=0.8, clip_on=False)
            ax_.plot((x_ - flip * tick, x_ + flip * tick), (1 - tick, 1 + tick),
                     transform=ax_.transAxes, color="k", lw=0.8, clip_on=False)
    return ax_l, ax_r


# -------------------------------------------------------- 图式 4：魔方串烧
def cube_skewer(fig, grids, titles=None, cmap: str = "viridis", vmin: float = 0.0,
                vmax: float = 1.0, arrow: bool = True, cbar: bool = True,
                label_fs=None):
    """把 N 个网格快照串成一条线（魔方串烧）。

    grids: 长度 N 的列表，每项是 2D 数组（同一坐标系、同一形状）。
    🔴 红线：**所有块共用 vmin/vmax 与 cmap**（否则不可比）；N 建议 4–6。
    返回 axes 列表。
    """
    n = len(grids)
    gs = GridSpec(1, n, figure=fig, wspace=0.15)
    axes = []
    im = None
    for i, grid in enumerate(grids):
        ax = fig.add_subplot(gs[0, i])
        im = ax.imshow(grid, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title((titles[i] if titles and i < len(titles) else f"t{i}"),
                     fontsize=label_fs)
        for s in ax.spines.values():
            s.set_linewidth(0.6)
        if i > 0 and arrow:
            ax.annotate("", xy=(-0.16, 0.5), xytext=(-0.44, 0.5), xycoords="axes fraction",
                        arrowprops=dict(arrowstyle="-|>", color="0.35", lw=1.0))
        axes.append(ax)
    if cbar and im is not None:
        cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.01)
        cb.ax.tick_params(labelsize=(label_fs or 7))
    return axes


if __name__ == "__main__":                       # 自检：四个图式各出一张，证明工具箱可用
    import os
    import numpy as np
    out = os.path.join(os.environ.get("TEMP", "."), "sci_figures_selftest")
    os.makedirs(out, exist_ok=True)
    use()
    rng = np.random.default_rng(0)

    fig, ax = plt.subplots(); ax.plot(range(10), np.cumsum(rng.normal(0, 1, 10)), color=PALETTE[0])
    nail(ax, 6, ax.get_lines()[0].get_ydata()[6], "钉：关键点")
    save(fig, os.path.join(out, "selftest_nail.pdf"))

    fig, ax = plt.subplots()
    staircase(ax, [0, 500, 1000, 2000, 5000], [10, 40, 70, 85, 92], events={1: "+SmoothL1", 3: "+课程"})
    ax.set_xlabel("轮次"); ax.set_ylabel("覆盖率 (%)")
    save(fig, os.path.join(out, "selftest_staircase.pdf"))

    fig = plt.figure()
    l, r = sliding_axis(fig)
    l.plot(range(50), rng.normal(0, 1, 50)); r.plot(range(4800, 5000), rng.normal(0, 1, 200))
    save(fig, os.path.join(out, "selftest_sliding.pdf"))

    fig = plt.figure(figsize=(7.0, 1.9))
    cube_skewer(fig, [rng.random((30, 30)) for _ in range(4)], titles=["0%", "50%", "80%", "92%"])
    save(fig, os.path.join(out, "selftest_skewer.pdf"))

    print("selftest OK ->", out)
