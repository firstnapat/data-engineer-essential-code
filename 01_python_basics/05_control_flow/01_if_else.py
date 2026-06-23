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
