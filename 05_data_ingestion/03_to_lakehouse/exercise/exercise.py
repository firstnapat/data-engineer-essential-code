"""
Exercise: Data Ingestion to Lakehouse — Initial Load & Upsert with Delta Lake
Practice the concepts from load_to_lakehouse.py on the QuickMart orders
(datasets/new-raw/orders.csv).

You will build a pipeline that:
  1. Extracts + cleans orders.csv (order_id is the stable upsert key)
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

RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
DELTA = "/tmp/lakehouse/exercise_orders"


# ── Task 1: Extract + Clean ─────────────────────────────────────────────────
# Read orders.csv and clean it. Unlike sales.csv, orders already has a natural
# key — order_id — so we don't need to synthesise one (but we must make it
# unique first, because the raw file has duplicate order_ids).
#   1. pd.read_csv with parse_dates=["order_date"]
#   2. Drop exact duplicates, then keep one row per order_id (the upsert key)
#   3. Normalise status (lower + strip, "canceled" -> "cancelled")
#   4. Drop amount <= 0
#   5. order_date -> string so Delta stores a stable type
#   6. Print: [extract] <N> rows
def extract(source: str) -> pd.DataFrame:
    df_raw = pd.read_csv(source, parse_dates=["order_date"])
    df_raw = df_raw.drop_duplicates().drop_duplicates(subset=["order_id"])
    df_raw["status"] = df_raw["status"].str.strip().str.lower().replace({"canceled": "cancelled"})
    df_raw = df_raw[df_raw["amount"] > 0]
    df_raw["order_date"] = df_raw["order_date"].dt.strftime("%Y-%m-%d")
    df_raw = df_raw.reset_index(drop=True)
    print(f"[extract] {len(df_raw)} rows")
    return df_raw


# ── Task 2: Initial Load ────────────────────────────────────────────────────
def initial_load(df: pd.DataFrame, path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    write_deltalake(path, df, mode="overwrite")
    print(f"[load] initial {len(df)} rows -> Delta table")


# ── Task 3: Upsert (MERGE) ──────────────────────────────────────────────────
# Merge incoming rows into the Delta table, keyed on order_id. Re-running the
# same batch won't duplicate rows — that's the idempotent lakehouse pattern.
def upsert(df: pd.DataFrame, path: str) -> None:
    dt = DeltaTable(path)
    (
        dt.merge(
            source=df,
            predicate="target.order_id = source.order_id",
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute()
    )
    print(f"[upsert] merged {len(df)} rows")


# ── Task 4 & 5: Run the Pipeline & Verify ───────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract + Clean ---")
    df = extract(os.path.join(RAW, "orders.csv"))
    assert df is not None, "extract() should return a DataFrame"
    assert df["order_id"].is_unique, "order_id must be unique to act as the upsert key"
    initial_rows = len(df)
    print(f"✓ Extracted {initial_rows} unique orders\n")

    print("--- Task 2: Initial Load ---")
    initial_load(df, DELTA)
    loaded = DeltaTable(DELTA).to_pandas()
    assert len(loaded) == initial_rows, f"Expected {initial_rows} rows, got {len(loaded)}"
    print(f"✓ Delta table created with {len(loaded)} rows\n")

    print("--- Task 3: Upsert (1 update + 1 insert) ---")
    first_id = int(df["order_id"].iloc[0])
    new_id   = int(df["order_id"].max()) + 1

    # UPDATE an existing order's amount...
    updated = df.head(1).copy()
    updated["amount"] = 999999.0

    # ...and INSERT a brand-new order.
    inserted = df.tail(1).copy()
    inserted["order_id"] = new_id

    batch = pd.concat([updated, inserted], ignore_index=True)
    upsert(batch, DELTA)
    print()

    print("--- Task 5: Verify ---")
    final = DeltaTable(DELTA).to_pandas()
    expected_rows = initial_rows + 1  # one new row added, one updated in place
    print(f"Final row count: {len(final)} (expected {expected_rows})")
    assert len(final) == expected_rows, \
        f"Expected {expected_rows} rows (initial {initial_rows} + 1 new), got {len(final)}"

    row = final.loc[final["order_id"] == first_id]
    assert len(row) == 1, f"Should have exactly one row with order_id={first_id}"
    assert row["amount"].iloc[0] == 999999.0, \
        f"order_id={first_id} should have amount=999999, got {row['amount'].iloc[0]}"
    assert (final["order_id"] == new_id).sum() == 1, "The new order should have been inserted"

    print(f"✓ order_id={first_id} amount updated to 999999")
    print(f"✓ order_id={new_id} inserted")
    print(f"✓ Total rows: {len(final)} (initial {initial_rows} + 1 inserted)")
    print("\n✓ All tasks complete!")
