#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🕒 v1 · 2026-10-08 20:40 · dsh-agent ｜ 变更：初稿：生成四个图式示例图（固定 seed，可复跑）

r"""
make_examples.py — 生成四个图式的示例图（仓库用截图 / README 展示）。

用途：本仓库的示例图必须**可复跑**，不能是手放的死图。
      运行后在 examples/ 下产出 4 张 PNG（200 dpi，控制体积）。

    python examples/make_examples.py

设计：用固定 seed 的合成数据，图里带中文标签 —— 顺便演示 CJK 字体链是否生效。
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mpl_style import PALETTE, cube_skewer, nail, save_pgf, sliding_axis, staircase, use  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(0)


def out(name: str) -> str:
    return os.path.join(OUT, name)


def example_nail() -> None:
    """图式 1：钉子 —— 趋势曲线上钉出关键点。"""
    fig, ax = plt.subplots()
    steps = np.arange(0, 1200, 10)
    curve = 95 - 60 * np.exp(-steps / 350) + RNG.normal(0, 0.8, steps.size)
    ax.plot(steps, curve, color=PALETTE[0], label="本文")
    ax.set_xlabel("训练步数")
    ax.set_ylabel("成功率 (%)")
    ax.set_ylim(30, 100)
    nail(ax, 400, curve[40], "达标 92.1%\n400 步 · 20 runs")
    ax.legend(loc="lower right")
    fig.savefig(out("fig1_nail.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def example_staircase() -> None:
    """图式 2：阶梯 —— 分阶段抬升，竖直段标注触发事件。"""
    fig, ax = plt.subplots()
    staircase(
        ax,
        xs=[0, 300, 700, 1200, 2000, 3500],
        ys=[8, 22, 38, 55, 74, 91],
        events={1: "+ SmoothL1", 3: "+ 课程学习", 4: "+ 认知奖励"},
        label="本文",
        color=PALETTE[0],
    )
    staircase(
        ax,
        xs=[0, 300, 700, 1200, 2000, 3500],
        ys=[6, 15, 26, 38, 52, 68],
        label="基线",
        color=PALETTE[2],
        marker="s",
        annotate_events=False,
    )
    ax.set_xlabel("训练轮次")
    ax.set_ylabel("覆盖率 (%)")
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right")
    fig.savefig(out("fig2_staircase.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def example_sliding() -> None:
    """图式 3：滑轴 —— 断轴看全貌 + 尾部细节。"""
    fig = plt.figure()
    ax_l, ax_r = sliding_axis(fig)
    tail = 80 + 15 * (1 - np.exp(-np.arange(200) / 60)) + RNG.normal(0, 1.2, 200)
    ax_l.plot(np.arange(200), tail, color=PALETTE[0])
    ax_l.set_ylabel("指标值")
    ax_r.plot(np.arange(4800, 5000), tail + RNG.normal(0, 0.6, 200), color=PALETTE[0])
    ax_l.set_xlim(0, 200)
    ax_r.set_xlim(4800, 5000)
    fig.text(0.5, 0.04, "训练步数（左：前期 0–200 ｜ 右：后期 4800–5000）",
             ha="center", fontsize=7)
    fig.savefig(out("fig3_sliding.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def example_skewer() -> None:
    """图式 4：魔方串烧 —— 多快照演化，共享 vmin/vmax。"""
    fig = plt.figure(figsize=(7.0, 1.9))
    grids = []
    for k in range(4):
        g = RNG.random((30, 30))
        cover = np.zeros_like(g)
        cover[: 8 + 5 * k, : 8 + 5 * k] = g[: 8 + 5 * k, : 8 + 5 * k]
        grids.append(cover)
    cube_skewer(fig, grids, titles=["0%", "50%", "80%", "92%"],
                cmap="viridis", vmin=0, vmax=1)
    fig.savefig(out("fig4_cube_skewer.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    applied = use()
    print("style applied:", applied)
    example_nail()
    example_staircase()
    example_sliding()
    example_skewer()
    # 顺带验证 pgf 后端可用（失败不影响 PNG 示例）
    try:
        fig, ax = plt.subplots()
        ax.plot([0, 1, 2], [0, 1, 4], color=PALETTE[0])
        save_pgf(fig, out("fig5_pgf_demo.pgf"))
        plt.close(fig)
        print("pgf backend: OK")
    except Exception as exc:  # pragma: no cover
        print("pgf backend: skipped ->", exc)
    print("examples ->", OUT)


if __name__ == "__main__":
    main()
