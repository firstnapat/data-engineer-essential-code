print("--- Positional Parameters ---")
def describe_person(name, age, city):
    print(f"  {name} is {age} years old from {city}.")

describe_person("Alice", 25, "Bangkok")

print("\n--- Default Parameters ---")
def greet(name, greeting="Hello"):
    print(f"  {greeting}, {name}!")

greet("Alice")
greet("Bob", "Hi")
greet("Charlie", greeting="Sawadee")

print("\n--- Keyword Arguments ---")
def create_profile(name, age, city, job="Unknown"):
    return {"name": name, "age": age, "city": city, "job": job}

profile = create_profile(age=30, name="Bob", city="Chiang Mai", job="Engineer")
print(f"  {profile}")

print("\n--- *args (variable positional) ---")
def sum_all(*numbers):
    return sum(numbers)

print(f"  sum_all(1,2,3):     {sum_all(1, 2, 3)}")
print(f"  sum_all(1,2,3,4,5): {sum_all(1, 2, 3, 4, 5)}")

print("\n--- **kwargs (variable keyword) ---")
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="Alice", age=25, city="Bangkok")

def build_query(table, **conditions):
    cond_str = " AND ".join(f"{k}='{v}'" for k, v in conditions.items())
    return f"SELECT * FROM {table} WHERE {cond_str}"

print(f"\n  {build_query('users', name='Alice', city='Bangkok')}")

print("\n--- Combining All Types ---")
def mixed(pos1, pos2, *args, kw1="default", **kwargs):
    print(f"  pos=({pos1},{pos2}), args={args}, kw1={kw1}, kwargs={kwargs}")

mixed(1, 2, 3, 4, kw1="custom", extra="value")
