import csv
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
CSV_FILE = os.path.join(DATASETS, "sales.csv")

print("--- csv.reader ---")
with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    print(f"Headers: {headers}")
    print("First 3 rows:")
    for i, row in enumerate(reader):
        if i >= 3:
            break
        print(f"  {row}")

print("\n--- csv.DictReader (rows as dicts) ---")
with open(CSV_FILE, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
print(f"First row: {rows[0]}")

print("\n--- Aggregations (pure Python) ---")
total_revenue = sum(float(r["revenue"]) for r in rows)
print(f"Total Revenue: {total_revenue:,.0f} THB")

by_category = {}
for r in rows:
    cat = r["category"]
    by_category[cat] = by_category.get(cat, 0) + float(r["revenue"])

print("\nRevenue by Category:")
for cat, rev in sorted(by_category.items(), key=lambda x: -x[1]):
    print(f"  {cat:<20} {rev:>12,.0f} THB")

print("\n--- Write CSV ---")
output = "/tmp/category_summary.csv"
with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["category", "revenue"])
    writer.writeheader()
    for cat, rev in sorted(by_category.items()):
        writer.writerow({"category": cat, "revenue": round(rev, 2)})
print(f"Summary written to {output}")
