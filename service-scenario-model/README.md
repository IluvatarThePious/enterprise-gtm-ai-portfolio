# Service Scenario Model

A small, reproducible model for testing a productized service offer before treating a sales target as cash available to spend.

Adapted from existing AI-assisted business-launch models. This edition narrows the scope to one fictional customer-proof service and adds explicit inputs, delivery obligations, and edge-case tests. All prices, fees, hours, and volumes are illustrative assumptions, not current market rates or forecasts.

## Run

```sh
python3 model.py
python3 model.py --inputs inputs.json --output output
python3 -m unittest discover -s tests -v
```

Python 3.10+; standard library only. Paths default to this project directory; explicit relative paths resolve from your current directory.

## What it measures

Cash balance from the scenario = settled charges − refunds − retained processing fees − delivery cash costs − startup costs − fixed costs.

Accrual contribution estimate = value of completed, nonrefunded orders − fees on all originally charged orders − delivery cash costs − startup costs − fixed costs.

The second measure is an illustrative comparison, not a full accounting profit calculation. Taxes, financing, depreciation, and other omitted business costs are excluded.

Outstanding delivery obligation value = unfinished nonrefunded orders × price. This indicates promised service at sales value, not estimated cost to fulfill.

The model also reports cash less a hypothetical value for founder time. That is an opportunity-cost comparison, not an expense actually paid.

## Assumptions worth challenging

- All booked orders are charged in full. Each charge eventually settles unless refunded.
- A refund is full-price, paid in the same period, and its original processing fee is retained.
- Unsettled payouts are shown net of processing fees; fees on those charges affect eventual economics but not current cash.
- Delivery cash costs are incurred only for orders on which work started.
- A refunded order can have consumed delivery resources; a refunded order no longer carries a delivery obligation.
- A paid unfinished order increases cash, but is not completed earned work.
- Fixed/startup spending is incurred even in the zero-sales scenario.

## Interpretation

Compare `base` with `one-payout-delayed`: completion is identical, but available cash differs. Compare both with `paid-not-delivered`: positive receipts do not demonstrate successful delivery or earned profit.

This tool does not predict demand. A useful next step is to replace assumed volumes, hours, and costs with observed paid-pilot records while retaining downside cases.
