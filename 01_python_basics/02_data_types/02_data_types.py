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
