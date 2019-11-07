#
# Memento
# Backend
# Assignment Models 
#

from ..app import db
from sqlalchemy.orm import validates
import re

# defines a task to be completed
class Task(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.String(2048), unique=False, nullable=False, default="")
    deadline = db.Column(db.DateTime, nullable=False) # utc timezone
    duration = db.Column(db.BigInteger, nullable=False) # seconds
    # whether the task is completed
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # relationships
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError ("Name must not be empty")
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError ("must be between 2 to 256 characters long")
        else:
            return name
        
    @validates('description')
    def validate_description(self, key, description)
        if not description:
            raise AssertionError ("Description must not be empty")
        elif len(description) < 10 or len(description) > 2048:
            raise AssertionError ("must be between 10 to 2048 characters long")
        else:
            return description

# defines a event to attend
class Event(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    description = db.Column(db.String(2048), unique=False, nullable=False, default="")
    start_time = db.Column(db.DateTime, nullable=False) # utc timezone
    duration = db.Column(db.BigInteger, nullable=False) # seconds
    # relationships
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError ("Name must not be empty")
        elif len(name) < 2 or len(name) > 256:
            raise AssertionError ("must be between 2 to 256 characters long")
        else:
            return name
    
    @validates('description')
    def validate_description(self, key, description)
        if not description:
            raise AssertionError ("Description must not be empty")
        elif len(description) < 10 or len(description) > 2048:
            raise AssertionError ("must be between 10 to 2048 characters long")
        else:
            return description

class Assignment(db.Model):
    # assignment item/types
    class Kind:
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
    assigner = db.relationship("User", foreign_keys=[assigner_id], lazy=True)

    @validates('kind')
    def validate_kind(self, key, kind):
        if not kind:
            raise AssertionError ('kind must not be empty')
        elif kind != "task" or kind !="event":
            raise AssertionError ('Enter either task or event')
        else:
            return kind