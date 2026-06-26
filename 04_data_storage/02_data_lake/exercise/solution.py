"""
Solution: Data Lake — Bronze / Silver / Gold with RustFS (QuickMart data)

Bronze = raw CSVs landed as-is (datasets/new-raw/ — dirty).
Silver = cleaned & deduplicated per table.
Gold   = business aggregates ready to query.
"""
import os
import io
from datetime import date
import pandas as pd
import boto3

RAW    = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
BUCKET = "exercise-lake"
TODAY  = date.today().isoformat()

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
    print(f"[lake] {len(df):>5} rows -> s3://{BUCKET}/{key}")

# --- Task 1 & 2: client + bucket ---------------------------------------------

existing = [b["Name"] for b in s3.list_buckets()["Buckets"]]
if BUCKET not in existing:
    s3.create_bucket(Bucket=BUCKET)
print(f"[lake] Bucket '{BUCKET}' ready")

# --- Task 3: Bronze — land raw CSVs as-is ------------------------------------

TABLES = ["customers", "products", "orders", "order_items", "deliveries"]

raw = {}
for name in TABLES:
    raw[name] = pd.read_csv(os.path.join(RAW, f"{name}.csv"))
    upload(raw[name], f"bronze/{name}/{TODAY}/data.parquet")

# --- Task 4: Silver — clean each dataset -------------------------------------

silver = {}

# customers: drop dup rows + dup ids, blank name, blank/invalid email; tidy tier
cust = raw["customers"].drop_duplicates().drop_duplicates(subset=["customer_id"]).copy()
cust = cust[cust["customer_name"].astype("string").str.strip().fillna("") != ""]
cust = cust[cust["email"].astype("string").str.contains(r"@.+\.", regex=True, na=False)]
cust["sub_tier"] = cust["sub_tier"].str.strip().str.title()
silver["customers"] = cust

# products: drop dup rows + dup ids, blank category, price <= 0
prod = raw["products"].drop_duplicates().copy()
prod["category"] = prod["category"].astype("string").str.strip()
prod = prod[prod["category"].notna() & (prod["category"] != "")]
prod = prod[prod["price"] > 0]
silver["products"] = prod.drop_duplicates(subset=["product_id"])

# orders: drop dup rows + dup ids, amount <= 0, tidy status, drop orphan customers
orders = raw["orders"].drop_duplicates().drop_duplicates(subset=["order_id"]).copy()
orders = orders[orders["amount"] > 0]
orders["status"] = orders["status"].str.strip().str.lower().replace({"canceled": "cancelled"})
orders = orders[orders["customer_id"].isin(silver["customers"]["customer_id"])]
silver["orders"] = orders

# order_items: drop dup rows, qty/unit_price <= 0, recompute subtotal
items = raw["order_items"].drop_duplicates().copy()
items = items[(items["qty"] > 0) & (items["unit_price"] > 0)]
items["subtotal"] = (items["qty"] * items["unit_price"]).round(2)
silver["order_items"] = items

# deliveries: drop dup rows, parcels <= 0, blank vehicle
deliv = raw["deliveries"].drop_duplicates().copy()
deliv = deliv[deliv["parcels_delivered"] > 0]
deliv = deliv[deliv["vehicle_id"].astype("string").str.strip().fillna("") != ""]
silver["deliveries"] = deliv

for name, df in silver.items():
    upload(df, f"silver/{name}/{TODAY}/data.parquet")

# --- Task 5: Gold — aggregate cleaned orders by status -----------------------

df_gold = (
    silver["orders"].groupby("status")
    .agg(order_count=("order_id", "count"),
         total_revenue=("amount", "sum"))
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
assert any("bronze/customers" in k for k in keys), "Missing bronze/customers"
assert any("silver/orders" in k for k in keys),    "Missing silver/orders"
assert any("gold/orders" in k for k in keys),      "Missing gold/orders"
print("\n✅ All verifications passed!")
