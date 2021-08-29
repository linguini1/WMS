# Console Display Functionality

# Imports

from programFiles.classes import *
from programFiles.functions import *

# Loading in database object
db = Database()

# Example warehouses
db.warehouses.append(Warehouse("Ottawa", 20, "12, 13"))
db.warehouses.append(Warehouse("Toronto", 300, "13, 13"))
db.warehouses.append(Warehouse("Mississauga", 15000, "14, 13"))
db.warehouses.append(Warehouse("Kanata", 1200, "15, 13"))
db.warehouses.append(Warehouse("Lanark", 6, "16, 13"))

# Showing dashboard of warehouses
print("     Name                 | Capacity    | Coordinates\n")  # Header row
for index, warehouse in enumerate(db.warehouses):
    print(f"({index + 1})", end="")
    for _ in range(3 - len(str(index + 1))):
        print(" ", end="")
    print(warehouse)

# Provide options
