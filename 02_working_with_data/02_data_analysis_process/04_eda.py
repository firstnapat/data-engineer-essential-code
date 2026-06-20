"""
Step 4: Exploratory Data Analysis (EDA)
=========================================
Goal: understand patterns, distributions, and relationships in the data
before building models or dashboards.

EDA checklist:
  - Overall summary statistics
  - Distribution of each variable
  - Aggregations by key dimensions (category, region, time)
  - Identify outliers
  - Spot correlations
"""
import csv
import os
from collections import defaultdict

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

with open(os.path.join(DATASETS, "sales.csv"), "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

revenues = [float(r["revenue"]) for r in rows]
quantities = [int(r["quantity"]) for r in rows]

print("=== Summary Statistics ===")
print(f"  Transactions:    {len(rows)}")
print(f"  Total Revenue:   {sum(revenues):>12,.0f} THB")
print(f"  Avg per Txn:     {sum(revenues)/len(revenues):>12,.0f} THB")
print(f"  Max single Txn:  {max(revenues):>12,.0f} THB")
print(f"  Min single Txn:  {min(revenues):>12,.0f} THB")

print("\n=== Revenue by Category ===")
by_cat = defaultdict(float)
for r in rows:
    by_cat[r["category"]] += float(r["revenue"])
total = sum(by_cat.values())
for cat, rev in sorted(by_cat.items(), key=lambda x: -x[1]):
    pct = rev / total * 100
    bar = "█" * int(pct / 3)
    print(f"  {cat:<20} {rev:>10,.0f}  {pct:5.1f}%  {bar}")

print("\n=== Revenue by Region ===")
by_region = defaultdict(float)
for r in rows:
    by_region[r["region"]] += float(r["revenue"])
for region, rev in sorted(by_region.items(), key=lambda x: -x[1]):
    print(f"  {region:<15} {rev:>10,.0f} THB")

print("\n=== Monthly Revenue Trend ===")
by_month = defaultdict(float)
for r in rows:
    month = r["date"][:7]    # YYYY-MM
    by_month[month] += float(r["revenue"])
for month, rev in sorted(by_month.items()):
    bar = "█" * int(rev / 20000)
    print(f"  {month}  {rev:>10,.0f}  {bar}")

print("\n=== Top 5 Products by Revenue ===")
by_product = defaultdict(float)
for r in rows:
    by_product[r["product"]] += float(r["revenue"])
top5 = sorted(by_product.items(), key=lambda x: -x[1])[:5]
for rank, (product, rev) in enumerate(top5, start=1):
    print(f"  #{rank} {product:<22} {rev:>10,.0f} THB")
