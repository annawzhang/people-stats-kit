"""人力量化统计工具箱：比例检验、样本量、漏斗置信区间、生存分析、评分校准。"""

from .proportion import two_proportion_z, sample_size_two_prop
from .funnel import funnel_rates, wilson_ci
from .survival import kaplan_meier, median_survival
from .calibration import calibration_bins, brier_score
from .synth import build_scenarios

__all__ = [
    "two_proportion_z",
    "sample_size_two_prop",
    "funnel_rates",
    "wilson_ci",
    "kaplan_meier",
    "median_survival",
    "calibration_bins",
    "brier_score",
    "build_scenarios",
]
