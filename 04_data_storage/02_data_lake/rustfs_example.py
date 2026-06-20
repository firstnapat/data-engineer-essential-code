"""
Data Lake storage using RustFS (S3-compatible object storage).
RustFS exposes the same API as AWS S3, so we use boto3.

Setup (Docker):
  docker run -p 9000:9000 -p 9001:9001 \\
    -e MINIO_ROOT_USER=minioadmin \\
    -e MINIO_ROOT_PASSWORD=minioadmin \\
    quay.io/minio/minio server /data --console-address ':9001'

Configure .env with S3_* variables from .env.example.
"""
import os
import io
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
S3_ACCESS   = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET   = os.getenv("S3_SECRET_KEY", "minioadmin")
BUCKET      = os.getenv("S3_BUCKET", "data-lake")

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

        df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])

        # Partition by month (common pattern in data lakes)
        for month, group in df.groupby(df["date"].dt.strftime("%Y-%m")):
            key = f"raw/sales/month={month}/data.parquet"
            upload_dataframe_as_parquet(s3, group, BUCKET, key)

        print("\n[lake] Objects in bucket:")
        for obj in list_objects(s3, BUCKET, prefix="raw/sales/"):
            print(f"  s3://{BUCKET}/{obj}")

        # Read back one partition
        df_back = download_dataframe(s3, BUCKET, "raw/sales/month=2024-01/data.parquet")
        print(f"\n[lake] Read back Jan 2024: {len(df_back)} rows")

    except Exception as e:
        print(f"Connection failed: {e}")
        print("Start RustFS/MinIO and check your .env settings.")
