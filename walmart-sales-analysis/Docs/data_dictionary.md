# Data dictionary

The original PDF shows these columns. Confirm the exact schema against your local `Walmart.csv` before relying on this dictionary.

| Column | Expected meaning | Notes |
|---|---|---|
| `invoice_id` | Transaction/invoice identifier | Integer-like identifier in the PDF |
| `branch` | Branch identifier | Original source column is shown as `Branch` |
| `city` | City associated with a transaction | Standardised to lowercase by cleaning script |
| `category` | Product category | Text category |
| `unit_price` | Price per unit | Dollar sign removed and converted to numeric |
| `quantity` | Units in transaction | Converted to numeric |
| `date` | Transaction date | PDF examples use day/month/two-digit-year format |
| `time` | Transaction time | Used to group transactions into time periods |
| `payment_method` | Payment method used | E.g., cash, credit card, e-wallet in the PDF output |
| `rating` | Customer rating | PDF summary shows values from 3 to 10 |
| `profit_margin` | Margin value associated with the transaction | Validate whether this is a decimal ratio and how it was defined |

## Data quality reported in the PDF

- Initial shape: 10,051 rows × 11 columns.
- Exact duplicate rows reported: 51.
- Missing values: 31 in `unit_price` and 31 in `quantity`.
- After dropping duplicate rows and rows with missing values, the notebook reports 9,969 rows × 11 columns.

The CSV itself was not included with the PDF, so these counts have not been independently re-run here.
