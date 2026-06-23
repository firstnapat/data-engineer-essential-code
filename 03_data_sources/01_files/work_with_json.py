"""
Work with a JSON data source (nested).   read -> inspect -> clean

json_normalize flattens the nested product list into a flat table.
"""
import os
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def read(path: str) -> pd.DataFrame:
    raw = pd.read_json(path)
    return pd.json_normalize(raw["products"])


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}, columns={list(df.columns)}")
    print(df.head())
    print("\ndtypes:")
    print(df.dtypes)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["name"] = df["name"].str.strip()
    df["category"] = df["category"].str.strip().str.title()
    df["unit_price"] = df["unit_price"].astype(int)
    return df


if __name__ == "__main__":
    df = read(os.path.join(DATASETS, "products.json"))
    inspect(df)
    cleaned = clean(df)
    print("\n[clean] sample:")
    print(cleaned[["id", "name", "category", "unit_price"]].head())
