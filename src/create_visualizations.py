"""Generate charts from the cleaned Walmart SQLite database."""
import argparse
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_bar(data: pd.DataFrame, x: str, y: str, title: str,
             xlabel: str, ylabel: str, path: Path, rotate: int = 0) -> None:
    if data.empty:
        print(f"Skipping empty chart: {title}")
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data[x].astype(str), data[y])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("data/walmart.db"))
    parser.add_argument("--output", type=Path, default=Path("outputs/charts"))
    args = parser.parse_args()
    if not args.database.exists():
        raise FileNotFoundError(f"Database not found: {args.database}. Run src/clean_data.py first.")
    args.output.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(args.database) as conn:
        payment = pd.read_sql_query("""
            SELECT payment_method, COUNT(*) AS transactions
            FROM walmart GROUP BY payment_method ORDER BY transactions DESC
        """, conn)
        ratings = pd.read_sql_query("""
            SELECT category, AVG(rating) AS avg_rating
            FROM walmart GROUP BY category ORDER BY avg_rating DESC
        """, conn)
        profit = pd.read_sql_query("""
            SELECT category,
                   SUM(unit_price * quantity * profit_margin) AS estimated_profit
            FROM walmart GROUP BY category ORDER BY estimated_profit DESC
        """, conn)
        shifts = pd.read_sql_query("""
            SELECT CASE WHEN time < '12:00:00' THEN 'Morning'
                        WHEN time < '17:00:00' THEN 'Afternoon'
                        ELSE 'Evening' END AS shift,
                   COUNT(*) AS transactions
            FROM walmart GROUP BY shift ORDER BY transactions DESC
        """, conn)

    save_bar(payment, "payment_method", "transactions",
             "Transactions by Payment Method", "Payment method",
             "Transactions", args.output / "transactions_by_payment_method.png")
    save_bar(ratings, "category", "avg_rating",
             "Average Customer Rating by Category", "Product category",
             "Average rating", args.output / "average_rating_by_category.png", 35)
    save_bar(profit, "category", "estimated_profit",
             "Estimated Profit by Product Category", "Product category",
             "Estimated profit (dataset formula)", args.output / "estimated_profit_by_category.png", 35)
    save_bar(shifts, "shift", "transactions",
             "Transactions by Time of Day", "Time period",
             "Transactions", args.output / "transactions_by_shift.png")


if __name__ == "__main__":
    main()
