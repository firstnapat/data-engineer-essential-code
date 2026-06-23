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

# .format() — older string formatting (still seen in legacy code)
print("\n--- .format() ---")
template = "{} x{} = {:,.2f} THB"
print(template.format("Wireless Mouse", 15, 9750.0))

# reading input (input() shown commented; simulated here so the script runs)
print("\n--- Input (simulated — normally use input()) ---")
# sku = input("Enter SKU: ")
# quantity = int(input("Enter quantity: "))
sku = "P001"
quantity = int("3")
print(f"Ordered {quantity} x {sku}")
