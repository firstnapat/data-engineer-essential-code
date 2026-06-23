"""
Exercise: Data Lake Storage — Uploading Products as Parquet to S3
Practice the concepts from rustfs_example.py (S3-compatible object storage).
Run: uv run 04_data_storage/02_data_lake/exercise/exercise.py

Setup (Docker — start RustFS/MinIO first):
  docker run -p 9000:9000 -p 9001:9001 \\
    -e MINIO_ROOT_USER=minioadmin \\
    -e MINIO_ROOT_PASSWORD=minioadmin \\
    quay.io/minio/minio server /data --console-address ':9001'

Configure .env with S3_ENDPOINT_URL, S3_ACCESS_KEY, S3_SECRET_KEY.
"""
import os
import io
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

try:
    # =========================================================================
    # Task 1: Create a boto3 S3 client
    # =========================================================================
    print("--- Task 1: Create S3 client ---")
    # TODO: Import boto3 and create an S3 client using:
    #   - endpoint_url  = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
    #   - aws_access_key_id = os.getenv("S3_ACCESS_KEY", "minioadmin")
    #   - aws_secret_access_key = os.getenv("S3_SECRET_KEY", "minioadmin")
    #   - region_name = "us-east-1"
    # Store the client in a variable called `s3`.
    # Hint: Use boto3.client("s3", endpoint_url=..., ...)
    import boto3

    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://localhost:9000"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin"),
        region_name="us-east-1",
    )

    print("[lake] S3 client created")

    # =========================================================================
    # Task 2: Create a bucket called 'exercise-lake'
    # =========================================================================
    print("\n--- Task 2: Create bucket ---")
    BUCKET = "exercise-lake"
    existing_buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if BUCKET not in existing_buckets:
        s3.create_bucket(Bucket=BUCKET)

    print(f"[lake] Bucket '{BUCKET}' ready")

    # =========================================================================
    # Task 3: Read products.json, flatten, and upload as Parquet
    # =========================================================================
    print("\n--- Task 3: Upload products as Parquet ---")
    with open(os.path.join(DATASETS, "products.json"), "r") as f:
        data = json.load(f)
    df_products = pd.json_normalize(data, record_path="products")

    buffer = io.BytesIO()
    df_products.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    s3.put_object(Bucket=BUCKET, Key="raw/products/data.parquet", Body=buffer.getvalue())

    print(f"[lake] Uploaded {len(df_products)} products -> s3://{BUCKET}/raw/products/data.parquet")

    # =========================================================================
    # Task 4: List all objects in the bucket
    # =========================================================================
    print("\n--- Task 4: List objects ---")
    resp = s3.list_objects_v2(Bucket=BUCKET)
    keys = [obj["Key"] for obj in resp.get("Contents", [])]
    for key in keys:
        print(f"  Key: {key}")

    # =========================================================================
    # Task 5: Download and read back the Parquet file
    # =========================================================================
    print("\n--- Task 5: Download and verify ---")
    resp = s3.get_object(Bucket=BUCKET, Key="raw/products/data.parquet")
    df_back = pd.read_parquet(io.BytesIO(resp["Body"].read()))

    print(f"[lake] Downloaded shape: {df_back.shape}")
    print(df_back.head(3))

    # --- Verification ---
    assert df_back.shape[0] == 13, f"Expected 13 products, got {df_back.shape[0]}"
    assert "category" in df_back.columns, "Missing 'category' column"
    assert "unit_price" in df_back.columns, "Missing 'unit_price' column"
    print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("Make sure RustFS/MinIO is running. Start it with:")
    print("  docker run -p 9000:9000 -p 9001:9001 \\")
    print("    -e MINIO_ROOT_USER=minioadmin \\")
    print("    -e MINIO_ROOT_PASSWORD=minioadmin \\")
    print("    quay.io/minio/minio server /data --console-address ':9001'")
