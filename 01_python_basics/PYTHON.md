# Python Basics Teacher Guide

เอกสารนี้รวบรวมโค้ดตัวอย่างที่สมบูรณ์แบบทั้งหมดในส่วนของ `01_python_basics` เพื่อให้ผู้สอนใช้เป็นคู่มือประกอบการสอน (Teacher Guide) หรือเฉลยสำหรับการจัดหัวข้อ Live Coding

---

## สารบัญ
1. [01 Variables](#01-variables)
2. [02 Data Types](#02-data-types)
3. [03 Operators](#03-operators)
4. [04 Input & Output](#04-input--output)
5. [05 Control Flow](#05-control-flow)
6. [06 Functions](#06-functions)
7. [07 Data Structures](#07-data-structures)
8. [08 Error Handling](#08-error-handling)
9. [09 String Manipulation](#09-string-manipulation)
10. [10 Modules](#10-modules)

---

## 01 Variables

### `01_variables.py`
```python
# basic variables — assignment and the 5 core types, told through one product
product_name = "Laptop Pro"      # str
unit_price = 35000.0             # float
stock = 50                       # int
is_active = True                 # bool
discount = None                  # None — "no value yet"

print("--- Product Variables ---")
print(f"Product: {product_name}, Price: {unit_price}, Stock: {stock}")
print(f"Active: {is_active}, Discount: {discount}")
print(f"type(product_name): {type(product_name)}, type(stock): {type(stock)}")

# multiple assignment — unpack a product row in one line
print("\n--- Multiple Assignment ---")
sku, category, supplier = "P001", "Electronics", "TechCorp"
print(f"sku={sku}, category={category}, supplier={supplier}")

# swap two values without a temp variable (e.g. reorder display columns)
low_price, high_price = 650, 35000
low_price, high_price = high_price, low_price
print(f"After swap: low_price={low_price}, high_price={high_price}")

# same starting value for several counters
units_sold = units_returned = units_damaged = 0
print(f"sold={units_sold}, returned={units_returned}, damaged={units_damaged}")

# naming conventions
print("\n--- Naming Conventions ---")
customer_name = "snake_case for variables"   # preferred in Python
MAX_STOCK_PER_SKU = 1000                      # constants in UPPER_SNAKE_CASE
_internal_cache = "prefix _ = internal use"
print(customer_name, MAX_STOCK_PER_SKU, _internal_cache)
```

---

## 02 Data Types

### `02_data_types.py`
```python
# integer — counts: stock on hand, quantity ordered
print("--- Integer ---")
stock = 50
warehouse_capacity = 1_000_000    # underscores for readability
print(f"stock={stock}, warehouse_capacity={warehouse_capacity}, type={type(stock)}")

# float — money: prices, revenue
print("\n--- Float ---")
unit_price = 35000.50
bulk_threshold = 1.5e3            # 1500.0 — order value to qualify for bulk pricing
print(f"unit_price={unit_price}, bulk_threshold={bulk_threshold}, type={type(unit_price)}")

# string — product/order text + common methods
print("\n--- String ---")
product = "Laptop Pro - Electronics"
print(f"value:   {product}")
print(f"upper:   {product.upper()}")
print(f"slice:   {product[0:10]}")
print(f"replace: {product.replace('Pro', 'Air')}")
print(f"split:   {'Bangkok,Chiang Mai,Phuket'.split(',')}")
print(f"strip:   {'  P001  '.strip()!r}")
print(f"len:     {len(product)}")

# boolean — order flags, stock availability
print("\n--- Boolean ---")
in_stock = stock > 0
print(f"in_stock = stock > 0 -> {in_stock}")
print(f"bool — 0:{bool(0)}, 50:{bool(50)}, '':{bool('')}, 'P001':{bool('P001')}, []:{bool([])}, None:{bool(None)}")

# type conversion (casting) — raw CSV/JSON fields arrive as strings
print("\n--- Type Conversion ---")
print(f"int('50'):       {int('50')}     (quantity from a CSV cell)")
print(f"float('35000'):  {float('35000')}  (price from a CSV cell)")
print(f"str(105000):     {str(105000)!r}   (revenue back to text)")
print(f"bool(0):         {bool(0)}    (0 stock -> not available)")
```

---

## 03 Operators

### `03_operators.py`
```python
quantity, unit_price = 3, 35000

# arithmetic — compute an order line
print("--- Arithmetic ---")
print(f"revenue    {quantity} * {unit_price} = {quantity * unit_price}")
print(f"add one     {quantity} + 1 = {quantity + 1}")
print(f"backorder   {quantity} - 5 = {quantity - 5}")
print(f"avg price   {unit_price} / {quantity} = {unit_price / quantity:.2f}  (true division)")
print(f"full boxes  17 // 6 = {17 // 6}     (floor division — items per box)")
print(f"leftover    17 %  6 = {17 % 6}      (modulus — items not in a full box)")
print(f"power       10 ** 3 = {10 ** 3}     (1000)")

# comparison — reorder checks
print("\n--- Comparison ---")
stock, reorder_level = 8, 10
print(f"stock == 0:       {stock == 0}")
print(f"stock != reorder: {stock != reorder_level}")
print(f"stock >  reorder: {stock > reorder_level}")
print(f"stock <  reorder: {stock < reorder_level}  (needs reorder)")

# logical — combine order conditions
print("\n--- Logical ---")
is_paid, is_in_stock = True, False
print(f"is_paid and is_in_stock: {is_paid and is_in_stock}  (can ship?)")
print(f"is_paid or  is_in_stock: {is_paid or is_in_stock}")
print(f"not is_in_stock:         {not is_in_stock}  (backorder)")
print(f"(stock>0) and is_paid:   {(stock > 0) and is_paid}")

# assignment — accumulate daily revenue
print("\n--- Assignment ---")
daily_revenue = 0
daily_revenue += 105000;  print(f"+= order 1: {daily_revenue}")
daily_revenue += 9750;    print(f"+= order 2: {daily_revenue}")
daily_revenue -= 5000;    print(f"-= refund:  {daily_revenue}")
daily_revenue *= 1;       print(f"*= 1:       {daily_revenue}")

# membership — is this a known value?
print("\n--- Membership ---")
categories = ["Electronics", "Furniture", "Clothing", "Accessories"]
print(f"'Electronics' in categories: {'Electronics' in categories}")
print(f"'Toys' not in categories:    {'Toys' not in categories}")
print(f"'Lap' in 'Laptop Pro':       {'Lap' in 'Laptop Pro'}")

# identity — same object vs equal value (matters when copying carts)
print("\n--- Identity ---")
cart1 = ["P001", "P002"]
cart2 = ["P001", "P002"]
cart3 = cart1
print(f"cart1 is cart2: {cart1 is cart2}  (different objects, equal contents)")
print(f"cart1 is cart3: {cart1 is cart3}  (same object — cart3 is an alias)")
```

---

## 04 Input & Output

### `04_input_output.py`
```python
# basic print() — sep and end
print("--- Basic print() ---")
print("Order received")
print("P001", "P002", "P003", sep=" | ")
print("Status:", end=" ")
print("shipped")

# f-strings — formatting prices, quantities, alignment for a report
print("\n--- f-strings ---")
product = "Laptop Pro"
unit_price = 34999.567
revenue = 1050000

print(f"Product: {product}")
print(f"Price: {unit_price:.2f}")        # 2 decimal places (THB)
print(f"Price: {unit_price:.0f}")        # rounded
print(f"Revenue: {revenue:,}")           # comma separator
print(f"Right-align: {product:>15}")     # right-align in 15 chars
print(f"Left-align:  {product:<15}|")    # left-align in 15 chars
print(f"Zero-pad SKU: P{7:05d}")         # P00007

# reading input (input() shown commented; simulated here so the script runs)
print("\n--- Input (simulated — normally use input()) ---")
# sku = input("Enter SKU: ")
# quantity = int(input("Enter quantity: "))
sku = "P001"
quantity = int("3")
print(f"Ordered {quantity} x {sku}")
```

---

## 05 Control Flow

### `01_if_else.py`
```python
# if / elif / else — classify stock level
print("--- If / Elif / Else ---")
stock = 8

if stock == 0:
    status = "out of stock"
elif stock < 10:
    status = "reorder now"
elif stock < 50:
    status = "low"
else:
    status = "healthy"

print(f"Stock: {stock} -> {status}")

# ternary (conditional expression) — free shipping threshold
print("\n--- Ternary (one-liner) ---")
order_total = 1200
shipping = "free" if order_total >= 1000 else "50 THB"
print(f"Order total {order_total} -> shipping: {shipping}")

# nested if — choose a carrier by region and weight
print("\n--- Nested If ---")
region = "Bangkok"
weight_kg = 12

if region == "Bangkok":
    carrier = "Same-day" if weight_kg <= 10 else "Next-day"
elif region in ("Chiang Mai", "Phuket"):
    carrier = "Express"
else:
    carrier = "Standard"

print(f"{region}, {weight_kg}kg -> {carrier}")

# combining conditions with and / or — can we fulfil this order?
print("\n--- and / or in conditions ---")
is_paid, in_stock = True, True
if is_paid and in_stock:
    print("Order can be shipped!")
else:
    print("Order on hold.")

# truthy / falsy — empty fields in a raw record are 'falsy'
print("\n--- Truthy / Falsy ---")
fields = [0, 50, "", "P001", None, [], ["P002"], {}, {"sku": "P001"}]
for val in fields:
    print(f"  {str(val):15} -> {'has value' if val else 'empty/missing'}")
```

### `02_for_loop.py`
```python
# iterating a list — order line items
print("--- Iterating a List ---")
cart = ["Laptop Pro", "Wireless Mouse", "Monitor 27in", "Webcam"]
for item in cart:
    print(f"  {item}")

# range() — start, stop, step
print("\n--- range() ---")
for day in range(5):
    print(f"Day{day}", end="  ")
print()
for sku_num in range(1, 11, 2):    # P001, P003, ...
    print(f"P{sku_num:03d}", end=" ")
print()
for countdown in range(3, 0, -1):  # stock countdown
    print(countdown, end=" ")
print()

# enumerate() — index + value (line numbers on an invoice)
print("\n--- enumerate() ---")
items = ["Laptop Pro", "Wireless Mouse", "Webcam"]
for line_no, item in enumerate(items, start=1):
    print(f"  Line {line_no}: {item}")

# zip() — loop over parallel lists (product + quantity)
print("\n--- zip() ---")
products = ["Laptop Pro", "Wireless Mouse", "Webcam"]
quantities = [3, 15, 5]
for product, qty in zip(products, quantities):
    print(f"  {product}: {qty} units")

# iterating a dictionary — one product record
print("\n--- Iterating a Dictionary ---")
product = {"sku": "P001", "name": "Laptop Pro", "stock": 50}
for field, value in product.items():
    print(f"  {field}: {value}")

# break and continue — scan stock, skip empties, stop at a full bin
print("\n--- break and continue ---")
stock_levels = [50, 0, 25, 0, 100]
for i, level in enumerate(stock_levels):
    if level == 0:
        continue            # skip out-of-stock items
    if level >= 100:
        print(f"  P{i:03d}: {level} (bin full, stop scan)")
        break
    print(f"  P{i:03d}: {level} ok")

# nested loop — stock grid: warehouses x products
print("\n--- Nested Loop (warehouse x product grid) ---")
grid = [[50, 200, 30], [12, 80, 0], [5, 150, 60]]
for w, row in enumerate(grid):
    for val in row:
        print(f"{val:4}", end="")
    print(f"   <- warehouse {w}")
```

### `03_while_loop.py`
```python
# basic while — sell units until stock runs out
print("--- Basic While ---")
stock = 5
while stock > 0:
    print(f"  sell 1 unit, stock left = {stock - 1}")
    stock -= 1

# while True + break — keep doubling an order until it crosses a threshold
print("\n--- While with break ---")
units = 1
while True:
    print(f"  {units}", end=" ")
    units *= 2
    if units > 50:
        break
print()

# while + continue — print only odd order IDs
print("\n--- While with continue ---")
order_id = 0
while order_id < 10:
    order_id += 1
    if order_id % 2 == 0:
        continue            # skip even IDs
    print(order_id, end=" ")
print()

# retry pattern — common when an ingestion API call fails
print("\n--- Retry Pattern (API ingestion) ---")
max_retries = 3
attempt = 0
success = False

while attempt < max_retries:
    attempt += 1
    print(f"  Fetching orders... attempt {attempt}")
    if attempt == 2:        # simulate success on the 2nd try
        success = True
        break

print("Fetched!" if success else "Gave up after max retries.")

# loop until a sentinel value — stop processing a stream at 'EOF'
print("\n--- Process Until Sentinel ---")
stream = ["100", "250", "EOF", "999"]
total_revenue = 0
for token in stream:
    if token == "EOF":
        print("End of stream.")
        break
    total_revenue += int(token)
print(f"Total revenue: {total_revenue}")
```

---

## 06 Functions

### `01_function_definition.py`
```python
# basic function — def and call
print("--- Basic Function ---")
def print_receipt_header():
    print("=== TechData Store Receipt ===")

print_receipt_header()

# docstring and return value
print("\n--- With Docstring ---")
def line_revenue(quantity, unit_price):
    """Return total revenue for one order line."""
    return quantity * unit_price

print(f"Revenue: {line_revenue(3, 35000):,}")
print(f"Docstring: {line_revenue.__doc__}")

# functions are first-class objects (pass them around like values)
print("\n--- Functions Are First-Class Objects ---")
def apply_vat(amount):      return round(amount * 1.07, 2)
def apply_discount(amount): return round(amount * 0.90, 2)

base = 1000
for adjust in [apply_vat, apply_discount]:
    print(f"  {adjust.__name__}(1000) = {adjust(base)}")

# lambda (anonymous) functions — quick, inline
print("\n--- Lambda Functions ---")
revenue = lambda qty, price: qty * price
print(f"revenue(3, 35000) = {revenue(3, 35000):,}")

products = [
    {"name": "Laptop Pro", "price": 35000},
    {"name": "Wireless Mouse", "price": 650},
    {"name": "Standing Desk", "price": 8500},
]
cheapest_first = sorted(products, key=lambda p: p["price"])
print(f"cheapest first: {[p['name'] for p in cheapest_first]}")

# scope — local vs global variables
print("\n--- Scope ---")
STORE_NAME = "TechData Store"     # global

def make_label(sku):
    prefix = "SKU"                # local to this function
    print(f"  {STORE_NAME} | {prefix}-{sku}")

make_label("P001")
print(f"Outside: STORE_NAME='{STORE_NAME}'")
# 'prefix' is not accessible here
```

### `02_parameters.py`
```python
# positional parameters
print("--- Positional Parameters ---")
def describe_product(sku, name, price):
    print(f"  {sku}: {name} ({price:,} THB)")

describe_product("P001", "Laptop Pro", 35000)

# default parameter values
print("\n--- Default Parameters ---")
def order_status(order_id, status="pending"):
    print(f"  Order {order_id}: {status}")

order_status(1001)
order_status(1002, "shipped")
order_status(1003, status="delivered")

# keyword arguments (order-independent)
print("\n--- Keyword Arguments ---")
def create_order(customer, sku, quantity, region="Bangkok"):
    return {"customer": customer, "sku": sku, "quantity": quantity, "region": region}

order = create_order(sku="P001", customer="Alice", quantity=3, region="Chiang Mai")
print(f"  {order}")

# *args — variable number of line totals to sum into an order total
print("\n--- *args (variable positional) ---")
def order_total(*line_totals):
    return sum(line_totals)

print(f"  order_total(105000, 9750):        {order_total(105000, 9750):,}")
print(f"  order_total(105000, 9750, 60000): {order_total(105000, 9750, 60000):,}")

# **kwargs — variable number of product attributes
print("\n--- **kwargs (variable keyword) ---")
def print_product(**attrs):
    for key, value in attrs.items():
        print(f"  {key}: {value}")

print_product(sku="P001", name="Laptop Pro", stock=50, supplier="TechCorp")

def build_query(table, **conditions):
    where = " AND ".join(f"{k}='{v}'" for k, v in conditions.items())
    return f"SELECT * FROM {table} WHERE {where}"

print(f"\n  {build_query('orders', region='Bangkok', status='shipped')}")

# combining all parameter types — a logistics event logger
print("\n--- Combining All Types ---")
def log_event(event, order_id, *tags, level="INFO", **context):
    print(f"  [{level}] {event} order={order_id} tags={tags} context={context}")

log_event("ship", 1001, "express", "fragile", level="WARN", carrier="Kerry")
```

### `03_return_values.py`
```python
# single return value
print("--- Single Return ---")
def revenue(quantity, unit_price):
    return quantity * unit_price

print(f"revenue(3, 35000) = {revenue(3, 35000):,}")

# multiple return values (tuple unpacking) — cheapest & most expensive
print("\n--- Multiple Return Values (tuple unpacking) ---")
def price_range(prices):
    return min(prices), max(prices)

low, high = price_range([650, 2500, 8500, 35000])
print(f"cheapest={low}, most expensive={high}")

def revenue_stats(revenues):
    return {
        "orders": len(revenues),
        "total": sum(revenues),
        "min": min(revenues),
        "max": max(revenues),
        "average": sum(revenues) / len(revenues),
    }

for key, val in revenue_stats([105000, 9750, 17000, 60000]).items():
    print(f"  {key}: {val:,.2f}")

# early return (guard clause) — avoid dividing by zero orders
print("\n--- Early Return (guard clause) ---")
def average_order_value(total_revenue, num_orders):
    if num_orders == 0:
        return None             # no orders yet
    return total_revenue / num_orders

print(f"AOV(192500, 4) = {average_order_value(192500, 4):,.2f}")
print(f"AOV(0, 0)      = {average_order_value(0, 0)}")

# generator — yield order IDs lazily (stream huge ranges without building a list)
print("\n--- Generator (yield) ---")
def order_ids(start, count):
    for i in range(count):
        yield f"ORD-{start + i:04d}"

print(f"order IDs: {list(order_ids(1001, 5))}")

# closure — function returning a function (a configurable discount)
print("\n--- Function Returning Function (closure) ---")
def make_discount(rate):
    def apply(price):
        return round(price * (1 - rate), 2)
    return apply

member_price = make_discount(0.10)     # 10% off
clearance_price = make_discount(0.50)  # 50% off
print(f"member_price(35000)={member_price(35000)}, clearance_price(35000)={clearance_price(35000)}")
```

---

## 07 Data Structures

### `01_list.py`
```python
# creating lists
print("--- Creating Lists ---")
stock_levels = [50, 200, 80, 30, 60]
mixed_row = ["P001", "Laptop Pro", 35000, True, None]   # a heterogeneous record
warehouses = [[50, 200], [12, 80], [5, 150]]            # nested: rows per warehouse
print(f"stock_levels: {stock_levels}, length: {len(stock_levels)}")

# accessing elements — indexing and slicing
print("\n--- Accessing Elements ---")
cart = ["Laptop Pro", "Wireless Mouse", "Webcam", "Monitor 27in", "Keyboard"]
print(f"first:     {cart[0]}")
print(f"last:      {cart[-1]}")
print(f"slice 1:3: {cart[1:3]}")
print(f"every 2nd: {cart[::2]}")
print(f"reversed:  {cart[::-1]}")

# modifying — append, insert, extend, pop, remove
print("\n--- Modifying ---")
order = ["P001", "P002"]
order.append("P006");           print(f"append:    {order}")
order.insert(1, "P009");        print(f"insert:    {order}")
order.extend(["P011", "P012"]); print(f"extend:    {order}")
removed = order.pop();          print(f"pop:       {order}  removed={removed}")
order.remove("P009");           print(f"remove:    {order}")

# sorting
print("\n--- Sorting ---")
prices = [35000, 650, 8500, 2800, 12000]
print(f"original:        {prices}")
print(f"sorted():        {sorted(prices)}")            # returns a new list
print(f"sorted(reverse): {sorted(prices, reverse=True)}")
prices.sort()
print(f"after .sort():   {prices}")

# searching — in and count
print("\n--- Searching ---")
print(f"'Webcam' in cart:   {'Webcam' in cart}")
print(f"count of 0 stock:   {[50, 0, 80, 0, 0].count(0)}")

# combining lists — + and *
print("\n--- Combining ---")
electronics = ["P001", "P002"]
furniture = ["P006", "P007"]
print(f"catalog:    {electronics + furniture}")
print(f"reorder x3: {['P001'] * 3}")
```

### `02_tuple.py`
```python
# creating tuples — immutable rows (SKU, qty, price)
print("--- Creating Tuples ---")
order_line = ("P001", 3, 35000.0)
single = ("P001",)                     # trailing comma is required for single-element tuple
rgb_label = (255, 128, 0)
print(f"order_line={order_line}, type={type(order_line)}")
print(f"single-element: {single}, type={type(single)}")

# accessing — indexing and slicing
print("\n--- Accessing ---")
print(f"sku={order_line[0]}, unit_price={order_line[-1]}, slice={order_line[1:]}")

# tuple unpacking
print("\n--- Tuple Unpacking ---")
sku, quantity, unit_price = order_line
print(f"sku={sku}, quantity={quantity}, unit_price={unit_price}")

first, *rest = ("P001", "P002", "P003", "P004")
print(f"first={first}, rest={rest}")

a, b = 10, 20
a, b = b, a    # swap via tuple
print(f"After swap: a={a}, b={b}")

# tuples are immutable — protects a record from accidental edits
print("\n--- Immutable ---")
try:
    order_line[1] = 99
except TypeError as e:
    print(f"Cannot modify tuple: {e}")

# tuples as dict keys (lists cannot be) — geo coords -> warehouse
print("\n--- Tuples as Dict Keys (lists cannot be) ---")
warehouses = {(13.75, 100.52): "Bangkok DC", (18.79, 98.98): "Chiang Mai DC"}
print(f"(13.75, 100.52) -> {warehouses[(13.75, 100.52)]}")

# namedtuple — access fields by name (a lightweight record type)
print("\n--- namedtuple ---")
from collections import namedtuple

Product = namedtuple("Product", ["sku", "name", "price", "stock"])
laptop = Product("P001", "Laptop Pro", 35000, 50)
print(f"laptop:       {laptop}")
print(f"laptop.name:  {laptop.name}, laptop.stock: {laptop.stock}")
```

### `03_dictionary.py`
```python
# creating dictionaries — a product record
print("--- Creating Dictionaries ---")
product = {"sku": "P001", "name": "Laptop Pro", "price": 35000, "stock": 50}
config = dict(host="localhost", port=5432, db="warehouse")
print(f"product: {product}")
print(f"config:  {config}")

# accessing values — [], .get(), default
print("\n--- Accessing Values ---")
print(f"product['name']:                {product['name']}")
print(f"product.get('stock'):           {product.get('stock')}")
print(f"product.get('supplier', 'N/A'): {product.get('supplier', 'N/A')}")

try:
    _ = product["supplier"]
except KeyError as e:
    print(f"KeyError for missing key: {e}")

# modifying — add, update, pop
print("\n--- Modifying ---")
order = {"order_id": 1001, "sku": "P001"}
order["quantity"] = 3;           print(f"add quantity:  {order}")
order["sku"] = "P002";           print(f"change sku:    {order}")
removed = order.pop("quantity"); print(f"pop quantity:  {order}  removed={removed}")
order.update({"status": "paid", "region": "Bangkok"}); print(f"update:        {order}")

# keys / values / items
print("\n--- Keys / Values / Items ---")
print(f"keys():   {list(product.keys())}")
print(f"values(): {list(product.values())}")
for key, value in product.items():
    print(f"  {key}: {value}")

# nested dictionary — customers keyed by ID
print("\n--- Nested Dictionary ---")
customers = {
    "U001": {"name": "Alice", "city": "Bangkok",    "tier": "gold"},
    "U002": {"name": "Bob",   "city": "Chiang Mai", "tier": "silver"},
}
for user_id, info in customers.items():
    print(f"  {user_id}: {info['name']} ({info['tier']}, {info['city']})")

# defaultdict — total revenue per category without pre-seeding keys
print("\n--- defaultdict ---")
from collections import defaultdict

revenue_by_category = defaultdict(float)
rows = [("Electronics", 105000), ("Furniture", 17000), ("Electronics", 9750), ("Clothing", 2800)]
for category, amount in rows:
    revenue_by_category[category] += amount
print(f"revenue_by_category: {dict(revenue_by_category)}")
```

### `04_set.py`
```python
# creating sets — duplicates removed automatically
print("--- Creating Sets ---")
skus_today = {"P001", "P002", "P002", "P006"}    # duplicates removed automatically
from_list = set(["P001", "P001", "P002"])
empty = set()                                      # {} makes a dict, not a set!
print(f"skus_today: {skus_today}")
print(f"from_list:  {from_list}")

# adding / removing — add, discard, remove
print("\n--- Adding / Removing ---")
cart = {"P001", "P002", "P006"}
cart.add("P009");      print(f"add:     {cart}")
cart.discard("P002");  print(f"discard: {cart}  (no error if missing)")
cart.remove("P006");   print(f"remove:  {cart}")

# set operations — compare what sold today vs yesterday
print("\n--- Set Operations ---")
today = {"P001", "P002", "P006", "P009"}
yesterday = {"P006", "P009", "P011", "P012"}
print(f"today:            {today}")
print(f"yesterday:        {yesterday}")
print(f"either day  | :   {today | yesterday}")
print(f"both days   & :   {today & yesterday}")
print(f"only today  - :   {today - yesterday}")
print(f"one day only ^:   {today ^ yesterday}")

# subset / superset / disjoint
print("\n--- Subset / Superset ---")
ordered = {"P001", "P002"}
catalog = {"P001", "P002", "P006", "P009"}
print(f"ordered.issubset(catalog):    {ordered.issubset(catalog)}")
print(f"catalog.issuperset(ordered):  {catalog.issuperset(ordered)}")
print(f"ordered.isdisjoint({{'P099'}}): {ordered.isdisjoint({'P099'})}")

# use case: distinct values from a column of order rows
print("\n--- Common Use Case: Remove Duplicates ---")
region_column = ["Bangkok", "Chiang Mai", "Bangkok", "Phuket", "Bangkok", "Chiang Mai"]
distinct_unordered = list(set(region_column))
distinct_ordered = list(dict.fromkeys(region_column))   # preserves first-seen order
print(f"raw column:         {region_column}")
print(f"distinct (set):     {distinct_unordered}")
print(f"distinct (ordered): {distinct_ordered}")

# use case: fast membership testing — validate a category column
print("\n--- Fast Membership Testing ---")
valid_categories = {"Electronics", "Furniture", "Clothing", "Accessories"}
incoming = ["Electronics", "Toys", "Clothing", "Gadgets"]
for value in incoming:
    status = "valid" if value in valid_categories else "REJECT"
    print(f"  {value:12} -> {status}")
```

### `05_comprehensions.py`
แนวคิดเดียวกับ list/dict/set ด้านบน แต่เขียนสั้นลงในบรรทัดเดียว — สร้าง collection จากการวนลูป
```python
# list comprehension — apply 7% VAT to a price list
print("--- List Comprehension ---")
prices = [650, 2500, 8500, 35000]
with_vat = [round(p * 1.07, 2) for p in prices]
print(f"with VAT: {with_vat}")

# with a filter (if) — keep only high-value line items
print("\n--- With Filter ---")
revenues = [105000, 9750, 17000, 60000, 450]
big_orders = [r for r in revenues if r >= 10000]
print(f"big orders (>=10k): {big_orders}")

# dict comprehension — SKU -> price lookup
print("\n--- Dict Comprehension ---")
skus = ["P001", "P002", "P006"]
unit_prices = [35000, 650, 8500]
price_book = {sku: price for sku, price in zip(skus, unit_prices)}
print(f"price book: {price_book}")

# set comprehension — distinct categories from order rows
print("\n--- Set Comprehension ---")
order_categories = ["Electronics", "Electronics", "Furniture", "Clothing"]
distinct = {c for c in order_categories}
print(f"distinct categories: {distinct}")
```

---

## 08 Error Handling

### `01_try_except.py`
```python
# basic try / except — a zero-item order slips into a calculation
print("--- Basic Try / Except ---")
try:
    avg_price = 35000 / 0       # zero items -> division by zero
except ZeroDivisionError:
    print("Cannot divide by zero items!")

# catching multiple exception types — parse a raw quantity field
print("\n--- Catching Multiple Exceptions ---")
def parse_quantity(value):
    try:
        return int(value)
    except ValueError:
        print(f"  ValueError: '{value}' is not a valid quantity")
        return None
    except TypeError:
        print(f"  TypeError: cannot convert {type(value).__name__} to int")
        return None

parse_quantity("3")
parse_quantity("three")
parse_quantity(None)

# accessing the exception object (as e) — missing field in a record
print("\n--- Except with Exception Info ---")
try:
    product = {"sku": "P001", "name": "Laptop Pro"}
    print(product["price"])
except KeyError as e:
    print(f"Missing field: {e} (type: {type(e).__name__})")

# else and finally — load a data file safely
print("\n--- else and finally ---")
def load_orders(filename):
    try:
        f = open(filename)
        content = f.read()
        f.close()
    except FileNotFoundError:
        print(f"  '{filename}' not found")
        return None
    else:
        print(f"  Loaded {len(content)} chars")
        return content
    finally:
        print("  finally: always runs (close connections here)")

load_orders("orders_missing.csv")

# raising exceptions — validate an order quantity
print("\n--- Raising Exceptions ---")
def validate_quantity(qty):
    if not isinstance(qty, int):
        raise TypeError(f"Quantity must be int, got {type(qty).__name__}")
    if qty <= 0:
        raise ValueError(f"Quantity {qty} must be positive")
    return True

try:
    validate_quantity(-2)
except ValueError as e:
    print(f"ValueError: {e}")

try:
    validate_quantity("3")
except TypeError as e:
    print(f"TypeError: {e}")

# custom exception class — a domain-specific validation error
print("\n--- Custom Exception ---")
class ProductValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Field '{field}': {message}")

try:
    raise ProductValidationError("unit_price", "must be greater than 0")
except ProductValidationError as e:
    print(f"ProductValidationError — field='{e.field}', msg='{e}'")
```

### `02_common_runtime_errors.py`
```python
# helper: run a function and report the error type if it raises
def safe_run(label, fn):
    try:
        result = fn()
        print(f"  {label}: OK -> {result}")
    except Exception as e:
        print(f"  {label}: {type(e).__name__}: {e}")

# NameError — referencing a column/variable that was never defined
print("--- NameError: variable used before assignment ---")
safe_run("unit_prince typo", lambda: unit_prince)  # noqa: F821  (misspelled 'unit_price')

# TypeError — operation on the wrong type (raw CSV fields are strings!)
print("\n--- TypeError ---")
safe_run("'3' + 35000",  lambda: "3" + 35000)      # quantity str + price int
safe_run("len(50)",      lambda: len(50))
safe_run("None + 1",     lambda: None + 1)         # a missing field

# ValueError — right type, wrong value
print("\n--- ValueError ---")
safe_run("int('three')", lambda: int("three"))     # bad quantity cell
safe_run("int('')",      lambda: int(""))          # empty cell

# IndexError — list index out of range
print("\n--- IndexError ---")
order_line = ["P001", 3, 35000]
safe_run("order_line[5]",  lambda: order_line[5])
safe_run("order_line[-9]", lambda: order_line[-9])

# KeyError — dict key / record field does not exist
print("\n--- KeyError ---")
product = {"sku": "P001"}
safe_run("product['price']", lambda: product["price"])

# AttributeError — attribute/method does not exist
print("\n--- AttributeError ---")
safe_run("'P001'.to_upper()", lambda: "P001".to_upper())   # it's .upper()
safe_run("(50).upper()",      lambda: (50).upper())

# ZeroDivisionError — averaging revenue over zero orders
print("\n--- ZeroDivisionError ---")
safe_run("105000 / 0",  lambda: 105000 / 0)
safe_run("105000 // 0", lambda: 105000 // 0)

# RecursionError — recursion too deep
print("\n--- RecursionError ---")
def keep_paging(page): return keep_paging(page + 1)   # forgot the stop condition
try:
    keep_paging(0)
except RecursionError:
    print("  RecursionError: maximum recursion depth exceeded")

# FileNotFoundError — opening a dataset that does not exist
print("\n--- FileNotFoundError ---")
try:
    open("orders_2099.csv")
except FileNotFoundError as e:
    print(f"  FileNotFoundError: {e}")
```

### `03_context_manager.py`
```python
# context managers (with statement) — guarantees resource cleanup (db connection, file closing)
print("--- Using with for File I/O ---")

# File is automatically closed when exiting the block, even if an exception occurs
with open("test_file.txt", "w") as f:
    f.write("P001,Laptop Pro,35000\n")

print("File written and automatically closed.")

# Simulating database/API resource connections
class MockDatabaseConnection:
    def __enter__(self):
        print("  Database Connection opened.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("  Database Connection closed automatically.")
        # Return False to propagate exceptions, True to suppress them
        return False

    def query(self, sql):
        print(f"  Executing: {sql}")

print("\n--- Custom Context Manager ---")
with MockDatabaseConnection() as db:
    db.query("SELECT * FROM sales")
```

---

## 09 String Manipulation

### `09_string_manipulation.py`
```python
# case methods — normalise a product name
print("--- Case Methods ---")
text = "laptop PRO"
print(f"upper():      {text.upper()}")
print(f"lower():      {text.lower()}")
print(f"title():      {text.title()}")
print(f"capitalize(): {text.capitalize()}")
print(f"swapcase():   {text.swapcase()}")

# stripping whitespace — trim a messy cell
print("\n--- Stripping ---")
raw = "   Bangkok   "
print(f"strip():    {raw.strip()!r}")
print(f"lstrip():   {raw.lstrip()!r}")
print(f"rstrip():   {raw.rstrip()!r}")
print(f"strip('P'): {'PPP001PPP'.strip('P')!r}")

# split and join — break a raw CSV row apart, then rebuild it
print("\n--- Split & Join ---")
csv_line = "2024-01-02,Laptop Pro,Electronics,3"
fields = csv_line.split(",")
print(f"split(','):     {fields}")
print(f"rsplit(',', 1): {csv_line.rsplit(',', 1)}")
print(f"join ' | ':     {' | '.join(fields)}")
multiline = "P001\nP002\nP003"
print(f"splitlines():   {multiline.splitlines()}")

# replace
print("\n--- Replace ---")
sku_path = "P001/P002/P006"
print(f"replace('/',','):  {sku_path.replace('/', ',')}")
print(f"replace (limit 1): {sku_path.replace('/', ',', 1)}")

# searching
print("\n--- Searching ---")
name = "Mechanical Keyboard"
print(f"find('Key'):        {name.find('Key')}")     # index, -1 if absent
print(f"find('Mouse'):      {name.find('Mouse')}")
print(f"count('a'):         {name.count('a')}")
print(f"'board' in name:    {'board' in name}")
print(f"startswith('Mech'): {name.startswith('Mech')}")
print(f"endswith('board'):  {name.endswith('board')}")

# content checks — validate raw cells
print("\n--- Content Checks ---")
print(f"'35000'.isdigit(): {'35000'.isdigit()}")    # a clean numeric cell
print(f"'P001'.isalpha():  {'P001'.isalpha()}")
print(f"'   '.isspace():   {'   '.isspace()}")

# formatting — build a report line
print("\n--- Formatting ---")
product, price = "Laptop Pro", 34999.5
print(f"f-string:   {product} -> {price:,.2f}")
print("format():   {} -> {:,.2f}".format(product, price))
print(f"pad/align:  |{product:<15}|{product:>15}|{product:^15}|")
print(f"number fmt: {1234567:,} | {0.07:.1%} | P{42:05d}")

# DE example: clean and normalise a messy region value
print("\n--- DE Example: Clean a Column Value ---")
messy = "  Bangkok , Thailand  "
clean = messy.strip().lower().replace(" ,", ",")
print(f"raw:   {messy!r}")
print(f"clean: {clean!r}")

# DE example: parse a raw order line into typed values
print("\n--- DE Example: Parse an Order Line ---")
line = "Laptop Pro,3,35000"
product, qty, price = line.split(",")
print(f"product={product}, revenue={int(qty) * int(price):,}")
```

---

## 10 Modules

### `sales_utils.py`
```python
"""sales_utils — a small example module to be imported by 10_modules.py.

A module is just a .py file. Anything defined here (constants, functions)
can be imported elsewhere with `import sales_utils` or `from sales_utils import ...`.

Theme: tiny reusable helpers for the store domain — revenue, VAT, stock, money.
"""

# module-level constants
VAT_RATE = 0.07
REORDER_LEVEL = 10


def calc_revenue(quantity, unit_price):
    """Return total revenue for one order line."""
    return quantity * unit_price


def add_vat(amount):
    """Return amount including VAT."""
    return amount * (1 + VAT_RATE)


def is_low_stock(stock, reorder_level=REORDER_LEVEL):
    """Return True when stock has fallen to/below the reorder level."""
    return stock <= reorder_level


def format_currency(amount):
    """Format a number as Thai Baht with thousands separators."""
    return f"฿{amount:,.2f}"


# This block runs ONLY when the file is executed directly (python sales_utils.py),
# NOT when it is imported. Useful for a quick self-test.
if __name__ == "__main__":
    print("Self-test of sales_utils:")
    rev = calc_revenue(3, 35000)
    print(f"  calc_revenue(3, 35000) = {rev}")
    print(f"  add_vat({rev})         = {add_vat(rev)}")
    print(f"  is_low_stock(8)        = {is_low_stock(8)}")
    print(f"  format_currency({rev}) = {format_currency(rev)}")
```

### `10_modules.py`
```python
import os
import sys

# importing your own module (sales_utils.py sits in the same folder)
# ensure this script's folder is importable, then import it
sys.path.insert(0, os.path.dirname(__file__))

# import the whole module — access members with module.name
print("--- import sales_utils ---")
import sales_utils

rev = sales_utils.calc_revenue(3, 35000)
print(f"sales_utils.calc_revenue(3, 35000) = {rev}")
print(f"sales_utils.VAT_RATE               = {sales_utils.VAT_RATE}")

# import specific names directly
print("\n--- from sales_utils import ... ---")
from sales_utils import is_low_stock, format_currency
print(f"is_low_stock(8)      = {is_low_stock(8)}")
print(f"format_currency(rev) = {format_currency(rev)}")

# import with an alias
print("\n--- import ... as alias ---")
import sales_utils as su
print(f"su.format_currency(su.add_vat(rev)) = {su.format_currency(su.add_vat(rev))}")

# importing from the standard library
print("\n--- standard library modules ---")
import math
from datetime import datetime
print(f"math.sqrt(144):  {math.sqrt(144)}")
print(f"math.pi:         {math.pi:.5f}")
print(f"datetime.now():  {datetime.now():%Y-%m-%d}")

# inspecting a module — __name__, __doc__, dir()
print("\n--- Inspecting a Module ---")
print(f"sales_utils.__name__: {sales_utils.__name__}")
print(f"sales_utils.__doc__:  {sales_utils.__doc__.splitlines()[0]}")
public = [n for n in dir(sales_utils) if not n.startswith("_")]
print(f"public members:       {public}")

# __name__ here is '__main__' because THIS file is the one being run
print(f"\nthis file's __name__:  {__name__}")
```

### `02_pathlib.py`
```python
# pathlib for filesystem operations (Modern standard instead of os.path)
print("--- pathlib.Path basic operations ---")
from pathlib import Path

# Get current file directory or workspace path
current_dir = Path(__file__).resolve().parent
print(f"Current folder:   {current_dir}")
print(f"Parent folder:    {current_dir.parent}")

# Create directories safely (DE pipeline target storage setup)
output_dir = current_dir / "output_data" / "year=2026" / "month=06"
output_dir.mkdir(parents=True, exist_ok=True)
print(f"Directory created: {output_dir.exists()}")

# Find files in a directory using Glob patterns
print("\n--- Search Files using Glob ---")
project_root = current_dir.parent.parent
print(f"Searching datasets folder in {project_root / 'datasets'}:")
for filepath in (project_root / "datasets").glob("*"):
    print(f"  Found file: {filepath.name} (Suffix: {filepath.suffix})")
```

### `03_datetime.py`
```python
# datetime and timezones (Crucial for data pipelines, timestamps, UTC formats)
print("--- datetime Basics ---")
from datetime import datetime, timezone, timedelta

# Local current time vs UTC (always store and work with UTC in databases/data lakes)
now_local = datetime.now()
now_utc = datetime.now(timezone.utc)
print(f"Local time: {now_local}")
print(f"UTC time:   {now_utc}")

# formatting time to string (strftime - formatting logs or path partition)
print("\n--- strftime (datetime -> string) ---")
date_str = now_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
partition_path = now_utc.strftime("year=%Y/month=%m/day=%d")
print(f"Formatted:  {date_str}")
print(f"Partition:  {partition_path}")

# parsing string to datetime object (strptime - parsing timestamp fields from raw CSV/JSON)
print("\n--- strptime (string -> datetime) ---")
raw_timestamp = "2026-06-23T14:46:00Z"
parsed_dt = datetime.strptime(raw_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
print(f"Parsed:     {parsed_dt} ({parsed_dt.tzinfo})")

# Timedelta (calculating data retention/expiration or SLA offsets)
yesterday = now_utc - timedelta(days=1)
print(f"\nYesterday UTC: {yesterday}")
```

### `04_json.py`
```python
# json module — Parsing raw API responses and database configs
print("--- json.loads (string -> python dict) ---")
import json

# Simulated API response payload
raw_json_str = """
{
    "sku": "P001",
    "name": "Laptop Pro",
    "price": 35000,
    "in_stock": true,
    "tags": ["electronics", "work"]
}
"""

data = json.loads(raw_json_str)
print(f"Type:         {type(data)}")
print(f"SKU:          {data['sku']}")
print(f"First tag:    {data['tags'][0]}")

# json.dumps (python dict -> string) - preparing payload to write to file or API request
print("\n--- json.dumps (dict -> string) ---")
config = {
    "host": "localhost",
    "port": 5432,
    "credentials": {
        "user": "postgres",
        "secret": "dbpass"
    }
}

json_payload = json.dumps(config, indent=4)
print(json_payload)
```
