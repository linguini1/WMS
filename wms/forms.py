# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange


# Warehouse form
class WarehouseForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=15)],
                       render_kw={"placeholder": "Name"})

    capacity = IntegerField('Capacity',
                            validators=[DataRequired(),
                                        NumberRange(min=100, max=9999999)],
                            render_kw={"placeholder": "Capacity"})

    submit = SubmitField("Submit")


# Item form
class ItemForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=2, max=15)],
                       render_kw={"placeholder": "Name"})
    price = DecimalField('Price',
                         validators=[DataRequired(),
                                     NumberRange(min=0.01, max=99999.99)],
                         render_kw={"placeholder": "Price"},
                         places=2)
    cost = DecimalField('Cost',
                        validators=[DataRequired(),
                                    NumberRange(min=0.01, max=99999.99)],
                        render_kw={"placeholder": "Cost"},
                        places=2)
    size = IntegerField('Size',
                        validators=[DataRequired(),
                                    NumberRange(min=1, max=500)],
                        render_kw={"placeholder": "Size"})
    lowThreshold = IntegerField('Low Stock Threshold',
                                validators=[DataRequired(),
                                            NumberRange(min=1, max=500)],
                                render_kw={"placeholder": "Low Stock Threshold"})

