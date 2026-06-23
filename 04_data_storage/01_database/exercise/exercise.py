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
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS dim_category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    print("[schema] dim_category table created")

    # =========================================================================
    # Task 2: Load unique categories into dim_category
    # =========================================================================
    print("\n--- Task 2: Load categories from sales.csv ---")
    for name in df["category"].unique():
        conn.execute("INSERT OR IGNORE INTO dim_category (name) VALUES (?)", (name,))

    print("[dim] Categories loaded")

    # =========================================================================
    # Task 3: Build a category lookup dictionary
    # =========================================================================
    print("\n--- Task 3: Build category lookup dict ---")
    cursor = conn.execute("SELECT category_id, name FROM dim_category")
    categories = {name: category_id for category_id, name in cursor.fetchall()}

    print(f"Category lookup: {categories}")

    # =========================================================================
    # Task 4: Create fact_sales with FK to dim_category + revenue query
    # =========================================================================
    print("\n--- Task 4: Create fact_sales and query revenue by category ---")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS fact_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date TEXT NOT NULL,
        category_id INTEGER REFERENCES dim_category(category_id),
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        revenue REAL NOT NULL
    );
    """)

    sales_tuples = [
        (str(row["date"]), categories[row["category"]], int(row["quantity"]), float(row["unit_price"]), float(row["revenue"]))
        for _, row in df.iterrows()
    ]
    conn.executemany(
        "INSERT INTO fact_sales (sale_date, category_id, quantity, unit_price, revenue) VALUES (?,?,?,?,?)",
        sales_tuples
    )

    revenue_by_cat = pd.read_sql_query("""
        SELECT c.name, SUM(f.revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_category c ON f.category_id = c.category_id
        GROUP BY c.name
        ORDER BY total_revenue DESC
    """, conn)

    # Uncomment after completing Step C:
    print(revenue_by_cat)

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
