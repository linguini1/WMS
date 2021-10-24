# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wms.models import Warehouse, ItemTemplate


# Warehouse form
class WarehouseForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=14)],
                       render_kw={"placeholder": "Name"})

    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=100, max=10000000)],
                            render_kw={"placeholder": "Capacity"})

    submitWarehouse = SubmitField("Submit")

    editing_details = False
    current_id = None

    def validate_name(self, name):

        if self.editing_details:
            warehouse_id = Warehouse.query.filter_by(name=name.data).first()._id

            print(warehouse_id, self.current_id)

            if warehouse_id != self.current_id:
                raise ValidationError("That warehouse name is already in use.")

        else:
            name = Warehouse.query.filter_by(name=name.data).first()
            if name:
                raise ValidationError("That warehouse name is already in use.")


# Item form
class ItemForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=15)],
                       render_kw={"placeholder": "Name"})
    price = DecimalField('Price',
                         validators=[DataRequired(),
                                     NumberRange(min=0.01, max=100000)],
                         render_kw={"placeholder": "Price"},
                         places=2)
    cost = DecimalField('Cost',
                        validators=[DataRequired(),
                                    NumberRange(min=0.01, max=100000)],
                        render_kw={"placeholder": "Cost"},
                        places=2)
    size = IntegerField('Size',
                        validators=[DataRequired(),
                                    NumberRange(min=1, max=10000)],
                        render_kw={"placeholder": "Size"})
    lowThreshold = IntegerField('Low Stock Threshold',
                                validators=[DataRequired(),
                                            NumberRange(min=1, max=10000)],
                                render_kw={"placeholder": "Low stock threshold"})
    submitItem = SubmitField("Submit")

    def validate_name(self, name):
        name = ItemTemplate.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError("That item name is already in use.")

