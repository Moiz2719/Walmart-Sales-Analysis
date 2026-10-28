# Walmart Sales Analysis

This project folder is part of a GitHub-ready starter package prepared from the supplied Walmart sales analytics notebook PDF. It includes cleaning, SQL analysis, visualisation scripts, documentation, and limitations.

> Note: The original Walmart CSV was not included with the notebook PDF. The scripts have not been validated against the original dataset yet. See `Docs/findings_and_limitations.md` before relying on the reported figures.

## Files
- `src/clean_data.py` — data-cleaning workflow
- `src/run_analysis.py` — SQL/Pandas business analysis
- `src/create_visualizations.py` — charts
- `sql/business_queries.sql` — SQL examples
- `Docs/` — overview, data dictionary, methodology, findings and limitations
- `data/README.md` — instructions for placing the dataset locally

## Setup
Install dependencies with `pip install -r requirements.txt`. Put the source CSV in the location described in `data/README.md`, then follow the run instructions in the project documentation.
