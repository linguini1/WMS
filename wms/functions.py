# Imports
import csv
import sqlalchemy.exc
from wms import db
from wms.models import Warehouse, Item, ItemTemplate
from wms.forms import constants

# Formatting number outputs


# Prices
def price_format(price: float, small=False) -> str:

    """
    Returns the number value rounded to two digits, with commas added to disperse large numbers as a string.
    Larger numbers will be written with letters, such as 10,000 being 10K, etc.
    """

    # Rounds the number
    price = round(price, 2)

    if small:
        if price >= 1000:
            price /= 1000
            return "{:.2f}K".format(price)

    if price < 10000:
        return "{:,.2f}".format(price)
    else:

        if 1000000 < price < 9000000:
            price /= 1000000
            return "{:.2f}M".format(price)

        price /= 1000
        return "{:.2f}K".format(price)


# Capacities
def capacity_format(capacity: int) -> str:

    """
    Returns the capacity with comma separation. Large capacities are displayed with a letter indicating their size,
    such as 10,000u becoming 10Ku.
    """

    if capacity < 10000:
        return "{:,}".format(capacity)
    elif 10000 <= capacity <= 999999:
        capacity /= 1000
        return "{:.2f}K".format(capacity)
    else:
        capacity /= 1000000
        return "{:.2f}M".format(capacity)


# Loading CSV data
def load_data(warehouses: bool, itemTemplates: bool, items: bool) -> bool:

    """
    Loads the corresponding csv file into the database. Returns True if loading was completed successfully, False if
    there was an error.
    """

    if warehouses:
        with open('wms/resources/warehouses.csv', 'r') as file:
            csv_reader = csv.reader(file)

            next(csv_reader)  # Pass the headings

            for line in csv_reader:

                name = line[0]
                capacity = line[1]

                # Converting from string
                try:
                    capacity = int(capacity)
                except ValueError:
                    print(f"Warehouse '{name}' has a capacity of {line[1]}, which is not a valid capacity.")
                    return False

                # Verify capacity is the right value
                if not constants["MINIMUM_CAPACITY"] <= capacity <= constants["MAXIMUM_CAPACITY"]:
                    print(f"Warehouse '{name}' does not have a capacity between {constants['MINIMUM_CAPACITY']} "
                          f"and {constants['MAXIMUM_CAPACITY']}.")
                    return False

                # Check for unique name
                try:
                    db.session.add(Warehouse(name=name, capacity=capacity))
                except sqlalchemy.exc.IntegrityError:
                    print(f"Warehouse '{name}' does not have a unique name.")
                    return False

        db.session.commit()
        print("Warehouses successfully added to database.")

    if itemTemplates:
        with open('wms/resources/item-templates.csv', 'r') as file:
            csv_reader = csv.reader(file)

            next(csv_reader)  # Pass the headings

            for line in csv_reader:

                name = line[0]
                price = line[1]
                cost = line[2]
                size = line[3]
                low_threshold = line[4]

                # Convert from strings
                try:
                    price = float(price)
                    cost = float(cost)
                    size = int(size)
                    low_threshold = int(low_threshold)
                except ValueError:
                    print(f"One or more numerical values for item template '{name}' are invalid. "
                          "Review data requirements again.")
                    return False

                # Check price
                if not constants["MINIMUM_COST"] <= price <= constants["MAXIMUM_COST"]:
                    print(f"Price of item '{name}' is not between {constants['MINIMUM_COST']} and"
                          f" {constants['MAXIMUM_COST']}.")
                    return False

                # Check cost
                if not constants["MINIMUM_COST"] <= cost <= constants["MAXIMUM_COST"]:
                    print(f"Cost of item '{name}' is not between {constants['MINIMUM_COST']} and"
                          f" {constants['MAXIMUM_COST']}.")
                    return False

                # Check size
                if not constants["MINIMUM_SIZE"] <= size <= constants["MAXIMUM_SIZE"]:
                    print(f"Size of item '{name}' is not between {constants['MINIMUM_SIZE']} and"
                          f" {constants['MAXIMUM_SIZE']}.")
                    return False

                # Check low threshold
                if not constants["MINIMUM_LOW_THRESH"] <= low_threshold <= constants["MAXIMUM_LOW_THRESH"]:
                    print(f"Size of item '{name}' is not between {constants['MINIMUM_LOW_THRESH']} and"
                          f" {constants['MAXIMUM_LOW_THRESH']}.")
                    return False

                # Check unique name
                try:
                    db.session.add(ItemTemplate(name=name,
                                                price=price,
                                                cost=cost,
                                                size=size,
                                                low_threshold=low_threshold))
                except sqlalchemy.exc.IntegrityError:
                    print(f"'{name}' is not a unique item template name.")
                    return False

        db.session.commit()
        print("Item templates successfully added to database.")

    if items:
        with open('wms/resources/items.csv', 'r') as file:
            csv_reader = csv.reader(file)

            next(csv_reader)  # Pass the headings

            for line in csv_reader:

                template = line[0]
                quantity = line[1]
                warehouse = line[2]

                try:
                    quantity = int(quantity)
                except ValueError:
                    print(f"'{quantity}' is an invalid quantity for item '{template}' at warehouse '{warehouse}'.")
                    return False

                # Check quantity
                if not 1 <= quantity <= constants["MAXIMUM_CAPACITY"]:
                    print(f"Quantity of item '{template}' at warehouse '{warehouse}' is not "
                          f"between 1 and {constants['MAXIMUM_CAPACITY']}.")
                    return False

                # Check if template exists
                template_object = ItemTemplate.query.filter_by(name=template).first()
                if template_object is None:
                    print(f"The item template for '{template}' does not exist.")
                    return False

                # Check if warehouse exists
                warehouse_object = Warehouse.query.filter_by(name=warehouse).first()
                if warehouse_object is None:
                    print(f"The warehouse '{warehouse}' does not exist.")
                    return False

                try:
                    db.session.add(Item(item_template_id=template_object.id,
                                        quantity=quantity,
                                        warehouse=warehouse_object.name))

                    # Verify there's enough capacity left for the item
                    if template_object.size * quantity > warehouse_object.remaining_capacity:
                        print(f"Warehouse '{warehouse_object.name}' doesn't have enough capacity for"
                              f" {quantity} '{template_object.name}'.")
                        return False

                except ValueError:
                    print("Something")

        db.session.commit()
        print("Items successfully added to database.")

    return True
