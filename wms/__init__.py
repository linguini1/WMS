# Imports
from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)
desktopApp = FlaskUI(app, width=1200, height=675)

from wms import routes  # Throws error but works