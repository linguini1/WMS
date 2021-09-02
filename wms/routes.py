# Imports
from flask import render_template, url_for, flash, redirect
from wms import app  # Throws error in Pycharm but works
from wms.forms import WarehouseForm, ItemForm

# Home page
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():

    # Forms
    warehouseForm = WarehouseForm()
    itemForm = ItemForm()

    # Form validation messages
    if warehouseForm.validate_on_submit():
        flash(f'Warehouse "{warehouseForm.name.data}" created.')

    if itemForm.validate_on_submit():
        flash(f'Item "{itemForm.name.data}" created.')

    return render_template('home.html', warehouseForm=warehouseForm, itemForm=itemForm)
