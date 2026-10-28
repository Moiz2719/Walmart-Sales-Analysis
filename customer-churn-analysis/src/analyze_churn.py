"""Create churn KPI tables and a concise metrics report from cleaned data."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "outputs" / "customer_churn_cleaned.csv"
DEFAULT_SOURCE_DB = ROOT / "data" / "customer_churn.db"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "tables"


def _group_churn(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "customers", "churn_rate_pct"])
    return (
        df.groupby(column, dropna=False)
        .agg(customers=("customerid", "nunique"), churn_rate_pct=("churn_flag", "mean"))
        .assign(churn_rate_pct=lambda x: (x["churn_rate_pct"] * 100).round(2))
        .reset_index()
        .sort_values("churn_rate_pct", ascending=False)
    )


def run_analysis(
    csv_path: Path = DEFAULT_CSV,
    source_db_path: Path = DEFAULT_SOURCE_DB,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict:
    if not csv_path.exists():
        raise FileNotFoundError(f"Cleaned CSV not found: {csv_path}. Run src/load_and_clean.py first.")

    df = pd.read_csv(csv_path, parse_dates=[
        c for c in ["subscription_start_date", "renewal_date", "cancellation_date",
                    "complaint_date", "dob"] if c in pd.read_csv(csv_path, nrows=0).columns
    ])
    if df.empty:
        raise ValueError("The cleaned dataset has no rows.")
    if not {"customerid", "churn_flag"}.issubset(df.columns):
        raise ValueError("Cleaned dataset must include customerid and churn_flag.")

    output_dir.mkdir(parents=True, exist_ok=True)
    churn_rate = float(df["churn_flag"].mean() * 100)
    metrics = {
        "customers": int(df["customerid"].nunique()),
        "churned_customers": int(df.loc[df["churn_flag"] == 1, "customerid"].nunique()),
        "churn_rate_pct": round(churn_rate, 2),
        "retention_rate_pct": round(100 - churn_rate, 2),
    }

    if "plan_type" in df.columns:
        _group_churn(df, "plan_type").to_csv(output_dir / "churn_by_plan.csv", index=False)
    if "state" in df.columns:
        _group_churn(df, "state").to_csv(output_dir / "churn_by_state.csv", index=False)
    if "subscription_type" in df.columns:
        _group_churn(df, "subscription_type").to_csv(
            output_dir / "churn_by_subscription_type.csv", index=False
        )
    if "churn_risk" in df.columns:
        df.groupby("churn_risk", dropna=False).agg(
            customers=("customerid", "nunique"),
            churn_rate_pct=("churn_flag", lambda x: round(float(x.mean() * 100), 2)),
        ).reset_index().to_csv(output_dir / "customers_by_churn_risk.csv", index=False)

    if "monthly_charges" in df.columns:
        charges = pd.to_numeric(df["monthly_charges"], errors="coerce")
        metrics["arpu_monthly_charges"] = round(float(charges.sum() / df["customerid"].nunique()), 2)
        metrics["monthly_charges_at_risk"] = round(float(charges[df["churn_flag"].eq(1)].sum()), 2)

    if "tenure_days" in df.columns:
        metrics["average_tenure_days"] = round(float(pd.to_numeric(df["tenure_days"], errors="coerce").mean()), 2)

    if "escalations" in df.columns:
        escalation_yes = df["escalations"].eq("Y")
        metrics["escalation_rate_pct_over_joined_customers"] = round(float(escalation_yes.mean() * 100), 2)
        metrics["escalation_churn_correlation"] = (
            round(float(escalation_yes.astype(int).corr(df["churn_flag"])), 2)
            if escalation_yes.nunique() > 1 and df["churn_flag"].nunique() > 1 else None
        )

    if source_db_path.exists():
        with sqlite3.connect(source_db_path) as connection:
            tables = {row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()}
            if "db_support" in tables:
                support = pd.read_sql_query("SELECT * FROM db_support", connection)
                metrics["average_complaints_per_customer"] = round(
                    float(len(support) / df["customerid"].nunique()), 2
                )

    metrics_path = output_dir / "kpi_summary.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"Analysis outputs: {output_dir}")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--source-db", type=Path, default=DEFAULT_SOURCE_DB)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    run_analysis(args.csv, args.source_db, args.output_dir)


if __name__ == "__main__":
    main()
