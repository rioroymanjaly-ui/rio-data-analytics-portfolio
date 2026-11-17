# RUIYA Operations Intelligence — Supplier & Fulfilment Analytics

**Python • SQL • Excel • KPI design • operational root-cause analysis**

A business-analytics portfolio demonstration developed from practical sourcing and operations questions: how do we identify underperforming suppliers, delivery exceptions, quality problems and quoted-vs-actual cost variances?

**Data provenance:** 1,800 deterministic, fictional purchase-order scenarios. None are actual RUIYA commercial transactions or customers, and no realised business savings are claimed.

## Business question

Where should an operations team intervene to improve on-time delivery and reduce cost/quality exceptions?

## Analytical scope

- Generated synthetic fulfilment records from six fictional suppliers across four regions
- Validated record uniqueness, quantities, delivery timings and monetary values
- Aggregated delivery SLA, quality, lead time, quoted-vs-actual cost and supplier scorecards
- Used SQL to investigate supplier-level delays, period trends and cost exposure
- Produced an Excel stakeholder dashboard showing headline KPIs and supplier comparison
- Designed a follow-up measurement plan rather than inferring causal outcomes from simulation

## Synthetic results (1,800 scenarios)

| Metric | Result |
|---|---:|
| On-time shipments | 47.44% |
| Late shipments | 946 |
| Quality incident rate | 4.44% |
| Mean lead time | 17.8 days |
| Cost variance against quotation | +1.46% |

The fictional supplier **IN-BETA** has 45.0% on-time delivery and a 13.33% quality incident rate. Its 3.1% cost variance warrants investigation **within this simulation**. The dataset intentionally encodes supplier differences and relatively tight delivery promises, so these findings are not causal or predictive of real suppliers.

## Technical evidence

The companion downloadable source package contains the generator, input validation, Python metrics, four SQL investigations, 8 automated unit tests, Excel workbook and generated 1,800-row CSV. All 8 tests passed locally (17 November 2026).

**Reproduce locally:** `python src/analyze.py` and `python -m unittest discover -s tests -v`.

**Limits:** Synthetic fixed-seed fixtures, no live ERP/CRM integrations, no supplier APIs, no predictive claims, no deployed production system, and no proprietary code.

## Practical recommendations

1. Audit promised lead times before blaming supplier execution.
2. Prioritize follow-ups using order-at-risk exceptions and quality issues.
3. Segment comparisons by geography, product and shipping method.
4. In a real pilot, measure on-time delivery, rework, unit cost variance and analyst follow-up hours before/after workflow changes.

Author: Rio Roy | MSc Data Analytics | Berlin.
