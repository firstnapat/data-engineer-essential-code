# integer
print("--- Integer ---")
count = 42
big_number = 1_000_000    # underscores for readability
print(f"count={count}, big_number={big_number}, type={type(count)}")

# float
print("\n--- Float ---")
price = 99.99
scientific = 1.5e3        # 1500.0
print(f"price={price}, scientific={scientific}, type={type(price)}")

# string — common methods
print("\n--- String ---")
message = "Hello, Data Engineer!"
print(f"value:   {message}")
print(f"upper:   {message.upper()}")
print(f"slice:   {message[0:5]}")
print(f"replace: {message.replace('Hello', 'Hi')}")
print(f"split:   {'Bangkok,Chiang Mai,Phuket'.split(',')}")
print(f"strip:   {'  spaces  '.strip()!r}")
print(f"len:     {len(message)}")

# boolean — truthy / falsy values
print("\n--- Boolean ---")
is_active = True
print(f"bool values — 0:{bool(0)}, 1:{bool(1)}, '':{bool('')}, 'hi':{bool('hi')}, []:{bool([])}, None:{bool(None)}")

# type conversion (casting)
print("\n--- Type Conversion ---")
print(f"int('123'):   {int('123')}")
print(f"float('3.14'):{float('3.14')}")
print(f"str(456):     {str(456)}")
print(f"bool(0):      {bool(0)}")
