# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wms.models import Warehouse, ItemTemplate

# Constants
MINIMUM_COST = 0.01
MAXIMUM_COST = 100000
MINIMUM_SIZE = 1
MAXIMUM_SIZE = 10000
MINIMUM_CAPACITY = 100
MAXIMUM_CAPACITY = 10000000
MINIMUM_LOW_THRESH = 1
MAXIMUM_LOW_THRESH = 10000
MINIMUM_NAME_LEN = 2
MAXIMUM_NAME_LEN = 14


# Warehouse form
class WarehouseForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=MINIMUM_NAME_LEN, max=MAXIMUM_NAME_LEN)],
                       render_kw={"placeholder": "Name"})

    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=MINIMUM_CAPACITY, max=MAXIMUM_CAPACITY)],
                            render_kw={"placeholder": "Capacity"})

    submitWarehouse = SubmitField("Submit")

    editing_details = False
    current_id = None

    def validate_name(self, name):

        if self.editing_details:
            matching_warehouse = Warehouse.query.filter_by(name=name.data).first()

            try:
                warehouse_id = matching_warehouse._id
                if warehouse_id != self.current_id:
                    raise ValidationError("That warehouse name is already in use.")
            except AttributeError:
                pass

        else:
            name = Warehouse.query.filter_by(name=name.data).first()
            if name:
                raise ValidationError("That warehouse name is already in use.")


# Item form
class ItemForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=MAXIMUM_NAME_LEN)],
                       render_kw={"placeholder": "Name"})
    price = DecimalField('Price',
                         validators=[DataRequired(),
                                     NumberRange(min=MINIMUM_COST, max=MAXIMUM_COST)],
                         render_kw={"placeholder": "Price"},
                         places=2)
    cost = DecimalField('Cost',
                        validators=[DataRequired(),
                                    NumberRange(min=MINIMUM_COST, max=MAXIMUM_COST)],
                        render_kw={"placeholder": "Cost"},
                        places=2)
    size = IntegerField('Size',
                        validators=[DataRequired(),
                                    NumberRange(min=MINIMUM_SIZE, max=MAXIMUM_SIZE)],
                        render_kw={"placeholder": "Size"})
    lowThreshold = IntegerField('Low Stock Threshold',
                                validators=[DataRequired(),
                                            NumberRange(min=MINIMUM_LOW_THRESH, max=MAXIMUM_LOW_THRESH)],
                                render_kw={"placeholder": "Low stock threshold"})
    submitItem = SubmitField("Submit")

    def validate_name(self, name):
        name = ItemTemplate.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError("That item name is already in use.")


# Add item to warehouse form
class AddItemForm(FlaskForm):

    warehouse = None

    item_name = SelectField('Item',
                            validators=[DataRequired()],
                            choices=[item.name for item in ItemTemplate.query.all()])

    quantity = IntegerField('Quantity',
                            validators=[DataRequired(),
                                        NumberRange(min=1, max=MAXIMUM_CAPACITY)],
                            render_kw={"placeholder": "Quantity"})

    submitItem = SubmitField("Submit")

    def update_choices(self):
        self.item_name.choices = [item.name for item in ItemTemplate.query.all()]

    def validate_quantity(self, quantity, item_name):
        item_size = ItemTemplate.query.filter_by(name=item_name).first().size
        if self.warehouse.remaining_capacity < quantity * item_size:
            raise ValidationError(f"Needs {quantity * item_size - self.warehouse.remaining_capacity}u more space.")
