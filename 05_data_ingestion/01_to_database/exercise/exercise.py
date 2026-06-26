"""
Exercise: Data Ingestion to Database — Build a CSV-to-SQLite Star Schema Pipeline
Practice the concepts from load_to_database.py on the QuickMart data
(datasets/new-raw/).

You will build a pipeline that:
  1. Extracts order_items.csv (the fact grain) + products.csv (the dimension)
  2. Validates the order-items schema
  3. Creates a star schema (dim_product + fact_order_items) in SQLite
  4. Cleans + loads the data (schema-on-write — bad rows don't get in)
  5. Queries the DB to verify correctness

Run: uv run 05_data_ingestion/01_to_database/exercise/exercise.py
"""
import os
import sqlite3
import pandas as pd

RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
DB_PATH = "/tmp/exercise_ingestion.db"

REQUIRED_COLUMNS = {"order_item_id", "order_id", "product_id", "qty", "unit_price", "subtotal"}


# ── Task 1: Extract ─────────────────────────────────────────────────────────
# Read order_items.csv into a DataFrame. Print: [extract] <N> rows from order_items.csv
def extract(source: str) -> pd.DataFrame:
    df_raw = pd.read_csv(source)
    print(f"[extract] {len(df_raw)} rows from order_items.csv")
    return df_raw


# ── Task 2: Validate ────────────────────────────────────────────────────────
# Check the schema is shaped as expected (this does NOT fix dirty values — that
# happens in load(); validation only fails fast on a structurally wrong file):
#   (a) all REQUIRED_COLUMNS present  -> ValueError(f"missing columns: {missing}")
#   (b) no nulls in product_id/qty/unit_price/subtotal -> ValueError("numeric fields contain nulls")
# Print "[validate] schema OK" then return the DataFrame.
def validate(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if df[["product_id", "qty", "unit_price", "subtotal"]].isnull().any().any():
        raise ValueError("numeric fields contain nulls")
    print("[validate] schema OK")
    return df


# ── Task 3: Create Schema ───────────────────────────────────────────────────
def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS dim_product (
        product_key  INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id   INTEGER NOT NULL UNIQUE,
        name         TEXT NOT NULL,
        category     TEXT NOT NULL,
        brand        TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS fact_order_items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL,
        product_key INTEGER REFERENCES dim_product(product_key),
        quantity    INTEGER NOT NULL,
        unit_price  REAL NOT NULL,
        subtotal    REAL NOT NULL
    );
    """)
    print("[schema] tables ready")


# ── Task 4: Load ────────────────────────────────────────────────────────────
# Clean both sources, then load the star schema:
#   Step A — dim_product: drop blank-category + duplicate products, insert
#   Step B — lookup dict {product_id: product_key}
#   Step C — fact: drop dups, drop qty<=0 / unit_price<=0, recompute subtotal,
#            keep only items whose product_id is in the dimension
#   Step D — insert fact rows with conn.executemany()
def load(conn: sqlite3.Connection, items: pd.DataFrame, products: pd.DataFrame) -> None:
    # Step A — clean + load the dimension
    products = products.copy()
    products["category"] = products["category"].astype("string").str.strip()
    products = products[products["category"].notna() & (products["category"] != "")]
    products = products.drop_duplicates(subset=["product_id"])
    conn.executemany(
        "INSERT OR IGNORE INTO dim_product (product_id, name, category, brand) VALUES (?,?,?,?)",
        products[["product_id", "product_name", "category", "brand"]].itertuples(index=False, name=None),
    )

    # Step B — lookup
    lookup = {pid: key for key, pid in conn.execute("SELECT product_key, product_id FROM dim_product")}

    # Step C — clean the fact
    items = items.drop_duplicates().copy()
    items = items[(items["qty"] > 0) & (items["unit_price"] > 0)]
    items = items[items["product_id"].isin(lookup)]
    items["subtotal"] = (items["qty"] * items["unit_price"]).round(2)

    # Step D — insert
    fact_rows = [
        (int(r["order_id"]), lookup[int(r["product_id"])],
         int(r["qty"]), float(r["unit_price"]), float(r["subtotal"]))
        for _, r in items.iterrows()
    ]
    conn.executemany(
        "INSERT INTO fact_order_items (order_id, product_key, quantity, unit_price, subtotal) "
        "VALUES (?,?,?,?,?)",
        fact_rows,
    )
    print(f"[load] {len(products)} products, {len(fact_rows)} fact rows loaded")


# ── Task 5: Run the Pipeline & Verify ───────────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract ---")
    items = extract(os.path.join(RAW, "order_items.csv"))
    products = pd.read_csv(os.path.join(RAW, "products.csv"))
    assert len(items) > 0, "order_items should not be empty"
    print(f"✓ Extracted {len(items)} order-item rows\n")

    print("--- Task 2: Validate ---")
    items = validate(items)
    print("✓ Validation passed\n")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        print("--- Task 3: Create Schema ---")
        create_schema(conn)
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()]
        assert "dim_product" in tables and "fact_order_items" in tables, "Schema not created"
        print("✓ Schema created\n")

        print("--- Task 4: Load ---")
        load(conn, items, products)
        dim_count  = conn.execute("SELECT COUNT(*) FROM dim_product").fetchone()[0]
        fact_count = conn.execute("SELECT COUNT(*) FROM fact_order_items").fetchone()[0]
        assert dim_count == 50, f"Expected 50 products, got {dim_count}"
        assert fact_count > 0, "fact_order_items should not be empty"
        # No orphan FKs allowed.
        orphans = conn.execute("""
            SELECT COUNT(*) FROM fact_order_items f
            LEFT JOIN dim_product p ON f.product_key = p.product_key
            WHERE p.product_key IS NULL
        """).fetchone()[0]
        assert orphans == 0, f"Found {orphans} orphan fact rows"
        print(f"✓ Loaded {dim_count} products + {fact_count} fact rows\n")

        print("--- Task 5: Verify — Revenue by Category ---")
        verify = pd.read_sql_query("""
            SELECT p.category, ROUND(SUM(f.subtotal), 2) AS revenue
            FROM fact_order_items f
            JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.category
            ORDER BY revenue DESC
        """, conn)
        print(verify)
        assert set(verify["category"]) == {"Beverage", "Snack", "Personal Care", "Household", "Food"}, \
            f"Unexpected categories: {set(verify['category'])}"
        print("\n✅ All verifications passed!")
