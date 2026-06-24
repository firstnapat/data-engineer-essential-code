"""
Exercise: Data Ingestion — RustFS Silver Layer → ClickHouse
Ingest cleaned Parquet files from the data lake directly into ClickHouse
using the s3() table function — no boto3 or pandas required.

Run: uv run 05_data_ingestion/04_datalake_to_warehouse/exercise/exercise.py

Pipeline: Connect → Load (idempotent) → Incremental

s3() syntax:
  s3(path, access_key, secret_key, format)

  Example:
    SELECT * FROM s3(
        'http://localhost:9000/exercise-lake/silver/users/2026-06-24/data.parquet',
        'ACCESS_KEY', 'SECRET_KEY',
        'Parquet'
    )

Authentication:
  ClickHouse — .env (CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_DB, ...)
  RustFS     — credentials.json at 04_data_storage/02_data_lake/credentials.json
"""
import os
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()

CREDS_PATH = os.path.join(os.path.dirname(__file__),
                          "../../../04_data_storage/02_data_lake/credentials.json")
BUCKET = "exercise-lake"
TODAY  = date.today().isoformat()

try:
    # =========================================================================
    # Task 1: Load credentials and connect to ClickHouse
    # =========================================================================
    print("--- Task 1: Connect ---")
    # TODO: Read credentials.json to get access_key and secret_key.
    #       Create a ClickHouse client using settings from .env.

    client = None  # Replace
    access_key = None
    secret_key = None
    endpoint   = "http://localhost:9000"
    print("[ingest] Connected")

    # =========================================================================
    # Task 2: Load — INSERT INTO ... SELECT FROM s3()
    # =========================================================================
    print("\n--- Task 2: Load Silver → ClickHouse ---")
    # TODO: For each table, truncate then INSERT using s3() table function.
    #       Path pattern: {endpoint}/{BUCKET}/silver/{table}/{TODAY}/data.parquet
    #
    # Tables: users, addresses, orders, order_items, transports

    # =========================================================================
    # Task 3: Validate
    # =========================================================================
    print("\n--- Task 3: Validate ---")
    # TODO: After loading, query each table and assert row count > 0.

    # =========================================================================
    # Task 4: Incremental — skip dates already loaded
    # =========================================================================
    print("\n--- Task 4: Incremental load ---")
    # TODO: Check whether today's partition exists in ClickHouse before loading.
    #       Skip tables that already have data for TODAY.
    #
    # Hint: track ingestion date in a separate ClickHouse table, or
    #       query MAX(ingestion_date) if you add that column to each table.

    # --- Verification ---
    # Uncomment after completing all tasks:
    # for table in ["users", "addresses", "orders", "order_items", "transports"]:
    #     count = client.execute(f"SELECT count() FROM {table}")[0][0]
    #     print(f"[verify] {table}: {count} rows")
    # print("\n✅ Pipeline complete!")

except Exception as e:
    print(f"\n❌ Pipeline failed: {e}")
    print("Check ClickHouse connection and credentials.json.")
