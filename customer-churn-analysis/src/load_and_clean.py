"""Load, clean, feature-engineer, and join the three churn source tables."""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "customer_churn.db"
DEFAULT_OUTPUT_DIR = ROOT / "outputs"


def load_source_tables(database_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not database_path.exists():
        raise FileNotFoundError(
            f"Source database not found: {database_path}. "
            "See data/README.md for the expected file and tables."
        )

    with sqlite3.connect(database_path) as connection:
        table_names = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        required = {"db_customer", "db_subscription", "db_support"}
        missing = required - table_names
        if missing:
            raise ValueError(f"Source database is missing required tables: {sorted(missing)}")

        customer = pd.read_sql_query("SELECT * FROM db_customer", connection)
        subscription = pd.read_sql_query("SELECT * FROM db_subscription", connection)
        support = pd.read_sql_query("SELECT * FROM db_support", connection)

    return customer, subscription, support


def clean_and_merge(
    customer: pd.DataFrame,
    subscription: pd.DataFrame,
    support: pd.DataFrame,
    as_of: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Apply the cleaning and feature engineering shown in the Colab notebook."""
    customer = customer.copy()
    subscription = subscription.copy()
    support = support.copy()

    # Customer table
    customer = customer.rename(columns={"name": "customer_name"})
    customer.drop(columns=["interests", "pincode"], errors="ignore", inplace=True)

    if "dob" in customer.columns:
        customer["dob"] = pd.to_datetime(customer["dob"], errors="coerce")

    if "gender" in customer.columns:
        customer["gender"] = customer["gender"].replace({
            "Men": "Male",
            "Women": "Female",
        })

    if {"state", "country"}.issubset(customer.columns):
        state_country_mapping = (
            customer.dropna(subset=["country"])
            .drop_duplicates(subset=["state"])
            .set_index("state")["country"]
            .to_dict()
        )
        customer["country"] = customer["country"].fillna(
            customer["state"].map(state_country_mapping)
        )

    # Subscription table
    for column in ["subscription_start_date", "renewal_date", "cancellation_date"]:
        if column in subscription.columns:
            subscription[column] = pd.to_datetime(subscription[column], errors="coerce")

    subscription["churn_flag"] = subscription["cancellation_date"].notna().astype(int)

    # Support table: drop the empty column and retain the latest complaint per customer.
    support.drop(columns=["col_1"], errors="ignore", inplace=True)
    if "complaint_date" in support.columns:
        support["complaint_date"] = pd.to_datetime(support["complaint_date"], errors="coerce")
    if not support.empty and {"complaint_date", "customerid"}.issubset(support.columns):
        support = (
            support.sort_values("complaint_date")
            .drop_duplicates("customerid", keep="last")
        )

    # Start from subscriptions so every subscription stays in the analysis.
    df = subscription.merge(customer, on="customerid", how="left")
    df = df.merge(support, on="customerid", how="left")

    as_of = pd.Timestamp.today().normalize() if as_of is None else pd.Timestamp(as_of).normalize()

    if "dob" in df.columns:
        df["age"] = ((as_of - df["dob"]).dt.days / 365.25).astype("Int64")

    if {"cancellation_date", "subscription_start_date"}.issubset(df.columns):
        end_date = df["cancellation_date"].fillna(as_of)
        df["tenure_days"] = (end_date - df["subscription_start_date"]).dt.days

    if "churn_score" in df.columns:
        conditions = [
            df["churn_score"] < 50,
            (df["churn_score"] >= 50) & (df["churn_score"] < 70),
            df["churn_score"] >= 70,
        ]
        df["churn_risk"] = np.select(
            conditions, ["Low", "Medium", "High"], default="Unknown"
        )

    return df


def run_cleaning(
    database_path: Path = DEFAULT_SOURCE,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> tuple[Path, Path]:
    customer, subscription, support = load_source_tables(database_path)
    df = clean_and_merge(customer, subscription, support)

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "customer_churn_cleaned.csv"
    analysis_db_path = output_dir / "customer_churn_analysis.db"

    df.to_csv(csv_path, index=False)
    with sqlite3.connect(analysis_db_path) as connection:
        df.to_sql("churn_data", connection, if_exists="replace", index=False)

    print(f"Customer rows: {len(customer):,}")
    print(f"Subscription rows: {len(subscription):,}")
    print(f"Support rows: {len(support):,}")
    print(f"Joined dataset shape: {df.shape}")
    print(f"Cleaned CSV: {csv_path}")
    print(f"Analysis database: {analysis_db_path}")
    return csv_path, analysis_db_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    run_cleaning(args.database, args.output_dir)


if __name__ == "__main__":
    main()
