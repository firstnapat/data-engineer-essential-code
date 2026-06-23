"""
Ingestion pipeline: a CSV data source -> relational database (schema-on-write).

Flow:  extract -> validate against the schema -> create schema -> load.

The destination star schema is designed in 04_data_storage/01_database. A
warehouse/database is **schema-on-write**: the tables must exist and the data
must conform BEFORE we load. SQLite is built in, so no setup is needed.
"""
import os
import sqlite3
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
DB_PATH = "/tmp/ingestion_warehouse.db"

# the contract the source must satisfy before it can enter the warehouse
REQUIRED_COLUMNS = {"date", "product", "category", "quantity", "unit_price", "revenue", "region"}


def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, parse_dates=["date"])
    print(f"[extract] {len(df)} rows from {os.path.basename(source)}")
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"source is missing required columns: {missing}")
    if df[["quantity", "unit_price", "revenue"]].isnull().any().any():
        raise ValueError("numeric fields contain nulls")
    print("[validate] source conforms to the schema")
    return df


def create_schema(conn: sqlite3.Connection) -> None:
    # schema FIRST — the destination must exist before any load
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL UNIQUE,
            category   TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dim_region (
            region_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS fact_sales (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date  TEXT NOT NULL,
            product_id INTEGER REFERENCES dim_product(product_id),
            region_id  INTEGER REFERENCES dim_region(region_id),
            quantity   INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            revenue    REAL NOT NULL
        );
    """)
    print("[schema] destination tables ready")


def load(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    for name, category in df[["product", "category"]].drop_duplicates().values:
        conn.execute("INSERT OR IGNORE INTO dim_product (name, category) VALUES (?, ?)", (name, category))
    for (name,) in df[["region"]].drop_duplicates().values:
        conn.execute("INSERT OR IGNORE INTO dim_region (name) VALUES (?)", (name,))

    products = {name: pid for pid, name in conn.execute("SELECT product_id, name FROM dim_product")}
    regions = {name: rid for rid, name in conn.execute("SELECT region_id, name FROM dim_region")}

    rows = [
        (str(r["date"]), products[r["product"]], regions[r["region"]],
         int(r["quantity"]), float(r["unit_price"]), float(r["revenue"]))
        for _, r in df.iterrows()
    ]
    conn.executemany(
        "INSERT INTO fact_sales (sale_date, product_id, region_id, quantity, unit_price, revenue) "
        "VALUES (?,?,?,?,?,?)",
        rows,
    )
    print(f"[load] {len(rows)} fact rows -> {DB_PATH}")


if __name__ == "__main__":
    df = validate(extract(os.path.join(DATASETS, "sales.csv")))

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)          # fresh DB for a repeatable demo
    with sqlite3.connect(DB_PATH) as conn:
        create_schema(conn)         # 1. schema
        load(conn, df)              # 2. load into it
        verify = pd.read_sql_query(
            "SELECT p.category, SUM(f.revenue) AS revenue "
            "FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id "
            "GROUP BY p.category ORDER BY revenue DESC",
            conn,
        )
    print("\n--- Verify: revenue by category (queried from the DB) ---")
    print(verify)
