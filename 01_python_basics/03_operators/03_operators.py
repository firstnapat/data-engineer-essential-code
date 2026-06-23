a, b = 10, 3

# arithmetic operators
print("--- Arithmetic ---")
print(f"{a} + {b}  = {a + b}")
print(f"{a} - {b}  = {a - b}")
print(f"{a} * {b}  = {a * b}")
print(f"{a} / {b}  = {a / b:.4f}  (true division)")
print(f"{a} // {b} = {a // b}     (floor division)")
print(f"{a} % {b}  = {a % b}      (modulus)")
print(f"{a} ** {b} = {a ** b}     (power)")

# comparison operators
print("\n--- Comparison ---")
print(f"{a} == {b}: {a == b}")
print(f"{a} != {b}: {a != b}")
print(f"{a} >  {b}: {a > b}")
print(f"{a} <  {b}: {a < b}")

# logical operators (and / or / not)
print("\n--- Logical ---")
print(f"True and False: {True and False}")
print(f"True or  False: {True or False}")
print(f"not True:       {not True}")
print(f"(5>3) and (2<4): {(5 > 3) and (2 < 4)}")

# assignment operators (+=, -=, ...)
print("\n--- Assignment ---")
total = 100
total += 50;  print(f"+=50:  {total}")
total -= 30;  print(f"-=30:  {total}")
total *= 2;   print(f"*=2:   {total}")
total //= 3;  print(f"//=3:  {total}")

# membership operators (in / not in)
print("\n--- Membership ---")
fruits = ["apple", "banana", "cherry"]
print(f"'apple' in fruits:      {'apple' in fruits}")
print(f"'grape' not in fruits:  {'grape' not in fruits}")
print(f"'ban' in 'banana':      {'ban' in 'banana'}")

# identity operators (is) — same object vs equal value
print("\n--- Identity ---")
lst1 = [1, 2, 3]
lst2 = [1, 2, 3]
lst3 = lst1
print(f"lst1 is lst2: {lst1 is lst2}  (different objects)")
print(f"lst1 is lst3: {lst1 is lst3}  (same object)")
