"""
Ingest an XML catalog into a DataFrame.

Two common approaches:
  1. pandas.read_xml  — quick, when the structure is a flat list of records
  2. xml.etree        — full control for nested / attribute-heavy XML
Pattern: extract -> transform -> validate
Requires: lxml (used by pandas.read_xml)
"""
import os
import xml.etree.ElementTree as ET
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def extract_with_pandas(filepath: str) -> pd.DataFrame:
    """Quick path: each <product> element becomes a row."""
    df = pd.read_xml(filepath, xpath=".//product")
    print(f"[pandas] {len(df)} products, columns={list(df.columns)}")
    return df


def extract_with_etree(filepath: str) -> pd.DataFrame:
    """Manual path: also captures root attributes (store, last_updated)."""
    root = ET.parse(filepath).getroot()
    store = root.get("store")
    records = [{child.tag: child.text for child in product}
               for product in root.findall("product")]
    df = pd.DataFrame(records)
    df["store"] = store
    print(f"[etree] {len(df)} products from store '{store}'")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["unit_price"] = df["unit_price"].astype(int)
    df["stock"] = df["stock"].astype(int)
    return df


def validate(df: pd.DataFrame) -> None:
    assert df["id"].is_unique, "Product IDs must be unique"
    assert (df["unit_price"] > 0).all(), "unit_price must be positive"
    print("[validate] OK")


if __name__ == "__main__":
    src = os.path.join(DATASETS, "products.xml")

    df = transform(extract_with_pandas(src))
    validate(df)
    print("\n--- Ingested Products (from XML) ---")
    print(df[["id", "name", "category", "unit_price", "stock"]].head())

    print("\n--- etree approach (keeps root attributes) ---")
    df2 = extract_with_etree(src)
    print(df2[["id", "name", "store"]].head(3))
