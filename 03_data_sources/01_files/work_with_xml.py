"""
Work with an XML data source.   read -> inspect -> clean

pandas.read_xml selects records with an xpath. Requires lxml.
"""
import os
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def read(path: str) -> pd.DataFrame:
    return pd.read_xml(path, xpath=".//product")


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}, columns={list(df.columns)}")
    print(df.head())
    print("\ndtypes:")
    print(df.dtypes)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["unit_price"] = df["unit_price"].astype(int)
    df["stock"] = df["stock"].astype(int)
    df["name"] = df["name"].str.strip()
    return df


if __name__ == "__main__":
    df = read(os.path.join(DATASETS, "products.xml"))
    inspect(df)
    cleaned = clean(df)
    print("\n[clean] numeric dtypes:", dict(cleaned[["unit_price", "stock"]].dtypes.astype(str)))
