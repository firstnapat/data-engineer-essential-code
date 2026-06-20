print("--- Basic print() ---")
print("Hello, World!")
print("A", "B", "C", sep=" | ")
print("No newline -", end=" ")
print("same line")

print("\n--- f-strings ---")
name = "Alice"
score = 98.567
salary = 75000

print(f"Name: {name}")
print(f"Score: {score:.2f}")       # 2 decimal places
print(f"Score: {score:.0f}")       # rounded
print(f"Salary: {salary:,}")       # comma separator
print(f"Right-align: {name:>10}")  # right-align in 10 chars
print(f"Left-align:  {name:<10}|") # left-align in 10 chars
print(f"Zero-pad:    {42:05d}")    # 00042

print("\n--- .format() ---")
template = "Hello, {}! You scored {:.1f}%."
print(template.format("Bob", 87.5))

print("\n--- Input (simulated — normally use input()) ---")
# user_name = input("Enter your name: ")
# age = int(input("Enter your age: "))
user_name = "Bob"
age = int("30")
print(f"Hello {user_name}, you are {age} years old.")
