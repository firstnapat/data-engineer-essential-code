# creating dictionaries — a product record
print("--- Creating Dictionaries ---")
product = {"sku": "P001", "name": "Laptop Pro", "price": 35000, "stock": 50}
config = dict(host="localhost", port=5432, db="warehouse")
print(f"product: {product}")
print(f"config:  {config}")

# accessing values — [], .get(), default
print("\n--- Accessing Values ---")
print(f"product['name']:                {product['name']}")
print(f"product.get('stock'):           {product.get('stock')}")
print(f"product.get('supplier', 'N/A'): {product.get('supplier', 'N/A')}")

try:
    _ = product["supplier"]
except KeyError as e:
    print(f"KeyError for missing key: {e}")

# modifying — add, update, pop
print("\n--- Modifying ---")
order = {"order_id": 1001, "sku": "P001"}
order["quantity"] = 3;           print(f"add quantity:  {order}")
order["sku"] = "P002";           print(f"change sku:    {order}")
removed = order.pop("quantity"); print(f"pop quantity:  {order}  removed={removed}")
order.update({"status": "paid", "region": "Bangkok"}); print(f"update:        {order}")

# keys / values / items
print("\n--- Keys / Values / Items ---")
print(f"keys():   {list(product.keys())}")
print(f"values(): {list(product.values())}")
for key, value in product.items():
    print(f"  {key}: {value}")

# nested dictionary — customers keyed by ID
print("\n--- Nested Dictionary ---")
customers = {
    "U001": {"name": "Alice", "city": "Bangkok",    "tier": "gold"},
    "U002": {"name": "Bob",   "city": "Chiang Mai", "tier": "silver"},
}
for user_id, info in customers.items():
    print(f"  {user_id}: {info['name']} ({info['tier']}, {info['city']})")

# defaultdict — total revenue per category without pre-seeding keys
print("\n--- defaultdict ---")
from collections import defaultdict

revenue_by_category = defaultdict(float)
rows = [("Electronics", 105000), ("Furniture", 17000), ("Electronics", 9750), ("Clothing", 2800)]
for category, amount in rows:
    revenue_by_category[category] += amount
print(f"revenue_by_category: {dict(revenue_by_category)}")
