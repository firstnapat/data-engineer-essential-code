"""
Exercise: Data Ingestion to Data Lake — Partition by Region & Read with Pruning
Practice the concepts from load_to_lake.py.

You will build a pipeline that:
  1. Extracts data from sales.csv
  2. Lands it as partitioned Parquet files (one per region)
  3. Reads the lake back by discovering partition files
  4. Adds partition pruning to read only specific regions
  5. Verifies the Bangkok partition

Run: uv run 05_data_ingestion/02_to_data_lake/exercise/exercise.py
"""
import os
import glob
import shutil
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
LAKE = "/tmp/lake/exercise_sales"


# ── Task 1: Extract ─────────────────────────────────────────────────────────
# Write an extract() function that reads sales.csv into a DataFrame.
# - Use pd.read_csv with parse_dates=["date"]
# - Print the row count: [extract] <N> rows from sales.csv
# - Return the DataFrame
def extract(source: str) -> pd.DataFrame:
    # TODO: Read the CSV file with date parsing and return the DataFrame
    pass


# ── Task 2: Land Partitioned ────────────────────────────────────────────────
# Write a land_partitioned() function that partitions by REGION (not month).
# For each unique region value, create a folder and write a Parquet file:
#   LAKE/region=Bangkok/data.parquet
#   LAKE/region=Chiang Mai/data.parquet
#   etc.
#
# Steps:
#   1. Clean up: if root path exists, use shutil.rmtree(root) to remove it
#   2. Group the DataFrame by "region"
#   3. For each group, create the folder with os.makedirs(folder, exist_ok=True)
#   4. Write the group to data.parquet (index=False)
#   5. Print: [land] <N> rows -> region=<region>/data.parquet
def land_partitioned(df: pd.DataFrame, root: str) -> None:
    # TODO: Clean up existing path
    # TODO: Group by region and write one Parquet file per group
    pass


# ── Task 3: Read Lake ───────────────────────────────────────────────────────
# Write a read_lake() function that discovers all Parquet files and unions them.
#   1. Use glob.glob(os.path.join(root, "region=*", "*.parquet")) to find files
#   2. Sort the file list for deterministic order
#   3. Read each file with pd.read_parquet and union with pd.concat(ignore_index=True)
#   4. Print: [read] <N> partition file(s) -> <M> rows
#   5. Return the concatenated DataFrame
#
# ── Task 4: Partition Pruning ────────────────────────────────────────────────
# Add an optional `regions` parameter (list[str] | None = None) to read_lake().
# When regions is provided, filter the discovered files to only those whose
# path contains "region=<value>" for any value in the regions list.
#   Hint: files = [f for f in files if any(f"region={r}" in f for r in regions)]
def read_lake(root: str, regions: list[str] | None = None) -> pd.DataFrame:
    # TODO: Discover all partition files with glob
    # TODO: If regions is provided, filter files (partition pruning)
    # TODO: Read and concat all matching files
    # TODO: Print file count and row count, then return
    pass


# ── Task 5: Run the Pipeline & Verify ───────────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract ---")
    df = extract(os.path.join(DATASETS, "sales.csv"))
    assert df is not None, "extract() should return a DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"
    initial_rows = len(df)
    print(f"✓ Extracted {initial_rows} rows\n")

    print("--- Task 2: Land Partitioned by Region ---")
    land_partitioned(df, LAKE)
    # Verify partition folders were created
    partition_dirs = glob.glob(os.path.join(LAKE, "region=*"))
    assert len(partition_dirs) > 0, "Should have created partition directories"
    print(f"✓ Created {len(partition_dirs)} region partitions\n")

    print("--- Task 3: Read Entire Lake ---")
    everything = read_lake(LAKE)
    assert everything is not None, "read_lake() should return a DataFrame"
    assert len(everything) == initial_rows, (
        f"Expected {initial_rows} total rows, got {len(everything)}"
    )
    print(f"✓ Read back all {len(everything)} rows\n")

    # Show revenue by region from the lake
    print("Revenue by region (from lake):")
    print(everything.groupby("region")["revenue"].sum().sort_values(ascending=False))
    print()

    print("--- Task 4 & 5: Partition Pruning — Bangkok Only ---")
    bangkok = read_lake(LAKE, regions=["Bangkok"])
    assert bangkok is not None, "read_lake() with region filter should return a DataFrame"
    assert len(bangkok) < initial_rows, "Filtered result should have fewer rows than full dataset"
    # Verify only Bangkok data
    if "region" in bangkok.columns:
        assert (bangkok["region"] == "Bangkok").all(), "Should only contain Bangkok rows"
    print(f"✓ Bangkok partition: {len(bangkok)} rows (pruned from {initial_rows} total)")
    print("\n✓ All tasks complete!")
