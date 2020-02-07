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
    # whether the task is start/completed
    started = db.Column(db.Boolean, nullable=False, default=False)
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
    def validate_description(self, key, description):
        if len(description) > 2048:
            raise AssertionError ("Description should not exceed 2048 charactersx")
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
    def validate_description(self, key, description):
        if len(description) > 2048:
            raise AssertionError ("Description should not exceed 2048 charactersx")
        else:
            return description

    @validates('duration')
    def validate_duration(self, key, duration):
        if not duration:
            raise AssertionError ("Duration cannot be empty")
        else:
            return duration

    @validates('start_time')
    def validate_start_time(self, key, start_time):
        if not start_time:
            raise AssertionError("Start time cannot be empty.")
        else:
            return start_time

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
        kind_list = [Assignment.Kind.Task, Assignment.Kind.Event]
        if not kind:
            raise AssertionError ('kind must not be empty')
        elif kind not in kind_list:
            raise AssertionError ('Enter either Task or Event')
        else:
            return kind
