import pandas as pd
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")

print("=== Descriptive Statistics ===")
print(df[["quantity", "unit_price", "revenue"]].describe().round(2))

print("\n=== Aggregation — groupby ===")
by_category = (
    df.groupby("category")["revenue"]
    .agg(total="sum", mean="mean", count="count")
    .sort_values("total", ascending=False)
)
print(by_category.round(0))

print("\n=== Aggregation — multiple columns ===")
summary = df.groupby("region").agg(
    total_revenue=("revenue", "sum"),
    total_qty=("quantity", "sum"),
    transactions=("revenue", "count"),
).sort_values("total_revenue", ascending=False)
print(summary)

print("\n=== Monthly Trend ===")
monthly = df.groupby("month")["revenue"].sum()
print(monthly)

print("\n=== Pivot Table ===")
pivot = df.pivot_table(
    values="revenue",
    index="region",
    columns="category",
    aggfunc="sum",
    fill_value=0,
)
print(pivot.astype(int))

print("\n=== value_counts ===")
print(df["category"].value_counts())

print("\n=== Correlation ===")
print(df[["quantity", "unit_price", "revenue"]].corr().round(3))
