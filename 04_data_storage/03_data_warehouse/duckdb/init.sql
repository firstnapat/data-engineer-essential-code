-- =============================================================================
-- QuickMart — load new-raw CSVs into DuckDB
-- =============================================================================

CREATE OR REPLACE TABLE customers AS
SELECT * FROM read_csv_auto('/datasets/customers.csv', header = true);

CREATE OR REPLACE TABLE products AS
SELECT * FROM read_csv_auto('/datasets/products.csv', header = true);

CREATE OR REPLACE TABLE orders AS
SELECT * FROM read_csv_auto('/datasets/orders.csv', header = true);

CREATE OR REPLACE TABLE order_items AS
SELECT * FROM read_csv_auto('/datasets/order_items.csv', header = true);

CREATE OR REPLACE TABLE deliveries AS
SELECT * FROM read_csv_auto('/datasets/deliveries.csv', header = true);

-- =============================================================================
-- Demo table — ราคาซ้ำกันใน category เดียวกัน (ใช้สอน window functions)
-- =============================================================================

CREATE OR REPLACE TABLE products_demo (
    product_id   VARCHAR,
    product_name VARCHAR,
    category     VARCHAR,
    brand        VARCHAR,
    price        DOUBLE
);

INSERT INTO products_demo VALUES
-- Electronics — Laptop สองตัวราคาเท่ากัน
('D001', 'Laptop Pro X',       'Electronics', 'TechBrand',   45000),
('D002', 'Laptop Business Z',  'Electronics', 'OfficeBrand', 45000),  -- ราคาเท่ากับ D001
('D003', 'Monitor 27in',       'Electronics', 'DisplayTech', 12000),
('D004', 'Webcam HD',          'Electronics', 'TechBrand',    3500),
('D005', 'Wireless Mouse',     'Electronics', 'PeriphCo',      650),
-- Food — Chips สองตัวราคาเท่ากัน
('D006', 'Lays Original 50g',  'Food',        'Lays',            35),
('D007', 'Nestle Crunch 50g',  'Food',        'Nestle',          35),  -- ราคาเท่ากับ D006
('D008', 'Pocky Chocolate',    'Food',        'Glico',           25),
('D009', 'Oreo Mini',          'Food',        'Nabisco',         20),
-- Clothing — Shoes สองตัวราคาเท่ากัน
('D010', 'Running Shoes A',    'Clothing',    'SportWear',     2800),
('D011', 'Running Shoes B',    'Clothing',    'SportWear',     2800),  -- ราคาเท่ากับ D010
('D012', 'Sports Shirt',       'Clothing',    'SportWear',      890),
('D013', 'Compression Socks',  'Clothing',    'SportWear',      350);

-- =============================================================================
-- Quick sanity check
-- =============================================================================

SELECT 'customers'  AS tbl, count(*) AS rows FROM customers  UNION ALL
SELECT 'products'   AS tbl, count(*) AS rows FROM products   UNION ALL
SELECT 'orders'     AS tbl, count(*) AS rows FROM orders     UNION ALL
SELECT 'order_items'AS tbl, count(*) AS rows FROM order_items UNION ALL
SELECT 'deliveries' AS tbl, count(*) AS rows FROM deliveries  UNION ALL
SELECT 'products_demo' AS tbl, count(*) AS rows FROM products_demo
ORDER BY tbl;

CHECKPOINT;