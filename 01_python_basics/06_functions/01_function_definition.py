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
