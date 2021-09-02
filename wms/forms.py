# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
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
