"""
Ingest CSV files into a structured format with validation.
Pattern: extract -> validate schema -> transform -> load
"""
import pandas as pd
import os
from datetime import datetime

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

EXPECTED_SCHEMA = {
    "date":       "object",
    "product":    "object",
    "category":   "object",
    "quantity":   "int64",
    "unit_price": "int64",
    "revenue":    "int64",
    "region":     "object",
}

VALID_CATEGORIES = {"Electronics", "Furniture", "Clothing", "Accessories"}


def extract(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["date"])
    print(f"[extract] Loaded {len(df)} rows from {os.path.basename(filepath)}")
    return df


def validate(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    errors = []

    missing = df.isnull().sum()
    for col, count in missing[missing > 0].items():
        errors.append(f"Column '{col}' has {count} missing values")

    invalid_cats = set(df["category"].unique()) - VALID_CATEGORIES
    if invalid_cats:
        errors.append(f"Unknown categories: {invalid_cats}")

    mismatch = df[abs(df["quantity"] * df["unit_price"] - df["revenue"]) > 0.01]
    if len(mismatch):
        errors.append(f"{len(mismatch)} rows have revenue != quantity * unit_price")

    return df, errors


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df["product"] = df["product"].str.strip()
    df["region"] = df["region"].str.strip()
    return df


def load(df: pd.DataFrame, output_path: str) -> None:
    df.to_parquet(output_path, index=False)
    print(f"[load] {len(df)} rows -> {output_path}")


def ingest_sales_csv(source: str, output: str) -> None:
    df = extract(source)
    df, errors = validate(df)
    if errors:
        for err in errors:
            print(f"[validate] ERROR: {err}")
        raise ValueError("Validation failed — see errors above")
    print(f"[validate] OK")
    df = transform(df)
    load(df, output)


if __name__ == "__main__":
    src = os.path.join(DATASETS, "sales.csv")
    out = "/tmp/sales_ingested.parquet"
    ingest_sales_csv(src, out)

    # Verify
    result = pd.read_parquet(out)
    print(f"\nLoaded back: {result.shape}")
    print(result.head(3))
