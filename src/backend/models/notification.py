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
    # kinds/types
    class Kind:
        Task = "task"
        Event = "event"
        Notice = "notice"

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(64), nullable=False)
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    notifications = db.relationship("Notification", backref=db.backref("channel"),
                                    lazy=True)

    @validates('kind')
    def validate_kind(self, key, kind):
        kind_list = [Channel.Kind.Task,
                     Channel.Kind.Event,
                     Channel.Kind.Notice]
        if not kind:
            raise AssertionError("kind must not be empty")
        elif kind not in kind_list:
            raise AssertionError('Enter either Event , Task or Notice')
        else:
            return kind

# defines a notification that is send to a channel
class Notification(db.Model):
    # model fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    firing_time = db.Column(db.DateTime, nullable=False) # utc timezone

    # relationships
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=True)

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
        time_till_fire = (self.firing_time - datetime.utcnow()).total_seconds()
        # max secs after firing time for a notification to be considered still pending 
        pending_window = 60.0
        return True if time_till_fire > -pending_window else False
