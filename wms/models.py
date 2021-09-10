# Imports
from wms import db


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


db.drop_all()
db.create_all()