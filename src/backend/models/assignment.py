#
# Memento
# Backend
# Assignment Models 
#

from enum import Enum
from ..app import db

# defines a task to be completed
class Task(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.String(2048), unique=False, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.BigInteger, nullable=False) # seconds
    # relationships
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", lazy=True)

# defines a event to attend
class Event(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.String(2048), unique=False, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.BigInteger, nullable=False) # seconds
    # relationships
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", lazy=True)

class Assignment(db.Model):
    # assignment item/types
    class Kind(Enum):
        Task = "task"
        Event = "event"

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    # relationship
    item_id = db.Column(db.Integer, nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignee = db.relationship("User", foreign_keys=[assignee_id], lazy=True)

    assigner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignee = db.relationship("User", foreign_keys=[assigner_id], lazy=True)
