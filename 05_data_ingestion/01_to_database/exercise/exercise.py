"""
Exercise: Data Ingestion to Database — Build a CSV-to-SQLite Star Schema Pipeline
Practice the concepts from load_to_database.py.

You will build a pipeline that:
  1. Extracts data from sales.csv
  2. Validates it against a required schema
  3. Creates a star schema (dim_product + fact_sales) in SQLite
  4. Loads the data into the schema
  5. Queries the DB to verify correctness

Run: uv run 05_data_ingestion/01_to_database/exercise/exercise.py
"""
import os
import sqlite3
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../../datasets")
DB_PATH = "/tmp/exercise_ingestion.db"

REQUIRED_COLUMNS = {"date", "product", "category", "quantity", "unit_price", "revenue", "region"}


# ── Task 1: Extract ─────────────────────────────────────────────────────────
# Write an extract() function that reads sales.csv into a DataFrame.
# - Use pd.read_csv with parse_dates=["date"]
# - Print the row count in the format: [extract] <N> rows from sales.csv
# - Return the DataFrame
def extract(source: str) -> pd.DataFrame:
    # TODO: Read the CSV file with date parsing and return the DataFrame
    pass


# ── Task 2: Validate ────────────────────────────────────────────────────────
# Write a validate() function that checks two things:
#   (a) All REQUIRED_COLUMNS exist in the DataFrame
#       Hint: use set difference — REQUIRED_COLUMNS - set(df.columns)
#       Raise ValueError(f"missing columns: {missing}") if any are missing
#   (b) No nulls in quantity, unit_price, or revenue
#       Hint: df[["quantity", "unit_price", "revenue"]].isnull().any().any()
#       Raise ValueError("numeric fields contain nulls") if there are nulls
# Print "[validate] schema OK" if all checks pass, then return the DataFrame.
def validate(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: Check for missing columns
    # TODO: Check for nulls in numeric fields
    # TODO: Print success message and return df
    pass


# ── Task 3: Create Schema ───────────────────────────────────────────────────
# Write a create_schema() function that creates TWO tables using conn.executescript():
#
#   dim_product:
#     product_id  INTEGER PRIMARY KEY AUTOINCREMENT
#     name        TEXT NOT NULL UNIQUE
#     category    TEXT NOT NULL
#
#   fact_sales:
#     id          INTEGER PRIMARY KEY AUTOINCREMENT
#     sale_date   TEXT NOT NULL
#     product_id  INTEGER REFERENCES dim_product(product_id)
#     quantity    INTEGER NOT NULL
#     unit_price  REAL NOT NULL
#     revenue     REAL NOT NULL
#
# Use CREATE TABLE IF NOT EXISTS. Print "[schema] tables ready".
def create_schema(conn: sqlite3.Connection) -> None:
    # TODO: Execute DDL to create dim_product and fact_sales tables
    pass


# ── Task 4: Load ────────────────────────────────────────────────────────────
# Write a load() function that:
#   Step A — Insert unique products into dim_product using INSERT OR IGNORE
#     Hint: df[["product", "category"]].drop_duplicates().values gives you rows
#   Step B — Build a lookup dict: {product_name: product_id}
#     Hint: conn.execute("SELECT product_id, name FROM dim_product")
#   Step C — Build a list of fact_sales tuples from the DataFrame
#     Each tuple: (sale_date, product_id, quantity, unit_price, revenue)
#   Step D — Insert all rows using conn.executemany()
# Print "[load] <N> fact rows loaded".
def load(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    # TODO: Step A — insert unique products
    # TODO: Step B — build product name → id lookup
    # TODO: Step C — build fact row tuples
    # TODO: Step D — executemany into fact_sales
    pass


# ── Task 5: Run the Pipeline & Verify ───────────────────────────────────────
if __name__ == "__main__":
    print("--- Task 1: Extract ---")
    df = extract(os.path.join(DATASETS, "sales.csv"))
    assert df is not None, "extract() should return a DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"
    print(f"✓ Extracted {len(df)} rows\n")

    print("--- Task 2: Validate ---")
    df = validate(df)
    assert df is not None, "validate() should return the DataFrame"
    print("✓ Validation passed\n")

    # Fresh DB each run
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        print("--- Task 3: Create Schema ---")
        create_schema(conn)
        # Verify tables exist
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()]
        assert "dim_product" in tables, "dim_product table should exist"
        assert "fact_sales" in tables, "fact_sales table should exist"
        print("✓ Schema created\n")

        print("--- Task 4: Load ---")
        load(conn, df)
        fact_count = conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
        assert fact_count == len(df), f"Expected {len(df)} fact rows, got {fact_count}"
        print(f"✓ Loaded {fact_count} rows into fact_sales\n")

        print("--- Task 5: Verify — Revenue by Category ---")
        # TODO: Write a SQL query that JOINs fact_sales with dim_product
        #       to get total revenue by category, ordered by revenue DESC.
        # Hint: SELECT p.category, SUM(f.revenue) AS revenue
        #       FROM fact_sales f
        #       JOIN dim_product p ON f.product_id = p.product_id
        #       GROUP BY p.category ORDER BY revenue DESC
        verify = pd.read_sql_query(
            # TODO: Replace this string with the correct SQL query
            "SELECT 1",
            conn,
        )
        print(verify)
        assert "category" in verify.columns, "Query should return a 'category' column"
        assert "revenue" in verify.columns, "Query should return a 'revenue' column"
        print("✓ Verification query works!")
