"""
Exercise: Database Storage — Building a Product Dimension + Order-Items Fact
Practice the concepts from storage_db.py (star schema with SQLite) on the
QuickMart dataset (datasets/new-raw/).

The raw CSVs are DIRTY (duplicates, blank categories, qty=0, bad prices), so
you must clean them before loading — schema-on-write means bad rows don't get in.
Run: uv run 04_data_storage/01_database/exercise/exercise.py
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "/tmp/exercise_warehouse.db"
RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")

# Remove old DB to start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Load raw QuickMart data
products_raw = pd.read_csv(os.path.join(RAW, "products.csv"))
items_raw    = pd.read_csv(os.path.join(RAW, "order_items.csv"))
print(f"Loaded {len(products_raw)} raw product rows, {len(items_raw)} raw order-item rows")

with sqlite3.connect(DB_PATH) as conn:

    # =========================================================================
    # Task 1: Create dim_product table
    # =========================================================================
    # A dimension table holds one clean row per business entity. We keep the
    # source product_id as the natural key (UNIQUE) so the fact table can join.
    print("\n--- Task 1: Create dim_product table ---")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS dim_product (
        product_key  INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id   INTEGER NOT NULL UNIQUE,
        product_name TEXT NOT NULL,
        category     TEXT NOT NULL,
        brand        TEXT NOT NULL
    );
    """)
    print("[schema] dim_product table created")

    # =========================================================================
    # Task 2: Clean + load unique products into dim_product
    # =========================================================================
    # Dirty rows to drop: blank category, then keep one row per product_id.
    print("\n--- Task 2: Clean and load products ---")
    products_clean = products_raw.copy()
    products_clean["category"] = products_clean["category"].astype("string").str.strip()
    products_clean = products_clean[products_clean["category"].notna() & (products_clean["category"] != "")]
    products_clean = products_clean.drop_duplicates(subset=["product_id"])

    for _, r in products_clean.iterrows():
        conn.execute(
            "INSERT OR IGNORE INTO dim_product (product_id, product_name, category, brand) "
            "VALUES (?, ?, ?, ?)",
            (int(r["product_id"]), r["product_name"], r["category"], r["brand"]),
        )
    print(f"[dim] {len(products_clean)} clean products loaded")

    # =========================================================================
    # Task 3: Build a product lookup dictionary {product_id: product_key}
    # =========================================================================
    print("\n--- Task 3: Build product lookup dict ---")
    cursor = conn.execute("SELECT product_key, product_id FROM dim_product")
    product_keys = {product_id: product_key for product_key, product_id in cursor.fetchall()}
    print(f"Lookup has {len(product_keys)} products")

    # =========================================================================
    # Task 4: Create fact_order_items + clean-load + revenue-by-category query
    # =========================================================================
    print("\n--- Task 4: Create fact_order_items and query revenue by category ---")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS fact_order_items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL,
        product_key INTEGER REFERENCES dim_product(product_key),
        quantity    INTEGER NOT NULL,
        unit_price  REAL NOT NULL,
        subtotal    REAL NOT NULL
    );
    """)

    # Clean order_items: drop exact dups, drop qty<=0 / unit_price<=0,
    # recompute subtotal (the raw one is sometimes wrong), keep mappable products.
    items_clean = items_raw.drop_duplicates().copy()
    items_clean = items_clean[(items_clean["qty"] > 0) & (items_clean["unit_price"] > 0)]
    items_clean = items_clean[items_clean["product_id"].isin(product_keys)]
    items_clean["subtotal"] = (items_clean["qty"] * items_clean["unit_price"]).round(2)

    fact_rows = [
        (int(r["order_id"]), product_keys[int(r["product_id"])],
         int(r["qty"]), float(r["unit_price"]), float(r["subtotal"]))
        for _, r in items_clean.iterrows()
    ]
    conn.executemany(
        "INSERT INTO fact_order_items (order_id, product_key, quantity, unit_price, subtotal) "
        "VALUES (?,?,?,?,?)",
        fact_rows,
    )
    print(f"[fact] {len(fact_rows)} clean order-item rows loaded")

    revenue_by_cat = pd.read_sql_query("""
        SELECT p.category, ROUND(SUM(f.subtotal), 2) AS total_revenue
        FROM fact_order_items f
        JOIN dim_product p ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """, conn)
    print(revenue_by_cat)

    # =========================================================================
    # Task 5: Verification
    # =========================================================================
    print("\n--- Task 5: Verification ---")
    verify_df = pd.read_sql_query("SELECT * FROM dim_product", conn)
    print(f"dim_product rows: {len(verify_df)}")

    # All 50 base products survive cleaning (every product_id has a clean row).
    assert len(verify_df) == 50, f"Expected 50 products, got {len(verify_df)}"
    assert set(verify_df["category"]) == {"Beverage", "Snack", "Personal Care", "Household", "Food"}, \
        f"Unexpected categories: {set(verify_df['category'])}"
    assert verify_df["category"].str.strip().ne("").all(), "Blank category leaked into dim_product"

    fact_count = pd.read_sql_query("SELECT COUNT(*) AS cnt FROM fact_order_items", conn)["cnt"][0]
    assert fact_count == len(fact_rows), f"Expected {len(fact_rows)} fact rows, got {fact_count}"
    # Every fact row must reference a real dimension row (no orphan FKs).
    orphans = pd.read_sql_query("""
        SELECT COUNT(*) AS n FROM fact_order_items f
        LEFT JOIN dim_product p ON f.product_key = p.product_key
        WHERE p.product_key IS NULL
    """, conn)["n"][0]
    assert orphans == 0, f"Found {orphans} fact rows with no matching product"

    print("\n✅ All verifications passed!")
