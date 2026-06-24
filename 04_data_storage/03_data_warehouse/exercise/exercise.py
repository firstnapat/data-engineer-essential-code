"""
Exercise: Data Warehouse — Multi-table Load with ClickHouse
Practice the concepts from clickhouse_example.py (column-oriented OLAP).
Run: uv run 04_data_storage/03_data_warehouse/exercise/exercise.py

Setup (Docker — start ClickHouse first):
  docker run -d --name de-clickhouse \\
    -p 8123:8123 -p 9009:9000 \\
    -v $(pwd)/datasets/raw:/var/lib/clickhouse/user_files \\
    clickhouse/clickhouse-server

Configure .env:
  CLICKHOUSE_HOST=localhost
  CLICKHOUSE_PORT=9009
  CLICKHOUSE_DB=default
  CLICKHOUSE_USER=default
  CLICKHOUSE_PASSWORD=

Datasets: datasets/raw/ — see datasets/er_diagram.md for schema.
"""
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

try:
    # =========================================================================
    # Task 1: Connect to ClickHouse
    # =========================================================================
    print("--- Task 1: Connect to ClickHouse ---")
    # TODO: Create a ClickHouse client using settings from .env.
    from clickhouse_driver import Client

    CH_HOST     = os.getenv("CLICKHOUSE_HOST", "localhost")
    CH_PORT     = int(os.getenv("CLICKHOUSE_PORT", "9009"))
    CH_DB       = os.getenv("CLICKHOUSE_DB", "default")
    CH_USER     = os.getenv("CLICKHOUSE_USER", "default")
    CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

    client = None  # Replace with your Client(...) call
    print("[dw] Connected to ClickHouse")

    # =========================================================================
    # Task 2: Create all 5 tables
    # =========================================================================
    print("\n--- Task 2: Create tables ---")
    # TODO: Create tables for users, addresses, orders, order_items, transports.
    #       Use ENGINE = MergeTree(). See datasets/er_diagram.md for schema.

    print("[dw] All tables ready")

    # =========================================================================
    # Task 3: Insert data from CSV into each table
    # =========================================================================
    print("\n--- Task 3: Insert data ---")
    # TODO: Read each CSV from datasets/raw/ and insert into its table.

    # =========================================================================
    # Task 4: Revenue by order status
    # =========================================================================
    print("\n--- Task 4: Revenue by order status ---")
    # TODO: Query total revenue and order count grouped by status.

    REVENUE_SQL = """
    -- TODO: Write your query here
    """

    # data, cols = client.execute(REVENUE_SQL, with_column_types=True)
    # print(pd.DataFrame(data, columns=[c[0] for c in cols]))

    # =========================================================================
    # Task 5: Top 5 users by total spend
    # =========================================================================
    print("\n--- Task 5: Top 5 users by total spend ---")
    # TODO: Join orders and users to find the top 5 spenders.

    TOP_USERS_SQL = """
    -- TODO: Write your query here
    """

    # data, cols = client.execute(TOP_USERS_SQL, with_column_types=True)
    # print(pd.DataFrame(data, columns=[c[0] for c in cols]))

    # --- Verification ---
    # Uncomment after completing all tasks:
    # for table, expected in [("users", 65), ("orders", 108), ("order_items", 198)]:
    #     count = client.execute(f"SELECT count() FROM {table}")[0][0]
    #     assert count == expected, f"{table}: expected {expected}, got {count}"
    # print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ ClickHouse connection failed: {e}")
    print("Make sure ClickHouse is running. Start it with:")
    print("  docker run -d --name de-clickhouse \\")
    print("    -p 8123:8123 -p 9009:9000 \\")
    print("    -v $(pwd)/datasets/raw:/var/lib/clickhouse/user_files \\")
    print("    clickhouse/clickhouse-server")