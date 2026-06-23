# case methods — normalise a product name
print("--- Case Methods ---")
text = "laptop PRO"
print(f"upper():      {text.upper()}")
print(f"lower():      {text.lower()}")
print(f"title():      {text.title()}")
print(f"capitalize(): {text.capitalize()}")
print(f"swapcase():   {text.swapcase()}")

# stripping whitespace — trim a messy cell
print("\n--- Stripping ---")
raw = "   Bangkok   "
print(f"strip():    {raw.strip()!r}")
print(f"lstrip():   {raw.lstrip()!r}")
print(f"rstrip():   {raw.rstrip()!r}")
print(f"strip('P'): {'PPP001PPP'.strip('P')!r}")

# split and join — break a raw CSV row apart, then rebuild it
print("\n--- Split & Join ---")
csv_line = "2024-01-02,Laptop Pro,Electronics,3"
fields = csv_line.split(",")
print(f"split(','):     {fields}")
print(f"rsplit(',', 1): {csv_line.rsplit(',', 1)}")
print(f"join ' | ':     {' | '.join(fields)}")
multiline = "P001\nP002\nP003"
print(f"splitlines():   {multiline.splitlines()}")

# replace
print("\n--- Replace ---")
sku_path = "P001/P002/P006"
print(f"replace('/',','):  {sku_path.replace('/', ',')}")
print(f"replace (limit 1): {sku_path.replace('/', ',', 1)}")

# searching
print("\n--- Searching ---")
name = "Mechanical Keyboard"
print(f"find('Key'):        {name.find('Key')}")     # index, -1 if absent
print(f"find('Mouse'):      {name.find('Mouse')}")
print(f"count('a'):         {name.count('a')}")
print(f"'board' in name:    {'board' in name}")
print(f"startswith('Mech'): {name.startswith('Mech')}")
print(f"endswith('board'):  {name.endswith('board')}")

# content checks — validate raw cells
print("\n--- Content Checks ---")
print(f"'35000'.isdigit(): {'35000'.isdigit()}")    # a clean numeric cell
print(f"'P001'.isalpha():  {'P001'.isalpha()}")
print(f"'   '.isspace():   {'   '.isspace()}")

# formatting — build a report line
print("\n--- Formatting ---")
product, price = "Laptop Pro", 34999.5
print(f"f-string:   {product} -> {price:,.2f}")
print("format():   {} -> {:,.2f}".format(product, price))
print(f"pad/align:  |{product:<15}|{product:>15}|{product:^15}|")
print(f"number fmt: {1234567:,} | {0.07:.1%} | P{42:05d}")

# DE example: clean and normalise a messy region value
print("\n--- DE Example: Clean a Column Value ---")
messy = "  Bangkok , Thailand  "
clean = messy.strip().lower().replace(" ,", ",")
print(f"raw:   {messy!r}")
print(f"clean: {clean!r}")

# DE example: parse a raw order line into typed values
print("\n--- DE Example: Parse an Order Line ---")
line = "Laptop Pro,3,35000"
product, qty, price = line.split(",")
print(f"product={product}, revenue={int(qty) * int(price):,}")
