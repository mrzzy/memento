#
# Memento
# Backend
# Flask App
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from . import config

# app core componments
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# api components
from .api.error import err
from .api.iam import iam

# register api component bluerints
app.register_blueprint(iam)
app.register_blueprint(err)

# root route
@app.route('/')
def route_root():
    return "Memento Backend API is up and running!"

# health check route
@app.route('/healthz')
def healh_check():
    return "OK"
