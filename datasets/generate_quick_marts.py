"""
Generate QuickMart mock data with realistic dirty-data issues.
Output -> datasets/new-raw/*.csv  (the RAW layer students must clean in staging)

Dirty issues injected on purpose (so staging/clean/validate tasks have real work):
  customers   - duplicate rows, blank/invalid email, sub_tier case mess, blank name
  products    - duplicate rows, price=0/negative, blank category, price outlier
  orders      - duplicate rows, amount<=0, status case mess, orphan customer_id, future date
  order_items - duplicate rows, qty=0, wrong subtotal, unit_price outlier/negative
  deliveries  - duplicate rows, parcels=0, parcels outlier, blank vehicle_id

Run: uv run datasets/generate_quick_marts.py
"""
import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "new-raw")
os.makedirs(OUT_DIR, exist_ok=True)

# ── config ────────────────────────────────────────────────────────────────────
NUM_CUSTOMERS  = 1000
NUM_PRODUCTS   = 50
NUM_ORDERS     = 3000
NUM_DELIVERIES = 1000

first_names = ["Wanna", "Burin", "Siriporn", "Itthipat", "Kamon",
               "Fah", "Narin", "Pattara", "Somchai", "Somsri"]
last_names  = ["Klinkaew", "Udomsak", "Choosri", "Dingam", "Fongfah",
               "Mongkol", "Ongkham", "Panya", "Rakdee", "Sukjai"]
sub_tiers   = ["Bronze", "Silver", "Gold", "Platinum"]
categories  = ["Beverage", "Snack", "Personal Care", "Household", "Food"]
brands      = ["Nestle", "Singha", "PepsiCo", "Tao Kae Noi", "Colgate",
               "Unilever", "Mama", "CP", "Lays", "Oishi"]
vehicles    = ["TRUCK-A", "TRUCK-B", "TRUCK-C", "TRUCK-D", "VAN-1", "VAN-2"]
order_statuses = ["completed", "completed", "completed", "completed",
                  "processing", "cancelled"]


def rand_date(start_year=2022, end_year=2023):
    start = datetime(start_year, 1, 1)
    delta = (datetime(end_year, 12, 31) - start).days
    return start + timedelta(days=random.randrange(delta))


# ── 1. generate clean base data ───────────────────────────────────────────────

customers = []
for i in range(NUM_CUSTOMERS):
    cid   = 1001 + i
    name  = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"{name.replace(' ', '.').lower()}@email.com"
    tier  = random.choice(sub_tiers)
    created = rand_date(2021, 2023).strftime("%Y-%m-%d")
    customers.append([cid, name, email, tier, created])

products = []
for i in range(NUM_PRODUCTS):
    pid   = 3001 + i
    cat   = random.choice(categories)
    brand = random.choice(brands)
    name  = f"{brand} Product {pid}"
    price = round(random.uniform(15.0, 350.0), 2)
    products.append([pid, name, cat, brand, price])

orders      = []
order_items = []
item_id     = 5001

for i in range(NUM_ORDERS):
    oid    = 4001 + i
    cid    = random.choice(customers)[0]
    odate  = rand_date(2022, 2023).strftime("%Y-%m-%d")
    status = random.choice(order_statuses)
    total  = 0.0
    for _ in range(random.randint(1, 5)):
        prod       = random.choice(products)
        pid        = prod[0]
        unit_price = prod[4]
        qty        = random.randint(1, 10)
        subtotal   = round(qty * unit_price, 2)
        total     += subtotal
        order_items.append([item_id, oid, pid, qty, unit_price, subtotal])
        item_id   += 1
    orders.append([oid, cid, odate, status, round(total, 2)])

deliveries = []
d_start = datetime(2023, 1, 1)
for i in range(NUM_DELIVERIES):
    did     = 6001 + i
    ddate   = (d_start + timedelta(days=(i // 5))).strftime("%Y-%m-%d")
    vehicle = random.choice(vehicles)
    parcels = random.randint(50, 300)
    deliveries.append([did, ddate, vehicle, parcels])


# ── 2. inject dirty data ──────────────────────────────────────────────────────

def pick(lst, n):
    """Return n random copies of rows from lst (copies, so edits don't alias)."""
    return [list(r) for r in random.choices(lst, k=n)]


# ── customers ──
customers += pick(customers, 40)                       # exact duplicates
for r in pick(customers, 20):                          # blank email
    r[2] = ""
    customers.append(r)
for r in pick(customers, 10):                          # invalid email
    base = r[1].replace(" ", ".")
    r[2] = random.choice([base, f"{base}@", "N/A", "null"])
    customers.append(r)
for r in pick(customers, 15):                          # sub_tier case mess
    r[3] = random.choice(["gold", "GOLD", "platinum", "SILVER", "silver", "bronze"])
    customers.append(r)
for r in pick(customers, 5):                           # blank name
    r[1] = ""
    customers.append(r)
random.shuffle(customers)

# ── products ──
products += pick(products, 8)                          # exact duplicates
for r in pick(products, 3):                            # price = 0
    r[4] = 0.0
    products.append(r)
for r in pick(products, 2):                            # negative price
    r[4] = round(random.uniform(-200.0, -5.0), 2)
    products.append(r)
for r in pick(products, 2):                            # blank category
    r[2] = ""
    products.append(r)
for r in pick(products, 2):                            # price outlier
    r[4] = 99999.0
    products.append(r)
random.shuffle(products)

# ── orders ──
orders += pick(orders, 120)                            # exact duplicates
for r in pick(orders, 40):                             # amount = 0
    r[4] = 0.0
    orders.append(r)
for r in pick(orders, 20):                             # negative amount
    r[4] = round(random.uniform(-5000.0, -1.0), 2)
    orders.append(r)
for r in pick(orders, 30):                             # status case mess
    r[3] = random.choice(["Completed", "COMPLETED", "Processing",
                          "Cancelled", "CANCELLED", "canceled"])
    orders.append(r)
for r in pick(orders, 15):                             # orphan customer_id
    r[1] = random.choice([9001, 9002, 9003, 9999])
    orders.append(r)
for r in pick(orders, 10):                             # future order_date
    r[2] = rand_date(2025, 2026).strftime("%Y-%m-%d")
    orders.append(r)
random.shuffle(orders)

# ── order_items ──
order_items += pick(order_items, 200)                  # exact duplicates
for r in pick(order_items, 50):                        # qty = 0
    r[3] = 0
    order_items.append(r)
for r in pick(order_items, 40):                        # subtotal != qty*unit_price
    r[5] = round(r[5] * random.uniform(0.5, 1.8), 2)
    order_items.append(r)
for r in pick(order_items, 10):                        # unit_price outlier
    r[4] = 99999.0
    r[5] = round(r[3] * 99999.0, 2)
    order_items.append(r)
for r in pick(order_items, 10):                        # negative unit_price
    r[4] = round(random.uniform(-500.0, -1.0), 2)
    r[5] = round(r[3] * r[4], 2)
    order_items.append(r)
random.shuffle(order_items)

# ── deliveries ──
deliveries += pick(deliveries, 40)                     # exact duplicates
for r in pick(deliveries, 20):                         # parcels = 0
    r[3] = 0
    deliveries.append(r)
for r in pick(deliveries, 5):                          # parcels outlier
    r[3] = random.choice([9999, 10000, 15000])
    deliveries.append(r)
for r in pick(deliveries, 10):                         # blank vehicle_id
    r[2] = ""
    deliveries.append(r)
random.shuffle(deliveries)


# ── 3. write CSVs ─────────────────────────────────────────────────────────────

def write_csv(name, header, data):
    path = os.path.join(OUT_DIR, f"{name}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)
    print(f"  {name}.csv  ->  {len(data)} rows")

print("Generating QuickMart dirty raw data into datasets/new-raw/ ...")
write_csv("customers",   ["customer_id", "customer_name", "email", "sub_tier", "created_at"],         customers)
write_csv("products",    ["product_id", "product_name", "category", "brand", "price"],                 products)
write_csv("orders",      ["order_id", "customer_id", "order_date", "status", "amount"],                orders)
write_csv("order_items", ["order_item_id", "order_id", "product_id", "qty", "unit_price", "subtotal"], order_items)
write_csv("deliveries",  ["delivery_id", "delivery_date", "vehicle_id", "parcels_delivered"],          deliveries)
print("Done.")
