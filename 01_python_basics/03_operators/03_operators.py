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
