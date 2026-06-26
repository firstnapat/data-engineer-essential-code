"""
Exercise: Data Ingestion to Data Lake — Partition by Status & Read with Pruning
Practice the concepts from load_to_lake.py on the QuickMart orders
(datasets/new-raw/orders.csv).

You will build a pipeline that:
  1. Extracts + cleans orders.csv (the raw file is dirty)
  2. Lands it as partitioned Parquet files (one per order status)
  3. Reads the lake back by discovering partition files
  4. Adds partition pruning to read only specific statuses
  5. Verifies the 'completed' partition

Run: uv run 05_data_ingestion/02_to_data_lake/exercise/exercise.py
"""
import os
import glob
import shutil
import pandas as pd

RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
LAKE = "/tmp/lake/exercise_orders"


# ── Task 1: Extract + Clean ─────────────────────────────────────────────────
# Read orders.csv and clean it (the raw file has duplicates, mixed-case status,
# and amount <= 0 rows):
#   1. pd.read_csv with parse_dates=["order_date"]
#   2. Drop exact duplicate rows, then keep one row per order_id
#   3. Normalise status: lower-case + strip, and map "canceled" -> "cancelled"
#   4. Drop rows where amount <= 0
#   5. Print: [extract] <N> clean rows from orders.csv
def extract(source: str) -> pd.DataFrame:
    df_raw = pd.read_csv(source, parse_dates=["order_date"])
    df_raw = df_raw.drop_duplicates().drop_duplicates(subset=["order_id"])
    df_raw["status"] = df_raw["status"].str.strip().str.lower().replace({"canceled": "cancelled"})
    df_raw = df_raw[df_raw["amount"] > 0]
    print(f"[extract] {len(df_raw)} clean rows from orders.csv")
    return df_raw


# ── Task 2: Land Partitioned ────────────────────────────────────────────────
# Partition by STATUS. For each unique status value, create a folder and write
# a Parquet file:
#   LAKE/status=completed/data.parquet
#   LAKE/status=processing/data.parquet
#   LAKE/status=cancelled/data.parquet
def land_partitioned(df: pd.DataFrame, root: str) -> None:
    if os.path.exists(root):
        shutil.rmtree(root)

    for status, group in df.groupby("status"):
        folder = os.path.join(root, f"status={status}")
        os.makedirs(folder, exist_ok=True)
        group.to_parquet(os.path.join(folder, "data.parquet"), index=False)
        print(f"[land] {len(group)} rows -> status={status}/data.parquet")


# ── Task 3 + 4: Read Lake with optional Partition Pruning ───────────────────
# Discover all Parquet files and union them. When `statuses` is provided, only
# read the matching partitions (pruning) instead of scanning the whole lake.
def read_lake(root: str, statuses: list[str] | None = None) -> pd.DataFrame:
    files = glob.glob(os.path.join(root, "status=*", "*.parquet"))
    files.sort()

    if statuses is not None:
        files = [f for f in files if any(f"status={s}" in f for s in statuses)]

    dfs = [pd.read_parquet(f) for f in files]
    df_lake = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    print(f"[read] {len(files)} partition file(s) -> {len(df_lake)} rows")
    return df_lake


# ── Task 5: Run the Pipeline & Verify ───────────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract + Clean ---")
    df = extract(os.path.join(RAW, "orders.csv"))
    assert df is not None, "extract() should return a DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"
    assert set(df["status"].unique()) == {"completed", "processing", "cancelled"}, \
        f"Unexpected statuses after cleaning: {set(df['status'].unique())}"
    clean_rows = len(df)
    print(f"✓ Extracted {clean_rows} clean rows\n")

    print("--- Task 2: Land Partitioned by Status ---")
    land_partitioned(df, LAKE)
    partition_dirs = glob.glob(os.path.join(LAKE, "status=*"))
    assert len(partition_dirs) == 3, f"Expected 3 status partitions, got {len(partition_dirs)}"
    print(f"✓ Created {len(partition_dirs)} status partitions\n")

    print("--- Task 3: Read Entire Lake ---")
    everything = read_lake(LAKE)
    assert len(everything) == clean_rows, f"Expected {clean_rows} total rows, got {len(everything)}"
    print(f"✓ Read back all {len(everything)} rows\n")

    print("Revenue by status (from lake):")
    print(everything.groupby("status")["amount"].sum().sort_values(ascending=False))
    print()

    print("--- Task 4 & 5: Partition Pruning — Completed Only ---")
    completed = read_lake(LAKE, statuses=["completed"])
    assert len(completed) < clean_rows, "Filtered result should have fewer rows than full dataset"
    assert (completed["status"] == "completed").all(), "Should only contain completed rows"
    print(f"✓ Completed partition: {len(completed)} rows (pruned from {clean_rows} total)")
    print("\n✓ All tasks complete!")
