"""Create visuals describing the customer segments."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "customers_segmented.csv"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "charts"
FEATURES = [
    "Age", "Income", "Children_Total", "Recency", "Total_Spending",
    "Total_Purchases", "NumWebVisitsMonth", "NumDealsPurchases",
]


def run_visualizations(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if "Segment_ID" not in df.columns:
        raise ValueError("Segment_ID is missing. Run src/segment_customers.py first.")

    # Cluster sizes
    counts = df["Segment_ID"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts.index.astype(str), counts.values)
    ax.set(title="Customers per Segment", xlabel="Segment ID", ylabel="Customer Count")
    fig.tight_layout()
    fig.savefig(output_dir / "segment_sizes.png", dpi=160)
    plt.close(fig)

    # Segment average spending, with optional categories.
    spend_cols = [c for c in ["MntWines", "MntFruits", "MntMeatProducts",
                               "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
                  if c in df.columns]
    if spend_cols:
        spend = df.groupby("Segment_ID")[spend_cols].mean()
        fig, ax = plt.subplots(figsize=(11, 6))
        spend.plot(kind="bar", ax=ax)
        ax.set(title="Average Product Spending by Segment", xlabel="Segment ID",
               ylabel="Average spend (source units)")
        ax.tick_params(axis="x", labelrotation=0)
        fig.tight_layout()
        fig.savefig(output_dir / "spending_by_segment.png", dpi=160)
        plt.close(fig)

    # PCA provides a 2D view of multivariate clusters; axes are components, not original units.
    features = [c for c in FEATURES if c in df.columns]
    if len(features) >= 2 and len(df) >= 3:
        X = df[features].apply(pd.to_numeric, errors="coerce")
        X = X.replace([float("inf"), float("-inf")], float("nan"))
        X = X.fillna(X.median()).fillna(0)
        scaled = StandardScaler().fit_transform(X)
        points = PCA(n_components=2, random_state=42).fit_transform(scaled)
        plot_df = pd.DataFrame({
            "PC1": points[:, 0], "PC2": points[:, 1],
            "Segment_ID": df["Segment_ID"].astype(str).values,
        })
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(data=plot_df, x="PC1", y="PC2", hue="Segment_ID",
                        alpha=0.75, s=45, ax=ax)
        ax.set_title("Customer Segments (PCA Projection)")
        fig.tight_layout()
        fig.savefig(output_dir / "segments_pca.png", dpi=160)
        plt.close(fig)

    # Spending vs income, if available.
    if {"Income", "Total_Spending"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.scatterplot(data=df, x="Income", y="Total_Spending", hue="Segment_ID",
                        alpha=0.75, s=45, ax=ax)
        ax.set_title("Income and Total Spending by Segment")
        fig.tight_layout()
        fig.savefig(output_dir / "income_vs_spending.png", dpi=160)
        plt.close(fig)

    print(f"Charts saved to: {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Segmented dataset not found: {args.input}. Run segmentation first.")
    run_visualizations(pd.read_csv(args.input), args.output_dir)


if __name__ == "__main__":
    main()
