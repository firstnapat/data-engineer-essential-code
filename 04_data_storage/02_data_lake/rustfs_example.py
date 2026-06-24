"""
Data Lake storage using RustFS (S3-compatible object storage).
RustFS exposes the same API as AWS S3, so we use boto3.

Demonstrates the medallion architecture with products_raw.csv:
  Bronze — raw data as-is (CSV → Parquet, no changes)
  Silver — cleaned (deduplicated, category standardized)
  Gold   — aggregated (category summary)

Setup (Docker):
  docker run -d --name de-rustfs \\
    -p 9000:9000 -p 9001:9001 \\
    quay.io/minio/minio server /data --console-address ':9001'

Authentication: place credentials.json (downloaded from RustFS webui) next to this file.
"""
import os
import io
import json
from datetime import date
import pandas as pd

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

with open(CREDENTIALS_PATH) as f:
    _creds = json.load(f)

S3_ENDPOINT = f"http://{_creds['url'].replace('9001', '9000')}"
S3_ACCESS   = _creds["accessKey"]
S3_SECRET   = _creds["secretKey"]
BUCKET      = "data-lake"
TODAY       = date.today().isoformat()

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def get_s3_client():
    import boto3
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS,
        aws_secret_access_key=S3_SECRET,
        region_name="us-east-1",
    )


def ensure_bucket(s3, bucket: str) -> None:
    existing = [b["Name"] for b in s3.list_buckets()["Buckets"]]
    if bucket not in existing:
        s3.create_bucket(Bucket=bucket)
        print(f"[lake] Created bucket '{bucket}'")
    else:
        print(f"[lake] Bucket '{bucket}' already exists")


def upload_dataframe_as_parquet(s3, df: pd.DataFrame, bucket: str, key: str) -> None:
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
    print(f"[lake] Uploaded {len(df)} rows -> s3://{bucket}/{key}")


def list_objects(s3, bucket: str, prefix: str = "") -> list[str]:
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in resp.get("Contents", [])]


def download_dataframe(s3, bucket: str, key: str) -> pd.DataFrame:
    resp = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(resp["Body"].read()))


if __name__ == "__main__":
    try:
        s3 = get_s3_client()
        ensure_bucket(s3, BUCKET)

        df_raw = pd.read_csv(os.path.join(DATASETS, "raw/products_raw.csv"))

        # ------------------------------------------------------------------
        # Bronze — raw data as-is, partitioned by ingestion date
        # ------------------------------------------------------------------
        upload_dataframe_as_parquet(
            s3, df_raw, BUCKET,
            f"bronze/products/{TODAY}/data.parquet",
        )

        # ------------------------------------------------------------------
        # Silver — deduplicated + category standardized to Title Case
        # ------------------------------------------------------------------
        df_silver = df_raw.copy()
        df_silver["category"] = df_silver["category"].str.title()
        df_silver = df_silver.drop_duplicates(subset=["product_id"])
        upload_dataframe_as_parquet(
            s3, df_silver, BUCKET,
            f"silver/products/{TODAY}/data.parquet",
        )

        # ------------------------------------------------------------------
        # Gold — category summary (count, avg price, total stock)
        # ------------------------------------------------------------------
        df_gold = (
            df_silver.groupby("category")
            .agg(
                total_products=("product_id", "count"),
                avg_price=("unit_price", "mean"),
                total_stock=("stock_qty", "sum"),
            )
            .reset_index()
            .round(2)
        )
        upload_dataframe_as_parquet(
            s3, df_gold, BUCKET,
            f"gold/products/{TODAY}/category_summary.parquet",
        )

        print("\n[lake] All objects in bucket:")
        for obj in list_objects(s3, BUCKET):
            print(f"  s3://{BUCKET}/{obj}")

    except Exception as e:
        print(f"Connection failed: {e}")
        print("Start RustFS/MinIO and check credentials.json.")
