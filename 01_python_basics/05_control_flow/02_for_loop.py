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
