"""
Solution: Data Lake — Bronze / Silver / Gold with RustFS
"""
import os
import io
from datetime import date
import pandas as pd
import boto3

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
BUCKET   = "exercise-lake"
TODAY    = date.today().isoformat()

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1",
)

# --- helpers -----------------------------------------------------------------

def to_parquet_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_parquet(buf, index=False, engine="pyarrow")
    buf.seek(0)
    return buf.getvalue()

def upload(df: pd.DataFrame, key: str) -> None:
    s3.put_object(Bucket=BUCKET, Key=key, Body=to_parquet_bytes(df))
    print(f"[lake] {len(df):>4} rows -> s3://{BUCKET}/{key}")

# --- Task 1 & 2: client + bucket ---------------------------------------------

existing = [b["Name"] for b in s3.list_buckets()["Buckets"]]
if BUCKET not in existing:
    s3.create_bucket(Bucket=BUCKET)
print(f"[lake] Bucket '{BUCKET}' ready")

# --- Task 3: Bronze ----------------------------------------------------------

TABLES = ["users", "addresses", "orders", "order_items", "transports"]

raw = {}
for name in TABLES:
    raw[name] = pd.read_csv(os.path.join(DATASETS, f"raw/{name}_raw.csv"))
    upload(raw[name], f"bronze/{name}/{TODAY}/data.parquet")

# --- Task 4: Silver ----------------------------------------------------------

silver = {}

silver["users"] = raw["users"].drop_duplicates(subset=["email"])

silver["addresses"] = raw["addresses"].copy()
silver["addresses"]["province"] = silver["addresses"]["province"].str.title()
silver["addresses"] = silver["addresses"].dropna(subset=["postal_code"])

silver["orders"] = raw["orders"].drop_duplicates(subset=["order_id"])

silver["order_items"] = raw["order_items"].copy()
silver["order_items"]["subtotal"] = (
    silver["order_items"]["quantity"] * silver["order_items"]["unit_price"]
).round(2)

silver["transports"] = raw["transports"].copy()
silver["transports"].loc[
    silver["transports"]["status"] != "delivered", "delivered_at"
] = None

for name, df in silver.items():
    upload(df, f"silver/{name}/{TODAY}/data.parquet")

# --- Task 5: Gold ------------------------------------------------------------

df_gold = (
    silver["orders"].groupby("status")
    .agg(order_count=("order_id", "count"),
         total_revenue=("total_amount", "sum"))
    .reset_index()
    .round(2)
)
upload(df_gold, f"gold/orders/{TODAY}/status_summary.parquet")

# --- Task 6: List ------------------------------------------------------------

resp = s3.list_objects_v2(Bucket=BUCKET)
print("\n[lake] All objects:")
for obj in resp.get("Contents", []):
    print(f"  s3://{BUCKET}/{obj['Key']}")

# --- Verification ------------------------------------------------------------

resp = s3.list_objects_v2(Bucket=BUCKET)
keys = [obj["Key"] for obj in resp.get("Contents", [])]
assert any("bronze/users" in k for k in keys),  "Missing bronze/users"
assert any("silver/orders" in k for k in keys), "Missing silver/orders"
assert any("gold/orders" in k for k in keys),   "Missing gold/orders"
print("\n✅ All verifications passed!")
