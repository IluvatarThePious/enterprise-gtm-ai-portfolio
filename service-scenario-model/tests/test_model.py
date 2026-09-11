import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("scenario_model", ROOT / "model.py")
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.inputs = json.loads((ROOT / "inputs.json").read_text())
        self.scenarios = {s["name"]: s for s in self.inputs["scenarios"]}

    def result(self, name):
        return MODEL.calculate(self.inputs, self.scenarios[name])

    def test_delay_affects_cash_not_completed_economics(self):
        base, delayed = self.result("base"), self.result("one-payout-delayed")
        self.assertEqual(base["scenario_net_cash"], 2071.8)
        self.assertEqual(delayed["scenario_net_cash"], 1198.2)
        self.assertAlmostEqual(base["scenario_net_cash"] - delayed["scenario_net_cash"], delayed["unsettled_net_payout"])
        self.assertEqual(base["accrual_contribution_estimate"], delayed["accrual_contribution_estimate"])

    def test_refund_retains_fee_and_delivery_cost(self):
        self.assertEqual(self.result("refund-after-work")["scenario_net_cash"], -509.4)

    def test_paid_unfinished_is_obligation_not_earned_work(self):
        row = self.result("paid-not-delivered")
        self.assertEqual(row["delivery_obligation_at_sales_value"], 2700)
        self.assertEqual(row["completed_retained_orders"], 0)
        self.assertLess(row["accrual_contribution_estimate"], 0)
        self.assertGreater(row["scenario_net_cash"], 0)

    def test_zero_sales_and_zero_hours(self):
        scenario = dict(self.scenarios["zero-sales"], founder_hours=0)
        row = MODEL.calculate(self.inputs, scenario)
        self.assertEqual(row["scenario_net_cash"], -450)
        self.assertIsNone(row["cash_per_founder_hour"])

    def test_impossible_counts_rejected(self):
        with self.assertRaises(ValueError):
            MODEL.calculate(self.inputs, dict(self.scenarios["base"], refunded=1))
        with self.assertRaises(ValueError):
            MODEL.calculate(self.inputs, dict(self.scenarios["base"], booked=3.5))

    def test_nonfinite_inputs_rejected(self):
        with self.assertRaises(ValueError):
            MODEL.calculate(dict(self.inputs, price="NaN"), self.scenarios["base"])


if __name__ == "__main__":
    unittest.main()
