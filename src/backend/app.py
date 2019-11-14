#
# Memento
# Backend
# Flask App
#

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sockets import Sockets

from . import config

# app core componments
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
starmigrate = Migrate(app, db)
cors = CORS(app, allow_headers='Content-Type')
sockets = Sockets(app)

# register api components
from .api import register_api
register_api(app, sockets)

## basic routes
# root route - backend status
@app.route('/')
def route_status():
    return "Memento Backend API is up and running!"

# k8s health check route
@app.route('/healthz')
def health_check():
    return "OK"
