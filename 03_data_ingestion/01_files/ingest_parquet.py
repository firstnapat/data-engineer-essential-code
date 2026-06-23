"""
Ingest Parquet — the columnar, compressed format preferred for analytics/DE.

Parquet stores the schema alongside the data, so dtypes survive a round-trip,
and you can read just the columns you need.
Pattern: (build a sample) -> read -> inspect
Requires: pyarrow
"""
import os
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def write_parquet(df: pd.DataFrame, path: str) -> None:
    df.to_parquet(path, index=False, compression="snappy")
    print(f"[write] {len(df)} rows -> {path} ({os.path.getsize(path):,} bytes)")


def read_parquet(path: str, columns: list[str] | None = None) -> pd.DataFrame:
    # column pruning: read only the columns you need (a Parquet superpower)
    df = pd.read_parquet(path, columns=columns)
    print(f"[read] {df.shape} from {os.path.basename(path)} (columns={columns or 'all'})")
    return df


if __name__ == "__main__":
    # build a sample parquet from the CSV so the demo is self-contained
    src = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
    out = "/tmp/sales.parquet"
    write_parquet(src, out)

    full = read_parquet(out)
    print("\n--- dtypes preserved (note datetime64, not object) ---")
    print(full.dtypes)

    print("\n--- column pruning: read only date + revenue ---")
    slim = read_parquet(out, columns=["date", "revenue"])
    print(slim.head())
