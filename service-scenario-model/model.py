"""Illustrative service cash and delivery scenarios. No third-party packages."""
import argparse
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def number(value):
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError("Numeric inputs must be finite and nonnegative")
    return result


def money(value):
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate(inputs, scenario):
    price, rate, flat, variable, startup, fixed, hourly = (
        number(inputs[k]) for k in (
            "price", "fee_rate", "fee_fixed", "delivery_cost_per_started_order",
            "startup_cost", "fixed_cost", "founder_hourly_value"
        )
    )
    if price <= 0 or rate > 1:
        raise ValueError("Price must be positive and fee rate at most 1")
    counts = [scenario[k] for k in ("booked", "started", "completed_retained", "settled", "refunded")]
    if any(type(v) is not int or v < 0 for v in counts):
        raise ValueError("Order counts must be nonnegative integers")
    booked, started, completed, settled, refunded = counts
    if not (completed <= started <= booked and refunded <= settled <= booked and completed + refunded <= booked):
        raise ValueError("Inconsistent order counts")
    hours = number(scenario["founder_hours"])
    fee = (price * rate + flat).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if fee > price:
        raise ValueError("Processing fee cannot exceed price in this model")
    delivery = started * variable
    costs = delivery + startup + fixed
    cash = settled * (price - fee) - refunded * price - costs
    accrual = completed * price - booked * fee - costs
    outstanding = booked - completed - refunded
    return {
        "scenario": scenario["name"],
        "booked_orders": booked,
        "completed_retained_orders": completed,
        "gross_settled_receipts": money(settled * price),
        "refunds_paid": money(refunded * price),
        "settled_processing_fees": money(settled * fee),
        "delivery_cash_cost": money(delivery),
        "startup_cost": money(startup),
        "fixed_cost": money(fixed),
        "scenario_net_cash": money(cash),
        "unsettled_net_payout": money((booked - settled) * (price - fee)),
        "unfinished_nonrefunded_orders": outstanding,
        "delivery_obligation_at_sales_value": money(outstanding * price),
        "accrual_contribution_estimate": money(accrual),
        "founder_hours": float(hours),
        "cash_per_founder_hour": money(cash / hours) if hours else None,
        "cash_less_imputed_founder_time": money(cash - hours * hourly),
    }


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=root / "inputs.json")
    parser.add_argument("--output", type=Path, default=root / "output")
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text())
    rows = [calculate(inputs, scenario) for scenario in inputs["scenarios"]]
    if not rows:
        raise ValueError("Supply at least one scenario")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "scenarios.json").write_text(json.dumps(rows, indent=2) + "\n")
    with (args.output / "scenarios.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"{row['scenario']}: cash {row['scenario_net_cash']:,.2f}; unfinished orders {row['unfinished_nonrefunded_orders']}")


if __name__ == "__main__":
    main()
