"""
Exercise: File Formats — Read, Inspect, and Clean multiple file types
Practice the read → inspect → clean pattern from the teaching scripts:
  work_with_csv.py, work_with_json.py, work_with_parquet.py, work_with_text.py

Run: uv run 03_data_sources/01_files/exercise/exercise.py
"""
import os
import re
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

# ---------------------------------------------------------------------------
# Task 1: Read products.json and flatten the nested 'products' array
# ---------------------------------------------------------------------------
print("--- Task 1: Read and flatten products.json ---")

# TODO: Use pd.read_json() to load products.json, then pd.json_normalize()
#       to flatten the nested 'products' array into a flat DataFrame.
# Hint: raw = pd.read_json(path) gives you the top-level keys as columns.
#       The 'products' column contains the nested list of dicts.
#       pd.json_normalize(raw["products"]) flattens it.
products_path = os.path.join(DATASETS, "products.json")
raw_products = pd.read_json(products_path)
products_df = pd.json_normalize(raw_products["products"])

print(f"products shape: {products_df.shape}")
print(products_df.head(3))

# Verification
assert products_df.shape == (13, 6), f"Expected (13, 6), got {products_df.shape}"
assert "name" in products_df.columns, "Expected 'name' column after flattening"
print("✓ Task 1 passed\n")


# ---------------------------------------------------------------------------
# Task 2: Read sales.csv with date parsing
# ---------------------------------------------------------------------------
print("--- Task 2: Read sales.csv and parse dates ---")

# TODO: Read sales.csv using pd.read_csv() with the parse_dates parameter
#       to automatically convert the 'date' column to datetime.
# Hint: parse_dates=["date"]
sales_path = os.path.join(DATASETS, "sales.csv")
sales_df = pd.read_csv(sales_path, parse_dates=["date"])

earliest = sales_df["date"].min()
latest = sales_df["date"].max()
print(f"Date range: {earliest.date()} to {latest.date()}")

# Verification
assert str(sales_df["date"].dtype).startswith("datetime64"), \
    f"Expected datetime64, got {sales_df['date'].dtype}"
assert str(earliest.date()) == "2024-01-02", f"Unexpected earliest date: {earliest}"
assert str(latest.date()) == "2024-03-30", f"Unexpected latest date: {latest}"
print("✓ Task 2 passed\n")


# ---------------------------------------------------------------------------
# Task 3: Write a clean() function for sales.csv
# ---------------------------------------------------------------------------
print("--- Task 3: Clean function for sales data ---")


# TODO: Complete the clean() function below.
#   1. Copy the DataFrame (df.copy())
#   2. Strip whitespace from 'product' and 'region' columns using .str.strip()
#   3. Drop duplicates with .drop_duplicates()
#   4. Convert 'date' column to datetime with pd.to_datetime()
#   5. Return the cleaned DataFrame
def clean(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    df_clean["product"] = df_clean["product"].str.strip()
    df_clean["region"] = df_clean["region"].str.strip()
    df_clean = df_clean.drop_duplicates()
    df_clean["date"] = pd.to_datetime(df_clean["date"])
    return df_clean


raw_sales = pd.read_csv(sales_path)
cleaned = clean(raw_sales)

print(f"Before clean: date dtype = {raw_sales['date'].dtype}")
print(f"After  clean: date dtype = {cleaned['date'].dtype}, {len(cleaned)} rows")

# Verification
assert str(cleaned["date"].dtype).startswith("datetime64"), \
    f"Expected datetime64 after clean, got {cleaned['date'].dtype}"
assert cleaned["product"].str.contains(r"^\s|\s$", regex=True).sum() == 0, \
    "Product column still has leading/trailing whitespace"
assert cleaned["region"].str.contains(r"^\s|\s$", regex=True).sum() == 0, \
    "Region column still has leading/trailing whitespace"
print("✓ Task 3 passed\n")


# ---------------------------------------------------------------------------
# Task 4: CSV → Parquet round-trip
# ---------------------------------------------------------------------------
print("--- Task 4: CSV → Parquet → verify dtypes preserved ---")

parquet_path = "/tmp/exercise_sales.parquet"

# TODO: Step A — Read sales.csv with parse_dates=["date"], then write to
#       Parquet using .to_parquet(parquet_path, index=False).
# Hint: This is the same pattern as _prepare_sample() in work_with_parquet.py.

df_to_parquet = pd.read_csv(sales_path, parse_dates=["date"])
df_to_parquet.to_parquet(parquet_path, index=False)

# TODO: Step B — Read the Parquet file back with pd.read_parquet() and
#       verify that the date column survived as datetime64.

parquet_df = pd.read_parquet(parquet_path)

print(f"Parquet dtypes:\n{parquet_df.dtypes}")
print(f"Parquet shape: {parquet_df.shape}")

# Verification
assert str(parquet_df["date"].dtype).startswith("datetime64"), \
    f"Expected datetime64 in Parquet, got {parquet_df['date'].dtype}"
assert parquet_df.shape[0] == 54, f"Expected 54 rows, got {parquet_df.shape[0]}"
print("✓ Task 4 passed\n")


# ---------------------------------------------------------------------------
# Task 5 (BONUS): Parse revenue from sample.txt using regex
# ---------------------------------------------------------------------------
print("--- Task 5 (BONUS): Parse 'Total Revenue' from sample.txt ---")

# TODO: Read datasets/sample.txt, find the line containing 'Total Revenue',
#       and extract the number as an integer.
# Hint: The line looks like "Total Revenue: 850,250 THB"
#       Use re.search() with a pattern like r"Total Revenue:\s*([\d,]+)\s*THB"
#       Then remove commas and convert to int.
sample_path = os.path.join(DATASETS, "sample.txt")

with open(sample_path, "r", encoding="utf-8") as f:
    text_content = f.read()

match = re.search(r"Total Revenue:\s*([\d,]+)\s*THB", text_content)
total_revenue = int(match.group(1).replace(",", "")) if match else 0

print(f"Total Revenue = {total_revenue:,} THB")

# Verification
assert total_revenue == 850250, f"Expected 850250, got {total_revenue}"
print("✓ Task 5 passed\n")


print("=" * 50)
print("All tasks passed! 🎉")
