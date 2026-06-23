# basic list comprehension
print("--- Basic List Comprehension ---")
squares = [i ** 2 for i in range(1, 6)]
print(f"squares: {squares}")

# list comprehension with a filter (if)
print("\n--- With Filter ---")
numbers = list(range(1, 11))
evens = [n for n in numbers if n % 2 == 0]
odd_squares = [n ** 2 for n in numbers if n % 2 != 0]
print(f"evens:       {evens}")
print(f"odd squares: {odd_squares}")

# transforming strings
print("\n--- String Operations ---")
words = ["  hello  ", "  world  ", "  python  "]
cleaned = [w.strip().upper() for w in words]
print(f"cleaned: {cleaned}")

fruits = ["apple", "banana", "cherry", "avocado", "blueberry"]
a_fruits = [f for f in fruits if f.startswith("a")]
print(f"starts with 'a': {a_fruits}")

# nested list comprehension (flatten / transpose)
print("\n--- Nested List Comprehension ---")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [val for row in matrix for val in row]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"flattened:   {flat}")
print(f"transposed:  {transposed}")

# dictionary comprehension
print("\n--- Dictionary Comprehension ---")
names = ["alice", "bob", "charlie"]
name_lengths = {name: len(name) for name in names}
print(f"name lengths: {name_lengths}")

prices = {"apple": 30, "banana": 15, "cherry": 80}
expensive = {k: v for k, v in prices.items() if v > 20}
print(f"expensive: {expensive}")

# set comprehension
print("\n--- Set Comprehension ---")
nums = [1, 2, 2, 3, 3, 3, 4]
unique_squares = {n ** 2 for n in nums}
print(f"unique squares: {unique_squares}")
