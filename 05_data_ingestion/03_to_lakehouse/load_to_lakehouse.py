"""
Ingestion pipeline: a data source -> data lakehouse (Delta Lake).

A lakehouse = lake storage (files) + warehouse features: ACID transactions,
schema enforcement, and upserts via MERGE. We do an initial load, then an
**idempotent** re-ingest that UPDATES existing rows and INSERTS new ones
instead of creating duplicates. No external service — Delta tables are files.
"""
import os
import shutil
import pandas as pd
from deltalake import DeltaTable, write_deltalake

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
DELTA = "/tmp/lakehouse/sales"


def extract(source: str) -> pd.DataFrame:
    df = pd.read_csv(source, parse_dates=["date"])
    df.insert(0, "sale_id", df.index.astype("int64"))   # stable key for upserts
    print(f"[extract] {len(df)} rows")
    return df


def initial_load(df: pd.DataFrame, path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    write_deltalake(path, df, mode="overwrite")
    print(f"[load] initial {len(df)} rows -> Delta table")


def upsert(df: pd.DataFrame, path: str) -> None:
    """MERGE on sale_id — re-running the same batch will not duplicate rows."""
    (
        DeltaTable(path)
        .merge(df, predicate="target.sale_id = source.sale_id",
               source_alias="source", target_alias="target")
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute()
    )
    print(f"[upsert] merged {len(df)} rows (schema enforced by Delta)")


if __name__ == "__main__":
    df = extract(os.path.join(DATASETS, "sales.csv"))
    initial_load(df, DELTA)

    # re-ingest: one UPDATE (existing sale_id) + one INSERT (new sale_id)
    updated = df.head(1).copy()
    updated["revenue"] = 999_999                       # correction to sale_id 0
    inserted = df.tail(1).copy()
    inserted["sale_id"] = int(df["sale_id"].max()) + 1  # brand-new id
    upsert(pd.concat([updated, inserted], ignore_index=True), DELTA)

    final = DeltaTable(DELTA).to_pandas()
    print(f"\n[verify] rows: {len(df)} initial + 1 inserted = {len(final)}")
    print(final.loc[final["sale_id"] == 0, ["sale_id", "product", "revenue"]])
