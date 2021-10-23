# Imports
from wms import db
from sqlalchemy.ext.hybrid import hybrid_property


# Template for creating items
class ItemTemplate(db.Model):

    """This template will simply store the information related to an item type.
    Individual items that will be associated with the warehouse they're stored in
    will inherit this information from the item templates."""

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    low_threshold = db.Column(db.Integer, nullable=False)

    instances = db.relationship('Item', backref='item_template', lazy=True)  # Instances using this item template


# Actual items
class Item(db.Model):

    """This template will be used to represent the actual items that are associated with a warehouse."""

    _id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    warehouse = db.Column(db.String(15), db.ForeignKey('warehouse.name'), nullable=False)

    item_template_id = db.Column(db.Integer, db.ForeignKey('item_template._id'), nullable=False)


# Warehouse
class Warehouse(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    items = db.relationship("Item", backref="home_warehouse", lazy=True)

    @hybrid_property
    def remaining_capacity(self):
        capacityUsed = 0
        for item in self.items:
            capacityUsed += item.quantity * ItemTemplate.query.filter_by(_id=item.item_template_id).size
        return self.capacity - capacityUsed

    @hybrid_property
    def possible_revenue(self):
        revenue = 0
        for item in self.items:
            item_temp = ItemTemplate.query.filter_by(_id=item.item_template_id)
            revenue += item.quantity * (item_temp.price - item_temp.cost)
        return revenue

    @hybrid_property
    def total_production_cost(self):
        total_production_cost = 0
        for item in self.items:
            total_production_cost += item.quantity * ItemTemplate.query.filter_by(_id=item.item_template_id).cost
        return total_production_cost

#db.drop_all()
db.create_all()