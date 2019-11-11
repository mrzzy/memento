#
# Memento
# Backend
# Notification API
#

from datetime import datetime
from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse as parse_datetime

from ..utils import parse_bool
from .utils import parse_params
from ..config import API_VERSION
from ..mapping.notification import *
from ..ops.notification import *

notify = Blueprint("notification", __name__)

## Channel API
# api - query channels
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channels")
def route_channels():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    user_id = request.args.get("user_id", None)
    if not user_id is None: user_id = int(user_id)

    # perform query
    channel_ids = query_channels(user_id, pending, skip, limit)
    return jsonify(channel_ids)

# api - read, create, update, delete channels
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channel", methods=["POST"])
@notify.route(f"/api/v{API_VERSION}/{notify.name}/channel/<channel_id>",
              methods=["GET", "PATCH", "DELETE"])
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
    elif request.method == "PATCH" and channel_id and request.is_json:
        # parse params in json
        params = parse_params(request, channel_mapping)
        # update channel with params in json
        update_channel(channel_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and channel_id:
        # delete channel with params in json
        delete_channel(channel_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

