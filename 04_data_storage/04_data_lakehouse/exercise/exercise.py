"""
Exercise: Data Lakehouse — Delta Lake with QuickMart Products
Practice the concepts from lakehouse_example.py (Delta Lake + time travel)
on the QuickMart product catalog (datasets/new-raw/products.csv).

No Docker needed — Delta tables are just files on disk.
Run: uv run 04_data_storage/04_data_lakehouse/exercise/exercise.py
"""
import os
import shutil
import pandas as pd
from deltalake import DeltaTable, write_deltalake

RAW = os.path.join(os.path.dirname(__file__), "../../../datasets/new-raw")
DELTA_PATH = "/tmp/delta/exercise_products"

# Clean up previous runs for a fresh start
if os.path.exists(DELTA_PATH):
    shutil.rmtree(DELTA_PATH)

# =========================================================================
# Task 1: Read + clean products.csv, write to a Delta table
# =========================================================================
# The raw catalog is dirty (duplicate rows, blank categories). Clean it down
# to one valid row per product before landing the first Delta version.
print("--- Task 1: Write products to Delta table ---")
products = pd.read_csv(os.path.join(RAW, "products.csv"))
products["category"] = products["category"].astype("string").str.strip()
products = products[products["category"].notna() & (products["category"] != "")]
products = products.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

write_deltalake(DELTA_PATH, products, mode="overwrite")
print(f"[lakehouse] Written {len(products)} rows to {DELTA_PATH}")

# =========================================================================
# Task 2: Read the Delta table back
# =========================================================================
print("\n--- Task 2: Read Delta table ---")
dt = DeltaTable(DELTA_PATH)
df_read = dt.to_pandas()
print(f"[lakehouse] Table shape: {df_read.shape}")
print(df_read.head(3))

# =========================================================================
# Task 3: Append 2 new product rows
# =========================================================================
print("\n--- Task 3: Append new products ---")
new_products = pd.DataFrame([
    {"product_id": 3101, "product_name": "Oishi Product 3101",
     "category": "Beverage", "brand": "Oishi", "price": 45.0},
    {"product_id": 3102, "product_name": "Mama Product 3102",
     "category": "Food", "brand": "Mama", "price": 32.5},
])
write_deltalake(DELTA_PATH, new_products, mode="append")
print(f"[lakehouse] Appended {len(new_products)} rows")

# =========================================================================
# Task 4: Show transaction history
# =========================================================================
print("\n--- Task 4: Transaction history ---")
dt = DeltaTable(DELTA_PATH)
for entry in dt.history():
    print(f"  version={entry.get('version')}, "
          f"operation={entry.get('operation')}, "
          f"timestamp={entry.get('timestamp')}")

# =========================================================================
# Task 5: Time travel — compare version 0 with current version
# =========================================================================
print("\n--- Task 5: Time travel ---")
df_v0 = DeltaTable(DELTA_PATH, version=0).to_pandas()
df_current = DeltaTable(DELTA_PATH).to_pandas()

print(f"Version 0 rows:  {len(df_v0)}")
print(f"Current rows:    {len(df_current)}")
print(f"Difference:      {len(df_current) - len(df_v0)}")

# --- Verification ---
assert len(df_v0) == 50, f"Version 0 should have 50 rows, got {len(df_v0)}"
assert len(df_current) == 52, f"Current version should have 52 rows, got {len(df_current)}"
assert len(df_current) - len(df_v0) == 2, "Difference should be 2 (appended rows)"

history = DeltaTable(DELTA_PATH).history()
assert len(history) == 2, f"Expected 2 versions in history, got {len(history)}"

print("\n✅ All verifications passed!")
