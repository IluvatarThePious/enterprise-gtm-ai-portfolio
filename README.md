# Enterprise GTM & AI Workflow Portfolio

**Peter Ryther · Enterprise sales, GTM strategy, and practical AI workflows**

This collection shows how I approach commercial problems: define the decision, make assumptions visible, build a useful workflow, and check what the evidence actually supports.

## Start here

| Project | Business question | What to inspect |
|---|---|---|
| [Customer Proof Sprint](customer-proof-sprint/README.md) | How can a seller turn pilot records into a persuasive, defensible customer story? | Fictional case study, source ledger, reusable prompt, claim checks, calculation script |
| [Pilot-to-Expansion Playbook](pilot-to-expansion/README.md) | What must be true before an enterprise automation pilot earns a larger rollout? | Qualification rubric, pilot charter, decision gates, manager review cadence |
| [Service Scenario Model](service-scenario-model/README.md) | How do sales volume, refunds, delivery capacity, and collection timing change a service offer's economics? | Runnable model, illustrative inputs, generated scenarios, edge-case tests |

**Five-minute tour:** read the customer story's claim boundaries, inspect the pilot decision memo, then run the scenario model and compare a completed project with a delayed payment.

## What these examples demonstrate

- Translating product capabilities into a measurable business question.
- Separating evidence, assumptions, calculations, and unverified claims.
- Defining how Sales, Operations, and Finance make a shared decision.
- Using AI to draft and structure work while retaining explicit review criteria.
- Making small analytical tools reproducible and understandable.

## Provenance and limits

These are AI-assisted portfolio work samples developed from my sales, GTM, and business-planning explorations. The customer story is a fictional example. The playbook is a generalized adaptation of interview-preparation work. The model is an illustrative planning tool. None is presented as a deployed production system, customer endorsement, measured commercial success, or proof of formal people-management experience.

AI assisted drafting, analysis, code generation, and this portfolio packaging. The artifacts make the assumptions and checks inspectable. Commercial outcomes should be judged from independently supported professional references and results, not inferred from these demonstrations.

No proprietary customer records, private interview transcripts, compensation plans, or third-party course materials are included.

## Run the checks

Python 3.10 or later; no third-party packages required.

```sh
python3 customer-proof-sprint/verify.py
python3 service-scenario-model/model.py
python3 -m unittest discover -s service-scenario-model/tests -v
```

The model writes its CSV and JSON results to `service-scenario-model/output/`.
