"""
Solution: Data Warehouse — Multi-table Load with ClickHouse
"""
import os
import pandas as pd
from dotenv import load_dotenv
from clickhouse_driver import Client

load_dotenv()

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

client = Client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", "9009")),
    database=os.getenv("CLICKHOUSE_DB", "default"),
    user=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
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
    client.execute(sql)
    client.execute(f"TRUNCATE TABLE IF EXISTS {table}")
print("[dw] All tables ready")

# --- Task 3: Insert data -----------------------------------------------------

def parse_dt(val):
    if pd.isna(val):
        return None
    from datetime import datetime
    return datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")

df_users = pd.read_csv(os.path.join(DATASETS, "raw/users_raw.csv"))
client.execute(
    "INSERT INTO users (user_id, name, email, phone, created_at) VALUES",
    [(int(r["user_id"]), r["name"], r["email"],
      r["phone"] if pd.notna(r["phone"]) else None,
      parse_dt(r["created_at"]))
     for r in df_users.to_dict("records")],
)
print(f"[dw] users: {len(df_users)} rows")

df_addr = pd.read_csv(os.path.join(DATASETS, "raw/addresses_raw.csv"))
client.execute(
    "INSERT INTO addresses (address_id, user_id, street, district, province, postal_code, country) VALUES",
    [(int(r["address_id"]), int(r["user_id"]), r["street"], r["district"],
      r["province"], r["postal_code"] if pd.notna(r["postal_code"]) else None, r["country"])
     for r in df_addr.to_dict("records")],
)
print(f"[dw] addresses: {len(df_addr)} rows")

df_orders = pd.read_csv(os.path.join(DATASETS, "raw/orders_raw.csv"))
client.execute(
    "INSERT INTO orders (order_id, user_id, shipping_address_id, order_date, status, total_amount) VALUES",
    [(int(r["order_id"]), int(r["user_id"]), int(r["shipping_address_id"]),
      parse_dt(r["order_date"]), r["status"], float(r["total_amount"]))
     for r in df_orders.to_dict("records")],
)
print(f"[dw] orders: {len(df_orders)} rows")

df_items = pd.read_csv(os.path.join(DATASETS, "raw/order_items_raw.csv"))
client.execute(
    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price, subtotal) VALUES",
    [(int(r["order_item_id"]), int(r["order_id"]), int(r["product_id"]),
      int(r["quantity"]), float(r["unit_price"]), float(r["subtotal"]))
     for r in df_items.to_dict("records")],
)
print(f"[dw] order_items: {len(df_items)} rows")

df_trans = pd.read_csv(os.path.join(DATASETS, "raw/transports_raw.csv"))
client.execute(
    "INSERT INTO transports (transport_id, order_id, carrier, tracking_number, shipped_at, delivered_at, status) VALUES",
    [(int(r["transport_id"]), int(r["order_id"]), r["carrier"],
      r["tracking_number"] if pd.notna(r["tracking_number"]) else None,
      parse_dt(r["shipped_at"]),
      parse_dt(r["delivered_at"]) if pd.notna(r["delivered_at"]) else None,
      r["status"])
     for r in df_trans.to_dict("records")],
)
print(f"[dw] transports: {len(df_trans)} rows")

# --- Task 4: Revenue by status -----------------------------------------------

REVENUE_SQL = """
    SELECT status,
           count()          AS order_count,
           sum(total_amount) AS total_revenue
    FROM orders
    GROUP BY status
    ORDER BY total_revenue DESC
"""
data, cols = client.execute(REVENUE_SQL, with_column_types=True)
print("\n--- Revenue by Status ---")
print(pd.DataFrame(data, columns=[c[0] for c in cols]))

# --- Task 5: Top 5 users -----------------------------------------------------

TOP_USERS_SQL = """
    SELECT u.name, sum(o.total_amount) AS total_spend
    FROM orders o
    JOIN users u ON o.user_id = u.user_id
    GROUP BY u.name
    ORDER BY total_spend DESC
    LIMIT 5
"""
data, cols = client.execute(TOP_USERS_SQL, with_column_types=True)
print("\n--- Top 5 Users by Spend ---")
print(pd.DataFrame(data, columns=[c[0] for c in cols]))

# --- Verification ------------------------------------------------------------

for table, expected in [("users", 65), ("orders", 108), ("order_items", 198)]:
    count = client.execute(f"SELECT count() FROM {table}")[0][0]
    assert count == expected, f"{table}: expected {expected}, got {count}"
print("\n✅ All verifications passed!")
