# Imports
import math

# Formatting number outputs


# Prices
def price_format(price, small=False):

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
def capacity_format(capacity):

    """
    Returns the capacity with comma separation. Large capacities are displayed with a letter indicating their size,
    such as 10,000u becoming 10Ku.
    """

    if capacity < 10000:
        return "{:,}".format(capacity)
    elif 10000 <= capacity <= 999999:
        capacity /= 1000
        return "{:.2f}M".format(capacity)
    else:
        capacity /= 1000000
        return "{:.2f}M".format(capacity)


