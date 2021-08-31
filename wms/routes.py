# Imports
from flask import render_template, url_for, flash, redirect
from wms import app  # Throws error in Pycharm but works

# Home page
@app.route("/")
def home():
    return "Hello!"
