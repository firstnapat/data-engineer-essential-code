"""
Exercise: Data Ingestion to Lakehouse — Initial Load & Upsert with Delta Lake
Practice the concepts from load_to_lakehouse.py.

You will build a pipeline that:
  1. Extracts data from sales.csv with a stable sale_id key
  2. Does an initial overwrite load into a Delta table
  3. Implements an idempotent upsert (MERGE) function
  4. Tests the upsert with an updated row and a new row
  5. Verifies the final table state

Run: uv run 05_data_ingestion/03_to_lakehouse/exercise/exercise.py
"""
import os
import shutil
import pandas as pd
from deltalake import DeltaTable, write_deltalake

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
DELTA = "/tmp/lakehouse/exercise_sales"


# ── Task 1: Extract ─────────────────────────────────────────────────────────
# Write an extract() function that reads sales.csv into a DataFrame.
# - Use pd.read_csv with parse_dates=["date"]
# - Add a sale_id column at position 0: df.insert(0, "sale_id", df.index.astype("int64"))
#   This gives each row a stable integer key needed for upserts.
# - Print: [extract] <N> rows
# - Return the DataFrame
def extract(source: str) -> pd.DataFrame:
    # TODO: Read CSV, add sale_id column, print count, return
    pass


# ── Task 2: Initial Load ────────────────────────────────────────────────────
# Write an initial_load() function that writes the DataFrame to a Delta table.
# - If the path already exists, remove it with shutil.rmtree(path)
# - Use write_deltalake(path, df, mode="overwrite")
# - Print: [load] initial <N> rows -> Delta table
def initial_load(df: pd.DataFrame, path: str) -> None:
    # TODO: Clean up existing path, then write Delta table
    pass


# ── Task 3: Upsert (MERGE) ──────────────────────────────────────────────────
# Write an upsert() function that merges incoming rows into the Delta table.
# This is the key lakehouse feature — re-running the same batch won't duplicate rows.
#
# Steps:
#   1. Open the existing table: DeltaTable(path)
#   2. Call .merge() with:
#        - df as the source DataFrame
#        - predicate="target.sale_id = source.sale_id"
#        - source_alias="source", target_alias="target"
#   3. Chain .when_matched_update_all()   — UPDATE existing rows
#   4. Chain .when_not_matched_insert_all() — INSERT new rows
#   5. Chain .execute()
#   6. Print: [upsert] merged <N> rows
def upsert(df: pd.DataFrame, path: str) -> None:
    # TODO: Implement the MERGE operation using DeltaTable API
    pass


# ── Task 4 & 5: Run the Pipeline & Verify ───────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract ---")
    df = extract(os.path.join(DATASETS, "sales.csv"))
    assert df is not None, "extract() should return a DataFrame"
    assert "sale_id" in df.columns, "DataFrame should have a sale_id column"
    initial_rows = len(df)
    print(f"✓ Extracted {initial_rows} rows with sale_id\n")

    print("--- Task 2: Initial Load ---")
    initial_load(df, DELTA)
    # Verify the Delta table was created
    dt = DeltaTable(DELTA)
    loaded = dt.to_pandas()
    assert len(loaded) == initial_rows, f"Expected {initial_rows} rows, got {len(loaded)}"
    print(f"✓ Delta table created with {len(loaded)} rows\n")

    print("--- Task 3: Upsert ---")
    # Build a small batch with:
    #   - One UPDATED row: change revenue of sale_id=0 to 999999
    #   - One NEW row: sale_id = max + 1 (brand new record)
    # TODO: Create 'updated' — copy df.head(1) and set revenue = 999999
    updated = df.head(1).copy()
    # TODO: Set the revenue to 999999
    # updated["revenue"] = ???

    # TODO: Create 'inserted' — copy df.tail(1) and set sale_id = max + 1
    inserted = df.tail(1).copy()
    # TODO: Set the sale_id to df["sale_id"].max() + 1
    # inserted["sale_id"] = ???

    # TODO: Concat updated and inserted, then call upsert()
    # batch = pd.concat([updated, inserted], ignore_index=True)
    # upsert(batch, DELTA)
    print()

    print("--- Task 5: Verify ---")
    final = DeltaTable(DELTA).to_pandas()
    expected_rows = initial_rows + 1  # one new row added
    print(f"Final row count: {len(final)} (expected {expected_rows})")
    assert len(final) == expected_rows, (
        f"Expected {expected_rows} rows (initial {initial_rows} + 1 new), got {len(final)}"
    )

    # Check that sale_id=0 now has revenue=999999
    row0 = final.loc[final["sale_id"] == 0]
    assert len(row0) == 1, "Should have exactly one row with sale_id=0"
    actual_revenue = row0["revenue"].iloc[0]
    assert actual_revenue == 999999, (
        f"sale_id=0 should have revenue=999999, got {actual_revenue}"
    )
    print(f"✓ sale_id=0 revenue updated to {actual_revenue}")
    print(f"✓ Total rows: {len(final)} (initial {initial_rows} + 1 inserted)")
    print("\n✓ All tasks complete!")
