# Imports
from flask import render_template, url_for, flash, redirect
from wms import app  # Throws error in Pycharm but works
from wms.forms import WarehouseForm

# Home page
@app.route("/")
@app.route("/home")
def home():
    form = WarehouseForm()
    return render_template('home.html', form=form)
