#
# Memento
# Backend
# Assignment API
#

from datetime import datetime
from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse as parse_datetime

from ..utils import parse_bool
from .utils import parse_params
from ..config import API_VERSION
from ..mapping.assignment import *
from ..ops.assignment import *

assign = Blueprint("assignment", __name__)

## Task API
# api - query tasks
@assign.route(f"/api/v{API_VERSION}/{assign.name}/tasks")
def route_tasks():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    author_id = request.args.get("author", None)
    if not author_id is None: author_id = int(author_id)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    limit_by = request.args.get("limit-by", None)
    if not limit_by is None: limit_by = parse_datetime(limit_by)

    # perform query
    task_ids = query_tasks(pending, author_id, limit_by, skip, limit)
    return jsonify(task_ids)

# api - read, create, update, delete tasks
@assign.route(f"/api/v{API_VERSION}/{assign.name}/task", methods=["POST"])
@assign.route(f"/api/v{API_VERSION}/{assign.name}/task/<task_id>", 
              methods=["GET", "PATCH", "DELETE"])
def route_task(task_id=None):
    if request.method == "GET" and task_id:
        # get task for id
        task = get_task(task_id)
        # convert to iso date format
        # add "Z" to signal utc timezone
        task["deadline"] = task["deadline"].isoformat() + "Z"
        return jsonify(task)
    elif request.method == "POST" and request.is_json:
        # create task with params in json
        params = parse_params(request, task_mapping)
        # parse datetime in iso format
        params["deadline"] = parse_datetime(params["deadline"])
        task_id = create_task(**params)
        return jsonify({ "id": task_id })
    elif request.method == "PATCH" and task_id and request.is_json:
        # parse params in json
        params = parse_params(request, task_mapping)
        # parse datetime in iso format
        params["deadline"] = parse_datetime(params["deadline"])
        # update task with params in json
        update_task(task_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and task_id:
        # delete task with params in json
        delete_task(task_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError


## Event API
# api - query events
@assign.route(f"/api/v{API_VERSION}/{assign.name}/events")
def route_events():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    author_id = request.args.get("author", None)
    if not author_id is None: author_id = int(author_id)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    limit_by = request.args.get("limit-by", None)
    if not limit_by is None: limit_by = parse_datetime(limit_by)

    # perform query
    event_ids = query_events(pending, author_id, limit_by, skip, limit)
    return jsonify(event_ids)

# api - read, create, update, delete events
@assign.route(f"/api/v{API_VERSION}/{assign.name}/event", methods=["POST"])
@assign.route(f"/api/v{API_VERSION}/{assign.name}/event/<event_id>",
              methods=["GET", "PATCH", "DELETE"])
def route_event(event_id=None):
    if request.method == "GET" and event_id:
        # get event for id
        event = get_event(event_id)
        # convert to iso date format
        # add "Z" to signal utc timezone
        event["start_time"] = event["start_time"].isoformat() + "Z"
        return jsonify(event)
    elif request.method == "POST" and request.is_json:
        # create event with params in json
        params = parse_params(request, event_mapping)
        # parse datetime in iso format
        params["start_time"] = parse_datetime(params["start_time"])
        event_id = create_event(**params)
        return jsonify({ "id": event_id })
    elif request.method == "PATCH" and event_id and request.is_json:
        # parse params in json
        params = parse_params(request, event_mapping)
        # parse datetime in iso format
        params["start_time"] = parse_datetime(params["start_time"])
        # update event with params in json
        update_event(event_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and event_id:
        # delete event with params in json
        delete_event(event_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError
