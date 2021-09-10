# Imports
from flask import render_template, url_for, flash, redirect
from wms import app, db  # Throws error in Pycharm but works
from wms.forms import WarehouseForm, ItemForm
from wms.models import Warehouse, Item, ItemTemplate


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
        db.session.add(Warehouse(name=warehouseForm.name.data.title(),
                                 capacity=warehouseForm.capacity.data))
        db.session.commit()
        print(Warehouse.query.all())
        return redirect(url_for('home'))

    if itemForm.validate_on_submit():
        db.session.add(ItemTemplate(name=itemForm.name.data.title(),
                                    price=itemForm.price.data,
                                    cost=itemForm.cost.data,
                                    size=itemForm.size.data,
                                    low_threshold=itemForm.lowThreshold.data))
        db.session.commit()
        print(ItemTemplate.query.all())
        flash(f'Item "{itemForm.name.data}" created.')
        return redirect(url_for('home'))

    return render_template('home.html', warehouseForm=warehouseForm, itemForm=itemForm)


# Warehouses list page
@app.route("/warehouses", methods=["GET", "POST"])
def warehouses():

    # Forms
    warehouseForm = WarehouseForm()
    itemForm = ItemForm()

    # Information
    warehouseList = Warehouse.query.all()

    # Form validation messages
    if warehouseForm.validate_on_submit():
        flash(f'Warehouse "{warehouseForm.name.data}" created.')
        db.session.add(Warehouse(name=warehouseForm.name.data,
                                 capacity=warehouseForm.capacity.data))
        db.session.commit()
        print(Warehouse.query.all())

    return render_template('warehouses.html',
                           warehouseForm=warehouseForm,
                           itemForm=itemForm,
                           warehouses=warehouseList)
