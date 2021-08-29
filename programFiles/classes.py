# Classes

# Imports
import WMS.programFiles.functions as fxn
import os


# Item class
class Item:

    def __init__(self, name, size, price, cost):

        # Converting to numbers
        for var in [["Size", size], ["Price", price], ["Cost", cost]]:
            try:
                var[1] = float(var[1])
            except ValueError:
                raise ValueError(f"{var[0]} must be a number.")
        size = int(size)

        # Value check
        if price <= 0 or size <= 0 or cost <= 0:
            raise ValueError("This value must be greater than 0.")
        elif price > 999999 or size < 99999999 or cost < 999999:
            raise ValueError("Number too large.")

        # Check if name already exists here

        # Name length
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or less.")

        self.name = name  # Should not already exist in database
        self.size = size
        self.price = price
        self.cost = cost
        self.quantity = 0

    def __str__(self):

        string = ""  # Base string

        for var in [[self.name, 20], [self.size, 10], [self.price, 10]]:
            string += str(var[0])
            for _ in range(var[1] - len(str(var[0]))):
                string += " "
            string += " | "

        # Cost
        string += str(self.size)

    def calculate_profit(self, percent=False):

        # Calculate the profit in $
        profit = self.price - self.cost

        # Calculate the profit margin (nearest percent)
        if percent:
            profit = round((profit / self.cost) * 100)

        return profit

    def add_items(self, amount):

        # Adding the amount to the quantity
        self.quantity += amount

    def remove_items(self, amount):

        # Checking if it's possible to remove this amount of items (no negative quantity)
        if self.quantity - amount < 0:
            print(f"There are only {self.quantity} items in stock. You removed {amount - self.quantity} too many.")

        # It's possible to remove this amount of items
        else:
            self.quantity -= amount

    def edit_name(self, newName):
        self.name = newName  # Check if this name is already being used


# Warehouse class
class Warehouse:

    def __init__(self, name, capacity, coordinates):

        # Value checking
        try:
            capacity = int(capacity)
        except ValueError:
            raise ValueError("Storage capacity must be an integer.")

        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        elif capacity > 99999999:
            raise ValueError("Capacity is too large. Try again.")

        # Coordinate conversion
        try:
            coordinates = coordinates.split(",")
            coords = []
            for _ in coordinates:
                coords.append(int(_))
            coordinates = coords
        except ValueError:
            raise ValueError("Coordinates must be two integers separated by a comma.")

        # Coordinate check goes here

        # Name length
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or less.")

        self.name = name
        self.capacity = capacity
        self.items = []  # Functionality should be added so items can be added from a pre-existing list during init
        self.coordinates = coordinates

    def __str__(self):
        string = ""  # Base string

        for var in [[self.name, 20], [self.capacity, 10]]:
            string += str(var[0])
            for _ in range(var[1] - len(str(var[0]))):
                string += " "
            string += " | "

        # Coordinates
        string += str(self.coordinates)

        return string

    def save(self):

        # Saving data for next load
        with open(f"../saveFiles/{self.name}.txt", "w") as file:
            pass

    def add_item(self, item, new=False):

        # Should provide a list of existing items to choose from
        # If a new item is added, it should have a different name than pre-existing items

        # New item is created
        if new:
            pass  # Create new item here

        # Item is selected from pre-existing list, no checks necessary
        else:
            self.items.append(item)

    def remove_item(self, itemName):
        self.items.remove(itemName)

    def edit_name(self, newName):
        self.name = newName  # Check warehouse list first to ensure no duplicate names

    def edit_coordinates(self, newCoordinates):
        self.coordinates = newCoordinates  # Check if coordinates are being used / exist

    def display_items(self):
        for item in self.items:
            print(item)


# Database class
class Database:

    def __init__(self):
        self.items = []
        self.warehouses = []

        # Check if there is a save file to read from
        if os.path.isfile("../saveFiles/main.txt"):
            # Load save data
            pass

    def add_warehouse(self):

        while True:
            # Getting required data
            name = input("Warehouse name: ")
            capacity = input("Storage capacity: ")
            coordinates = input("Coordinates: ")
            print()

            # Create warehouse
            try:
                self.warehouses.append(Warehouse(name, capacity, coordinates))
                break
            except ValueError as e:
                print(e)
                input("Press enter to continue.")
                fxn.clear_screen()

    def quit(self):
        # Write all data to the main.txt file
        pass
