#
# Memento
# Backend
# Notification Models 
#

from ..app import db
from sqlalchemy.orm import validates
import re

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
        if not description:
            raise AssertionError('description must not be empty') 

        elif len(description) < 10 or len(description) > 1024:
            raise AssertionError ('must be between 10 to 1024 characters long')
        else:
            return description
