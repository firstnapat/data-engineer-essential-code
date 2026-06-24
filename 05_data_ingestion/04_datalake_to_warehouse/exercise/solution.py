"""
Solution: Data Ingestion — RustFS Silver Layer → ClickHouse via s3() function
"""
import os
import json
from datetime import date, datetime
from dotenv import load_dotenv
from clickhouse_driver import Client

load_dotenv()

CREDS_PATH = os.path.join(os.path.dirname(__file__),
                          "../../../04_data_storage/02_data_lake/credentials.json")
BUCKET = "exercise-lake"
TODAY  = date.today().isoformat()

# --- Task 1: Connect ---------------------------------------------------------

with open(CREDS_PATH) as f:
    creds = json.load(f)

access_key = creds["accessKey"]
secret_key = creds["secretKey"]
endpoint   = f"http://{creds['url'].replace('9001', '9000')}"

client = Client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", "9009")),
    database=os.getenv("CLICKHOUSE_DB", "default"),
    user=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
)
print("[ingest] Connected")

# --- Task 2: Load Silver → ClickHouse via s3() -------------------------------

TABLES = ["users", "addresses", "orders", "order_items", "transports"]

for table in TABLES:
    path = f"{endpoint}/{BUCKET}/silver/{table}/{TODAY}/data.parquet"
    client.execute(f"TRUNCATE TABLE IF EXISTS {table}")
    client.execute(f"""
        INSERT INTO {table}
        SELECT * FROM s3('{path}', '{access_key}', '{secret_key}', 'Parquet')
    """)
    count = client.execute(f"SELECT count() FROM {table}")[0][0]
    print(f"[ingest] {table}: {count} rows loaded")

# --- Task 3: Validate --------------------------------------------------------

for table in TABLES:
    count = client.execute(f"SELECT count() FROM {table}")[0][0]
    assert count > 0, f"{table} is empty after load"
print("[ingest] Validation passed")

# --- Task 4: Incremental — skip if already loaded today ----------------------

loaded_tables = []
for table in TABLES:
    path = f"{endpoint}/{BUCKET}/silver/{table}/{TODAY}/data.parquet"
    try:
        result = client.execute(f"""
            SELECT count() FROM s3('{path}', '{access_key}', '{secret_key}', 'Parquet')
        """)
        if result[0][0] > 0:
            count_in_ch = client.execute(f"SELECT count() FROM {table}")[0][0]
            if count_in_ch > 0:
                print(f"[ingest] {table}/{TODAY} already loaded — skipping")
                loaded_tables.append(table)
    except Exception:
        print(f"[ingest] {table}/{TODAY} partition not found — skipping")

print(f"\n[ingest] Already loaded today: {loaded_tables or 'none'}")

# --- Verification ------------------------------------------------------------

for table in TABLES:
    count = client.execute(f"SELECT count() FROM {table}")[0][0]
    print(f"[verify] {table}: {count} rows")
print("\n✅ Pipeline complete!")
