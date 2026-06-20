"""
Ingest JSON files — handles both flat and nested structures.
"""
import json
import pandas as pd
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[load] Loaded JSON from {os.path.basename(filepath)}")
    return data


def normalize_products(data: dict) -> pd.DataFrame:
    """Flatten nested product catalog into a flat DataFrame."""
    products = data.get("products", [])
    df = pd.json_normalize(products)   # handles nested keys automatically
    df["store"] = data.get("store")
    df["last_updated"] = pd.to_datetime(data.get("last_updated"))
    print(f"[normalize] {len(df)} products, columns: {list(df.columns)}")
    return df


def validate_products(df: pd.DataFrame) -> None:
    assert df["id"].is_unique, "Product IDs must be unique"
    assert df["unit_price"].gt(0).all(), "unit_price must be positive"
    assert df["stock"].ge(0).all(), "stock cannot be negative"
    print("[validate] OK")


def ingest_products_json(source: str) -> pd.DataFrame:
    data = load_json(source)
    df = normalize_products(data)
    validate_products(df)
    return df


if __name__ == "__main__":
    src = os.path.join(DATASETS, "products.json")
    df = ingest_products_json(src)

    print("\n--- Ingested Products ---")
    print(df[["id", "name", "category", "unit_price", "stock"]])

    out = "/tmp/products_ingested.parquet"
    df.to_parquet(out, index=False)
    print(f"\nWritten to {out}")
