# creating tuples — a fixed-shape record that shouldn't change
print("--- Creating Tuples ---")
order_line = ("P001", 3, 35000)        # (sku, quantity, unit_price)
single = ("P001",)                      # trailing comma required for one element
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
