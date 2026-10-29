# Findings

## Results transcribed from the supplied PDF

The following findings are transcribed from the notebook export.

### Data preparation
- Initial dataset: 10,051 rows and 11 columns.
- Duplicate rows detected: 51.
- Missing values: 31 in `unit_price` and 31 in `quantity`.
- Dataset after the notebook's duplicate and missing-row removal: 9,969 rows and 11 columns.

### Payment methods
The PDF shows the following transaction counts after cleaning:

| Payment method | Transactions | Quantity |
|---|---:|---:|
| Cash | 1,832 | 4,984 |
| Credit card | 4,256 | 9,567 |
| Ewallet | 3,881 | 8,932 |

Credit cards have the highest transaction count in the displayed result.

### Estimated profit by category
The PDF displays the following output for `SUM(unit_price * quantity * profit_margin)`:

| Category | Displayed value |
|---|---:|
| Fashion accessories | 192,314.8932 |
| Home and lifestyle | 192,213.6381 |
| Electronic accessories | 30,772.4895 |
| Food and beverages | 21,552.8622 |
| Sports and travel | 20,613.8082 |
| Health and beauty | 18,671.7345 |

