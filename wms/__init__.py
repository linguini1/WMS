# Imports
from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TESTING"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = '8e3416a9c67b328517b7b758875aaea0'
desktopApp = FlaskUI(app,
                     width=1200,
                     height=675,
                     browser_path='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

from wms import routes  # Throws error but works