"""
Ingest Avro — a row-based format with an explicit, evolvable schema.

Common in streaming/Kafka pipelines. Each file embeds its schema, so readers
always know the field types. Pattern: define schema -> write -> read
Requires: fastavro
"""
import os
import pandas as pd
import fastavro

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

# an Avro schema declares every field and its type up front
SCHEMA = {
    "type": "record",
    "name": "Sale",
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


def write_avro(df: pd.DataFrame, path: str) -> None:
    records = df.to_dict("records")
    parsed = fastavro.parse_schema(SCHEMA)
    with open(path, "wb") as f:
        fastavro.writer(f, parsed, records)
    print(f"[write] {len(records)} records -> {path} ({os.path.getsize(path):,} bytes)")


def read_avro(path: str) -> pd.DataFrame:
    with open(path, "rb") as f:
        records = list(fastavro.reader(f))
    df = pd.DataFrame(records)
    print(f"[read] {df.shape} from {os.path.basename(path)}")
    return df


if __name__ == "__main__":
    # read date as string to match the schema's string field
    src = pd.read_csv(os.path.join(DATASETS, "sales.csv"), dtype={"date": str})
    out = "/tmp/sales.avro"
    write_avro(src, out)

    df = read_avro(out)
    print("\n--- Round-tripped via Avro ---")
    print(df.head())
    print(f"\nschema fields: {[f['name'] for f in SCHEMA['fields']]}")
