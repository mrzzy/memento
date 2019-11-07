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
    # TODO: cascade delete notifications
    channel = Channel.query.get(channel_id)
    db.session.delete(channel)
    db.session.commit()
