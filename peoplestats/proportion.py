"""双比例 z 检验与双样本样本量估算（触达文案 AB / 渠道转化）。"""

from __future__ import annotations

import math

from .mathutil import norm_ppf, norm_sf


def two_proportion_z(success_a: int, n_a: int, success_b: int, n_b: int) -> dict:
    """比较两组成功率（如回复率）。返回 rate、diff、z、双侧 p、相对提升。"""
    if n_a <= 0 or n_b <= 0:
        raise ValueError("样本量必须为正")
    p1, p2 = success_a / n_a, success_b / n_b
    pooled = (success_a + success_b) / (n_a + n_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    if se == 0:
        z = 0.0
        p = 1.0
    else:
        z = (p2 - p1) / se
        p = 2 * norm_sf(abs(z))
    lift = None if p1 == 0 else (p2 - p1) / p1
    return {
        "rate_a": p1,
        "rate_b": p2,
        "diff": p2 - p1,
        "lift": lift,
        "z": z,
        "p_value": p,
        "n_a": n_a,
        "n_b": n_b,
        "success_a": success_a,
        "success_b": success_b,
    }


def sample_size_two_prop(
    p1: float,
    p2: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> dict:
    """估算每组需要多少人，才能以给定功效检出 p1→p2 的差异（双侧）。"""
    if not (0 < p1 < 1 and 0 < p2 < 1):
        raise ValueError("p1、p2 须在 (0,1)")
    if p1 == p2:
        raise ValueError("效应量为 0，样本量无定义")
    z_a = norm_ppf(1 - alpha / 2)
    z_b = norm_ppf(power)
    pooled = (p1 + p2) / 2
    num = (z_a * math.sqrt(2 * pooled * (1 - pooled)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    n = math.ceil(num / (p2 - p1) ** 2)
    return {
        "n_per_group": n,
        "p1": p1,
        "p2": p2,
        "alpha": alpha,
        "power": power,
        "effect": p2 - p1,
    }
