#
# Memento
# Backend
# Notification API
#

import json
from datetime import datetime
from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse as parse_datetime
from geventwebsocket.exceptions import WebSocketError

from ..utils import parse_bool
from .utils import parse_params
from ..config import API_VERSION
from ..mapping.notification import *
from ..ops.notification import *

notify = Blueprint("notification", __name__)
notify_ws = Blueprint("notification", __name__)

## Channel API
# api - query channels
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channels")
@authenticate(kind="access")
def route_channels():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    user_id = request.args.get("user", None)
    if not user_id is None: user_id = int(user_id)

    # perform query
    channel_ids = query_channels(user_id, pending, skip, limit)
    return jsonify(channel_ids)

# api - read, create, delete channels
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channel", methods=["POST"])
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channel/<channel_id>",
              methods=["GET", "DELETE"])
@authenticate(kind="access")
def route_channel(channel_id=None):
    if request.method == "GET" and channel_id:
        # get channel for id
        channel = get_channel(channel_id)
        return jsonify(channel)
    elif request.method == "POST" and request.is_json:
        # create channel with params in json
        params = parse_params(request, channel_mapping)
        channel_id = create_channel(**params)
        return jsonify({ "id": channel_id })
    elif request.method == "DELETE" and channel_id:
        # delete channel with params in json
        delete_channel(channel_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

## Notify API
# api - query notifications
@notify.route(f"/api/v{API_VERSION}/{notify.name}/notifys")
@authenticate(kind="access")
def route_notifys():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    channel_id = request.args.get("channel", None)
    if not channel_id is None: channel_id = str(channel_id)
    scope = request.args.get("scope")
    if not scope is None: scope = str(scope)
    scope_target = request.args.get("scope_target")
    if not scope_target is None: scope_target = int(scope_target)

    # perform query
    notify_ids = query_notifys(pending, channel_id, skip, limit, scope, scope_target)
    return jsonify(notify_ids)

# api - read, create, update, delete notifys
@notify.route(f"/api/v{API_VERSION}/{notify.name}/notify", methods=["POST"])
@notify.route(f"/api/v{API_VERSION}/{notify.name}/notify/<notify_id>",
              methods=["GET", "PATCH", "DELETE"])
@authenticate(kind="access")
def route_notify(notify_id=None):
    if request.method == "GET" and notify_id:
        # get notify for id
        notify = get_notify(notify_id)
        # convert to iso date format
        # add "Z" to signal utc timezone
        notify["firingTime"] = notify["firingTime"].isoformat() + "Z"
        return jsonify(notify)
    elif request.method == "POST" and request.is_json:
        # create notify with params in json
        params = parse_params(request, notify_mapping)
        # parse datetime in iso format
        if not params["firing_time"] is None:
            params["firing_time"] = parse_datetime(params["firing_time"])

        notify_id = create_notify(**params)
        return jsonify({ "id": notify_id })
    elif request.method == "PATCH" and notify_id and request.is_json:
        # parse params in json
        params = parse_params(request, notify_mapping)
        # parse datetime in iso format
        params["firing_time"] = parse_datetime(params["firing_time"])
        # update notify with params in json
        update_notify(notify_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and notify_id:
        # delete notify with params in json
        delete_notify(notify_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

# api - subscribe to recieve notifications over websocket
@notify_ws.route(f"/api/v{API_VERSION}/{notify_ws.name}/subscribe")
def route_subscribe(socket):
    # parse request args
    channel_id = request.args.get("channel", None)
    if not channel_id is None:
        channel_ids = [ str(channel_id) ]
    else:
        # channel id is not specified, assume all channels
        channel_ids = query_channels()

    # build callback to handle subscriptions
    def handler(subscribe_id, message):
        # handle notification message
        print(f"handling message: {message}")
        notify = handle_notify(subscribe_id, message)
        if socket.closed: # check if client is still connected
            # client disconnected: unsubscribe from further callbacks
            unsubscribe_channel(subscribe_id)
        elif not notify is None and not type(notify) == str:
            # convert to iso date format
            # add "Z" to signal utc timezone
            notify["firingTime"] = notify["firingTime"].isoformat() + "Z"
            # send notification to client
            try:
                socket.send(json.dumps(notify))
            except WebSocketError:
                # websocket error: probably socket closed
                socket.close()
        elif notify == "close":
            # channel has closed: disconnect the client
            socket.close()
            unsubscribe_channel(subscribe_id)

        # return db connection to pool
        # required to prevent the connection pool from 
        # running out of connnections and causing timeouts
        db.session.remove()

    # subscribe to channels with callack
    for channel_id in channel_ids:
        print(f"subscribe channel: {channel_id}")
        subscribe_channel(channel_id, handler)

    # required to prevent websocket from closing
    # return db connection to pool
    # required to prevent the connection pool from 
    # running out of connnections and causing timeouts
    db.session.remove()
    while True: time.sleep(600)
