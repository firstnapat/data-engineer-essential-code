"""
Step 2: Data Collection
=======================
Understand the raw data before touching it:
  - Where does it come from?
  - What format is it in?
  - How large is it?
  - What are the fields and their expected types?
"""
import csv
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
CSV_FILE = os.path.join(DATASETS, "sales.csv")

print("=== Data Profile ===")
with open(CSV_FILE, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Source:      {CSV_FILE}")
print(f"Rows:        {len(rows)}")
print(f"Columns:     {list(rows[0].keys())}")
print(f"Date range:  {rows[0]['date']} -> {rows[-1]['date']}")
print(f"Sample row:  {rows[0]}")

print("\n=== Unique Values ===")
categories = sorted(set(r["category"] for r in rows))
regions = sorted(set(r["region"] for r in rows))
products = sorted(set(r["product"] for r in rows))
print(f"Categories ({len(categories)}): {categories}")
print(f"Regions    ({len(regions)}):    {regions}")
print(f"Products   ({len(products)}):   {products}")

print("\n=== Value Ranges ===")
quantities = [int(r["quantity"]) for r in rows]
revenues = [float(r["revenue"]) for r in rows]
print(f"Quantity: min={min(quantities)}, max={max(quantities)}, avg={sum(quantities)/len(quantities):.1f}")
print(f"Revenue:  min={min(revenues):,.0f}, max={max(revenues):,.0f}, avg={sum(revenues)/len(revenues):,.0f}")
