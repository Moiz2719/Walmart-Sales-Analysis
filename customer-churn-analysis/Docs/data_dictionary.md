# Data dictionary

The notebook PDF shows three source tables. Confirm exact fields against the actual SQLite file before using the scripts in a production setting.

## Customer table: `db_customer`

| Field | Meaning in notebook | Cleaning action |
|---|---|---|
| `customerid` | Customer identifier used to join tables | Kept as text |
| `name` | Customer name | Renamed to `customer_name` |
| `country` | Customer country | Missing values may be filled from the state mapping |
| `state` | Customer state | Used for grouped churn summaries |
| `gender` | Gender label | `Men` / `Women` standardised to `Male` / `Female` |
| `dob` | Date of birth | Parsed as a datetime |
| `interests`, `pincode` | Additional customer attributes | Dropped in the notebook cleaning step |

## Subscription table: `db_subscription`

| Field | Meaning in notebook |
|---|---|
| `customerid` | Customer identifier |
| `subscription_start_date` | Subscription start date |
| `subscription_type` | Acquisition/source category (e.g. Paid, Referral, Organic) |
| `renewal_date` | Renewal date |
| `plan_type` | Basic, Standard, or Premium plan category |
| `contract_type` | Contract category |
| `cancellation_date` | Cancellation date; presence is used to flag churn |
| `cancellation_reason` | Recorded cancellation reason, where available |
| `monthly_charges` | Monthly recurring charges |
| `cltv` | Customer lifetime value field in source |
| `churn_score` | Source churn score used to define risk bands |

The notebook creates `churn_flag`: 1 when `cancellation_date` is present, otherwise 0. It then labels `churn_risk` as Low for scores below 50, Medium for 50–69, and High for 70 or above.

## Support table: `db_support`

| Field | Meaning in notebook |
|---|---|
| `customerid` | Customer identifier |
| `complaint_date` | Complaint date |
| `escalations` | Escalation flag, with `Y` indicating an escalation |
| `csat_score` | Customer satisfaction score |
| `comment` | Support comment, where available |
| `col_1` | Empty column removed by the notebook |

The notebook sorts support rows by complaint date and keeps the latest record for each customer before joining it to subscriptions.
