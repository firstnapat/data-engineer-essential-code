"""
Generate raw CSV datasets for e-commerce scenario.
Intentional data quality issues are embedded for cleaning/transformation practice.

Issues per file:
  products_raw.csv   — 3 duplicate product_id rows, category inconsistent case
  users_raw.csv      — 5 duplicate emails (diff user_id), phone format mixed/null
  addresses_raw.csv  — postal_code missing ~8%, province inconsistent case
  orders_raw.csv     — 8 duplicate order rows, total_amount sometimes wrong
  order_items_raw.csv — subtotal != quantity*unit_price for ~8% of rows
  transports_raw.csv — tracking_number null for some shipped orders,
                       delivered_at set but status still "in_transit"
"""
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "Somsak", "Malee", "Wichai", "Napa", "Anucha", "Pimjai", "Thana",
    "Rattana", "Kitti", "Manat", "Anchalee", "Chonthicha", "Pornthip",
    "Parinya", "Wanna", "Somchai", "Siriporn", "Nattha", "Burin", "Lalita",
    "Chaiwat", "Duangjai", "Ekkarat", "Fah", "Gamon", "Hathai", "Itthipat",
    "Jirapat", "Kamon", "Ladda", "Monthon", "Narin", "Orapin", "Pattara",
    "Rawin", "Saowalak", "Tawan", "Ubon", "Vipada", "Warut",
]

LAST_NAMES = [
    "Jaidee", "Rakdee", "Suksawat", "Pongthai", "Charoensuk", "Meesuk",
    "Dingam", "Saengthong", "Thongkham", "Sainam", "Bunnak", "Choosri",
    "Daengdee", "Ekpracha", "Fongfah", "Gritsana", "Hengsawat", "Inchan",
    "Jankham", "Klinkaew", "Lertchai", "Mongkol", "Nakorn", "Ongkham",
    "Panya", "Raksit", "Sawangsri", "Theparat", "Udomsak", "Wongsri",
]

PROVINCES = [
    "Bangkok", "Chiang Mai", "Phuket", "Khon Kaen",
    "Nakhon Ratchasima", "Chonburi", "Udon Thani", "Songkhla",
]

DISTRICTS = {
    "Bangkok":            ["Watthana", "Chatuchak", "Bang Rak", "Sathon", "Huai Khwang"],
    "Chiang Mai":         ["Mueang", "San Kamphaeng", "Hang Dong", "Mae Rim"],
    "Phuket":             ["Mueang", "Thalang", "Kathu"],
    "Khon Kaen":          ["Mueang", "Chonnabot", "Ban Phai", "Ubolratana"],
    "Nakhon Ratchasima":  ["Mueang", "Pak Chong", "Sikhio", "Chok Chai"],
    "Chonburi":           ["Mueang", "Bang Lamung", "Si Racha", "Phan Thong"],
    "Udon Thani":         ["Mueang", "Ban Dung", "Kumphawapi"],
    "Songkhla":           ["Mueang", "Hat Yai", "Chana"],
}

POSTAL_CODES = {
    "Bangkok":            ["10110", "10900", "10310", "10120", "10400"],
    "Chiang Mai":         ["50000", "50130", "50230", "50180"],
    "Phuket":             ["83000", "83110", "83120"],
    "Khon Kaen":          ["40000", "40180", "40110"],
    "Nakhon Ratchasima":  ["30000", "30130", "30140"],
    "Chonburi":           ["20000", "20150", "20110"],
    "Udon Thani":         ["41000", "41190", "41110"],
    "Songkhla":           ["90000", "90110", "90120"],
}

STREETS = ["Sukhumvit", "Silom", "Rama IV", "Phahon Yothin",
           "Charoen Nakhon", "Ratchadaphisek", "Lat Phrao", "Nawamin"]

# (product_id, name, category_clean, brand, unit_price, stock_qty)
PRODUCTS_CLEAN = [
    (3001, "iPhone 15 Pro",          "Electronics", "Apple",             42900.00, 50),
    (3002, "Samsung Galaxy S24",     "Electronics", "Samsung",           35900.00, 40),
    (3003, "iPad Air 5",             "Electronics", "Apple",             21900.00, 30),
    (3004, "MacBook Air M2",         "Electronics", "Apple",             52900.00, 20),
    (3005, "Sony WH-1000XM5",        "Electronics", "Sony",              10900.00, 60),
    (3006, "Nike Air Max 270",       "Clothing",    "Nike",               4500.00, 80),
    (3007, "Adidas Ultraboost 22",   "Clothing",    "Adidas",             5200.00, 70),
    (3008, "Levi's 501 Jeans",       "Clothing",    "Levi's",             1990.00,100),
    (3009, "Uniqlo AIRism T-Shirt",  "Clothing",    "Uniqlo",              390.00,200),
    (3010, "H&M Slim Fit Chinos",    "Clothing",    "H&M",                 890.00,150),
    (3011, "Dyson V15 Vacuum",       "Electronics", "Dyson",             24900.00, 15),
    (3012, "Nescafe Gold 200g",      "Food",        "Nestle",              320.00,300),
    (3013, "Lay's Classic 75g",      "Food",        "PepsiCo",              35.00,500),
    (3014, "Meji Milk 1L",           "Food",        "Meji",                 52.00,400),
    (3015, "Whey Protein 2kg",       "Sports",      "Optimum Nutrition",  2900.00, 45),
    (3016, "Yoga Mat 6mm",           "Sports",      "Decathlon",           590.00, 80),
    (3017, "Kettlebell 16kg",        "Sports",      "Rogue",              1290.00, 30),
    (3018, "Python Crash Course",    "Books",       "No Starch Press",     890.00, 60),
    (3019, "Atomic Habits",          "Books",       "Penguin",             490.00, 90),
    (3020, "Data Engineering Book",  "Books",       "O'Reilly",           1290.00, 40),
    (3021, "Cetaphil Face Wash",     "Beauty",      "Cetaphil",            490.00,120),
    (3022, "Sunscreen SPF50+",       "Beauty",      "Biore",               289.00,150),
    (3023, "Vitamin C Serum 30ml",   "Beauty",      "Some By Mi",          650.00, 80),
    (3024, "Logitech MX Master 3",   "Electronics", "Logitech",           3900.00, 55),
    (3025, "Dell 27\" Monitor",      "Electronics", "Dell",               8900.00, 25),
    (3026, "HDMI Cable 2m",          "Electronics", "Ugreen",              290.00,200),
    (3027, "Running Shorts",         "Clothing",    "Nike",                890.00,100),
    (3028, "Basketball",             "Sports",      "Spalding",           1490.00, 35),
    (3029, "Green Tea 50 bags",      "Food",        "Lipton",              129.00,250),
    (3030, "Collagen Powder 200g",   "Beauty",      "Meji",                890.00, 70),
]

CARRIERS = ["Kerry Express", "Thailand Post", "Flash Express", "J&T Express", "DHL"]
ORDER_STATUSES = ["pending", "processing", "completed", "cancelled", "refunded"]


def rdate(start, end):
    delta = end - start
    return start + timedelta(
        days=random.randint(0, delta.days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUT, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {len(rows):>4} rows → {filename}")


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def gen_products():
    rows = []
    # intentional category case issues on 4 rows
    bad_case = {3010: "clothing", 3011: "ELECTRONICS", 3002: "electronics", 3022: "BEAUTY"}
    for pid, name, cat, brand, price, stock in PRODUCTS_CLEAN:
        category = bad_case.get(pid, cat)
        rows.append(dict(product_id=pid, name=name, category=category,
                         brand=brand, unit_price=price, stock_qty=stock))
    # 3 duplicate rows (same product_id)
    for pid in random.sample([p[0] for p in PRODUCTS_CLEAN[:15]], 3):
        orig = next(r for r in rows if r["product_id"] == pid)
        rows.append(orig.copy())
    return rows


def gen_users():
    rows = []
    uid = 1001
    name_pairs = [(f, l) for f in FIRST_NAMES for l in LAST_NAMES]
    random.shuffle(name_pairs)
    used_emails = set()

    for i in range(60):
        first, last = name_pairs[i]
        base = f"{first.lower()}.{last.lower()}"
        email = f"{base}@email.com"
        n = 1
        while email in used_emails:
            email = f"{base}{n}@email.com"
            n += 1
        used_emails.add(email)

        digits = f"{random.randint(60,99)}{random.randint(1000000,9999999)}"
        phone = random.choices(
            [f"0{digits[:9]}", f"+660{digits[:8]}", f"660{digits[:8]}", None],
            weights=[70, 15, 10, 5],
        )[0]

        created = rdate(datetime(2023, 1, 1), datetime(2024, 3, 31))
        rows.append(dict(user_id=uid, name=f"{first} {last}", email=email,
                         phone=phone,
                         created_at=created.strftime("%Y-%m-%d %H:%M:%S")))
        uid += 1

    # 5 duplicate emails (same email, new user_id)
    for src in random.sample(rows[:30], 5):
        dup = src.copy()
        dup["user_id"] = uid
        dup["name"] = src["name"] + " Jr"
        rows.append(dup)
        uid += 1

    return rows


def gen_addresses(users):
    rows = []
    aid = 2001
    orig_users = [u for u in users if not u["name"].endswith(" Jr")]

    for user in orig_users:
        count = random.choices([1, 2], weights=[65, 35])[0]
        for _ in range(count):
            prov = random.choice(PROVINCES)
            # province inconsistency ~20% of rows
            prov_val = random.choices(
                [prov, prov.lower(), prov.upper(), prov[:3].upper()],
                weights=[75, 12, 8, 5],
            )[0]
            district = random.choice(DISTRICTS[prov])
            postal = random.choice(POSTAL_CODES[prov])
            if random.random() < 0.08:
                postal = None  # missing postal code
            street_num = random.randint(1, 999)
            street_name = random.choice(STREETS)
            rows.append(dict(
                address_id=aid,
                user_id=user["user_id"],
                street=f"{street_num} {street_name} Rd",
                district=district,
                province=prov_val,
                postal_code=postal,
                country="Thailand",
            ))
            aid += 1

    return rows[:80]


def gen_orders(users, addresses):
    rows = []
    oid = 4001
    orig_user_ids = [u["user_id"] for u in users if not u["name"].endswith(" Jr")]
    addr_by_user: dict[int, list] = {}
    for a in addresses:
        addr_by_user.setdefault(a["user_id"], []).append(a["address_id"])

    for _ in range(100):
        uid = random.choice(orig_user_ids)
        addr_id = random.choice(addr_by_user.get(uid, [addresses[0]["address_id"]]))
        odate = rdate(datetime(2024, 1, 1), datetime(2024, 3, 31))
        status = random.choices(
            ORDER_STATUSES, weights=[10, 15, 60, 10, 5]
        )[0]
        rows.append(dict(
            order_id=oid,
            user_id=uid,
            shipping_address_id=addr_id,
            order_date=odate.strftime("%Y-%m-%d %H:%M:%S"),
            status=status,
            total_amount=0,  # filled after order_items
        ))
        oid += 1

    # 8 duplicate rows
    for src in random.sample(rows[:50], 8):
        rows.append(src.copy())

    return rows


def gen_order_items(orders):
    rows = []
    iid = 5001
    order_totals: dict[int, float] = {}

    seen = set()
    unique_orders = []
    for o in orders:
        if o["order_id"] not in seen:
            seen.add(o["order_id"])
            unique_orders.append(o)

    for order in unique_orders:
        num_items = random.choices([1, 2, 3, 4], weights=[40, 35, 15, 10])[0]
        chosen = random.sample(PRODUCTS_CLEAN, num_items)
        total = 0.0
        for pid, name, cat, brand, unit_price, stock in chosen:
            qty = random.randint(1, 4)
            correct_sub = round(qty * unit_price, 2)
            # ~8% rows have wrong subtotal
            if random.random() < 0.08:
                subtotal = round(correct_sub * random.uniform(0.80, 1.20), 2)
            else:
                subtotal = correct_sub
            rows.append(dict(
                order_item_id=iid,
                order_id=order["order_id"],
                product_id=pid,
                quantity=qty,
                unit_price=unit_price,
                subtotal=subtotal,
            ))
            total += correct_sub
            iid += 1
        order_totals[order["order_id"]] = round(total, 2)

    # back-fill total_amount on orders
    for o in orders:
        o["total_amount"] = order_totals.get(o["order_id"], 0.0)

    return rows


def gen_transports(orders):
    rows = []
    tid = 6001

    seen = set()
    unique_orders = []
    for o in orders:
        if o["order_id"] not in seen:
            seen.add(o["order_id"])
            unique_orders.append(o)

    shippable = [o for o in unique_orders if o["status"] in ("processing", "completed")]
    chosen = random.sample(shippable, min(90, len(shippable)))

    for order in chosen:
        odate = datetime.strptime(order["order_date"], "%Y-%m-%d %H:%M:%S")
        shipped = odate + timedelta(days=random.randint(1, 3))
        delivered = shipped + timedelta(days=random.randint(1, 7))
        carrier = random.choice(CARRIERS)
        prefix = carrier[:3].upper()
        tracking = f"{prefix}{random.randint(100000000, 999999999)}TH"

        if order["status"] == "processing":
            t_status = random.choice(["picked_up", "in_transit"])
            delivered_at = None
            # bug: ~10% in_transit rows have delivered_at set
            if t_status == "in_transit" and random.random() < 0.10:
                delivered_at = delivered.strftime("%Y-%m-%d %H:%M:%S")
        else:
            t_status = "delivered"
            delivered_at = delivered.strftime("%Y-%m-%d %H:%M:%S")

        # bug: ~5% rows missing tracking even though shipped
        if random.random() < 0.05:
            tracking = None

        rows.append(dict(
            transport_id=tid,
            order_id=order["order_id"],
            carrier=carrier,
            tracking_number=tracking,
            shipped_at=shipped.strftime("%Y-%m-%d %H:%M:%S"),
            delivered_at=delivered_at,
            status=t_status,
        ))
        tid += 1

    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating raw CSV datasets...")

    products  = gen_products()
    users     = gen_users()
    addresses = gen_addresses(users)
    orders    = gen_orders(users, addresses)
    items     = gen_order_items(orders)
    transports = gen_transports(orders)

    write_csv("products_raw.csv",    products,
              ["product_id","name","category","brand","unit_price","stock_qty"])
    write_csv("users_raw.csv",       users,
              ["user_id","name","email","phone","created_at"])
    write_csv("addresses_raw.csv",   addresses,
              ["address_id","user_id","street","district","province","postal_code","country"])
    write_csv("orders_raw.csv",      orders,
              ["order_id","user_id","shipping_address_id","order_date","status","total_amount"])
    write_csv("order_items_raw.csv", items,
              ["order_item_id","order_id","product_id","quantity","unit_price","subtotal"])
    write_csv("transports_raw.csv",  transports,
              ["transport_id","order_id","carrier","tracking_number","shipped_at","delivered_at","status"])

    total = sum([len(products), len(users), len(addresses),
                 len(orders), len(items), len(transports)])
    print(f"\nTotal rows across all files: {total}")
    print("\nData quality issues embedded:")
    print("  products_raw.csv   — category case inconsistency, 3 duplicate product_id rows")
    print("  users_raw.csv      — 5 duplicate emails (diff user_id), phone format mixed/null")
    print("  addresses_raw.csv  — ~8% missing postal_code, province case inconsistency")
    print("  orders_raw.csv     — 8 duplicate order rows, total_amount pre-filled from items")
    print("  order_items_raw.csv — ~8% rows subtotal != quantity * unit_price")
    print("  transports_raw.csv  — ~5% missing tracking_number, ~10% delivered_at/status mismatch")
