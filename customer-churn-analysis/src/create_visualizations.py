"""Generate churn analysis charts from the cleaned customer dataset."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "outputs" / "customer_churn_cleaned.csv"
DEFAULT_OUTPUT = ROOT / "outputs" / "charts"


def run_visualizations(csv_path: Path = DEFAULT_CSV, output_dir: Path = DEFAULT_OUTPUT) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"Cleaned CSV not found: {csv_path}. Run the cleaning step first.")

    df = pd.read_csv(csv_path, parse_dates=[
        c for c in ["subscription_start_date", "cancellation_date", "dob", "complaint_date"]
        if c in pd.read_csv(csv_path, nrows=0).columns
    ])
    output_dir.mkdir(parents=True, exist_ok=True)
    if df.empty:
        raise ValueError("The cleaned dataset has no rows.")

    # Monthly churn trend, based on cancellation date.
    if {"cancellation_date", "churn_flag"}.issubset(df.columns):
        churned = df.loc[df["churn_flag"].eq(1)].copy()
        churned["cancellation_month"] = churned["cancellation_date"].dt.to_period("M")
        trend = churned.groupby("cancellation_month").size().sort_index()
        if not trend.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(trend.index.astype(str), trend.values, marker="o")
            ax.set(title="Monthly Churn Trend", xlabel="Cancellation Month",
                   ylabel="Number of Churned Customers")
            ax.tick_params(axis="x", labelrotation=45)
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            fig.savefig(output_dir / "monthly_churn_trend.png", dpi=160)
            plt.close(fig)

    # Churn rate by plan type and state.
    for column, filename, title, xlabel in [
        ("plan_type", "churn_rate_by_plan.png", "Churn Rate by Plan Type", "Plan Type"),
        ("state", "churn_rate_by_state.png", "Churn Rate by State", "State"),
    ]:
        if column in df.columns:
            rates = df.groupby(column, dropna=False)["churn_flag"].mean().mul(100).sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(rates.index.astype(str), rates.values)
            ax.set(title=title, xlabel=xlabel, ylabel="Churn Rate (%)")
            ax.tick_params(axis="x", labelrotation=40)
            fig.tight_layout()
            fig.savefig(output_dir / filename, dpi=160)
            plt.close(fig)

    # Correlation heatmap using the notebook's selected features.
    selected = [c for c in ["plan_type", "contract_type", "churn_score",
                            "churn_flag", "churn_risk", "escalations"] if c in df.columns]
    if len(selected) >= 2:
        heatmap_df = df[selected].copy()
        for column in ["plan_type", "contract_type", "churn_risk", "escalations"]:
            if column in heatmap_df.columns:
                heatmap_df[column] = LabelEncoder().fit_transform(heatmap_df[column].astype(str))
        for column in heatmap_df.columns:
            heatmap_df[column] = pd.to_numeric(heatmap_df[column], errors="coerce")
        corr = heatmap_df.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap")
        fig.tight_layout()
        fig.savefig(output_dir / "correlation_heatmap.png", dpi=160)
        plt.close(fig)

    # Pairplot for numeric variables used in the notebook.
    numeric = [c for c in ["churn_score", "churn_flag", "monthly_charges", "age", "tenure_days"]
               if c in df.columns]
    if len(numeric) >= 2:
        grid = sns.pairplot(df[numeric].apply(pd.to_numeric, errors="coerce").dropna(), diag_kind="hist")
        grid.fig.savefig(output_dir / "churn_numeric_pairplot.png", dpi=160, bbox_inches="tight")
        plt.close(grid.fig)

    print(f"Charts saved to: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    run_visualizations(args.csv, args.output_dir)


if __name__ == "__main__":
    main()
