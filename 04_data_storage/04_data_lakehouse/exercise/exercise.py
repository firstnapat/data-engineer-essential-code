"""
Exercise: Data Lakehouse — Delta Lake with Products Data
Practice the concepts from lakehouse_example.py (Delta Lake + time travel).
Run: uv run 04_data_storage/04_data_lakehouse/exercise/exercise.py

No Docker needed — Delta tables are just files on disk.
"""
import os
import json
import shutil
import pandas as pd
from deltalake import DeltaTable, write_deltalake

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
DELTA_PATH = "/tmp/delta/exercise_products"

# Clean up previous runs for a fresh start
if os.path.exists(DELTA_PATH):
    shutil.rmtree(DELTA_PATH)

# =========================================================================
# Task 1: Read products.json, flatten, and write to Delta table
# =========================================================================
print("--- Task 1: Write products to Delta table ---")
# TODO (Step A): Read products.json and flatten the "products" array.
#       data = json.load(open(os.path.join(DATASETS, "products.json")))
#       df_products = pd.json_normalize(data, record_path="products")

# TODO (Step B): Write df_products to a Delta table using:
#       write_deltalake(DELTA_PATH, df_products, mode="overwrite")

# print(f"[lakehouse] Written {len(df_products)} rows to {DELTA_PATH}")

# =========================================================================
# Task 2: Read the Delta table back
# =========================================================================
print("\n--- Task 2: Read Delta table ---")
# TODO: Read the Delta table back using DeltaTable and convert to pandas.
#       dt = DeltaTable(DELTA_PATH)
#       df_read = dt.to_pandas()
#       Print the shape and first 3 rows.

# print(f"[lakehouse] Table shape: {df_read.shape}")
# print(df_read.head(3))

# =========================================================================
# Task 3: Append 2 new product rows
# =========================================================================
print("\n--- Task 3: Append new products ---")
# TODO: Create a DataFrame with 2 new products and append to the Delta table.
#       Use write_deltalake(DELTA_PATH, new_products, mode="append").
#
#       new_products = pd.DataFrame([
#           {"id": "P014", "name": "USB-C Hub", "category": "Electronics",
#            "unit_price": 1200, "stock": 75, "supplier": "TechCorp"},
#           {"id": "P015", "name": "Desk Lamp", "category": "Furniture",
#            "unit_price": 890, "stock": 120, "supplier": "FurniturePro"},
#       ])

# print(f"[lakehouse] Appended {len(new_products)} rows")

# =========================================================================
# Task 4: Show transaction history
# =========================================================================
print("\n--- Task 4: Transaction history ---")
# TODO: Create a DeltaTable and call .history() to see the transaction log.
#       dt = DeltaTable(DELTA_PATH)
#       for entry in dt.history():
#           print(f"  version={entry['version']}, "
#                 f"operation={entry['operation']}, "
#                 f"timestamp={entry['timestamp']}")

# =========================================================================
# Task 5: Time travel — compare version 0 with current version
# =========================================================================
print("\n--- Task 5: Time travel ---")
# TODO (Step A): Read version 0 (initial load) using:
#       dt_v0 = DeltaTable(DELTA_PATH, version=0)
#       df_v0 = dt_v0.to_pandas()

# TODO (Step B): Read the current (latest) version:
#       dt_current = DeltaTable(DELTA_PATH)
#       df_current = dt_current.to_pandas()

# TODO (Step C): Compare and print row counts for both versions.
#       Print the difference (should be 2 — the rows we appended).

# Uncomment after completing:
# print(f"Version 0 rows:  {len(df_v0)}")
# print(f"Current rows:    {len(df_current)}")
# print(f"Difference:      {len(df_current) - len(df_v0)}")

# --- Verification ---
# Uncomment after completing all tasks:
# assert len(df_v0) == 13, f"Version 0 should have 13 rows, got {len(df_v0)}"
# assert len(df_current) == 15, f"Current version should have 15 rows, got {len(df_current)}"
# assert len(df_current) - len(df_v0) == 2, "Difference should be 2 (appended rows)"
#
# dt_hist = DeltaTable(DELTA_PATH)
# history = dt_hist.history()
# assert len(history) == 2, f"Expected 2 versions in history, got {len(history)}"
#
# print("\n✅ All verifications passed!")
