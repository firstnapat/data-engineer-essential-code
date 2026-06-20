import pandas as pd
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")
CSV_FILE = os.path.join(DATASETS, "sales.csv")

print("=== Read CSV ===")
df = pd.read_csv(CSV_FILE, parse_dates=["date"])
print(df.head())
print(f"\nShape:  {df.shape}")
print(f"Dtypes:\n{df.dtypes}")

print("\n=== Inspect ===")
print(df.describe())
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nUnique categories: {df['category'].unique()}")
print(f"Unique regions:    {df['region'].unique()}")

print("\n=== Date Utilities (since date is parsed) ===")
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b")
df["day_of_week"] = df["date"].dt.day_name()
print(df[["date", "month", "month_name", "day_of_week"]].head(6))

print("\n=== Write to CSV ===")
output = "/tmp/sales_with_date_parts.csv"
df.to_csv(output, index=False)
print(f"Written to {output}")
