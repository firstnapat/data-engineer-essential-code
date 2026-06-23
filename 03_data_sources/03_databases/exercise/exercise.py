"""
Exercise: Databases — Seed, Query, and Aggregate with SQLite
Practice the seed → read (SQL) → inspect pattern from work_with_db.py

Uses SQLite (built-in, no extra setup needed).
Run: uv run 03_data_sources/03_databases/exercise/exercise.py
"""
import os
import sqlite3
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
DB_PATH = "/tmp/exercise_source.db"

# ---------------------------------------------------------------------------
# Task 1: Seed the database from sales.csv
# ---------------------------------------------------------------------------
print("--- Task 1: Seed SQLite database from sales.csv ---")

# TODO: Read sales.csv into a DataFrame, then write it to a SQLite database
#       at DB_PATH into a table called 'sales'.
# Steps:
#   1. pd.read_csv() to load sales.csv
#   2. sqlite3.connect(DB_PATH) to open a connection
#   3. df.to_sql("sales", conn, if_exists="replace", index=False)
# Hint: Use a `with` statement for the connection, as in work_with_db.py.

sales_path = os.path.join(DATASETS, "sales.csv")
# TODO: your code here

print(f"[seed] DB ready at {DB_PATH}")

# Quick verification: count rows in the table
with sqlite3.connect(DB_PATH) as conn:
    count = pd.read_sql_query("SELECT COUNT(*) AS n FROM sales", conn)["n"][0]
assert count == 55, f"Expected 55 rows in 'sales' table, got {count}"
print(f"✓ Task 1 passed — {count} rows seeded\n")


# ---------------------------------------------------------------------------
# Task 2: Write a reusable read() function
# ---------------------------------------------------------------------------
print("--- Task 2: Reusable read() function ---")


# TODO: Write a read() function that takes:
#   - db_path (str): path to the SQLite database file
#   - sql (str): the SQL query to execute
#   - params (tuple): optional query parameters, default ()
# It should return a DataFrame using pd.read_sql_query().
# Hint: This is the exact same pattern as read() in work_with_db.py.
def read(db_path: str, sql: str, params: tuple = ()) -> pd.DataFrame:
    ...  # TODO: replace with your code


# Verification: simple query
test_df = read(DB_PATH, "SELECT * FROM sales LIMIT 3")
assert len(test_df) == 3, f"Expected 3 rows, got {len(test_df)}"
assert "product" in test_df.columns, "Expected 'product' column"
print(test_df)
print("✓ Task 2 passed\n")


# ---------------------------------------------------------------------------
# Task 3: Top 3 products by total revenue
# ---------------------------------------------------------------------------
print("--- Task 3: Top 3 products by total revenue ---")

# TODO: Write a SQL query that:
#   - Groups by 'product'
#   - Sums the 'revenue' column (alias: total_revenue)
#   - Orders by total_revenue descending
#   - Limits to the top 3
# Then call read(DB_PATH, sql) to execute it.
# Hint: SELECT product, SUM(revenue) AS total_revenue
#       FROM sales GROUP BY product ORDER BY total_revenue DESC LIMIT 3

top3_sql = """
-- TODO: write your SQL here
"""
top3_df = read(DB_PATH, top3_sql)
print(top3_df)

# Verification
assert len(top3_df) == 3, f"Expected 3 rows, got {len(top3_df)}"
assert top3_df.iloc[0]["product"] == "Laptop Pro", \
    f"Expected 'Laptop Pro' as top product, got '{top3_df.iloc[0]['product']}'"
assert top3_df.iloc[0]["total_revenue"] == 805000, \
    f"Expected 805000 total revenue, got {top3_df.iloc[0]['total_revenue']}"
print("✓ Task 3 passed\n")


# ---------------------------------------------------------------------------
# Task 4: Parameterised query — Bangkok Electronics
# ---------------------------------------------------------------------------
print("--- Task 4: Parameterised query — Bangkok Electronics ---")

# TODO: Write a SQL query with ? placeholders that selects
#       date, product, quantity, revenue
#       from sales
#       where region = ? AND category = ?
# Then call read() with params=("Bangkok", "Electronics").
# Hint: This is the same pattern as the filtered query in work_with_db.py.

param_sql = """
-- TODO: write your SQL here with ? placeholders
"""
bangkok_electronics = read(DB_PATH, param_sql, params=("Bangkok", "Electronics"))
print(bangkok_electronics)

# Verification
assert len(bangkok_electronics) > 0, "Expected at least 1 row"
# All rows should be Bangkok + Electronics
for _, row in bangkok_electronics.iterrows():
    if "region" in bangkok_electronics.columns:
        assert row["region"] == "Bangkok", f"Expected Bangkok, got {row['region']}"
print(f"Found {len(bangkok_electronics)} Bangkok Electronics transactions")
print("✓ Task 4 passed\n")


# ---------------------------------------------------------------------------
# Task 5: Count transactions per region
# ---------------------------------------------------------------------------
print("--- Task 5: Transactions per region ---")

# TODO: Write a SQL query that:
#   - Counts the number of transactions per region (alias: txn_count)
#   - Groups by region
#   - Orders by txn_count descending
# Hint: SELECT region, COUNT(*) AS txn_count FROM sales
#       GROUP BY region ORDER BY txn_count DESC

region_sql = """
-- TODO: write your SQL here
"""
region_df = read(DB_PATH, region_sql)
print(region_df)

# Verification
assert len(region_df) >= 4, f"Expected at least 4 regions, got {len(region_df)}"
assert region_df.iloc[0]["region"] == "Bangkok", \
    f"Expected 'Bangkok' as top region, got '{region_df.iloc[0]['region']}'"
total_txns = region_df["txn_count"].sum()
assert total_txns == 55, f"Expected 55 total transactions, got {total_txns}"
print("✓ Task 5 passed\n")


print("=" * 50)
print("All tasks passed! 🎉")
