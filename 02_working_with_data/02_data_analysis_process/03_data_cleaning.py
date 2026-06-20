"""
Step 3: Data Cleaning and Manipulation
=======================================
Common issues to check and fix:
  - Missing / null values
  - Duplicate rows
  - Incorrect data types
  - Inconsistent strings (casing, whitespace, typos)
  - Out-of-range / impossible values
"""
import csv
import os
from datetime import datetime

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

with open(os.path.join(DATASETS, "sales.csv"), "r", encoding="utf-8") as f:
    raw_rows = list(csv.DictReader(f))

print(f"Rows loaded: {len(raw_rows)}")

# --- Check for missing values ---
print("\n=== Missing Values ===")
for col in raw_rows[0].keys():
    missing = sum(1 for r in raw_rows if not r[col].strip())
    print(f"  {col:<15}: {missing} missing")

# --- Check for duplicates ---
print("\n=== Duplicate Check ===")
seen = set()
dupes = 0
for r in raw_rows:
    key = (r["date"], r["product"], r["region"])
    if key in seen:
        dupes += 1
    seen.add(key)
print(f"  Duplicate (date+product+region) rows: {dupes}")

# --- Type coercion and validation ---
print("\n=== Type Conversion & Validation ===")
cleaned = []
errors = []

for i, r in enumerate(raw_rows, start=2):    # row 1 = header
    try:
        row = {
            "date":       datetime.strptime(r["date"], "%Y-%m-%d").date(),
            "product":    r["product"].strip(),
            "category":   r["category"].strip(),
            "quantity":   int(r["quantity"]),
            "unit_price": float(r["unit_price"]),
            "revenue":    float(r["revenue"]),
            "region":     r["region"].strip(),
        }
        # Cross-check: revenue should equal quantity * unit_price
        expected_revenue = row["quantity"] * row["unit_price"]
        if abs(expected_revenue - row["revenue"]) > 0.01:
            errors.append(f"Row {i}: revenue mismatch ({row['revenue']} != {expected_revenue})")
        else:
            cleaned.append(row)
    except (ValueError, KeyError) as e:
        errors.append(f"Row {i}: {e}")

print(f"  Clean rows: {len(cleaned)}")
print(f"  Errors:     {len(errors)}")
for err in errors:
    print(f"    {err}")
