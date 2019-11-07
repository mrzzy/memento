#
# Memento
# Backend
# Notification Ops
#

from datetime import datetime

from ..app import db
from ..models.notification import *
from .utils import apply_bound, map_dict

## Channel Ops
# query ids of channels
# user_id - show only channels used by the user with user_id
# pending - show only channels with pending notifications
# skip - skip the first skip channels
# limit - output ids limit to the first limit channels
def query_channels(user_id=None, pending=None, skip=0, limit=None):
    channel_ids = Channel.query.with_entities(Channel.id)
    # apply filters
    if not user_id is None: channel_ids.filter_by(user_id=user_id)
    if not pending is None:
        now = datetime.utcnow()
        channel_ids.join(Notification, Channel.id == Notification.channel_id)
        if pending: channel_ids = channel_ids.filter(Notification.firing_time > now)
        else: channel_ids = channel_ids.filter(Notification.firing_time <= now)
    # apply skip & limit
    channel_ids = [ i[0] for i in channel_ids ]
    return apply_bound(channel_ids, skip, limit)

# get channel for channel id
# returns channel as a dict
def get_channel(channel_id):
    channel = Channel.query.get(channel_id)
    # map fields to dict
    mapping = [
        ("id", "id"),
        ("kind", "kind"),
        ("user_id", "userId")
    ]
    return map_dict(channel, mapping)

# create a channel
# kind - kind of channel (task/event/notice)
# user_id - id of user using this channel
# returns id the new channel
def create_channel(kind, user_id):
    channel = Channel(kind=kind, user_id=user_id)
    db.session.add(channel)
    db.session.commit()
    return channel.id

# update channel with channel_id
# kind - kind of channel (task/event/notice)
# user_id - id of user using this channel
def update_channel(channel_id, kind=None, user_id=None):
    channel = Channel.query.get(channel_id)
    if not kind is None: channel.kind = kind
    if not user_id is None: channel.user_id = user_id
    db.session.commit()

# delete the channel with the given channel id
# als cascade deletes any dependent objects
def delete_channel(channel_id):
    # cascade delete notifications
    notify_ids = query_notify(channel_id=channel_id)
    for notify_id in notify_ids: delete_notify(notify_id)

    channel = Channel.query.get(channel_id)
    db.session.delete(channel)
    db.session.commit()

## Notification Ops
# query ids of notifications
# pending - show only pending notifications
# channel_id - show only notifications sent on channel with channel id
# skip - skip the first skip channels
# limit - output ids limit to the first limit channels
def query_notify(pending=None, channel_id=None, skip=0, limit=None):
    notify_ids = Notification.query.with_entities(Notification.id)
    # apply filters
    if not pending is None:
        now = datetime.utcnow()
        if pending == True:
            notify_ids = notify_ids.filter(Notification.firing_time > now)
        else:
            notify_ids = notify_ids.filter(Notification.firing_time <= now)
    if not channel_id is None:
        notify_ids = notify_ids.filter_by(channel_id=channel_id)
    # apply skip & limit
    notify_id = [ i[0] for i in notify_ids ]
    return apply_bound(notify_id, skip, limit)

# get notification for notify_id
def get_notify(notify_id):
    notify = Notification.query.get(notify_id)
    # map fields to dict
    mapping = [
        ("title", "title"),
        ("description", "description"),
        ("firing_time", "firingTime"),
        ("channel_id", "channelId")
    ]
    return map_dict(notify, mapping)

# create an notification
# title - title of the notification
# firing_time - firing datetime of the notification
# channel_id - id of the channel to send the notification
# returns the id of the new notification
def create_notify(title, firing_time, channel_id, description=""):
    notify = Notification(title=title, firing_time=firing_time,
                          channel_id=channel_id, description=description)
    db.session.add(notify)
    db.session.commit()

    return notify.id

# update notification with the given notification id
# title - title of the notification
# firing_time - firing datetime of the notification
# channel_id - id of the channel to send the notification
# returns the id of the new notification
def update_notify(notify_id, title=None, firing_time=None, channel_id=None,
                  description=None):
    notify = Notification.query.get(notify_id)
    if not title is None: notify.title = title
    if not firing_time is None: notify.firing_time = firing_time
    if not channel_id is None: notify.channel_id = channel_id
    if not description is None: notify.description = description
    db.session.commit()

# delete notification with the given notify_id
def delete_notify(notify_id):
    notify = Notification.query.get(notify_id)
    db.session.delete(notify)
    db.session.commit()

