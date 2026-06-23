# creating dictionaries
print("--- Creating Dictionaries ---")
person = {"name": "Alice", "age": 25, "city": "Bangkok"}
config = dict(host="localhost", port=5432, db="mydb")
print(f"person: {person}")
print(f"config: {config}")

# accessing values — [], .get(), default
print("\n--- Accessing Values ---")
print(f"person['name']:                {person['name']}")
print(f"person.get('age'):             {person.get('age')}")
print(f"person.get('email', 'N/A'):    {person.get('email', 'N/A')}")

try:
    _ = person["email"]
except KeyError as e:
    print(f"KeyError for missing key: {e}")

# modifying — add, update, pop
print("\n--- Modifying ---")
d = {"a": 1, "b": 2}
d["c"] = 3;               print(f"add 'c':       {d}")
d["a"] = 99;              print(f"update 'a':    {d}")
deleted = d.pop("b");     print(f"pop('b'):      {d}  deleted={deleted}")
d.update({"x": 10, "y": 20}); print(f"update dict:   {d}")

# keys / values / items
print("\n--- Keys / Values / Items ---")
product = {"name": "Laptop", "price": 35000, "stock": 50}
print(f"keys():   {list(product.keys())}")
print(f"values(): {list(product.values())}")
for key, value in product.items():
    print(f"  {key}: {value}")

# nested dictionary
print("\n--- Nested Dictionary ---")
employees = {
    "E001": {"name": "Alice", "dept": "Engineering", "salary": 60000},
    "E002": {"name": "Bob",   "dept": "Data",        "salary": 55000},
}
for emp_id, info in employees.items():
    print(f"  {emp_id}: {info['name']} ({info['dept']})")

# defaultdict — auto default value for missing keys
print("\n--- defaultdict ---")
from collections import defaultdict

word_count = defaultdict(int)
for word in ["apple", "banana", "apple", "cherry", "apple"]:
    word_count[word] += 1
print(f"word_count: {dict(word_count)}")
