# Item class

class Item:

    def __init__(self, name, price, cost, size, lowThreshold):
        self.name = name
        self.price = price
        self.cost = cost
        self.size = size
        self.quantity = 0
        self.lowThreshold = lowThreshold


class Warehouse:

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.items = []
        self.spaceUsed = 0
        self.remainingCapacity = self.capacity
        self.merchCostTotal = 0
        self.revenue = 0
        self.merchPriceTotal = 0
