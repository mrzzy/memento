#
# Memento
# Backend
# Notification Ops
#

from datetime import datetime

from ..app import db
from ..models.notification import *
from ..mapping.notification import *
from ..utils import apply_bound, map_dict
from ..api.error import NotFoundError

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
        channel_ids = channel_ids.outerjoin(Notification, Channel.id == Notification.channel_id)
        if pending: channel_ids = channel_ids.filter(Notification.firing_time > now)
    # apply skip & limit
    channel_ids = [ i[0] for i in channel_ids ]
    return apply_bound(channel_ids, skip, limit)

# get channel for channel id
# returns channel as a dict
# throws NotFoundError if no channel with channel_id is found
def get_channel(channel_id):
    channel = Channel.query.get(channel_id)
    if channel is None: raise NotFoundError
    # map fields to dict
    return map_dict(channel, channel_mapping)

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
# throws NotFoundError if no channel with channel_id is found
def update_channel(channel_id, kind=None, user_id=None):
    channel = Channel.query.get(channel_id)
    if channel is None: raise NotFoundError
    # update channel fields
    if not kind is None: channel.kind = kind
    if not user_id is None: channel.user_id = user_id
    db.session.commit()

# delete the channel with the given channel id
# also cascade deletes any dependent objects
# throws NotFoundError if no channel with channel_id is found
def delete_channel(channel_id):
    channel = Channel.query.get(channel_id)
    if channel is None: raise NotFoundError

    # cascade delete notifications
    notify_ids = query_notifys(channel_id=channel_id)
    for notify_id in notify_ids: delete_notify(notify_id)

    db.session.delete(channel)
    db.session.commit()

## Notification Ops
# query ids of notifications
# pending - show only pending notifications
# channel_id - show only notifications sent on channel with channel id
# skip - skip the first skip channels
# limit - output ids limit to the first limit channels
def query_notifys(pending=None, channel_id=None, skip=0, limit=None):
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
# throws NotFoundError if no notify with notify_id is found
def get_notify(notify_id):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    # map fields to dict
    return map_dict(notify, notify_mapping)

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
# throws NotFoundError if no notify with notify_id is found
def update_notify(notify_id, title=None, firing_time=None, channel_id=None,
                  description=None):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    # update notification fields
    if not title is None: notify.title = title
    if not firing_time is None: notify.firing_time = firing_time
    if not channel_id is None: notify.channel_id = channel_id
    if not description is None: notify.description = description
    db.session.commit()

# delete notification with the given notify_id
# throws NotFoundError if no notify with notify_id is found
def delete_notify(notify_id):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    db.session.delete(notify)
    db.session.commit()
