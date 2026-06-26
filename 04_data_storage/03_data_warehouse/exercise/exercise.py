"""
Exercise: Data Warehouse — Layered Load into ClickHouse (raw / staging / mart)
Practice the concepts from clickhouse_example.py (column-oriented OLAP) on the
QuickMart dataset (datasets/new-raw/).

Build three layers:
  raw.*     — the dirty CSVs landed as-is
  staging.* — cleaned & deduplicated
  mart.*    — aggregations ready to query

Setup: docker compose up -d clickhouse

Configure .env:
  CLICKHOUSE_HOST=localhost
  CLICKHOUSE_PORT=8123
  CLICKHOUSE_DB=default
  CLICKHOUSE_USER=default
  CLICKHOUSE_PASSWORD=clickhouse

Datasets: datasets/new-raw/ — customers, products, orders, order_items, deliveries.
They are DIRTY (duplicates, blank/invalid values, amount<=0, future dates);
the staging layer is where you clean them.

Run: uv run 04_data_storage/03_data_warehouse/exercise/exercise.py
"""
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")

try:
    # =========================================================================
    # Task 1: Connect to ClickHouse
    # =========================================================================
    print("--- Task 1: Connect to ClickHouse ---")
    # TODO: Create a ClickHouse client using clickhouse_connect.get_client(...)
    #       Load host/port/user/password from .env.
    import clickhouse_connect

    CH_HOST     = os.getenv("CLICKHOUSE_HOST", "localhost")
    CH_PORT     = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    CH_DB       = os.getenv("CLICKHOUSE_DB", "default")
    CH_USER     = os.getenv("CLICKHOUSE_USER", "default")
    CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse")

    client = None  # Replace with clickhouse_connect.get_client(...)
    print("[dw] Connected to ClickHouse")

    # =========================================================================
    # Task 2: Raw layer — create raw.* tables and load the 5 CSVs as-is
    # =========================================================================
    print("\n--- Task 2: Raw layer ---")
    # TODO: CREATE DATABASE raw, then a raw table per dataset
    #       (customers, products, orders, order_items, deliveries).
    #       Make text columns Nullable(String) so dirty/blank values land OK.
    #       Read each CSV with pandas and client.insert(table, rows, column_names=[...]).

    print("[dw] Raw tables loaded")

    # =========================================================================
    # Task 3: Staging layer — clean & deduplicate from raw
    # =========================================================================
    print("\n--- Task 3: Staging layer ---")
    # TODO: CREATE DATABASE staging, then INSERT ... SELECT from raw with cleaning:
    #   customers   — dedup by customer_id, drop blank name / invalid email, tidy sub_tier
    #   products    — dedup by product_id, drop blank category / price<=0
    #   orders      — dedup by order_id, drop amount<=0, lower(status), drop orphan customers
    #   order_items — dedup by order_item_id, drop qty<=0 / unit_price<=0, recompute subtotal
    #   deliveries  — dedup by delivery_id, drop parcels<=0 / blank vehicle
    # Hint: ClickHouse supports SELECT DISTINCT ON (key) and parseDateTimeBestEffort().

    print("[dw] Staging tables loaded")

    # =========================================================================
    # Task 4: Mart layer — aggregate and query
    # =========================================================================
    print("\n--- Task 4: Mart layer ---")
    # TODO: Build at least 2 mart tables from staging, e.g.
    #   mart.order_summary    — orders grouped by status (count, total revenue)
    #   mart.category_revenue — sum(order_items.subtotal) joined to products by product_id
    # Then print them with client.query_df(...).

    # --- Verification ---
    # Uncomment after completing all tasks (cleaning removes the dirty rows, so
    # staging is smaller than raw):
    # raw_orders = client.query("SELECT count() FROM raw.orders").result_rows[0][0]
    # stg_orders = client.query("SELECT count() FROM staging.orders").result_rows[0][0]
    # assert raw_orders > stg_orders, "staging.orders should be smaller than raw"
    # assert client.query("SELECT count() FROM staging.products").result_rows[0][0] == 50
    # print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ ClickHouse connection failed: {e}")
    print("Make sure ClickHouse is running:  docker compose up -d clickhouse")
