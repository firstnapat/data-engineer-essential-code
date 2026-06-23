"""
Work with a CSV data source.   read -> inspect -> clean
"""
import os
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def read(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}")
    print(df.head())
    print("\ndtypes:")
    print(df.dtypes)
    print("\nmissing per column:")
    print(df.isnull().sum())


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])      # text -> datetime
    df["product"] = df["product"].str.strip()
    df["region"] = df["region"].str.strip()
    df = df.drop_duplicates()
    return df


if __name__ == "__main__":
    df = read(os.path.join(DATASETS, "sales.csv"))
    inspect(df)
    cleaned = clean(df)
    print(f"\n[clean] date dtype now {cleaned['date'].dtype}, {len(cleaned)} rows after dedup")
