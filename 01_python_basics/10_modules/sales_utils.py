"""sales_utils — a small example module to be imported by 10_modules.py.

A module is just a .py file. Anything defined here (constants, functions)
can be imported elsewhere with `import sales_utils` or `from sales_utils import ...`.

Theme: tiny reusable helpers for the store domain — revenue, VAT, stock, money.
"""

# module-level constants
VAT_RATE = 0.07
REORDER_LEVEL = 10


def calc_revenue(quantity, unit_price):
    """Return total revenue for one order line."""
    return quantity * unit_price


def add_vat(amount):
    """Return amount including VAT."""
    return amount * (1 + VAT_RATE)


def is_low_stock(stock, reorder_level=REORDER_LEVEL):
    """Return True when stock has fallen to/below the reorder level."""
    return stock <= reorder_level


def format_currency(amount):
    """Format a number as Thai Baht with thousands separators."""
    return f"฿{amount:,.2f}"


# This block runs ONLY when the file is executed directly (python sales_utils.py),
# NOT when it is imported. Useful for a quick self-test.
if __name__ == "__main__":
    print("Self-test of sales_utils:")
    rev = calc_revenue(3, 35000)
    print(f"  calc_revenue(3, 35000) = {rev}")
    print(f"  add_vat({rev})         = {add_vat(rev)}")
    print(f"  is_low_stock(8)        = {is_low_stock(8)}")
    print(f"  format_currency({rev}) = {format_currency(rev)}")
