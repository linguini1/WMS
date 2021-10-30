# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wms.models import Warehouse, ItemTemplate

# Constants
constants = {
    "MINIMUM_COST": 0.01,
    "MAXIMUM_COST": 100000,
    "MINIMUM_SIZE": 1,
    "MAXIMUM_SIZE": 10000,
    "MINIMUM_CAPACITY": 100,
    "MAXIMUM_CAPACITY": 10000000,
    "MINIMUM_LOW_THRESH": 1,
    "MAXIMUM_LOW_THRESH": 10000,
    "MINIMUM_NAME_LEN": 2,
    "MAXIMUM_NAME_LEN": 14
}


# Warehouse form
class WarehouseForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=constants["MINIMUM_NAME_LEN"], max=constants["MAXIMUM_NAME_LEN"])],
                       render_kw={"placeholder": "Name"})

    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=constants["MINIMUM_CAPACITY"], max=constants["MAXIMUM_CAPACITY"])],
                            render_kw={"placeholder": "Capacity"})

    submitWarehouse = SubmitField("Submit")

    editing_details = False
    current_id = None

    def validate_name(self, name):

        if self.editing_details:
            matching_warehouse = Warehouse.query.filter_by(name=name.data).first()

            try:
                warehouse_id = matching_warehouse.id
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
                                   Length(min=2, max=constants["MAXIMUM_NAME_LEN"])],
                       render_kw={"placeholder": "Name"})
    price = DecimalField('Price',
                         validators=[DataRequired(),
                                     NumberRange(min=constants["MINIMUM_COST"], max=constants["MAXIMUM_COST"])],
                         render_kw={"placeholder": "Price"},
                         places=2)
    cost = DecimalField('Cost',
                        validators=[DataRequired(),
                                    NumberRange(min=constants["MINIMUM_COST"], max=constants["MAXIMUM_COST"])],
                        render_kw={"placeholder": "Cost"},
                        places=2)
    size = IntegerField('Size',
                        validators=[DataRequired(),
                                    NumberRange(min=constants["MINIMUM_SIZE"], max=constants["MAXIMUM_SIZE"])],
                        render_kw={"placeholder": "Size"})
    lowThreshold = IntegerField('Low Stock Threshold',
                                validators=[DataRequired(),
                                            NumberRange(min=constants["MINIMUM_LOW_THRESH"],
                                                        max=constants["MAXIMUM_LOW_THRESH"])],
                                render_kw={"placeholder": "Low stock threshold"})
    submitItem = SubmitField("Submit")

    editing_details = False
    current_id = None

    def validate_name(self, name):
        if self.editing_details:
            matching_item = ItemTemplate.query.filter_by(name=name.data).first()

            try:
                item_id = matching_item.id
                if item_id != self.current_id:
                    raise ValidationError("That item name is already in use.")
            except AttributeError:
                pass

        else:
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
                                        NumberRange(min=1, max=constants["MAXIMUM_CAPACITY"])],
                            render_kw={"placeholder": "Quantity"})

    submitItem = SubmitField("Submit")

    def update_choices(self):
        self.item_name.choices = [item.name for item in ItemTemplate.query.all()]

    def validate_quantity(self, quantity):
        item_size = ItemTemplate.query.filter_by(name=self.item_name.data).first().size
        if self.warehouse.remaining_capacity < quantity.data * item_size:
            raise ValidationError(f"Needs {quantity.data * item_size - self.warehouse.remaining_capacity}u more space.")
