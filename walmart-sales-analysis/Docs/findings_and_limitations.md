# Findings and limitations

## Results transcribed from the supplied PDF

These are values shown in the notebook export; they have not been independently reproduced because the source CSV was not provided.

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

**Caution:** the source PDF also shows an apparently incomplete price-conversion line. These values should be treated as reported output from the PDF, not validated results. Re-run the analysis with the actual CSV before publishing them as final findings.

## Limitations and checks required

1. The CSV was not included with the PDF, so all results need to be reproduced.
2. Sample dates in the PDF appear to be from 2019, but a notebook query compares 2022 and 2023. Confirm the actual date range before reporting year-over-year changes.
3. The PDF's `unit_price` conversion line appears truncated/incomplete. The provided script performs explicit numeric conversion and reports invalid/missing rows.
4. The `profit_margin` field's definition and scale are not documented in the supplied PDF. The formula used is an estimated measure and may not equal accounting profit.
5. Branch and city labels, date parsing, and the source's duplicate definition should be checked against the raw file.
6. No causal conclusions can be drawn from these descriptive summaries alone.

## Next validation steps

- Run the pipeline against the original CSV.
- Compare resulting row counts with the PDF.
- Check minimum and maximum dates.
- Validate that price, quantity, rating, and margin values are plausible.
- Regenerate tables and charts, then update this document with verified outputs.
