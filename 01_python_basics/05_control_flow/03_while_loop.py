# basic while loop
print("--- Basic While ---")
count = 0
while count < 5:
    print(f"  count = {count}")
    count += 1

# while True + break
print("\n--- While with break ---")
number = 1
while True:
    print(f"  {number}", end=" ")
    number *= 2
    if number > 50:
        break
print()

# while + continue
print("\n--- While with continue ---")
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue    # skip evens
    print(i, end=" ")
print()

# retry pattern (common in data engineering)
print("\n--- Retry Pattern ---")
max_retries = 3
attempt = 0
success = False

while attempt < max_retries:
    attempt += 1
    print(f"  Attempt {attempt}...")
    if attempt == 2:     # simulate success on 2nd try
        success = True
        break

print("Succeeded!" if success else "Max retries reached.")

# loop until a sentinel value
print("\n--- Collecting Until Sentinel Value (simulated) ---")
inputs = ["10", "20", "stop", "30"]
total = 0
for val in inputs:
    if val == "stop":
        print("Stopped.")
        break
    total += int(val)
print(f"Total: {total}")
