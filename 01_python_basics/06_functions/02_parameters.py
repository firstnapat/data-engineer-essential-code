# positional parameters
print("--- Positional Parameters ---")
def describe_product(sku, name, price):
    print(f"  {sku}: {name} ({price:,} THB)")

describe_product("P001", "Laptop Pro", 35000)

# default parameter values
print("\n--- Default Parameters ---")
def order_status(order_id, status="pending"):
    print(f"  Order {order_id}: {status}")

order_status(1001)
order_status(1002, "shipped")
order_status(1003, status="delivered")

# keyword arguments (order-independent)
print("\n--- Keyword Arguments ---")
def create_order(customer, sku, quantity, region="Bangkok"):
    return {"customer": customer, "sku": sku, "quantity": quantity, "region": region}

order = create_order(sku="P001", customer="Alice", quantity=3, region="Chiang Mai")
print(f"  {order}")

# *args — variable number of line totals to sum into an order total
print("\n--- *args (variable positional) ---")
def order_total(*line_totals):
    return sum(line_totals)

print(f"  order_total(105000, 9750):        {order_total(105000, 9750):,}")
print(f"  order_total(105000, 9750, 60000): {order_total(105000, 9750, 60000):,}")

# **kwargs — variable number of product attributes
print("\n--- **kwargs (variable keyword) ---")
def print_product(**attrs):
    for key, value in attrs.items():
        print(f"  {key}: {value}")

print_product(sku="P001", name="Laptop Pro", stock=50, supplier="TechCorp")

def build_query(table, **conditions):
    where = " AND ".join(f"{k}='{v}'" for k, v in conditions.items())
    return f"SELECT * FROM {table} WHERE {where}"

print(f"\n  {build_query('orders', region='Bangkok', status='shipped')}")

# combining all parameter types — a logistics event logger
print("\n--- Combining All Types ---")
def log_event(event, order_id, *tags, level="INFO", **context):
    print(f"  [{level}] {event} order={order_id} tags={tags} context={context}")

log_event("ship", 1001, "express", "fragile", level="WARN", carrier="Kerry")
