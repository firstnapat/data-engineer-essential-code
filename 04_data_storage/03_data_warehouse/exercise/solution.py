"""
Solution: Data Warehouse — Layered Load with ClickHouse (raw / staging / mart)
on the QuickMart dataset (datasets/new-raw/).

  raw.*     — data as-is from the dirty source CSVs
  staging.* — cleaned & deduplicated
  mart.*    — aggregated, ready to query

Setup: docker compose up -d clickhouse   (HTTP on :8123)
Run:   uv run 04_data_storage/03_data_warehouse/exercise/solution.py
"""
import os
import pandas as pd
import clickhouse_connect
from dotenv import load_dotenv


def to_rows(df: pd.DataFrame, cols: list) -> list:
    """DataFrame -> list-of-rows, replacing NaN/NaT with None."""
    return [
        [None if pd.isna(v) else v for v in row]
        for row in df[cols].itertuples(index=False, name=None)
    ]


load_dotenv()
RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
    database=os.getenv("CLICKHOUSE_DB", "default"),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "clickhouse"),
)
print("[dw] Connected to ClickHouse")

# =============================================================================
# Task 1: Create databases (layers)
# =============================================================================
# Drop + recreate so the layer schemas are always rebuilt cleanly each run.
for db in ("raw", "staging", "mart"):
    client.command(f"DROP DATABASE IF EXISTS {db}")
    client.command(f"CREATE DATABASE {db}")
print("[dw] Databases: raw, staging, mart")

# =============================================================================
# Task 2: Raw layer — load the dirty CSVs as-is
# =============================================================================
# Text columns are Nullable(String) and numeric columns are wide types so that
# dirty values (blank category, amount<=0, future dates) all land without error.
RAW_SCHEMAS = {
    "raw.customers": """
        CREATE TABLE IF NOT EXISTS raw.customers (
            customer_id   UInt32,
            customer_name Nullable(String),
            email         Nullable(String),
            sub_tier      Nullable(String),
            created_at    Nullable(String)
        ) ENGINE = MergeTree() ORDER BY customer_id
    """,
    "raw.products": """
        CREATE TABLE IF NOT EXISTS raw.products (
            product_id   UInt32,
            product_name Nullable(String),
            category     Nullable(String),
            brand        Nullable(String),
            price        Float64
        ) ENGINE = MergeTree() ORDER BY product_id
    """,
    "raw.orders": """
        CREATE TABLE IF NOT EXISTS raw.orders (
            order_id    UInt32,
            customer_id UInt32,
            order_date  String,
            status      String,
            amount      Float64
        ) ENGINE = MergeTree() ORDER BY order_id
    """,
    "raw.order_items": """
        CREATE TABLE IF NOT EXISTS raw.order_items (
            order_item_id UInt32,
            order_id      UInt32,
            product_id    UInt32,
            qty           Int32,
            unit_price    Float64,
            subtotal      Float64
        ) ENGINE = MergeTree() ORDER BY order_item_id
    """,
    "raw.deliveries": """
        CREATE TABLE IF NOT EXISTS raw.deliveries (
            delivery_id       UInt32,
            delivery_date     String,
            vehicle_id        Nullable(String),
            parcels_delivered Int32
        ) ENGINE = MergeTree() ORDER BY delivery_id
    """,
}

for table, sql in RAW_SCHEMAS.items():
    client.command(sql)
    client.command(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] Raw tables ready")

df_customers = pd.read_csv(os.path.join(RAW, "customers.csv"))
df_products  = pd.read_csv(os.path.join(RAW, "products.csv"))
df_orders    = pd.read_csv(os.path.join(RAW, "orders.csv"))
df_items     = pd.read_csv(os.path.join(RAW, "order_items.csv"))
df_deliv     = pd.read_csv(os.path.join(RAW, "deliveries.csv"))

CUSTOMERS_COLS  = ["customer_id", "customer_name", "email", "sub_tier", "created_at"]
PRODUCTS_COLS   = ["product_id", "product_name", "category", "brand", "price"]
ORDERS_COLS     = ["order_id", "customer_id", "order_date", "status", "amount"]
ITEMS_COLS      = ["order_item_id", "order_id", "product_id", "qty", "unit_price", "subtotal"]
DELIVERIES_COLS = ["delivery_id", "delivery_date", "vehicle_id", "parcels_delivered"]

client.insert("raw.customers",   to_rows(df_customers, CUSTOMERS_COLS),  column_names=CUSTOMERS_COLS)
client.insert("raw.products",    to_rows(df_products,  PRODUCTS_COLS),   column_names=PRODUCTS_COLS)
client.insert("raw.orders",      to_rows(df_orders,    ORDERS_COLS),     column_names=ORDERS_COLS)
client.insert("raw.order_items", to_rows(df_items,     ITEMS_COLS),      column_names=ITEMS_COLS)
client.insert("raw.deliveries",  to_rows(df_deliv,     DELIVERIES_COLS), column_names=DELIVERIES_COLS)

print(f"[raw] customers={len(df_customers)}, products={len(df_products)}, "
      f"orders={len(df_orders)}, order_items={len(df_items)}, deliveries={len(df_deliv)}")

# =============================================================================
# Task 3: Staging layer — clean & deduplicate from raw
# =============================================================================
STAGING_SCHEMAS = {
    "staging.customers": """
        CREATE TABLE IF NOT EXISTS staging.customers (
            customer_id   UInt32,
            customer_name String,
            email         String,
            sub_tier      LowCardinality(String),
            created_at    Date
        ) ENGINE = MergeTree() ORDER BY customer_id
    """,
    "staging.products": """
        CREATE TABLE IF NOT EXISTS staging.products (
            product_id   UInt32,
            product_name String,
            category     LowCardinality(String),
            brand        LowCardinality(String),
            price        Float64
        ) ENGINE = MergeTree() ORDER BY product_id
    """,
    "staging.orders": """
        CREATE TABLE IF NOT EXISTS staging.orders (
            order_id    UInt32,
            customer_id UInt32,
            order_date  Date,
            status      LowCardinality(String),
            amount      Float64
        ) ENGINE = MergeTree() ORDER BY (order_date, order_id)
    """,
    "staging.order_items": """
        CREATE TABLE IF NOT EXISTS staging.order_items (
            order_item_id UInt32,
            order_id      UInt32,
            product_id    UInt32,
            qty           UInt32,
            unit_price    Float64,
            subtotal      Float64
        ) ENGINE = MergeTree() ORDER BY (order_id, order_item_id)
    """,
    "staging.deliveries": """
        CREATE TABLE IF NOT EXISTS staging.deliveries (
            delivery_id       UInt32,
            delivery_date     Date,
            vehicle_id        LowCardinality(String),
            parcels_delivered UInt32
        ) ENGINE = MergeTree() ORDER BY (delivery_date, delivery_id)
    """,
}

for table, sql in STAGING_SCHEMAS.items():
    client.command(sql)
    client.command(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] Staging tables ready")

# customers: dedup by customer_id (the PK — emails are NOT unique here since
# names come from a small pool), drop blank name / invalid email, tidy tier
client.command("""
    INSERT INTO staging.customers
    SELECT DISTINCT ON (customer_id)
        customer_id, customer_name, lower(email),
        initcap(sub_tier), parseDateTimeBestEffortOrNull(created_at)
    FROM raw.customers
    WHERE customer_name != '' AND customer_name IS NOT NULL
      AND match(email, '@.+\\.')
      AND created_at IS NOT NULL
""")

# products: dedup by product_id, drop blank category / price<=0
client.command("""
    INSERT INTO staging.products
    SELECT DISTINCT ON (product_id)
        product_id, product_name, category, brand, price
    FROM raw.products
    WHERE category != '' AND category IS NOT NULL AND price > 0
""")

# orders: dedup by order_id, drop amount<=0, lower status, keep real customers
client.command("""
    INSERT INTO staging.orders
    SELECT DISTINCT ON (order_id)
        order_id, customer_id, parseDateTimeBestEffort(order_date),
        replaceAll(lower(status), 'canceled', 'cancelled'), amount
    FROM raw.orders
    WHERE amount > 0
      AND customer_id IN (SELECT customer_id FROM staging.customers)
""")

# order_items: dedup by PK, drop qty<=0 / unit_price<=0, recompute subtotal
client.command("""
    INSERT INTO staging.order_items
    SELECT DISTINCT ON (order_item_id)
           order_item_id, order_id, product_id, qty, unit_price,
           round(qty * unit_price, 2)
    FROM raw.order_items
    WHERE qty > 0 AND unit_price > 0
""")

# deliveries: dedup by PK, drop parcels<=0 / blank vehicle
client.command("""
    INSERT INTO staging.deliveries
    SELECT DISTINCT ON (delivery_id)
           delivery_id, parseDateTimeBestEffort(delivery_date),
           vehicle_id, parcels_delivered
    FROM raw.deliveries
    WHERE parcels_delivered > 0 AND vehicle_id != '' AND vehicle_id IS NOT NULL
""")

s_counts = {t: client.query(f"SELECT count() FROM staging.{t}").result_rows[0][0]
            for t in ("customers", "products", "orders", "order_items", "deliveries")}
print("[staging] " + ", ".join(f"{k}={v}" for k, v in s_counts.items()))

# =============================================================================
# Task 4: Mart layer — aggregations
# =============================================================================

# order_summary: orders grouped by status
client.command("""
    CREATE TABLE IF NOT EXISTS mart.order_summary (
        status        LowCardinality(String),
        order_count   UInt32,
        total_revenue Float64
    ) ENGINE = MergeTree() ORDER BY status
""")
client.command("TRUNCATE TABLE IF EXISTS mart.order_summary")
client.command("""
    INSERT INTO mart.order_summary
    SELECT status, count() AS order_count, round(sum(amount), 2) AS total_revenue
    FROM staging.orders GROUP BY status
""")

# category_revenue: order_items joined to products
client.command("""
    CREATE TABLE IF NOT EXISTS mart.category_revenue (
        category LowCardinality(String),
        revenue  Float64
    ) ENGINE = MergeTree() ORDER BY category
""")
client.command("TRUNCATE TABLE IF EXISTS mart.category_revenue")
client.command("""
    INSERT INTO mart.category_revenue
    SELECT p.category, round(sum(i.subtotal), 2) AS revenue
    FROM staging.order_items i
    JOIN staging.products p ON i.product_id = p.product_id
    GROUP BY p.category
    ORDER BY revenue DESC
""")
print("[dw] Mart tables populated")

# =============================================================================
# Task 5: Query the mart
# =============================================================================
print("\n--- Order Summary by Status ---")
print(client.query_df("SELECT * FROM mart.order_summary ORDER BY total_revenue DESC"))

print("\n--- Revenue by Category ---")
print(client.query_df("SELECT * FROM mart.category_revenue ORDER BY revenue DESC"))

# --- Verification ------------------------------------------------------------
raw_orders  = client.query("SELECT count() FROM raw.orders").result_rows[0][0]
stg_orders  = client.query("SELECT count() FROM staging.orders").result_rows[0][0]
mart_rows   = client.query("SELECT count() FROM mart.order_summary").result_rows[0][0]
assert raw_orders > stg_orders, "staging.orders should be smaller than raw (dirty rows dropped)"
assert mart_rows > 0,           "mart.order_summary is empty"
print("\n✅ All verifications passed!")
