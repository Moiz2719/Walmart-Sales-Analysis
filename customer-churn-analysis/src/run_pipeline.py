"""Run the churn analysis workflow from the repository root."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow modules in this folder to be imported when this script is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from load_and_clean import run_cleaning
from analyze_churn import run_analysis
from create_visualizations import run_visualizations

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DB = ROOT / "data" / "customer_churn.db"
OUTPUT_DIR = ROOT / "outputs"


def main() -> None:
    cleaned_csv, _ = run_cleaning(SOURCE_DB, OUTPUT_DIR)
    run_analysis(cleaned_csv, SOURCE_DB, OUTPUT_DIR / "tables")
    run_visualizations(cleaned_csv, OUTPUT_DIR / "charts")
    print("\nPipeline complete. Review the generated tables and charts under outputs/.")


if __name__ == "__main__":
    main()
