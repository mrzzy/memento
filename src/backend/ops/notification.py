#
# Memento
# Backend
# Notification Ops
#

import time
import gevent
from flask import jsonify
from datetime import datetime

from ..app import db
from ..models.notification import *
from ..mapping.notification import *
from ..utils import apply_bound, map_dict
from ..api.error import NotFoundError
from ..messaging.broker import LocalBroker
from ..ops.auth import authenticate

# notification message broker
message_broker = LocalBroker()

## Channel Ops
# query ids of channels
# user_id - show only channels used by the user with user_id
# pending - show only channels with pending notifications
# skip - skip the first skip channels
# limit - output ids limit to the first limit channels
def query_channels(user_id=None, pending=None, skip=0, limit=None):
    channel_ids = Channel.query.with_entities(Channel.id)
    # apply filters
    if not user_id is None: 
        channel_ids = channel_ids.filter_by(user_id=user_id)
    if not pending is None:
        now = datetime.utcnow()
        channel_ids = channel_ids.outerjoin(Notification, Channel.id == Notification.channel_id)
        if pending: channel_ids = channel_ids.filter(Notification.firing_time > now)
        else: channel_ids = channel_ids.filter(Notification.firing_time <= now)
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

# create a channel for  user
# user_id - id of user using this channel
# returns id the new channel
def create_channel(user_id):
    channel = Channel(user_id=user_id)
    channel.id = str(channel)
    db.session.add(channel)
    db.session.commit()
    return channel.id

# delete the channel with the given channel id
# also cascade deletes any dependent objects
# throws NotFoundError if no channel with channel_id is found
def delete_channel(channel_id):
    channel = Channel.query.get(channel_id)
    if channel is None: raise NotFoundError
    import  traceback
    try:

        # clear subscribers to channel
        message_broker.publish(f"channel/{channel_id}", f"close/{channel_id}")
        message_broker.clear(f"channel/{channel_id}")

        # cascade delete notifications
        notify_ids = query_notifys(channel_id=channel_id)
        for notify_id in notify_ids: delete_notify(notify_id)

        db.session.delete(channel)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()

## Notification Ops
# query ids of notifications
# pending - show only pending notifications
# channel_id - show only notifications sent on channel with channel id
# skip - skip the first skip channels
# limit - output ids limit to the first limit channels
# scope - show only notifications that are scoped to the given scope 
# scope_target - show only notifications that are scoped to the given scope target 
def query_notifys(pending=None, channel_id=None, skip=0, limit=None,
                  scope=None, scope_target=None):
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
    if not scope is None:
        notify_ids = notify_ids.filter_by(scope=scope)
    if not scope_target is None:
        notify_ids = notify_ids.filter_by(scope_target=scope_target)
    # apply skip & limit
    notify_id = [ i[0] for i in notify_ids ]
    return apply_bound(notify_id, skip, limit)

# get notification for notify_id
# throws NotFoundError if no notify with notify_id is found
def get_notify(notify_id):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    # map fields to dict
    notify_dict = map_dict(notify, notify_mapping)

    return notify_dict

# create an notification
# title - title of the notification
# channel_id - id of the channel to send the notification
# subject - subject of the notification
# scope - defines type of object of which notification is scoped by
# scope_target - defines the id of the object of which the notification is scoped by
# firing_time - firing datetime of the notification
# description - description of the notification
# returns the id of the new notification
def create_notify(title, channel_id, subject=Notification.Subject.Changed,
                  scope=None, scope_target=None,
                  firing_time=None, description=""):
    # check if firing_time is none
    # if so, assume that notification fires now.
    if firing_time is None: firing_time = datetime.utcnow()

    # create notification
    notify = Notification(title=title, firing_time=firing_time, subject=subject,
                          scope=scope, scope_target=scope_target,
                          channel_id=channel_id, description=description)
    db.session.add(notify)
    db.session.commit()

    # notify users of notification change 
    if notify.pending: schedule_notify(notify.id)

    return notify.id

# update notification with the given notification id
# title - title of the notification
# channel_id - id of the channel to send the notification
# subject - subject of the notification
# scope - defines type of object of which notification is scoped by
# scope_target - defines the id of the object of which the notification is scoped by
# firing_time - firing datetime of the notification
# description - description of the notification
# returns the id of the new notification
# throws NotFoundError if no notify with notify_id is found
def update_notify(notify_id, channel_id=None, title=None, subject=None,
                  scope=None, scope_target=None,
                  firing_time=None, description=None):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    # update notification fields
    if not title is None: notify.title = title
    if not firing_time is None: notify.firing_time = firing_time
    if not channel_id is None: notify.channel_id = channel_id
    if not description is None: notify.description = description
    if not scope is None: notify.scope = scope
    if not scope_target is None: notify.scope_target = scope_target
    if not subject is None: notify.subject = subject
    db.session.commit()

    # notify users of notification change 
    if notify.pending: schedule_notify(notify.id)

# delete notification with the given notify_id
# throws NotFoundError if no notify with notify_id is found
def delete_notify(notify_id):
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    db.session.delete(notify)
    db.session.commit()

# reschedule all pending notifications for firing (ie after backend reboot.)
def reschedule_all_notifies():
    notify_ids = query_notifys(pending=True)
    for notify_id in notify_ids: schedule_notify(notify_id)

## Subscription Ops
# subscribe to recieve notifications from channel
# channel_id - id of the channel to recieve notification from
# callback(notify) - callback to run on notification
#   notify - the notification as dict, other
# returns a subscribe_id of the subscription
def subscribe_channel(channel_id, callback):
    channel = Channel.query.get(channel_id)
    if channel is None: raise NotFoundError

    return message_broker.subscribe(f"channel/{channel_id}", callback)

# unsubscribe to stop recieving notifications from channel
# subscribe_id - id of the subscription to unsubscribe
def unsubscribe_channel(subscribe_id):
    message_broker.unsubscribe(subscribe_id)


# schedule the firing of the given pending notification 
# raises ValueError if attempting to schedule a notification that is not pending.
# notify_id - id of the notification to send
def schedule_notify(notify_id):
    # extract notification fields
    notify = Notification.query.get(notify_id)
    if notify is None: raise NotFoundError
    channel_id = notify.channel_id
    firing_time = notify.firing_time

    if not notify.pending:
        # notification no longer pending
        raise ValueError( "Attempted to schedule a notification that is not pending")

    def fire_notify():
        # return db connection to pool
        # required to prevent the connection pool from 
        # running out of connnections and causing timeouts
        db.session.remove()
        # wait till notification firing time
        time_till_fire = (firing_time - datetime.utcnow()).total_seconds()
        time.sleep(max(0, time_till_fire))
        # publish firing message on channel
        message_broker.publish(f"channel/{channel_id}", f"notify/{notify_id}")
    gevent.spawn(fire_notify)

# defines a handler to handle notification/channel messages published
# returns a notification as dict if handled a notification message
# returns None if recieved a channel close message
def handle_notify(subscribe_id, message):
    notify = None
    if "notify/" in message:
        # recieved notification message
        _, notify_id = message.split("/")
        notify = get_notify(notify_id)
    elif "close/" in message:
        # recieved channel close message: unsubscribe from channel
        unsubscribe_channel(subscribe_id)
    else:
        raise NotImplementedError(f"Unknown message: {message}")

    return notify
