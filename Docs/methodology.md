# Methodology

## 1. Load and inspect

Read the CSV with pandas. Review row/column counts, sample records, data types, numerical summaries, duplicate rows, and missing values.

## 2. Clean

- Standardise column names to lowercase.
- Remove the `$` symbol from `unit_price` and convert it to numeric.
- Convert `quantity` to numeric.
- Parse `date` using the day/month/year format visible in the notebook.
- Standardise city text.
- Remove exact duplicate rows.
- Remove records missing required price, quantity, or date values.
- Derive weekday and year fields from the parsed date.

Invalid numeric/date values become missing during conversion and are removed from the required analysis fields. Check the console output to understand how many rows this affects.

## 3. Store data

Write the cleaned DataFrame to a SQLite table named `walmart`. The database is a generated local artifact and is excluded from Git by `.gitignore`.

## 4. Analyse with SQL

Use grouping, aggregate functions, common table expressions, and window functions to compare payment methods, branch/category ratings, weekday activity, estimated profit, time-of-day transaction counts, and annual revenue.

## 5. Visualise

Generate bar charts for payment-method volume, average ratings by category, the dataset-derived estimated-profit measure, and transaction volume by time of day.

## 6. Interpret carefully

Treat charts as descriptive, not causal. Validate the date range and `profit_margin` definition before making claims about year-over-year performance or actual accounting profit.
