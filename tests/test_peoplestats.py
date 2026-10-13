import math
import unittest

from peoplestats.proportion import two_proportion_z, sample_size_two_prop
from peoplestats.funnel import wilson_ci, funnel_rates
from peoplestats.survival import kaplan_meier, median_survival
from peoplestats.calibration import calibration_bins, brier_score
from peoplestats.synth import build_scenarios
from peoplestats.mathutil import norm_cdf, norm_ppf


class TestMath(unittest.TestCase):
    def test_norm_roundtrip(self):
        for p in (0.025, 0.5, 0.975):
            self.assertAlmostEqual(norm_cdf(norm_ppf(p)), p, places=4)


class TestProportion(unittest.TestCase):
    def test_known_direction(self):
        r = two_proportion_z(355, 800, 423, 800)
        self.assertGreater(r["rate_b"], r["rate_a"])
        self.assertLess(r["p_value"], 0.01)

    def test_equal_rates_high_p(self):
        r = two_proportion_z(50, 100, 50, 100)
        self.assertAlmostEqual(r["z"], 0.0)
        self.assertGreater(r["p_value"], 0.9)

    def test_sample_size_positive(self):
        n = sample_size_two_prop(0.44, 0.52)["n_per_group"]
        self.assertGreater(n, 100)
        self.assertLess(n, 2000)


class TestFunnel(unittest.TestCase):
    def test_wilson_contains_phat(self):
        lo, hi = wilson_ci(50, 100)
        self.assertLessEqual(lo, 0.5)
        self.assertGreaterEqual(hi, 0.5)

    def test_funnel_monotonic_n(self):
        rows = funnel_rates([
            {"name": "新简历", "n": 100},
            {"name": "初筛通过", "n": 40},
            {"name": "电话面", "n": 30},
        ])
        self.assertIsNone(rows[0]["rate"])
        self.assertAlmostEqual(rows[1]["rate"], 0.4)
        self.assertAlmostEqual(rows[2]["rate"], 0.75)


class TestSurvival(unittest.TestCase):
    def test_all_events_median(self):
        times = [10, 20, 30, 40]
        events = [1, 1, 1, 1]
        curve = kaplan_meier(times, events)
        self.assertAlmostEqual(curve[0]["survival"], 1.0)
        self.assertLessEqual(curve[-1]["survival"], 0.0 + 1e-9)
        med = median_survival(curve)
        self.assertIsNotNone(med)
        self.assertGreaterEqual(med, 10)


class TestCalibration(unittest.TestCase):
    def test_perfect_scores(self):
        scores = [0.1, 0.2, 0.8, 0.9]
        outcomes = [0, 0, 1, 1]
        bins = calibration_bins(scores, outcomes)
        self.assertEqual(sum(b["n"] for b in bins), 4)
        self.assertLess(brier_score(scores, outcomes), 0.05)


class TestSynth(unittest.TestCase):
    def test_scenarios_shape(self):
        sc = build_scenarios(42)
        self.assertEqual(len(sc["funnel"]), 6)
        self.assertEqual(sc["funnel"][0]["name"], "新简历")
        self.assertEqual(len(sc["survival"]["times"]), len(sc["survival"]["events"]))


if __name__ == "__main__":
    unittest.main()
