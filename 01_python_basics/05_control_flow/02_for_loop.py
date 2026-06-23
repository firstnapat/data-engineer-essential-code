# iterating a list
print("--- Iterating a List ---")
fruits = ["apple", "banana", "cherry", "date"]
for fruit in fruits:
    print(f"  {fruit}")

# range() — start, stop, step
print("\n--- range() ---")
for i in range(5):
    print(i, end=" ")
print()
for i in range(1, 11, 2):   # start, stop, step
    print(i, end=" ")
print()
for i in range(10, 0, -2):  # countdown
    print(i, end=" ")
print()

# enumerate() — index + value
print("\n--- enumerate() ---")
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"  [{index}] {color}")

# zip() — loop over two lists together
print("\n--- zip() ---")
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# iterating a dictionary
print("\n--- Iterating a Dictionary ---")
person = {"name": "Alice", "age": 25, "city": "Bangkok"}
for key, value in person.items():
    print(f"  {key}: {value}")

# break and continue
print("\n--- break and continue ---")
for i in range(10):
    if i == 3:
        continue    # skip 3
    if i == 7:
        break       # stop at 7
    print(i, end=" ")
print()

# nested loop
print("\n--- Nested Loop (matrix) ---")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for val in row:
        print(f"{val:3}", end="")
    print()
