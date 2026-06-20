"""
Data Lakehouse using Delta Lake format (via deltalake + DuckDB).

Lakehouse = Data Lake storage (files) + Data Warehouse features:
  - ACID transactions
  - Schema enforcement
  - Time travel (read older versions)
  - Efficient upserts (MERGE)

No external service needed — Delta tables are just files on disk (or S3).
"""
import os
import pandas as pd
import duckdb
from deltalake import DeltaTable, write_deltalake

DATASETS  = os.path.join(os.path.dirname(__file__), "../../datasets")
DELTA_PATH = "/tmp/delta/sales"


def write_initial_load(df: pd.DataFrame, path: str) -> None:
    write_deltalake(path, df, mode="overwrite")
    print(f"[lakehouse] Written {len(df)} rows to Delta table at {path}")


def append_records(new_df: pd.DataFrame, path: str) -> None:
    write_deltalake(path, new_df, mode="append")
    print(f"[lakehouse] Appended {len(new_df)} rows")


def read_table(path: str) -> pd.DataFrame:
    dt = DeltaTable(path)
    return dt.to_pandas()


def show_history(path: str) -> None:
    dt = DeltaTable(path)
    print("[lakehouse] Transaction history:")
    for entry in dt.history()[:5]:
        print(f"  version={entry['version']}, op={entry['operation']}, ts={entry['timestamp']}")


def time_travel(path: str, version: int) -> pd.DataFrame:
    dt = DeltaTable(path, version=version)
    df = dt.to_pandas()
    print(f"[lakehouse] Read version {version}: {len(df)} rows")
    return df


def query_with_duckdb(path: str, sql: str) -> pd.DataFrame:
    """DuckDB can query Delta tables directly without loading into memory."""
    conn = duckdb.connect()
    conn.execute("INSTALL delta; LOAD delta;")
    result = conn.execute(sql.format(path=path)).df()
    return result


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])

    print("=== Write Initial Load ===")
    write_initial_load(df, DELTA_PATH)

    print("\n=== Append New Records ===")
    new_data = pd.DataFrame([{
        "date": pd.Timestamp("2024-04-01"), "product": "Laptop Pro",
        "category": "Electronics", "quantity": 2, "unit_price": 35000.0,
        "revenue": 70000.0, "region": "Bangkok",
    }])
    append_records(new_data, DELTA_PATH)

    print("\n=== Read Current Table ===")
    current = read_table(DELTA_PATH)
    print(f"Total rows: {len(current)}")
    print(current.tail(3))

    print("\n=== Transaction History ===")
    show_history(DELTA_PATH)

    print("\n=== Time Travel: Read Version 0 (initial load) ===")
    v0 = time_travel(DELTA_PATH, version=0)
    print(f"Version 0 rows: {len(v0)}")

    print("\n=== Query with DuckDB (SQL on Delta files) ===")
    try:
        result = query_with_duckdb(DELTA_PATH, """
            SELECT category, SUM(revenue) AS total_revenue
            FROM delta_scan('{path}')
            GROUP BY category
            ORDER BY total_revenue DESC
        """)
        print(result)
    except Exception as e:
        print(f"DuckDB Delta extension not available: {e}")
        # Fallback: query pandas DataFrame
        result = current.groupby("category")["revenue"].sum().sort_values(ascending=False)
        print(result)
