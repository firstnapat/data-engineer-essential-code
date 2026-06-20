import pandas as pd
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])

print("=== Select Columns ===")
print(df[["product", "revenue"]].head())

print("\n=== Filter Rows ===")
electronics = df[df["category"] == "Electronics"]
print(f"Electronics rows: {len(electronics)}")

high_revenue = df[df["revenue"] > 50000]
print(f"Revenue > 50k rows: {len(high_revenue)}")

bkk_electronics = df[(df["region"] == "Bangkok") & (df["category"] == "Electronics")]
print(f"Bangkok Electronics: {len(bkk_electronics)} rows")

print("\n=== isin() ---")
top_regions = ["Bangkok", "Chiang Mai"]
df_top = df[df["region"].isin(top_regions)]
print(f"Bangkok + Chiang Mai: {len(df_top)} rows")

print("\n=== query() — readable filters ---")
result = df.query("revenue > 50000 and category == 'Electronics'")
print(result[["date", "product", "revenue", "region"]])

print("\n=== loc[] — label-based ---")
print(df.loc[0:2, ["product", "quantity", "revenue"]])

print("\n=== iloc[] — position-based ---")
print(df.iloc[0:3, [1, 3, 5]])   # rows 0-2, columns 1,3,5

print("\n=== sort_values ---")
top5 = df.sort_values("revenue", ascending=False).head(5)
print(top5[["date", "product", "revenue", "region"]])
