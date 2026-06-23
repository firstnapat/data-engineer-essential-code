import pandas as pd
import os

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")

# load sales (fact table) and products (dimension table)
sales = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
products = pd.read_json(os.path.join(DATASETS, "products.json")).get("products")
products = pd.json_normalize(products)   # flatten list-of-dicts into a DataFrame

print("=== Two Tables ===")
print(f"sales:    {sales.shape}  columns={list(sales.columns)}")
print(f"products: {products.shape}  columns={list(products.columns)}")

# inner merge — keep only rows with a match in both tables
print("\n=== Inner Merge (sales x products) ===")
# sales.product matches products.name; bring in supplier and stock
enriched = sales.merge(
    products[["name", "supplier", "stock"]],
    left_on="product",
    right_on="name",
    how="inner",
).drop(columns="name")
print(enriched[["product", "supplier", "stock", "revenue"]].head())
print(f"rows: {len(sales)} sales -> {len(enriched)} after inner merge")

# join types — inner / left / right / outer on small tables
print("\n=== Join Types (small demo tables) ===")
left = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Carol"]})
right = pd.DataFrame({"id": [2, 3, 4], "city": ["Bangkok", "Phuket", "Chiang Mai"]})
print(f"inner:\n{left.merge(right, on='id', how='inner')}")
print(f"\nleft:\n{left.merge(right, on='id', how='left')}")
print(f"\nright:\n{left.merge(right, on='id', how='right')}")
print(f"\nouter:\n{left.merge(right, on='id', how='outer')}")

# indicator — see where each row came from
print("\n=== indicator=True ===")
print(left.merge(right, on="id", how="outer", indicator=True))

# suffixes — disambiguate overlapping column names
print("\n=== suffixes for overlapping columns ===")
q1 = pd.DataFrame({"region": ["BKK", "HKT"], "revenue": [100, 200]})
q2 = pd.DataFrame({"region": ["BKK", "HKT"], "revenue": [150, 250]})
print(q1.merge(q2, on="region", suffixes=("_q1", "_q2")))

# concat — stack rows vertically (union)
print("\n=== concat (vertical / rows) ===")
jan = sales[sales["date"].dt.month == 1]
feb = sales[sales["date"].dt.month == 2]
stacked = pd.concat([jan, feb], ignore_index=True)
print(f"jan={len(jan)} + feb={len(feb)} -> concat={len(stacked)}")

# concat — join columns horizontally
print("\n=== concat (horizontal / columns) ===")
a = pd.DataFrame({"x": [1, 2, 3]})
b = pd.DataFrame({"y": [4, 5, 6]})
print(pd.concat([a, b], axis=1))

# practical: revenue by supplier (needs the merge above)
print("\n=== Practical: Revenue by Supplier ===")
by_supplier = (
    enriched.groupby("supplier")["revenue"].sum().sort_values(ascending=False)
)
print(by_supplier.astype(int))
