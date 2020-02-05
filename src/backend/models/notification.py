#
# Memento
# Backend
# Notification Models 
#

import re
from datetime import datetime

from sqlalchemy.orm import validates

from ..app import db

# defines a channel where notifications are sent
class Channel(db.Model):
    # model fields
    id = db.Column(db.String, primary_key=True)
    # relationships
    # enforce that only one channel be created for each user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    notifications = db.relationship("Notification", backref=db.backref("channel"), lazy=True)

    # generates a unique str representation of the channel based on model fields
    # this string should be used as the model's id on creation
    # returns a string representation of the channel
    def __str__(self):
        return f"user..{self.user_id}"

# defines a notification that is send to a channel
class Notification(db.Model):
    # defines notification types
    # scope defines the type of object that the notification targets.
    # or global if the notification does not target a specific object
    class Scope:
        Task = "task"
        Event = "event"

    # subject defines the purpose of which the notification is sent
    class Subject:
        Changed = "changed"
        Assigned = "assigned"
        Started = "started"
        DueSoon = "soondue"
        Completed = "completed"
        Overdue = "overdue"

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128), nullable=False, default=Subject.Changed)
    firing_time = db.Column(db.DateTime, nullable=False) # utc timezone
    # notification scope - defines which object is referenced by notification if any
    scope = db.Column(db.String(64), nullable=True)
    scope_target = db.Column(db.Integer, nullable=True)
    # human readable title & description
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=True)

    # relationships
    channel_id = db.Column(db.String, db.ForeignKey("channel.id"), nullable=False)

    @validates('title')
    def validate_title (self, key, title):
        if not title:
            raise AssertionError('title must not be empty')
        elif len(title) < 2 or len(title) > 256:
            raise AssertionError('must be between 2 to 256 characters long')
        else:
            return title

    @validates('description')
    def validate_description (self, key, description):
        if len(description) > 1024:
            raise AssertionError("Description must not exceed 1024 characters")
        else:
            return description

    ## convenience properties
    # checks if the notification is pending firing
    # returns True if pending firing False otherwise
    @property
    def pending(self):
        time_till_fire = (datetime.utcnow() - self.firing_time).total_seconds()
        # max secs after firing time for a notification to be considered still pending 
        pending_window = 60.0
        return True if time_till_fire > -pending_window else False

    @property
    def due(self):
        time_till_fire = (datetime.utcnow() - self.firing_time).total_seconds()
        # max secs after firing time for a notification to be considered be due
        due_window = 30.0
        return True if abs(time_till_fire) < due_window else False
