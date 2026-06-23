# single return value
print("--- Single Return ---")
def revenue(quantity, unit_price):
    return quantity * unit_price

print(f"revenue(3, 35000) = {revenue(3, 35000):,}")

# multiple return values (tuple unpacking) — cheapest & most expensive
print("\n--- Multiple Return Values (tuple unpacking) ---")
def price_range(prices):
    return min(prices), max(prices)

low, high = price_range([650, 2500, 8500, 35000])
print(f"cheapest={low}, most expensive={high}")

def revenue_stats(revenues):
    return {
        "orders": len(revenues),
        "total": sum(revenues),
        "min": min(revenues),
        "max": max(revenues),
        "average": sum(revenues) / len(revenues),
    }

for key, val in revenue_stats([105000, 9750, 17000, 60000]).items():
    print(f"  {key}: {val:,.2f}")

# early return (guard clause) — avoid dividing by zero orders
print("\n--- Early Return (guard clause) ---")
def average_order_value(total_revenue, num_orders):
    if num_orders == 0:
        return None             # no orders yet
    return total_revenue / num_orders

print(f"AOV(192500, 4) = {average_order_value(192500, 4):,.2f}")
print(f"AOV(0, 0)      = {average_order_value(0, 0)}")

# generator — yield order IDs lazily (stream huge ranges without building a list)
print("\n--- Generator (yield) ---")
def order_ids(start, count):
    for i in range(count):
        yield f"ORD-{start + i:04d}"

print(f"order IDs: {list(order_ids(1001, 5))}")

# closure — function returning a function (a configurable discount)
print("\n--- Function Returning Function (closure) ---")
def make_discount(rate):
    def apply(price):
        return round(price * (1 - rate), 2)
    return apply

member_price = make_discount(0.10)     # 10% off
clearance_price = make_discount(0.50)  # 50% off
print(f"member_price(35000)={member_price(35000)}, clearance_price(35000)={clearance_price(35000)}")
