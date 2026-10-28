"""Run the documented SQL business questions against walmart.db."""
import argparse
import sqlite3
from pathlib import Path

import pandas as pd

QUERIES = {
    "payment_method_summary": """
        SELECT payment_method,
               COUNT(*) AS transactions,
               SUM(quantity) AS total_quantity
        FROM walmart
        GROUP BY payment_method
        ORDER BY transactions DESC
    """,
    "top_rated_category_by_branch": """
        WITH ratings AS (
            SELECT branch, category, AVG(rating) AS avg_rating,
                   RANK() OVER (
                       PARTITION BY branch ORDER BY AVG(rating) DESC
                   ) AS rating_rank
            FROM walmart
            GROUP BY branch, category
        )
        SELECT branch, category, ROUND(avg_rating, 2) AS avg_rating
        FROM ratings
        WHERE rating_rank = 1
        ORDER BY branch
    """,
    "busiest_weekday_by_branch": """
        WITH daily AS (
            SELECT branch, day, COUNT(*) AS transactions,
                   RANK() OVER (
                       PARTITION BY branch ORDER BY COUNT(*) DESC
                   ) AS day_rank
            FROM walmart
            GROUP BY branch, day
        )
        SELECT branch, day, transactions
        FROM daily
        WHERE day_rank = 1
        ORDER BY branch
    """,
    "ratings_by_city_and_category": """
        SELECT city, category,
               ROUND(AVG(rating), 2) AS avg_rating,
               MIN(rating) AS min_rating,
               MAX(rating) AS max_rating
        FROM walmart
        GROUP BY city, category
        ORDER BY city, category
    """,
    "estimated_profit_by_category": """
        SELECT category,
               ROUND(SUM(unit_price * quantity * profit_margin), 2)
                   AS estimated_profit
        FROM walmart
        GROUP BY category
        ORDER BY estimated_profit DESC
    """,
    "payment_method_by_branch": """
        WITH payments AS (
            SELECT branch, payment_method, COUNT(*) AS transactions,
                   RANK() OVER (
                       PARTITION BY branch ORDER BY COUNT(*) DESC
                   ) AS payment_rank
            FROM walmart
            GROUP BY branch, payment_method
        )
        SELECT branch, payment_method AS most_used_payment, transactions
        FROM payments
        WHERE payment_rank = 1
        ORDER BY branch
    """,
    "transactions_by_shift": """
        SELECT CASE
                   WHEN time < '12:00:00' THEN 'Morning'
                   WHEN time < '17:00:00' THEN 'Afternoon'
                   ELSE 'Evening'
               END AS shift,
               COUNT(*) AS number_of_transactions
        FROM walmart
        GROUP BY shift
        ORDER BY number_of_transactions DESC
    """,
    "annual_revenue_by_branch": """
        SELECT branch, CAST(strftime('%Y', date) AS INTEGER) AS year,
               ROUND(SUM(unit_price * quantity), 2) AS revenue
        FROM walmart
        GROUP BY branch, CAST(strftime('%Y', date) AS INTEGER)
        ORDER BY branch, year
    """,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("data/walmart.db"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()
    if not args.database.exists():
        raise FileNotFoundError(f"Database not found: {args.database}. Run src/clean_data.py first.")

    args.output.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.database) as conn:
        for name, query in QUERIES.items():
            result = pd.read_sql_query(query, conn)
            result.to_csv(args.output / f"{name}.csv", index=False)
            print(f"\n## {name.replace('_', ' ').title()} ({len(result)} rows)")
            print(result.head(10).to_string(index=False))
            print(f"Full result saved to {args.output / f'{name}.csvg}")


if __name__ == "__main__":
    main()
