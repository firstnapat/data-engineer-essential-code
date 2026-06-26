"""
Demo: ROW_NUMBER vs RANK vs DENSE_RANK

สินค้าบางตัวใน category เดียวกันมีราคาเท่ากันเป๊ะ → เห็นความต่างชัดเจน
"""
import duckdb

# ---------------------------------------------------------------------------
# ข้อมูลตัวอย่าง — มีราคาซ้ำกันใน category เดียวกันตั้งใจ
# ---------------------------------------------------------------------------
PRODUCTS = [
    # Electronics — Laptop สองตัวราคาเท่ากัน
    ("P001", "Laptop Pro X",         "Electronics", 45000),
    ("P002", "Laptop Business Z",    "Electronics", 45000),  # ← ราคาเท่ากับ P001
    ("P003", "Monitor 27in",         "Electronics", 12000),
    ("P004", "Webcam HD",            "Electronics",  3500),
    ("P005", "Wireless Mouse",       "Electronics",   650),

    # Food — Chips สองตัวราคาเท่ากัน
    ("P006", "Lays Original 50g",    "Food",           35),
    ("P007", "Nestle Crunch 50g",    "Food",           35),  # ← ราคาเท่ากับ P006
    ("P008", "Pocky Chocolate",      "Food",           25),
    ("P009", "Oreo Mini",            "Food",           20),

    # Clothing — Shoes สองตัวราคาเท่ากัน
    ("P010", "Running Shoes A",      "Clothing",     2800),
    ("P011", "Running Shoes B",      "Clothing",     2800),  # ← ราคาเท่ากับ P010
    ("P012", "Sports Shirt",         "Clothing",      890),
    ("P013", "Compression Socks",    "Clothing",      350),
]

# ---------------------------------------------------------------------------
# สร้าง in-memory DuckDB แล้วยิง SQL
# ---------------------------------------------------------------------------
con = duckdb.connect()
con.execute("""
    CREATE TABLE products AS
    SELECT * FROM (VALUES
""" + ",\n        ".join(f"('{pid}', '{name}', '{cat}', {price})" for pid, name, cat, price in PRODUCTS) + """
    ) t(product_id, product_name, category, price)
""")

result = con.execute("""
    SELECT
        category,
        product_name,
        price,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS row_num,
        RANK()       OVER (PARTITION BY category ORDER BY price DESC) AS rnk,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS dense_rnk
    FROM products
    ORDER BY category, price DESC
""").fetchdf()

print(result.to_string(index=False))
