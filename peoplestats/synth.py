"""虚构人力场景数据：触达 AB、招聘漏斗、Offer 时长、评分校准。"""

from __future__ import annotations

import random


def _rng(seed: int) -> random.Random:
    return random.Random(seed)


def build_scenarios(seed: int = 42) -> dict:
    r = _rng(seed)

    # 场景 A：人才触达文案 AB（对齐 explainable-talent-scoring 回复率叙事）
    # 对照组 ~44%，实验组 ~53%
    n_a = n_b = 800
    reply_a = 355
    reply_b = 423

    # 场景 B：招聘漏斗（对齐 hiring-copilot 阶段名）
    funnel = [
        {"name": "新简历", "n": 360},
        {"name": "初筛通过", "n": 170},
        {"name": "电话面", "n": 168},
        {"name": "现场面", "n": 145},
        {"name": "Offer", "n": 58},
        {"name": "已入职", "n": 24},
    ]

    # 场景 C：投递→入职时长（天）；部分删失（仍在 Offer / 放弃观测）
    times, events = [], []
    for _ in range(120):
        t = 12 + r.expovariate(1 / 22)
        # ~25% 删失
        e = 0 if r.random() < 0.25 else 1
        if e == 0:
            t = min(t, 10 + r.random() * 40)
        times.append(round(t, 1))
        events.append(e)

    # 场景 D：初筛分（0–100）→ 现场面是否通过（对齐 hiring 分档）
    scores, outcomes = [], []
    for _ in range(400):
        s = r.betavariate(2.2, 2.0)  # 偏中高
        # 真实通过概率随分数上升，并带噪声
        p = 0.15 + 0.7 * s
        y = 1 if r.random() < p else 0
        scores.append(s)
        outcomes.append(y)

    # 样本量估算：想把回复率从 44% 做到 52%
    design = {"p1": 0.44, "p2": 0.52, "alpha": 0.05, "power": 0.8}

    return {
        "ab": {"label_a": "对照组 · 标准跟进", "label_b": "实验组 · 分层跟进",
               "success_a": reply_a, "n_a": n_a, "success_b": reply_b, "n_b": n_b},
        "funnel": funnel,
        "survival": {"times": times, "events": events},
        "calibration": {"scores": scores, "outcomes": outcomes},
        "design": design,
        "seed": seed,
    }
