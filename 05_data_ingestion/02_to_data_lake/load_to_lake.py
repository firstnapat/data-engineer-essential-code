"""
Ingestion pipeline: a data source -> data lake (schema-on-read).

A data lake lands raw/curated files as-is, partitioned so queries scan less.
Unlike a warehouse, there is **no schema up front** — we apply structure when
we READ. Here the local filesystem stands in for S3; the S3/RustFS version
lives in 04_data_storage/02_data_lake.
"""
import os
import glob
import shutil
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
LAKE = "/tmp/lake/sales"


def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, parse_dates=["date"])
    print(f"[extract] {len(df)} rows from {os.path.basename(source)}")
    return df


def land_partitioned(df: pd.DataFrame, root: str) -> None:
    """Write one parquet file per month: sales/month=YYYY-MM/data.parquet"""
    if os.path.exists(root):
        shutil.rmtree(root)
    df = df.copy()
    df["month"] = df["date"].dt.strftime("%Y-%m")
    for month, part in df.groupby("month"):
        folder = os.path.join(root, f"month={month}")
        os.makedirs(folder, exist_ok=True)
        part.drop(columns="month").to_parquet(os.path.join(folder, "data.parquet"), index=False)
        print(f"[land] {len(part):>2} rows -> month={month}/data.parquet")


def read_lake(root: str, months: list[str] | None = None) -> pd.DataFrame:
    """schema-on-read: discover partition files (optionally prune) and union them."""
    pattern = "month=*" if months is None else "month=(" + "|".join(months) + ")"
    files = sorted(glob.glob(os.path.join(root, "month=*", "*.parquet")))
    if months:
        files = [f for f in files if any(f"month={m}" in f for m in months)]
    df = pd.concat((pd.read_parquet(f) for f in files), ignore_index=True)
    print(f"[read] {len(files)} partition file(s) -> {len(df)} rows")
    return df


if __name__ == "__main__":
    df = extract(os.path.join(DATASETS, "sales.csv"))
    land_partitioned(df, LAKE)

    print("\n--- Query whole lake (schema applied at read time) ---")
    everything = read_lake(LAKE)
    print(everything.groupby("region")["revenue"].sum().sort_values(ascending=False))

    print("\n--- Partition pruning: read only 2024-01 ---")
    jan = read_lake(LAKE, months=["2024-01"])
    print(f"January rows: {len(jan)}")
