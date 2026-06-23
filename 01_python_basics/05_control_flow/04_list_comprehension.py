# basic list comprehension — apply 7% VAT to a price list
print("--- Basic List Comprehension ---")
prices = [650, 2500, 8500, 35000]
with_vat = [round(p * 1.07, 2) for p in prices]
print(f"prices:   {prices}")
print(f"with VAT: {with_vat}")

# with a filter (if) — only high-value line items
print("\n--- With Filter ---")
revenues = [105000, 9750, 17000, 60000, 450, 9000]
big_orders = [r for r in revenues if r >= 10000]
discounted = [r * 0.9 for r in revenues if r >= 50000]
print(f"big orders (>=10k): {big_orders}")
print(f"discount on >=50k:  {discounted}")

# transforming strings — normalise messy product names
print("\n--- String Operations ---")
raw_names = ["  laptop pro ", " wireless MOUSE ", "  webcam  "]
clean = [n.strip().title() for n in raw_names]
print(f"clean: {clean}")

products = ["Laptop Pro", "Wireless Mouse", "Webcam", "Water Bottle", "Wifi Router"]
w_products = [p for p in products if p.startswith("W")]
print(f"starts with 'W': {w_products}")

# nested list comprehension — flatten/transpose a warehouse stock grid
print("\n--- Nested List Comprehension ---")
grid = [[50, 200, 30], [12, 80, 0], [5, 150, 60]]
flat = [val for row in grid for val in row]
columns = [[row[i] for row in grid] for i in range(3)]
print(f"flattened:         {flat}")
print(f"columns (per SKU): {columns}")

# dictionary comprehension — SKU -> price lookup
print("\n--- Dictionary Comprehension ---")
skus = ["P001", "P002", "P006"]
unit_prices = [35000, 650, 8500]
price_book = {sku: price for sku, price in zip(skus, unit_prices)}
print(f"price book: {price_book}")

expensive = {sku: p for sku, p in price_book.items() if p > 1000}
print(f"expensive (>1000): {expensive}")

# set comprehension — distinct categories from order rows
print("\n--- Set Comprehension ---")
order_categories = ["Electronics", "Electronics", "Furniture", "Clothing", "Furniture"]
distinct = {c for c in order_categories}
print(f"distinct categories: {distinct}")
