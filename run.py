#!/usr/bin/env python3
"""生成虚构人力场景的量化报告 → docs/index.html。"""

from pathlib import Path

from peoplestats import (
    build_scenarios,
    two_proportion_z,
    sample_size_two_prop,
    funnel_rates,
    kaplan_meier,
    median_survival,
    calibration_bins,
    brier_score,
)
from peoplestats.report import render

ROOT = Path(__file__).resolve().parent


def main() -> None:
    sc = build_scenarios(42)
    ab = two_proportion_z(sc["ab"]["success_a"], sc["ab"]["n_a"], sc["ab"]["success_b"], sc["ab"]["n_b"])
    ss = sample_size_two_prop(**sc["design"])
    funnel = funnel_rates(sc["funnel"])
    curve = kaplan_meier(sc["survival"]["times"], sc["survival"]["events"])
    med = median_survival(curve)
    cal = calibration_bins(sc["calibration"]["scores"], sc["calibration"]["outcomes"])
    brier = brier_score(sc["calibration"]["scores"], sc["calibration"]["outcomes"])

    html = render({
        "ab_test": ab,
        "ab_labels": {"a": sc["ab"]["label_a"], "b": sc["ab"]["label_b"]},
        "sample_size": ss,
        "funnel": funnel,
        "survival": {
            "curve": curve,
            "median": med,
            "n": len(sc["survival"]["times"]),
            "n_events": sum(sc["survival"]["events"]),
        },
        "calibration": cal,
        "brier": brier,
    })
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"AB p={ab['p_value']:.4f} lift={ab['lift']:.1%}  n_per_group={ss['n_per_group']}  median_days={med}")
    print(f"报告 → {out}")


if __name__ == "__main__":
    main()
