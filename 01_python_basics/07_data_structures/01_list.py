# creating lists
print("--- Creating Lists ---")
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]
print(f"numbers: {numbers}, length: {len(numbers)}")

# accessing elements — indexing and slicing
print("\n--- Accessing Elements ---")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
print(f"first:    {fruits[0]}")
print(f"last:     {fruits[-1]}")
print(f"slice:    {fruits[1:3]}")
print(f"every 2nd:{fruits[::2]}")
print(f"reversed: {fruits[::-1]}")

# modifying — append, insert, extend, pop, remove
print("\n--- Modifying ---")
lst = [1, 2, 3]
lst.append(4);          print(f"append(4):       {lst}")
lst.insert(1, 99);      print(f"insert(1, 99):   {lst}")
lst.extend([5, 6]);     print(f"extend([5,6]):   {lst}")
removed = lst.pop();    print(f"pop():           {lst}  removed={removed}")
lst.remove(99);         print(f"remove(99):      {lst}")

# sorting
print("\n--- Sorting ---")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"original:          {nums}")
print(f"sorted():          {sorted(nums)}")             # returns new list
print(f"sorted(reverse):   {sorted(nums, reverse=True)}")
nums.sort()
print(f"after .sort():     {nums}")

# searching — in and count
print("\n--- Searching ---")
print(f"'apple' in fruits:  {'apple' in fruits}")
print(f"count('a' in nums): {[3,1,3,3].count(3)}")

# combining lists — + and *
print("\n--- Combining ---")
a = [1, 2, 3]
b = [4, 5, 6]
print(f"a + b: {a + b}")
print(f"a * 3: {a * 3}")
