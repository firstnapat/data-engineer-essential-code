"""
Work with a relational database as a data source.   seed -> read (SQL) -> inspect

Uses SQLite (built-in, no setup). Swap the connection string for PostgreSQL/MySQL.
"""
import os
import sqlite3
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
DB_PATH = "/tmp/source_sales.db"


def seed(db_path: str) -> None:
    """Create a demo DB from the CSV so we have something to query."""
    df = pd.read_csv(os.path.join(DATASETS, "sales.csv"))
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
    print(f"[seed] DB ready at {db_path}")


def read(db_path: str, sql: str, params: tuple = ()) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn, params=params)


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] {len(df)} rows")
    print(df)


if __name__ == "__main__":
    seed(DB_PATH)

    print("\n--- all sales (first 5) ---")
    inspect(read(DB_PATH, "SELECT * FROM sales LIMIT 5"))

    print("\n--- revenue by category (SQL aggregation) ---")
    inspect(read(DB_PATH, """
        SELECT category, SUM(revenue) AS total_revenue, COUNT(*) AS txns
        FROM sales GROUP BY category ORDER BY total_revenue DESC
    """))

    print("\n--- filtered query (parameterized) ---")
    inspect(read(DB_PATH,
                 "SELECT date, product, revenue FROM sales WHERE category=? AND region=? LIMIT 5",
                 ("Electronics", "Bangkok")))
