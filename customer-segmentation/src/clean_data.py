"""Clean the marketing campaign dataset and engineer customer-level features."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "marketing_campaign.csv"
DEFAULT_OUTPUT = ROOT / "outputs" / "customers_cleaned.csv"

SPEND_COLUMNS = [
    "MntWines", "MntFruits", "MntMeatProducts",
    "MntFishProducts", "MntSweetProducts", "MntGoldProds",
]
PURCHASE_COLUMNS = [
    "NumDealsPurchases", "NumWebPurchases",
    "NumCatalogPurchases", "NumStorePurchases",
]


def read_source(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Follow the instructions in data/README.md."
        )
    # Kaggle's source file is often tab-delimited despite the .csv extension.
    df = pd.read_csv(path, sep=None, engine="python")
    df.columns = df.columns.astype(str).str.strip()
    return df


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    if "ID" in df.columns:
        df = df.drop_duplicates(subset=["ID"], keep="first")
    else:
        df = df.drop_duplicates()

    # Numeric conversion and missing-income handling.
    if "Income" in df.columns:
        df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
        df = df.dropna(subset=["Income"])

    numeric_columns = [
        c for c in (
            ["Year_Birth", "Income", "Kidhome", "Teenhome", "Recency",
             "NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases",
             "NumStorePurchases", "NumWebVisitsMonth", "Response", "Complain"]
            + SPEND_COLUMNS
            + [f"AcceptedCmp{i}" for i in range(1, 6)]
        ) if c in df.columns
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if "Dt_Customer" in df.columns:
        df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], errors="coerce", dayfirst=True)

    if "Year_Birth" in df.columns:
        # Dataset is from the mid-2010s; use a fixed reference year for reproducibility.
        df["Age"] = 2014 - df["Year_Birth"]

    if {"Kidhome", "Teenhome"}.issubset(df.columns):
        df["Children_Total"] = df["Kidhome"].fillna(0) + df["Teenhome"].fillna(0)
        df["Family_Size"] = df["Children_Total"] + 1

    if "Children_Total" in df.columns:
        df["Is_Parent"] = (df["Children_Total"] > 0).astype(int)

    if "Marital_Status" in df.columns:
        living_with_map = {
            "Married": "Partner", "Together": "Partner",
            "Single": "Alone", "Divorced": "Alone",
            "Widow": "Alone", "Alone": "Alone",
            "Absurd": "Other", "YOLO": "Other",
        }
        df["Living_With"] = df["Marital_Status"].map(living_with_map).fillna("Unknown")

    available_spend = [c for c in SPEND_COLUMNS if c in df.columns]
    if available_spend:
        df["Total_Spending"] = df[available_spend].fillna(0).sum(axis=1)

    available_purchases = [c for c in PURCHASE_COLUMNS if c in df.columns]
    if available_purchases:
        df["Total_Purchases"] = df[available_purchases].fillna(0).sum(axis=1)

    campaigns = [f"AcceptedCmp{i}" for i in range(1, 6) if f"AcceptedCmp{i}" in df.columns]
    if campaigns:
        df["Campaigns_Accepted"] = df[campaigns].fillna(0).sum(axis=1)

    if "Dt_Customer" in df.columns and df["Dt_Customer"].notna().any():
        reference_date = df["Dt_Customer"].max()
        df["Customer_Tenure_Days"] = (reference_date - df["Dt_Customer"]).dt.days

    # Remove impossible age values while preserving original birth year for traceability.
    if "Age" in df.columns:
        df.loc[(df["Age"] < 18) | (df["Age"] > 100), "Age"] = np.nan

    return df.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    raw = read_source(args.input)
    print(f"Input shape: {raw.shape}")
    print(f"Exact duplicate rows: {raw.duplicated().sum()}")
    print(f"Missing values before cleaning (top columns):")
    print(raw.isna().sum().sort_values(ascending=False).head(10))

    cleaned = clean_and_engineer(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(args.output, index=False)

    print(f"Cleaned shape: {cleaned.shape}")
    print(f"Saved cleaned data to: {args.output}")


if __name__ == "__main__":
    main()
