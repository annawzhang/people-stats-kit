"""评分校准：把预测分（0–1）与真实转化对照。"""

from __future__ import annotations


def calibration_bins(
    scores: list[float],
    outcomes: list[int],
    edges: list[float] | None = None,
) -> list[dict]:
    """
    scores in [0,1]；outcomes 0/1。
    默认分箱：0–0.4 / 0.4–0.6 / 0.6–1.0（对齐初筛分档叙事）。
    """
    if len(scores) != len(outcomes):
        raise ValueError("scores 与 outcomes 长度须一致")
    edges = edges or [0.0, 0.4, 0.6, 1.0001]
    bins = []
    for lo, hi in zip(edges, edges[1:]):
        idx = [i for i, s in enumerate(scores) if lo <= s < hi]
        n = len(idx)
        if n == 0:
            bins.append({"label": f"{lo:.0%}-{hi:.0%}" if hi <= 1 else f"≥{lo:.0%}",
                         "n": 0, "mean_score": None, "rate": None})
            continue
        mean_s = sum(scores[i] for i in idx) / n
        rate = sum(outcomes[i] for i in idx) / n
        label = f"≥{lo:.0%}" if hi > 1 else f"{lo:.0%}-{min(hi,1):.0%}"
        # prettier labels for default edges
        if edges == [0.0, 0.4, 0.6, 1.0001]:
            label = {0.0: "0–39 分档", 0.4: "40–59 分档", 0.6: "≥60 分档"}[lo]
        bins.append({"label": label, "n": n, "mean_score": mean_s, "rate": rate,
                     "gap": rate - mean_s})
    return bins


def brier_score(scores: list[float], outcomes: list[int]) -> float:
    if not scores:
        return 0.0
    return sum((s - o) ** 2 for s, o in zip(scores, outcomes)) / len(scores)
