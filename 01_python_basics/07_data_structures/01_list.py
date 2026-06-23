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
