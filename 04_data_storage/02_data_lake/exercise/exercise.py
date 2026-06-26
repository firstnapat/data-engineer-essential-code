"""
Exercise: Data Lake — Bronze / Silver / Gold with RustFS
Practice the medallion architecture from rustfs_example.py.
Run: uv run 04_data_storage/02_data_lake/exercise/exercise.py

Setup (Docker — start RustFS first):
  docker run -d --name de-rustfs \\
    -p 9000:9000 -p 9001:9001 \\
    quay.io/minio/minio server /data --console-address ':9001'

Datasets: datasets/new-raw/ — the QuickMart raw CSVs (customers, products,
orders, order_items, deliveries). They are DIRTY (duplicates, blank/invalid
values, bad numbers); the Silver layer is where you clean them.
"""
import os
import io
from datetime import date
import pandas as pd

RAW      = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
BUCKET   = "exercise-lake"
TODAY    = date.today().isoformat()

try:
    # =========================================================================
    # Task 1: Create S3 client
    # =========================================================================
    print("--- Task 1: Create S3 client ---")
    # TODO: Create a boto3 S3 client pointing to local RustFS (localhost:9000).

    s3 = None  # Replace with your boto3.client(...) call
    print("[lake] S3 client created")

    # =========================================================================
    # Task 2: Ensure bucket exists
    # =========================================================================
    print(f"\n--- Task 2: Ensure bucket '{BUCKET}' exists ---")
    # TODO: Create the bucket if it doesn't exist.

    print(f"[lake] Bucket '{BUCKET}' ready")

    # =========================================================================
    # Task 3: Bronze — upload all 5 datasets as-is (CSV → Parquet)
    # =========================================================================
    print("\n--- Task 3: Bronze layer ---")
    # TODO: Read each CSV and upload as Parquet to bronze/{name}/{TODAY}/data.parquet
    #       Datasets: customers, products, orders, order_items, deliveries
    #       (read from RAW/{name}.csv)

    # =========================================================================
    # Task 4: Silver — clean each dataset and upload
    # =========================================================================
    print("\n--- Task 4: Silver layer ---")
    # TODO: Inspect each dataset, identify the issues, clean them,
    #       and upload to silver/{name}/{TODAY}/data.parquet

    # =========================================================================
    # Task 5: Gold — aggregate and upload
    # =========================================================================
    print("\n--- Task 5: Gold layer ---")
    # TODO: Aggregate the cleaned orders by status (count, total revenue)
    #       and upload to gold/orders/{TODAY}/status_summary.parquet

    # =========================================================================
    # Task 6: List all objects in the bucket
    # =========================================================================
    print("\n--- Task 6: List all objects ---")
    # TODO: Print every object key in BUCKET.

    # --- Verification ---
    # Uncomment after completing all tasks:
    # resp = s3.list_objects_v2(Bucket=BUCKET)
    # keys = [obj["Key"] for obj in resp.get("Contents", [])]
    # assert any("bronze/customers" in k for k in keys), "Missing bronze/customers"
    # assert any("silver/orders" in k for k in keys),    "Missing silver/orders"
    # assert any("gold/orders" in k for k in keys),      "Missing gold/orders"
    # print("\n✅ All verifications passed!")

except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("Make sure RustFS is running on localhost:9000.")
