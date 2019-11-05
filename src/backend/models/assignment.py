#
# Memento
# Backend
# Assignment Models 
#

from enum import Enum
from ..app import db

# defines a task
class Task(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
