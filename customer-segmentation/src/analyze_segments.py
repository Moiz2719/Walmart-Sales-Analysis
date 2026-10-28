"""Summarise customer profiles by assigned segment."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "customers_segmented.csv"
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "tables"


def profile_segments(df: pd.DataFrame) -> pd.DataFrame:
    if "Segment_ID" not in df.columns:
        raise ValueError("Segment_ID is missing. Run src/segment_customers.py first.")

    profile = df.groupby("Segment_ID").size().rename("Customers").to_frame()
    profile["Customer_Share_Pct"] = (profile["Customers"] / len(df) * 100).round(2)

    metrics = [
        "Age", "Income", "Recency", "Total_Spending", "Total_Purchases",
        "NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases",
        "NumStorePurchases", "NumWebVisitsMonth", "Campaigns_Accepted", "Response",
        "Customer_Tenure_Days",
    ]
    for column in metrics:
        if column in df.columns:
            profile[f"Avg_{column}"] = df.groupby("Segment_ID")[column].mean().round(2)

    spend_columns = [
        c for c in ("MntWines", "MntFruits", "MntMeatProducts",
                    "MntFishProducts", "MntSweetProducts", "MntGoldProds")
        if c in df.columns
    ]
    for column in spend_columns:
        profile[f"Avg_{column}"] = df.groupby("Segment_ID")[column].mean().round(2)

    return profile.reset_index().sort_values("Segment_ID")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Segmented dataset not found: {args.input}. Run segmentation first.")

    df = pd.read_csv(args.input)
    profile = profile_segments(df)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    profile.to_csv(args.output_dir / "segment_profile.csv", index=False)

    if {"Segment_ID", "Response"}.issubset(df.columns):
        campaign = df.groupby("Segment_ID")["Response"].agg(
            customers="count", campaign_response_rate="mean"
        ).reset_index()
        campaign["campaign_response_rate_pct"] = (campaign["campaign_response_rate"] * 100).round(2)
        campaign.drop(columns=["campaign_response_rate"]).to_csv(
            args.output_dir / "campaign_response_by_segment.csv", index=False
        )

    print(profile.to_string(index=False))
    print(f"Saved segment profiles to: {args.output_dir}")


if __name__ == "__main__":
    main()
