# Findings from the notebook export

The following figures are copied from the supplied PDF. They have not been independently rerun here because the SQLite source database was not included.

## Overall customer outcomes

| Metric | Notebook output |
|---|---:|
| Joined dataset shape | 21 rows × 21 columns |
| Churn rate | 28.57% |
| Retention rate | 71.43% |
| Average monthly charges per customer (labelled ARPU) | 18.85 |
| Average customer tenure | 1,549 days |
| Monthly charges associated with churned customers | 73.94 |
| Escalation rate in joined dataset | 19.05% |
| Average complaints per customer | 0.43 |
| Correlation between escalation and churn | 0.77 |

## Churn by plan

| Plan | Churn rate |
|---|---:|
| Basic | 60.00% |
| Standard | 22.22% |
| Premium | 14.29% |

## Churned customers by state

The notebook reports the following states among churned customers:

| State | Monthly charges | Churned users |
|---|---:|---:|
| Delhi | 13.99 | 1 |
| Karnataka | 20.98 | 2 |
| Meghalaya | 21.98 | 2 |
| Telangana | 16.99 | 1 |

## Churned customers by subscription source

| Subscription source | Monthly charges | Churned users |
|---|---:|---:|
| Paid | 12.99 | 1 |
| Referral (spelled `Refferal` in the source data) | 60.95 | 5 |

## Interpretation

- The notebook's Basic-plan group has the highest displayed churn rate among the three plan types.
- Most of the displayed churned customers were categorised under Referral acquisition/source.
- The reported escalation–churn correlation is positive in this small dataset, but it should not be interpreted as evidence of causation.
- With only 21 subscription records, segment percentages can change substantially with a small change in customer count.

These are source-reported values, not verified results. Rerun the scripts with the original database before relying on these figures for decisions or interview claims.
