import pandas as pd
import os

# A pandas Series is a 1-D labeled array — one DataFrame column is a Series.
# (Conceptually this comes before the DataFrame; kept here to avoid renumbering.)

# creating a Series
print("=== Creating a Series ===")
s = pd.Series([10, 20, 30, 40])
print(s)
print(f"values: {s.values}, dtype: {s.dtype}")

# custom index — labels instead of positions
print("\n=== Custom Index ===")
prices = pd.Series([35000, 650, 8500], index=["Laptop", "Mouse", "Desk"])
print(prices)

# access by label (.loc) vs position (.iloc)
print("\n=== Label vs Position ===")
print(f".loc['Mouse']: {prices.loc['Mouse']}")
print(f".iloc[0]:      {prices.iloc[0]}")
print(f"slice .iloc[:2]:\n{prices.iloc[:2]}")

# vectorized operations — no loops needed
print("\n=== Vectorized Operations ===")
print(f"prices * 1.07 (add VAT):\n{(prices * 1.07).round(0)}")
print(f"prices > 1000:\n{prices > 1000}")

# value_counts — frequency of each value
print("\n=== value_counts ===")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../datasets/sales.csv"))
print(df["region"].value_counts())

# map — element-wise replacement via dict or function
print("\n=== map ===")
codes = df["region"].map({"Bangkok": "BKK", "Phuket": "HKT", "Chiang Mai": "CNX"})
print(codes.value_counts())

# apply — run a function on each element
print("\n=== apply ===")
tier = df["revenue"].apply(lambda r: "high" if r >= 50000 else "normal")
print(tier.value_counts())

# missing data — isna / fillna
print("\n=== Missing Data ===")
with_gaps = pd.Series([1.0, None, 3.0, None, 5.0])
print(f"isna():\n{with_gaps.isna()}")
print(f"fillna(0):\n{with_gaps.fillna(0)}")
print(f"mean (skips NaN): {with_gaps.mean()}")

# a DataFrame column IS a Series
print("\n=== Series <-> DataFrame ===")
col = df["revenue"]
print(f"type(df['revenue']): {type(col).__name__}")
print(f"describe():\n{col.describe().round(2)}")
