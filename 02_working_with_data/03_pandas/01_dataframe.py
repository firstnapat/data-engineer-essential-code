import pandas as pd
import numpy as np

print("=== Creating a DataFrame ===")
data = {
    "name":   ["Alice", "Bob", "Charlie", "Diana"],
    "age":    [25, 30, 35, 28],
    "city":   ["Bangkok", "Chiang Mai", "Bangkok", "Phuket"],
    "salary": [50000, 65000, 72000, 58000],
}
df = pd.DataFrame(data)
print(df)

print("\n=== Basic Info ===")
print(f"Shape:   {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Index:   {list(df.index)}")
print(f"\nData types:\n{df.dtypes}")

print("\n=== head / tail / info / describe ===")
print(df.head(2))
print(df.tail(2))
df.info()
print(df.describe())

print("\n=== Accessing Data ===")
print(df["name"])                     # column as Series
print(df[["name", "salary"]])         # multiple columns
print(df.loc[0])                      # row by label
print(df.iloc[-1])                    # row by position
print(df.loc[df["city"] == "Bangkok"])# boolean filter

print("\n=== Adding / Modifying Columns ===")
df["bonus"] = df["salary"] * 0.1
df["total"] = df["salary"] + df["bonus"]
df["seniority"] = df["age"].apply(lambda a: "senior" if a >= 30 else "junior")
print(df)
