# Methodology

## 1. Load the data

Connect to the SQLite database and load `db_customer`, `db_subscription`, and `db_support` into Pandas DataFrames.

## 2. Clean and standardise

- Rename customer `name` to `customer_name`.
- Drop `interests`, `pincode`, and the empty `col_1` field where present.
- Parse date fields into Pandas datetimes.
- Standardise gender labels.
- Fill missing country values from the state-to-country mapping built from observed records.

## 3. Prepare churn and support data

- Set `churn_flag = 1` when `cancellation_date` is present, otherwise 0.
- Sort support records by `complaint_date` and keep the latest complaint per customer.
- Use churn-score thresholds below 50, from 50 to under 70, and 70 or above for Low, Medium, and High risk bands.

## 4. Join tables

Start with subscription records, left join customer data on `customerid`, then left join each customer's latest support record. This preserves the subscription cohort when customer or support details are missing.

## 5. Analyse

Calculate overall churn and retention; churn by plan, state, and subscription type; average monthly charges per customer; average tenure; monthly charges associated with churned customers; escalation rate; and the notebook's escalation/churn correlation.

## 6. Visualise and interpret

Create a monthly churn trend, churn by plan, churn by state, a correlation heatmap, and a numeric pairplot. Segment rates from very small groups should be described cautiously. Correlation is an association measure and does not establish that support escalations cause churn.

## Reproducibility note

Age and active-customer tenure depend on the date the script is run. Use a fixed analysis date when comparing results across reporting periods.
