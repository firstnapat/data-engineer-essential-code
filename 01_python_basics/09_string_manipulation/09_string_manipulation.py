# case methods
print("--- Case Methods ---")
text = "data Engineer"
print(f"upper():      {text.upper()}")
print(f"lower():      {text.lower()}")
print(f"title():      {text.title()}")
print(f"capitalize(): {text.capitalize()}")
print(f"swapcase():   {text.swapcase()}")

# stripping whitespace
print("\n--- Stripping ---")
raw = "   hello world   "
print(f"strip():  {raw.strip()!r}")
print(f"lstrip(): {raw.lstrip()!r}")
print(f"rstrip(): {raw.rstrip()!r}")
print(f"strip('x'): {'xxdataxx'.strip('x')!r}")

# split and join
print("\n--- Split & Join ---")
csv_line = "2024-01-02,Laptop Pro,Electronics,3"
fields = csv_line.split(",")
print(f"split(','):   {fields}")
print(f"rsplit(',',1):{csv_line.rsplit(',', 1)}")
print(f"join with ' | ': {' | '.join(fields)}")
multiline = "a\nb\nc"
print(f"splitlines(): {multiline.splitlines()}")

# replace
print("\n--- Replace ---")
path = "a/b/c/d"
print(f"replace('/','.'):  {path.replace('/', '.')}")
print(f"replace (limit 1): {path.replace('/', '.', 1)}")

# searching
print("\n--- Searching ---")
sentence = "the quick brown fox"
print(f"find('quick'):  {sentence.find('quick')}")    # index, -1 if absent
print(f"find('zzz'):    {sentence.find('zzz')}")
print(f"count('o'):     {sentence.count('o')}")
print(f"'fox' in text:  {'fox' in sentence}")
print(f"startswith('the'): {sentence.startswith('the')}")
print(f"endswith('fox'):   {sentence.endswith('fox')}")

# checks
print("\n--- Content Checks ---")
print(f"'12345'.isdigit():  {'12345'.isdigit()}")
print(f"'abc'.isalpha():    {'abc'.isalpha()}")
print(f"'  '.isspace():     {'  '.isspace()}")

# formatting (f-strings / .format / alignment)
print("\n--- Formatting ---")
name, score = "Alice", 98.567
print(f"f-string:    {name} -> {score:.1f}")
print("format():    {} -> {:.1f}".format(name, score))
print(f"pad/align:   |{name:<10}|{name:>10}|{name:^10}|")
print(f"number fmt:  {1234567:,} | {0.847:.1%} | {42:05d}")

# DE example: clean and normalize a messy column value
print("\n--- DE Example: Clean a Column Value ---")
messy = "  Bangkok , Thailand  "
clean = messy.strip().lower().replace(" ,", ",")
print(f"raw:   {messy!r}")
print(f"clean: {clean!r}")

# DE example: parse a raw CSV line into typed values
print("\n--- DE Example: Parse a CSV Line ---")
line = "Laptop Pro,3,35000"
product, qty, price = line.split(",")
print(f"product={product}, revenue={int(qty) * int(price):,}")
