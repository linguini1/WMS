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

    # Information
    warehouseList = Warehouse.query.all()

    try:
        largest = warehouseList[0]

        for warehouse in warehouseList:
            if warehouse.capacity > largest.capacity:
                largest = warehouse

    except IndexError:
        largest = "No data"

    productionCost = 0
    remainingCapacity = 0
    possibleRevenue = 0
    for warehouse in warehouseList:
        productionCost += warehouse.total_production_cost
        remainingCapacity += warehouse.remaining_capacity
        possibleRevenue += warehouse.possible_revenue

    # Form validation messages
    if warehouseForm.validate_on_submit():
        flash(f'Warehouse "{warehouseForm.name.data}" created.')
        db.session.add(Warehouse(name=warehouseForm.name.data.title(),
                                 capacity=warehouseForm.capacity.data))
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('home.html',
                           warehouseForm=warehouseForm,
                           itemForm=itemForm,
                           warehouseList=warehouseList,
                           possibleRevenue=possibleRevenue,
                           productionCost=productionCost,
                           remainingCapacity=remainingCapacity,
                           largestWarehouse=largest.name)


# Warehouses list page
@app.route("/warehouses", methods=["GET", "POST"])
def warehouses():

    # Forms
    warehouseForm = WarehouseForm()

    # Information
    warehouseList = Warehouse.query.all()
    possibleRevenue = 0
    for warehouse in warehouseList:
        possibleRevenue += warehouse.possible_revenue

    # Form validation messages
    if warehouseForm.validate_on_submit():
        flash(f'Warehouse "{warehouseForm.name.data}" created.')
        db.session.add(Warehouse(name=warehouseForm.name.data,
                                 capacity=warehouseForm.capacity.data))
        db.session.commit()
        return redirect(url_for('warehouses'))

    return render_template('warehouses.html',
                           warehouseForm=warehouseForm,
                           warehouses=warehouseList,
                           possibleRevenue=possibleRevenue)
