"""
Solution: Data Warehouse — Multi-table Load with ClickHouse
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

# --- Task 2: Create tables ---------------------------------------------------

SCHEMAS = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            user_id    UInt32,
            name       String,
            email      String,
            phone      Nullable(String),
            created_at DateTime
        ) ENGINE = MergeTree() ORDER BY user_id
    """,
    "addresses": """
        CREATE TABLE IF NOT EXISTS addresses (
            address_id  UInt32,
            user_id     UInt32,
            street      String,
            district    String,
            province    LowCardinality(String),
            postal_code Nullable(String),
            country     String
        ) ENGINE = MergeTree() ORDER BY (user_id, address_id)
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id            UInt32,
            user_id             UInt32,
            shipping_address_id UInt32,
            order_date          DateTime,
            status              LowCardinality(String),
            total_amount        Float32
        ) ENGINE = MergeTree() ORDER BY (order_date, order_id)
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id UInt32,
            order_id      UInt32,
            product_id    UInt32,
            quantity      UInt32,
            unit_price    Float32,
            subtotal      Float32
        ) ENGINE = MergeTree() ORDER BY (order_id, order_item_id)
    """,
    "transports": """
        CREATE TABLE IF NOT EXISTS transports (
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

for table, sql in SCHEMAS.items():
    client.command(sql)
    client.command(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] All tables ready")

# --- Task 3: Insert data -----------------------------------------------------

df_users = pd.read_csv(os.path.join(DATASETS, "raw/users_raw.csv"))
df_users["phone"] = df_users["phone"].where(pd.notna(df_users["phone"]), None)
df_users["created_at"] = pd.to_datetime(df_users["created_at"])
client.insert("users", df_users[["user_id","name","email","phone","created_at"]].values.tolist(),
              column_names=["user_id","name","email","phone","created_at"])
print(f"[dw] users: {len(df_users)} rows")

df_addr = pd.read_csv(os.path.join(DATASETS, "raw/addresses_raw.csv"))
df_addr["postal_code"] = df_addr["postal_code"].where(pd.notna(df_addr["postal_code"]), None)
client.insert("addresses",
              df_addr[["address_id","user_id","street","district","province","postal_code","country"]].values.tolist(),
              column_names=["address_id","user_id","street","district","province","postal_code","country"])
print(f"[dw] addresses: {len(df_addr)} rows")

df_orders = pd.read_csv(os.path.join(DATASETS, "raw/orders_raw.csv"))
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
client.insert("orders",
              df_orders[["order_id","user_id","shipping_address_id","order_date","status","total_amount"]].values.tolist(),
              column_names=["order_id","user_id","shipping_address_id","order_date","status","total_amount"])
print(f"[dw] orders: {len(df_orders)} rows")

df_items = pd.read_csv(os.path.join(DATASETS, "raw/order_items_raw.csv"))
client.insert("order_items",
              df_items[["order_item_id","order_id","product_id","quantity","unit_price","subtotal"]].values.tolist(),
              column_names=["order_item_id","order_id","product_id","quantity","unit_price","subtotal"])
print(f"[dw] order_items: {len(df_items)} rows")

df_trans = pd.read_csv(os.path.join(DATASETS, "raw/transports_raw.csv"))
df_trans["shipped_at"]   = pd.to_datetime(df_trans["shipped_at"])
df_trans["delivered_at"] = pd.to_datetime(df_trans["delivered_at"], errors="coerce")
df_trans["tracking_number"] = df_trans["tracking_number"].where(pd.notna(df_trans["tracking_number"]), None)
df_trans["delivered_at"]    = df_trans["delivered_at"].where(pd.notna(df_trans["delivered_at"]), None)
client.insert("transports",
              df_trans[["transport_id","order_id","carrier","tracking_number","shipped_at","delivered_at","status"]].values.tolist(),
              column_names=["transport_id","order_id","carrier","tracking_number","shipped_at","delivered_at","status"])
print(f"[dw] transports: {len(df_trans)} rows")

# --- Task 4: Revenue by status -----------------------------------------------

print("\n--- Revenue by Status ---")
print(client.query_df("""
    SELECT status, count() AS order_count, sum(total_amount) AS total_revenue
    FROM orders GROUP BY status ORDER BY total_revenue DESC
"""))

# --- Task 5: Top 5 users -----------------------------------------------------

print("\n--- Top 5 Users by Spend ---")
print(client.query_df("""
    SELECT u.name, sum(o.total_amount) AS total_spend
    FROM orders o JOIN users u ON o.user_id = u.user_id
    GROUP BY u.name ORDER BY total_spend DESC LIMIT 5
"""))

# --- Verification ------------------------------------------------------------

for table, expected in [("users", 65), ("orders", 108), ("order_items", 198)]:
    count = client.query(f"SELECT count() FROM {table}").result_rows[0][0]
    assert count == expected, f"{table}: expected {expected}, got {count}"
print("\n✅ All verifications passed!")
