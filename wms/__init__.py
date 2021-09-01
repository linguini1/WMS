# Imports
from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
desktopApp = FlaskUI(app,
                     width=1200,
                     height=675,
                     browser_path='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

from wms import routes  # Throws error but works