"""
Work with an AVRO data source (row-based, schema embedded).   read -> inspect -> clean

Avro stores everything per the schema (here dates are strings), so cleaning
re-applies types. We create a small sample from the CSV first.
Requires: fastavro
"""
import os
import pandas as pd
import fastavro

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
SAMPLE = "/tmp/sales_sample.avro"

SCHEMA = {
    "type": "record", "name": "Sale",
    "fields": [
        {"name": "date", "type": "string"},
        {"name": "product", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "quantity", "type": "int"},
        {"name": "unit_price", "type": "int"},
        {"name": "revenue", "type": "int"},
        {"name": "region", "type": "string"},
    ],
}


def _prepare_sample() -> None:
    df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), dtype={"date": str})
    with open(SAMPLE, "wb") as f:
        fastavro.writer(f, fastavro.parse_schema(SCHEMA), df.to_dict("records"))


def read(path: str) -> pd.DataFrame:
    with open(path, "rb") as f:
        return pd.DataFrame(list(fastavro.reader(f)))


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}")
    print(df.head())
    print("\ndtypes (date came back as object/string):")
    print(df.dtypes)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])      # re-apply the date type
    return df


if __name__ == "__main__":
    _prepare_sample()
    df = read(SAMPLE)
    inspect(df)
    cleaned = clean(df)
    print(f"\n[clean] date dtype now {cleaned['date'].dtype}")
