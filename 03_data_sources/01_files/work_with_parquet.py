"""
Work with a PARQUET data source (columnar, typed).   read -> inspect -> clean

Parquet stores dtypes with the data, so types survive and little cleaning is
needed. We create a small sample from the CSV first (we don't ship binaries).
Requires: pyarrow
"""
import os
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
SAMPLE = "/tmp/sales_sample.parquet"


def _prepare_sample() -> None:
    pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"]).to_parquet(SAMPLE, index=False)


def read(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}")
    print(df.head())
    print("\ndtypes (note: types came back from Parquet, e.g. datetime64):")
    print(df.dtypes)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # types are already correct, so cleaning is light — just trim text
    df = df.copy()
    df["product"] = df["product"].str.strip()
    return df


if __name__ == "__main__":
    _prepare_sample()
    df = read(SAMPLE)
    inspect(df)
    clean(df)
    print(f"\n[done] read {len(df)} rows from Parquet")
