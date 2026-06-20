"""
Store data in a relational database (SQLite demo, PostgreSQL in production).
Demonstrates: create tables, insert records, upsert pattern.
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "/tmp/warehouse.db"
DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL UNIQUE,
            category     TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_region (
            region_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS fact_sales (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date    TEXT NOT NULL,
            product_id   INTEGER REFERENCES dim_product(product_id),
            region_id    INTEGER REFERENCES dim_region(region_id),
            quantity     INTEGER NOT NULL,
            unit_price   REAL NOT NULL,
            revenue      REAL NOT NULL
        );
    """)
    print("[schema] Tables created")


def load_dimensions(conn: sqlite3.Connection, df: pd.DataFrame) -> tuple[dict, dict]:
    products = {name: None for name in df["product"].unique()}
    regions  = {name: None for name in df["region"].unique()}

    for name, category in df[["product", "category"]].drop_duplicates().values:
        conn.execute("INSERT OR IGNORE INTO dim_product (name, category) VALUES (?, ?)", (name, category))
    for (name,) in df[["region"]].drop_duplicates().values:
        conn.execute("INSERT OR IGNORE INTO dim_region (name) VALUES (?)", (name,))

    for row in conn.execute("SELECT product_id, name FROM dim_product"):
        products[row[1]] = row[0]
    for row in conn.execute("SELECT region_id, name FROM dim_region"):
        regions[row[1]] = row[0]

    print(f"[dim] {len(products)} products, {len(regions)} regions")
    return products, regions


def load_facts(conn: sqlite3.Connection, df: pd.DataFrame, products: dict, regions: dict) -> None:
    rows = [
        (str(r["date"]), products[r["product"]], regions[r["region"]],
         int(r["quantity"]), float(r["unit_price"]), float(r["revenue"]))
        for _, r in df.iterrows()
    ]
    conn.executemany(
        "INSERT INTO fact_sales (sale_date, product_id, region_id, quantity, unit_price, revenue) VALUES (?,?,?,?,?,?)",
        rows,
    )
    print(f"[facts] Inserted {len(rows)} rows")


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])

    with sqlite3.connect(DB_PATH) as conn:
        create_schema(conn)
        products, regions = load_dimensions(conn, df)
        load_facts(conn, df, products, regions)

        print("\n--- Verify: Revenue by Category ---")
        result = pd.read_sql_query("""
            SELECT p.category, SUM(f.revenue) AS total_revenue
            FROM fact_sales f
            JOIN dim_product p ON f.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_revenue DESC
        """, conn)
        print(result)
