"""
Solution: Data Warehouse — Layered Load with ClickHouse (raw / staging / mart)

  raw.*     — data as-is from source CSV
  staging.* — cleaned & deduplicated
  mart.*    — aggregated, ready to query
"""
import os
import pandas as pd
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

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

for db in ("raw", "staging", "mart"):
    client.command(f"CREATE DATABASE IF NOT EXISTS {db}")
print("[dw] Databases: raw, staging, mart")

# =============================================================================
# Task 2: Raw layer — create tables + insert as-is
# =============================================================================

RAW_SCHEMAS = {
    "raw.users": """
        CREATE TABLE IF NOT EXISTS raw.users (
            user_id    UInt32,
            name       String,
            email      String,
            phone      Nullable(String),
            created_at String
        ) ENGINE = MergeTree() ORDER BY user_id
    """,
    "raw.addresses": """
        CREATE TABLE IF NOT EXISTS raw.addresses (
            address_id  UInt32,
            user_id     UInt32,
            street      String,
            district    String,
            province    String,
            postal_code Nullable(String),
            country     String
        ) ENGINE = MergeTree() ORDER BY (user_id, address_id)
    """,
    "raw.orders": """
        CREATE TABLE IF NOT EXISTS raw.orders (
            order_id            UInt32,
            user_id             UInt32,
            shipping_address_id UInt32,
            order_date          String,
            status              String,
            total_amount        Float32
        ) ENGINE = MergeTree() ORDER BY (order_date, order_id)
    """,
    "raw.order_items": """
        CREATE TABLE IF NOT EXISTS raw.order_items (
            order_item_id UInt32,
            order_id      UInt32,
            product_id    UInt32,
            quantity      UInt32,
            unit_price    Float32,
            subtotal      Float32
        ) ENGINE = MergeTree() ORDER BY (order_id, order_item_id)
    """,
    "raw.transports": """
        CREATE TABLE IF NOT EXISTS raw.transports (
            transport_id    UInt32,
            order_id        UInt32,
            carrier         String,
            tracking_number Nullable(String),
            shipped_at      String,
            delivered_at    Nullable(String),
            status          String
        ) ENGINE = MergeTree() ORDER BY (order_id, transport_id)
    """,
}

for table, sql in RAW_SCHEMAS.items():
    client.command(sql)
    client.command(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] Raw tables ready")

# Insert raw data without any cleaning
df_users  = pd.read_csv(os.path.join(DATASETS, "raw/users_raw.csv"))
df_addr   = pd.read_csv(os.path.join(DATASETS, "raw/addresses_raw.csv"))
df_orders = pd.read_csv(os.path.join(DATASETS, "raw/orders_raw.csv"))
df_items  = pd.read_csv(os.path.join(DATASETS, "raw/order_items_raw.csv"))
df_trans  = pd.read_csv(os.path.join(DATASETS, "raw/transports_raw.csv"))

df_users["phone"]   = df_users["phone"].where(pd.notna(df_users["phone"]), None)
df_addr["postal_code"] = df_addr["postal_code"].where(pd.notna(df_addr["postal_code"]), None)
df_trans["tracking_number"] = df_trans["tracking_number"].where(pd.notna(df_trans["tracking_number"]), None)
df_trans["delivered_at"]    = df_trans["delivered_at"].where(pd.notna(df_trans["delivered_at"]), None)

client.insert("raw.users",       df_users[["user_id","name","email","phone","created_at"]].values.tolist(),
              column_names=["user_id","name","email","phone","created_at"])
client.insert("raw.addresses",   df_addr[["address_id","user_id","street","district","province","postal_code","country"]].values.tolist(),
              column_names=["address_id","user_id","street","district","province","postal_code","country"])
client.insert("raw.orders",      df_orders[["order_id","user_id","shipping_address_id","order_date","status","total_amount"]].values.tolist(),
              column_names=["order_id","user_id","shipping_address_id","order_date","status","total_amount"])
client.insert("raw.order_items", df_items[["order_item_id","order_id","product_id","quantity","unit_price","subtotal"]].values.tolist(),
              column_names=["order_item_id","order_id","product_id","quantity","unit_price","subtotal"])
client.insert("raw.transports",  df_trans[["transport_id","order_id","carrier","tracking_number","shipped_at","delivered_at","status"]].values.tolist(),
              column_names=["transport_id","order_id","carrier","tracking_number","shipped_at","delivered_at","status"])

print(f"[raw] users={len(df_users)}, addresses={len(df_addr)}, "
      f"orders={len(df_orders)}, order_items={len(df_items)}, transports={len(df_trans)}")

# =============================================================================
# Task 3: Staging layer — clean & deduplicate from raw
# =============================================================================

STAGING_SCHEMAS = {
    "staging.users": """
        CREATE TABLE IF NOT EXISTS staging.users (
            user_id    UInt32,
            name       String,
            email      String,
            phone      Nullable(String),
            created_at DateTime
        ) ENGINE = MergeTree() ORDER BY user_id
    """,
    "staging.addresses": """
        CREATE TABLE IF NOT EXISTS staging.addresses (
            address_id  UInt32,
            user_id     UInt32,
            street      String,
            district    String,
            province    LowCardinality(String),
            postal_code String,
            country     String
        ) ENGINE = MergeTree() ORDER BY (user_id, address_id)
    """,
    "staging.orders": """
        CREATE TABLE IF NOT EXISTS staging.orders (
            order_id            UInt32,
            user_id             UInt32,
            shipping_address_id UInt32,
            order_date          DateTime,
            status              LowCardinality(String),
            total_amount        Float32
        ) ENGINE = MergeTree() ORDER BY (order_date, order_id)
    """,
    "staging.order_items": """
        CREATE TABLE IF NOT EXISTS staging.order_items (
            order_item_id UInt32,
            order_id      UInt32,
            product_id    UInt32,
            quantity      UInt32,
            unit_price    Float32,
            subtotal      Float32
        ) ENGINE = MergeTree() ORDER BY (order_id, order_item_id)
    """,
    "staging.transports": """
        CREATE TABLE IF NOT EXISTS staging.transports (
            transport_id    UInt32,
            order_id        UInt32,
            carrier         String,
            tracking_number Nullable(String),
            shipped_at      DateTime,
            delivered_at    Nullable(DateTime),
            status          LowCardinality(String)
        ) ENGINE = MergeTree() ORDER BY (order_id, transport_id)
    """,
}

for table, sql in STAGING_SCHEMAS.items():
    client.command(sql)
    client.command(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] Staging tables ready")

# Populate staging by querying raw and applying cleaning
client.command("""
    INSERT INTO staging.users
    SELECT DISTINCT ON (email)
        user_id, name, email, phone, parseDateTimeBestEffort(created_at)
    FROM raw.users
    WHERE email != '' AND name != ''
""")

client.command("""
    INSERT INTO staging.addresses
    SELECT address_id, user_id, street, district,
           initcap(province), postal_code, country
    FROM raw.addresses
    WHERE postal_code != '' AND postal_code IS NOT NULL
""")

client.command("""
    INSERT INTO staging.orders
    SELECT DISTINCT ON (order_id)
        order_id, user_id, shipping_address_id,
        parseDateTimeBestEffort(order_date), lower(status), total_amount
    FROM raw.orders
    WHERE total_amount > 0
""")

client.command("""
    INSERT INTO staging.order_items
    SELECT order_item_id, order_id, product_id, quantity, unit_price,
           round(quantity * unit_price, 2)
    FROM raw.order_items
    WHERE quantity > 0 AND unit_price > 0
""")

client.command("""
    INSERT INTO staging.transports
    SELECT transport_id, order_id, carrier, tracking_number,
           parseDateTimeBestEffort(shipped_at),
           if(delivered_at IS NOT NULL, parseDateTimeBestEffort(delivered_at), NULL),
           lower(status)
    FROM raw.transports
""")

s_counts = {t: client.query(f"SELECT count() FROM staging.{t}").result_rows[0][0]
            for t in ("users","addresses","orders","order_items","transports")}
print("[staging] " + ", ".join(f"{k}={v}" for k, v in s_counts.items()))

# =============================================================================
# Task 4: Mart layer — aggregations
# =============================================================================

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
    SELECT status, count() AS order_count, round(sum(total_amount), 2) AS total_revenue
    FROM staging.orders GROUP BY status
""")

client.command("""
    CREATE TABLE IF NOT EXISTS mart.top_users (
        user_id     UInt32,
        name        String,
        total_spend Float64,
        order_count UInt32
    ) ENGINE = MergeTree() ORDER BY total_spend
""")
client.command("TRUNCATE TABLE IF EXISTS mart.top_users")
client.command("""
    INSERT INTO mart.top_users
    SELECT o.user_id, u.name,
           round(sum(o.total_amount), 2) AS total_spend,
           count() AS order_count
    FROM staging.orders o
    JOIN staging.users u ON o.user_id = u.user_id
    GROUP BY o.user_id, u.name
    ORDER BY total_spend DESC
""")
print("[dw] Mart tables populated")

# =============================================================================
# Task 5: Query the mart
# =============================================================================

print("\n--- Order Summary by Status ---")
print(client.query_df("SELECT * FROM mart.order_summary ORDER BY total_revenue DESC"))

print("\n--- Top 10 Users by Spend ---")
print(client.query_df("SELECT * FROM mart.top_users ORDER BY total_spend DESC LIMIT 10"))

# --- Verification ------------------------------------------------------------

raw_orders   = client.query("SELECT count() FROM raw.orders").result_rows[0][0]
stg_summary  = client.query("SELECT count() FROM mart.order_summary").result_rows[0][0]
assert raw_orders > 0,    "raw.orders is empty"
assert stg_summary > 0,   "mart.order_summary is empty"
print("\n✅ All verifications passed!")
