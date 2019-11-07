#
# Memento
# Backend
# Notification Models 
#

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

# defines a notification that is send to a channel
class Notification(db.Model):
    # notification kinds/types
    class Kind:
        Task = "task" # task
        Event = "event" # worker

    # model fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    firing_time = db.Column(db.DateTime, nullable=False) # utc timezone

    # relationships
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=True)
