"""
Exercise: Database Storage — Building a Category Dimension Table
Practice the concepts from storage_db.py (star schema with SQLite).
Run: uv run 04_data_storage/01_database/exercise/exercise.py
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "/tmp/exercise_warehouse.db"
DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")

# Remove old DB to start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Load sales data
df = pd.read_csv(os.path.join(DATASETS, "sales.csv"), parse_dates=["date"])
print(f"Loaded {len(df)} rows from sales.csv")
print(f"Unique categories: {sorted(df['category'].unique())}")

with sqlite3.connect(DB_PATH) as conn:

    # =========================================================================
    # Task 1: Create dim_category table
    # =========================================================================
    print("\n--- Task 1: Create dim_category table ---")
    # TODO: Use conn.executescript() to create a table called dim_category
    #       with columns:
    #         - category_id  INTEGER PRIMARY KEY AUTOINCREMENT
    #         - name         TEXT NOT NULL UNIQUE
    #       Use CREATE TABLE IF NOT EXISTS.

    print("[schema] dim_category table created")

    # =========================================================================
    # Task 2: Load unique categories into dim_category
    # =========================================================================
    print("\n--- Task 2: Load categories from sales.csv ---")
    # TODO: Get unique categories from df["category"] and insert each one
    #       into dim_category using:
    #         conn.execute("INSERT OR IGNORE INTO dim_category (name) VALUES (?)", (name,))
    #       Hint: loop over df["category"].unique()

    print("[dim] Categories loaded")

    # =========================================================================
    # Task 3: Build a category lookup dictionary
    # =========================================================================
    print("\n--- Task 3: Build category lookup dict ---")
    # TODO: Query dim_category to build a dictionary mapping name -> category_id.
    #       Use: conn.execute("SELECT category_id, name FROM dim_category")
    #       Store the result in a variable called `categories` (dict).
    #       Example result: {"Electronics": 1, "Furniture": 2, ...}
    categories = {}  # Replace with your code

    print(f"Category lookup: {categories}")

    # =========================================================================
    # Task 4: Create fact_sales with FK to dim_category + revenue query
    # =========================================================================
    print("\n--- Task 4: Create fact_sales and query revenue by category ---")
    # TODO (Step A): Use conn.executescript() to create fact_sales table with:
    #         - id           INTEGER PRIMARY KEY AUTOINCREMENT
    #         - sale_date    TEXT NOT NULL
    #         - category_id  INTEGER REFERENCES dim_category(category_id)
    #         - quantity     INTEGER NOT NULL
    #         - unit_price   REAL NOT NULL
    #         - revenue      REAL NOT NULL

    # TODO (Step B): Insert rows from df into fact_sales.
    #       For each row, look up the category_id using your `categories` dict.
    #       Use conn.executemany() with this SQL:
    #         "INSERT INTO fact_sales (sale_date, category_id, quantity, unit_price, revenue) VALUES (?,?,?,?,?)"
    #       Build a list of tuples: (str(row["date"]), categories[row["category"]],
    #                                int(row["quantity"]), float(row["unit_price"]),
    #                                float(row["revenue"]))

    # TODO (Step C): Write a SQL query that JOINs fact_sales with dim_category
    #       to get total revenue by category name. Use pd.read_sql_query().
    #       SQL hint:
    #         SELECT c.name, SUM(f.revenue) AS total_revenue
    #         FROM fact_sales f
    #         JOIN dim_category c ON f.category_id = c.category_id
    #         GROUP BY c.name
    #         ORDER BY total_revenue DESC
    #       Store the result in `revenue_by_cat`.

    # Uncomment after completing Step C:
    # print(revenue_by_cat)

    # =========================================================================
    # Task 5: Verification
    # =========================================================================
    print("\n--- Task 5: Verification ---")
    # TODO: Use pd.read_sql_query("SELECT * FROM dim_category", conn) to read
    #       the dim_category table into a DataFrame called `verify_df`.
    #       Then verify it has exactly 4 rows.
    verify_df = pd.read_sql_query("SELECT * FROM dim_category", conn)
    print(f"dim_category rows: {len(verify_df)}")
    print(verify_df)

    assert len(verify_df) == 4, f"Expected 4 categories, got {len(verify_df)}"
    assert set(verify_df["name"]) == {"Electronics", "Furniture", "Clothing", "Accessories"}, \
        f"Unexpected categories: {set(verify_df['name'])}"
    assert len(categories) == 4, f"Lookup dict should have 4 entries, got {len(categories)}"

    # Verify fact_sales has the right number of rows
    fact_count = pd.read_sql_query("SELECT COUNT(*) AS cnt FROM fact_sales", conn)
    assert fact_count["cnt"][0] == len(df), \
        f"Expected {len(df)} fact rows, got {fact_count['cnt'][0]}"

    print("\n✅ All verifications passed!")
