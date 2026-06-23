import os
import sys

# importing your own module (sales_utils.py sits in the same folder)
# ensure this script's folder is importable, then import it
sys.path.insert(0, os.path.dirname(__file__))

# import the whole module — access members with module.name
print("--- import sales_utils ---")
import sales_utils

rev = sales_utils.calc_revenue(3, 35000)
print(f"sales_utils.calc_revenue(3, 35000) = {rev}")
print(f"sales_utils.VAT_RATE               = {sales_utils.VAT_RATE}")

# import specific names directly
print("\n--- from sales_utils import ... ---")
from sales_utils import is_low_stock, format_currency
print(f"is_low_stock(8)      = {is_low_stock(8)}")
print(f"format_currency(rev) = {format_currency(rev)}")

# import with an alias
print("\n--- import ... as alias ---")
import sales_utils as su
print(f"su.format_currency(su.add_vat(rev)) = {su.format_currency(su.add_vat(rev))}")

# importing from the standard library
print("\n--- standard library modules ---")
import math
from datetime import datetime
print(f"math.sqrt(144):  {math.sqrt(144)}")
print(f"math.pi:         {math.pi:.5f}")
print(f"datetime.now():  {datetime.now():%Y-%m-%d}")

# inspecting a module — __name__, __doc__, dir()
print("\n--- Inspecting a Module ---")
print(f"sales_utils.__name__: {sales_utils.__name__}")
print(f"sales_utils.__doc__:  {sales_utils.__doc__.splitlines()[0]}")
public = [n for n in dir(sales_utils) if not n.startswith("_")]
print(f"public members:       {public}")

# __name__ here is '__main__' because THIS file is the one being run
print(f"\nthis file's __name__:  {__name__}")
