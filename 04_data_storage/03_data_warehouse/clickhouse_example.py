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
CREATE TABLE IF NOT EXISTS sales (
    sale_date   Date,
    product     String,
    category    LowCardinality(String),
    quantity    UInt32,
    unit_price  Float32,
    revenue     Float32,
    region      LowCardinality(String)
)
ENGINE = MergeTree()
ORDER BY (sale_date, category, region)
"""

ANALYTICS_QUERIES = {
    "Revenue by Category": """
        SELECT category,
               sum(revenue)     AS total_revenue,
               count()          AS transactions,
               avg(revenue)     AS avg_revenue
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """,
    "Monthly Trend": """
        SELECT toYYYYMM(sale_date)  AS month,
               sum(revenue)         AS total_revenue
        FROM sales
        GROUP BY month
        ORDER BY month
    """,
    "Top 5 Products": """
        SELECT product, sum(revenue) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 5
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
    client.execute("TRUNCATE TABLE IF EXISTS sales")
    print("[dw] Table 'sales' ready")


def insert_dataframe(client, df: pd.DataFrame) -> None:
    records = df.to_dict("records")
    client.execute(
        "INSERT INTO sales (sale_date, product, category, quantity, unit_price, revenue, region) VALUES",
        [
            (r["date"], r["product"], r["category"],
             int(r["quantity"]), float(r["unit_price"]), float(r["revenue"]), r["region"])
            for r in records
        ],
    )
    print(f"[dw] Inserted {len(records)} rows")


if __name__ == "__main__":
    try:
        client = get_client()
        df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])

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
