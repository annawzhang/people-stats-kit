"""招聘周期 / Offer 接受时长：Kaplan–Meier 与中位生存时间。"""

from __future__ import annotations


def kaplan_meier(times: list[float], events: list[int]) -> list[dict]:
    """
    times: 观察时长（天）；events: 1=已发生终点（入职/接受），0=删失（仍在流程/放弃未观测完）。
    返回按时间排序的生存曲线点 {t, at_risk, events, survival}。
    """
    if len(times) != len(events) or not times:
        raise ValueError("times 与 events 长度须一致且非空")
    pairs = sorted(zip(times, events), key=lambda x: x[0])
    n = len(pairs)
    surv = 1.0
    curve = [{"t": 0.0, "at_risk": n, "events": 0, "survival": 1.0}]
    i = 0
    while i < n:
        t = pairs[i][0]
        d = 0
        while i < n and pairs[i][0] == t:
            d += pairs[i][1]
            i += 1
        # at risk: 尚未在此前离开观察的人数 = n - 已处理条数 + 本时刻条数
        # 更标准：处理完时刻 t 之前的所有人后，时刻 t 开始时仍在风险集
        at_risk = n - (i - d)  # 进入时刻 t 时尚在场 = 总数 - 已严格早于 t 离开的
        # recount properly
        at_risk = sum(1 for tt, _ in pairs if tt >= t)
        if at_risk > 0 and d > 0:
            surv *= 1 - d / at_risk
        curve.append({"t": float(t), "at_risk": at_risk, "events": d, "survival": surv})
    return curve


def median_survival(curve: list[dict]) -> float | None:
    """生存函数首次 ≤ 0.5 的时间；若始终 >0.5 则返回 None。"""
    for pt in curve:
        if pt["survival"] <= 0.5:
            return pt["t"]
    return None
