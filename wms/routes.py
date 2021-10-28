print("routes.py")
# Imports
from flask import render_template, url_for, flash, redirect
from wms import app, db
from wms.forms import WarehouseForm, ItemForm, AddItemForm
from wms.models import Warehouse, Item, ItemTemplate
from wms.functions import price_format, capacity_format

# Constants
METHODS = ["GET", "POST"]


# Home page
@app.route("/", methods=METHODS)
@app.route("/home", methods=METHODS)
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
        largest = largest.name
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

    if itemForm.validate_on_submit():
        flash(f'Item "{itemForm.name.data}" created.')
        db.session.add(ItemTemplate(name=itemForm.name.data,
                                    price=itemForm.price.data,
                                    cost=itemForm.cost.data,
                                    size=itemForm.size.data,
                                    low_threshold=itemForm.lowThreshold.data))
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('home.html',
                           warehouseForm=warehouseForm,
                           itemForm=itemForm,
                           warehouseList=warehouseList,
                           possibleRevenue=possibleRevenue,
                           productionCost=productionCost,
                           remainingCapacity=remainingCapacity,
                           largestWarehouse=largest,
                           uniqueItems=len(ItemTemplate.query.all()),
                           price_format=price_format,
                           capacity_format=capacity_format)


# Warehouses list page
@app.route("/warehouses", methods=METHODS)
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
                           possibleRevenue=possibleRevenue,
                           price_format=price_format,
                           capacity_format=capacity_format)


# Items list page
@app.route("/items", methods=METHODS)
def items():

    # Forms
    itemForm = ItemForm()

    # Information
    itemList = ItemTemplate.query.all()

    possibleRevenue = 0
    for item in itemList:
        possibleRevenue += item.possible_revenue

    # Form validation messages
    if itemForm.validate_on_submit():
        flash(f'Item "{itemForm.name.data}" created.')
        db.session.add(ItemTemplate(name=itemForm.name.data,
                                    price=itemForm.price.data,
                                    cost=itemForm.cost.data,
                                    size=itemForm.size.data,
                                    low_threshold=itemForm.lowThreshold.data))
        db.session.commit()
        return redirect(url_for('items'))

    return render_template('items.html',
                           itemForm=itemForm,
                           itemList=itemList,
                           possibleRevenue=possibleRevenue,
                           price_format=price_format,
                           capacity_format=capacity_format)


# Warehouse view page
@app.route("/view-warehouse/<warehouse_name>", methods=METHODS)
def view_warehouse(warehouse_name):

    # Warehouse
    warehouse = Warehouse.query.filter_by(name=warehouse_name).first()

    # Forms
    warehouseForm = WarehouseForm()
    warehouseForm.editing_details = True
    warehouseForm.current_id = warehouse.id

    itemForm = AddItemForm()
    itemForm.update_choices()
    itemForm.warehouse = warehouse

    # Form validation messages
    if warehouseForm.validate_on_submit():
        warehouse.name = warehouseForm.name.data
        warehouse.capacity = warehouseForm.capacity.data
        db.session.commit()
        return redirect(url_for('view_warehouse', warehouse_name=warehouse.name))

    if itemForm.validate_on_submit():

        # If warehouse already has this item, add to stock
        if itemForm.item_name.data in warehouse.item_names:
            index = warehouse.item_names.index(itemForm.item_name.data)
            warehouse.items[index].quantity += itemForm.quantity.data
        else:  # New item being added
            db.session.add(Item(quantity=itemForm.quantity.data,
                                warehouse=warehouse.name,
                                item_template_id=ItemTemplate.query.filter_by(name=itemForm.item_name.data).first().id))

        db.session.commit()
        return redirect(url_for('view_warehouse', warehouse_name=warehouse.name))

    return render_template("view-warehouse.html",
                           warehouse=warehouse,
                           warehouseForm=warehouseForm,
                           itemForm=itemForm,
                           price_format=price_format,
                           capacity_format=capacity_format)


# Item view page
@app.route("/view-item/<item_name>", methods=METHODS)
def view_item(item_name):

    # Item
    item = ItemTemplate.query.filter_by(name=item_name).first()

    # Forms
    itemForm = ItemForm()
    itemForm.editing_details = True
    itemForm.current_id = item.id

    # Form validation
    if itemForm.validate_on_submit():
        item.name = itemForm.name.data
        item.price = itemForm.price.data
        item.cost = itemForm.cost.data
        item.size = itemForm.size.data
        item.low_threshold = itemForm.lowThreshold.data
        db.session.commit()
        return redirect(url_for('view_item', item_name=item.name))

    return render_template("view-item.html",
                           item=item,
                           price_format=price_format,
                           capacity_format=capacity_format,
                           itemForm=itemForm)
