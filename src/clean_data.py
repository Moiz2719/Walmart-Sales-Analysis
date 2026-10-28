"""Clean Walmart transaction data and save it to a SQLite database."""
import argparse
import sqlite3
from pathlib import Path

import pandas as pd


def clean_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, encoding_errors="ignore")
    print(f"Initial shape: {df.shape}")
    print("\nMissing values before cleaning:\n", df.isna().sum())
    print(f"\nDuplicate rows before cleaning: {df.duplicated().sum()}")

    # Standardise column names first, so later steps are consistent.
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"branch": "branch"})

    if "unit_price" in df.columns:
        price = df["unit_price"].astype("string").str.replace("$", "", regex=False).str.strip()
        df["unit_price"] = pd.to_numeric(price, errors="coerce")

    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # The PDF shows dates such as 05/01/19 and uses day/month/year.
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%y", errors="coerce")

    if "city" in df.columns:
        df["city"] = df["city"].astype("string").str.strip().str.lower()

    # Remove exact duplicate rows, then rows missing values required for analysis.
    before_duplicates = len(df)
    df = df.drop_duplicates()
    print(f"\nDuplicate rows removed: {before_duplicates - len(df)}")

    required = [c for c in ["unit_price", "quantity", "date"] if c in df.columns]
    before_missing = len(df)
    df = df.dropna(subset=required)
    print(f"Rows removed for missing/invalid required fields: {before_missing - len(df)}")

    if "date" in df.columns:
        df["day"] = df["date"].dt.day_name()
        df["year"] = df["date"].dt.year

    print(f"\nFinal shape: {df.shape}")
    print("\nMissing values after cleaning:\n", df.isna().sum())
    if "date" in df.columns and not df.empty:
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/Walmart.csv"))
    parser.add_argument("--database", type=Path, default=Path("data/walmart.db"))
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(
            f"Dataset not found: {args.input}. Add your authorised Walmart.csv file first."
        )

    df = clean_data(args.input)
    args.database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.database) as conn:
        df.to_sql("walmart", conn, if_exists="replace", index=False)
        total = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM walmart", conn)
    print(f"\nSaved {int(total.loc[0, 'total_rows']):,} rows to {args.database}")


if __name__ == "__main__":
    main()
