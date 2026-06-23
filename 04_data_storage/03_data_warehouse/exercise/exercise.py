"""
Exercise: Data Warehouse — Products Analytics with ClickHouse
Practice the concepts from clickhouse_example.py (column-oriented OLAP).
Run: uv run 04_data_storage/03_data_warehouse/exercise/exercise.py

Setup (Docker — start ClickHouse first):
  docker run -d --name clickhouse \\
    -p 9000:9000 -p 8123:8123 \\
    clickhouse/clickhouse-server

Configure .env with CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_DB,
CLICKHOUSE_USER, CLICKHOUSE_PASSWORD.
"""
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

try:
    # =========================================================================
    # Task 1: Connect to ClickHouse
    # =========================================================================
    print("--- Task 1: Connect to ClickHouse ---")
    # TODO: Import Client from clickhouse_driver and create a connection.
    #       Read settings from env vars with defaults:
    #         CH_HOST     = os.getenv("CLICKHOUSE_HOST", "localhost")
    #         CH_PORT     = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    #         CH_DB       = os.getenv("CLICKHOUSE_DB", "default")
    #         CH_USER     = os.getenv("CLICKHOUSE_USER", "default")
    #         CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
    #       Then create: client = Client(host=CH_HOST, port=CH_PORT,
    #                                    database=CH_DB, user=CH_USER,
    #                                    password=CH_PASSWORD)
    from clickhouse_driver import Client

    CH_HOST     = os.getenv("CLICKHOUSE_HOST", "localhost")
    CH_PORT     = int(os.getenv("CLICKHOUSE_PORT", "9000"))
    CH_DB       = os.getenv("CLICKHOUSE_DB", "default")
    CH_USER     = os.getenv("CLICKHOUSE_USER", "default")
    CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

    client = Client(host=CH_HOST, port=CH_PORT,
                                 database=CH_DB, user=CH_USER,
                                 password=CH_PASSWORD)

    print("[dw] Connected to ClickHouse")

    # =========================================================================
    # Task 2: Create the 'products' table
    # =========================================================================
    print("\n--- Task 2: Create products table ---")
    # TODO: Write a CREATE TABLE IF NOT EXISTS statement for 'products' with:
    #         id          String
    #         name        String
    #         category    LowCardinality(String)
    #         unit_price  Float32
    #         stock       UInt32
    #         supplier    String
    #       ENGINE = MergeTree()
    #       ORDER BY (category, id)
    #
    #       Execute with: client.execute(CREATE_PRODUCTS_SQL)
    #       Then truncate: client.execute("TRUNCATE TABLE IF EXISTS products")

    CREATE_PRODUCTS_SQL = """
    CREATE TABLE IF NOT EXISTS products (
        id String,
        name String,
        category LowCardinality(String),
        unit_price Float32,
        stock UInt32,
        supplier String
    ) ENGINE = MergeTree()
    ORDER BY (category, id)
    """

    client.execute(CREATE_PRODUCTS_SQL)
    client.execute("TRUNCATE TABLE IF EXISTS products")
    print("[dw] Table 'products' ready")

    # =========================================================================
    # Task 3: Read products.json and insert all rows
    # =========================================================================
    print("\n--- Task 3: Insert product data ---")
    data = json.load(open(os.path.join(DATASETS, "products.json")))
    df = pd.json_normalize(data, record_path="products")

    records = df.to_dict("records")
    client.execute(
        "INSERT INTO products (id, name, category, unit_price, stock, supplier) VALUES",
        [(r["id"], r["name"], r["category"],
          float(r["unit_price"]), int(r["stock"]), r["supplier"])
         for r in records]
    )

    print(f"[dw] Inserted {len(records)} products")

    # =========================================================================
    # Task 4: Analytics query — avg price and total stock by category
    # =========================================================================
    print("\n--- Task 4: Average price & total stock by category ---")
    ANALYTICS_SQL = """
    SELECT category, avg(unit_price) AS avg_price, sum(stock) AS total_stock
    FROM products
    GROUP BY category
    ORDER BY avg_price DESC
    """

    data, cols = client.execute(ANALYTICS_SQL, with_column_types=True)
    col_names = [c[0] for c in cols]
    result = pd.DataFrame(data, columns=col_names)
    print(result)

    # =========================================================================
    # Task 5: Low stock alert — products with stock < 50
    # =========================================================================
    print("\n--- Task 5: Low stock alert (stock < 50) ---")
    LOW_STOCK_SQL = """
    SELECT id, name, category, stock
    FROM products
    WHERE stock < 50
    ORDER BY stock ASC
    """

    data, cols = client.execute(LOW_STOCK_SQL, with_column_types=True)
    col_names = [c[0] for c in cols]
    low_stock_df = pd.DataFrame(data, columns=col_names)
    print(low_stock_df)

    # --- Verification ---
    row_count = client.execute("SELECT count() FROM products")[0][0]
    assert row_count == 13, f"Expected 13 products, got {row_count}"
    cat_count = client.execute("SELECT uniq(category) FROM products")[0][0]
    assert cat_count == 4, f"Expected 4 categories, got {cat_count}"
    print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ ClickHouse connection failed: {e}")
    print("Make sure ClickHouse is running. Start it with:")
    print("  docker run -d --name clickhouse \\")
    print("    -p 9000:9000 -p 8123:8123 \\")
    print("    clickhouse/clickhouse-server")
