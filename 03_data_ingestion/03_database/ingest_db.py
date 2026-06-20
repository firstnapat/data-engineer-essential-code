"""
Ingest data from a database using SQLAlchemy.
Uses SQLite (built-in, no setup) for the demo.
Swap the connection string for PostgreSQL, MySQL, etc.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "/tmp/demo_sales.db"
DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def seed_database(db_path: str) -> None:
    """Create and populate a demo SQLite database from the CSV."""
    df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS regions (
                region_name TEXT PRIMARY KEY,
                country     TEXT DEFAULT 'Thailand'
            )
        """)
        for r in df["region"].unique():
            conn.execute("INSERT OR IGNORE INTO regions VALUES (?, ?)", (r, "Thailand"))
    print(f"[seed] Database ready at {db_path}")


def query_database(db_path: str, sql: str, params: tuple = ()) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(sql, conn, params=params)
    print(f"[query] {len(df)} rows returned")
    return df


if __name__ == "__main__":
    seed_database(DB_PATH)

    print("\n--- All sales (first 5) ---")
    df_all = query_database(DB_PATH, "SELECT * FROM sales LIMIT 5")
    print(df_all)

    print("\n--- Revenue by category (SQL aggregation) ---")
    df_cat = query_database(DB_PATH, """
        SELECT category,
               SUM(revenue)  AS total_revenue,
               COUNT(*)      AS transactions,
               AVG(revenue)  AS avg_revenue
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """)
    print(df_cat)

    print("\n--- Filtered query: Electronics in Bangkok ---")
    df_filtered = query_database(DB_PATH,
        "SELECT date, product, quantity, revenue FROM sales WHERE category=? AND region=?",
        ("Electronics", "Bangkok"),
    )
    print(df_filtered)

    # --- SQLAlchemy (PostgreSQL example, commented out) ---
    # from sqlalchemy import create_engine
    # import os
    # engine = create_engine(
    #     f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    #     f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    # )
    # df = pd.read_sql("SELECT * FROM sales LIMIT 100", engine)
