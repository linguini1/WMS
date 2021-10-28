print("models.py")
# Imports
from wms import db
from sqlalchemy.ext.hybrid import hybrid_property

# Constants
MAXIMUM_NAME_LEN = 14
LARGE_SCALE_SIZE = 150


# Template for creating items
class ItemTemplate(db.Model):

    """This template will simply store the information related to an item type.
    Individual items that will be associated with the warehouse they're stored in
    will inherit this information from the item templates."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAXIMUM_NAME_LEN), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    low_threshold = db.Column(db.Integer, nullable=False)

    instances = db.relationship('Item', backref='item_template', lazy=True)  # Instances using this item template

    @hybrid_property
    def total_stock(self):
        total_stock = 0
        for instance in self.instances:
            total_stock += instance.quantity
        return total_stock

    @hybrid_property
    def possible_revenue(self):
        return self.total_stock * (self.price - self.cost)

    @hybrid_property
    def warehouses(self):
        return [instance.warehouse for instance in self.instances]

    @hybrid_property
    def stock(self):
        stock = 0
        for instance in self.instances:
            stock += instance.quantity
        return stock


# Actual items
class Item(db.Model):

    """This template will be used to represent the actual items that are associated with a warehouse."""

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    warehouse = db.Column(db.String(MAXIMUM_NAME_LEN), db.ForeignKey('warehouse.name'), nullable=False)

    item_template_id = db.Column(db.Integer, db.ForeignKey('item_template.id'), nullable=False)


# Warehouse
class Warehouse(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAXIMUM_NAME_LEN), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    items = db.relationship("Item", backref="home_warehouse", lazy=True)

    @hybrid_property
    def remaining_capacity(self):
        capacityUsed = 0
        for item in self.items:
            capacityUsed += item.quantity * ItemTemplate.query.filter_by(id=item.item_template_id).first().size
        return self.capacity - capacityUsed

    @hybrid_property
    def possible_revenue(self):
        revenue = 0
        for item in self.items:
            item_temp = ItemTemplate.query.filter_by(id=item.item_template_id).first()
            revenue += item.quantity * (item_temp.price - item_temp.cost)
        return revenue

    @hybrid_property
    def total_production_cost(self):
        total_production_cost = 0
        for item in self.items:
            total_production_cost += item.quantity * ItemTemplate.query.filter_by(id=item.item_template_id).first().cost
        return total_production_cost

    @hybrid_property
    def low_stock_items(self):
        low_stock = []
        for item in self.items:
            if item.quantity <= ItemTemplate.query.filter_by(id=item.item_template_id).first().low_threshold:
                low_stock.append(item)
        return low_stock

    @hybrid_property
    def large_scale_items(self):
        large = []
        for item in self.items:
            if ItemTemplate.query.filter_by(id=item.item_template_id).first().size >= LARGE_SCALE_SIZE:
                large.append(item)
        return large

    @hybrid_property
    def item_names(self):
        return [ItemTemplate.query.filter_by(id=item.item_template_id).first().name for item in self.items]


db.drop_all()
db.create_all()
