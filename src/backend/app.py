#
# Memento
# Backend
# Flask App
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from .models import *

# root route
@app.route('/')
def route_root():
    return "Memento Backend API is up and running!"

# health check route
@app.route('/healthz')
def healh_check():
    return "OK"

if __name__ == "__main__":
    db.create_all()
