"""招聘 / 转化漏斗：各步转化率 + Wilson 置信区间。"""

from __future__ import annotations

import math

from .mathutil import norm_ppf


def wilson_ci(successes: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n <= 0:
        return (0.0, 0.0)
    z = norm_ppf(1 - alpha / 2)
    phat = successes / n
    denom = 1 + z * z / n
    centre = phat + z * z / (2 * n)
    margin = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))
    lo = max(0.0, (centre - margin) / denom)
    hi = min(1.0, (centre + margin) / denom)
    return (lo, hi)


def funnel_rates(counts: list[dict], alpha: float = 0.05) -> list[dict]:
    """
    counts: [{name, n}, ...] 漏斗自上而下人数。
    返回每步相对上一步的转化率与 Wilson CI；第一步无转化率。
    """
    out = []
    for i, step in enumerate(counts):
        name, n = step["name"], int(step["n"])
        row = {"name": name, "n": n, "rate": None, "ci": None, "from": None}
        if i > 0:
            prev = int(counts[i - 1]["n"])
            rate = n / prev if prev else 0.0
            lo, hi = wilson_ci(n, prev, alpha)
            row.update({"rate": rate, "ci": (lo, hi), "from": counts[i - 1]["name"]})
        out.append(row)
    return out
