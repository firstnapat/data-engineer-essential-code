"""
Exercise: Data Warehouse — Load Data into ClickHouse
Practice the concepts from clickhouse_example.py (column-oriented OLAP).
Run: uv run 04_data_storage/03_data_warehouse/exercise/exercise.py

Setup (Docker — start ClickHouse first):
  docker run -d --name de-clickhouse \\
    -p 8123:8123 -p 9009:9000 \\
    -v $(pwd)/datasets/raw:/var/lib/clickhouse/user_files \\
    -e CLICKHOUSE_PASSWORD=clickhouse \\
    clickhouse/clickhouse-server

Configure .env:
  CLICKHOUSE_HOST=localhost
  CLICKHOUSE_PORT=8123
  CLICKHOUSE_DB=default
  CLICKHOUSE_USER=default
  CLICKHOUSE_PASSWORD=clickhouse

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
    # Task 2: Create tables for all 5 datasets
    # =========================================================================
    print("\n--- Task 2: Create tables ---")
    # TODO: Create tables for users, addresses, orders, order_items, transports.
    #       See datasets/er_diagram.md for the schema of each table.
    #       Use client.command(sql) for DDL.

    print("[dw] Tables ready")

    # =========================================================================
    # Task 3: Insert data from CSV files
    # =========================================================================
    print("\n--- Task 3: Insert data ---")
    # TODO: Load each dataset from datasets/raw/*.csv and insert into its table.
    #       Use client.insert(table, rows, column_names=[...])

    print("[dw] Data inserted")

    # =========================================================================
    # Task 4: Run analytics queries
    # =========================================================================
    print("\n--- Task 4: Analytics ---")
    # TODO: Write at least 2 analytical queries that JOIN across tables.
    #       Use client.query_df(sql) to return results as a DataFrame.
    #       Example ideas: top users by total spend, orders by status + region.

    # --- Verification ---
    # Uncomment after completing all tasks:
    # assert client.query("SELECT count() FROM users").result_rows[0][0] == 80
    # assert client.query("SELECT count() FROM orders").result_rows[0][0] == 108
    # print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ ClickHouse connection failed: {e}")
    print("Make sure ClickHouse is running. Start it with:")
    print("  docker run -d --name de-clickhouse \\")
    print("    -p 8123:8123 -p 9009:9000 \\")
    print("    -v $(pwd)/datasets/raw:/var/lib/clickhouse/user_files \\")
    print("    -e CLICKHOUSE_PASSWORD=clickhouse \\")
    print("    clickhouse/clickhouse-server")
