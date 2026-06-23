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
