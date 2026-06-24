"""
Data Warehouse storage using ClickHouse.
ClickHouse is optimized for analytical queries (OLAP) — column-oriented,
compressed, extremely fast aggregations.

Setup (Docker):
  docker run -d --name clickhouse -p 9000:9000 -p 8123:8123 clickhouse/clickhouse-server

Configure .env with CLICKHOUSE_* variables from .env.example.
"""
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CH_HOST     = os.getenv("CLICKHOUSE_HOST", "localhost")
CH_PORT     = int(os.getenv("CLICKHOUSE_PORT", "9000"))
CH_DB       = os.getenv("CLICKHOUSE_DB", "default")
CH_USER     = os.getenv("CLICKHOUSE_USER", "default")
CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS products (
    product_id  UInt32,
    name        String,
    category    LowCardinality(String),
    brand       LowCardinality(String),
    unit_price  Float32,
    stock_qty   UInt32
)
ENGINE = MergeTree()
ORDER BY (category, brand, product_id)
"""

ANALYTICS_QUERIES = {
    "Products by Category": """
        SELECT category,
               count()            AS total_products,
               avg(unit_price)    AS avg_price,
               sum(stock_qty)     AS total_stock
        FROM products
        GROUP BY category
        ORDER BY total_products DESC
    """,
    "Top Brands by Stock Value": """
        SELECT brand,
               sum(unit_price * stock_qty) AS stock_value,
               count()                     AS num_products
        FROM products
        GROUP BY brand
        ORDER BY stock_value DESC
        LIMIT 5
    """,
    "Price Range by Category": """
        SELECT category,
               min(unit_price) AS min_price,
               max(unit_price) AS max_price,
               avg(unit_price) AS avg_price
        FROM products
        GROUP BY category
        ORDER BY avg_price DESC
    """,
}


def get_client():
    from clickhouse_driver import Client
    return Client(
        host=CH_HOST, port=CH_PORT, database=CH_DB,
        user=CH_USER, password=CH_PASSWORD,
    )


def setup_table(client) -> None:
    client.execute(CREATE_TABLE_SQL)
    client.execute("TRUNCATE TABLE IF EXISTS products")
    print("[dw] Table 'products' ready")


def insert_dataframe(client, df: pd.DataFrame) -> None:
    records = df.to_dict("records")
    client.execute(
        "INSERT INTO products (product_id, name, category, brand, unit_price, stock_qty) VALUES",
        [
            (int(r["product_id"]), r["name"], r["category"],
             r["brand"], float(r["unit_price"]), int(r["stock_qty"]))
            for r in records
        ],
    )
    print(f"[dw] Inserted {len(records)} rows")


if __name__ == "__main__":
    try:
        client = get_client()
        df = pd.read_csv(os.path.join(DATASETS, "raw/products_raw.csv"))

        setup_table(client)
        insert_dataframe(client, df)

        for label, sql in ANALYTICS_QUERIES.items():
            print(f"\n--- {label} ---")
            rows = client.execute(sql, with_column_types=True)
            data, cols = rows
            col_names = [c[0] for c in cols]
            result = pd.DataFrame(data, columns=col_names)
            print(result)

    except Exception as e:
        print(f"ClickHouse connection failed: {e}")
        print("Start ClickHouse and check your .env settings.")
