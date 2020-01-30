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
from ..ops.auth import authenticate

assign = Blueprint("assignment", __name__)

## Task API
# api - query tasks
@assign.route(f"/api/v{API_VERSION}/{assign.name}/tasks")
@authenticate(kind="access")
def route_tasks():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    author_id = request.args.get("author", None)
    if not author_id is None: author_id = int(author_id)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    started = request.args.get("started", None)
    if not started is None: started = parse_bool(started)
    due_by = request.args.get("due-by", None)
    if not due_by is None: due_by = parse_datetime(due_by)
    assignee_id = request.args.get("assignee", None)
    if not assignee_id is None: assignee_idf = int(assignee_id)
    for_day = request.args.get("for-day", None)
    if not for_day is None: for_day = parse_datetime(for_day)

    # perform query
    task_ids = query_tasks(pending, started, author_id, due_by, skip, limit,
                           assignee_id, for_day)
    return jsonify(task_ids)

# api - read, create, update, delete tasks
@assign.route(f"/api/v{API_VERSION}/{assign.name}/task", methods=["POST"])
@assign.route(f"/api/v{API_VERSION}/{assign.name}/task/<task_id>",
              methods=["GET", "PATCH", "DELETE"])
@authenticate(kind="access")
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
@authenticate(kind="access")
def route_events():
    # parse query params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    author_id = request.args.get("author", None)
    if not author_id is None: author_id = int(author_id)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    due_by = request.args.get("limit-by", None)
    if not due_by is None: due_by = parse_datetime(due_by)
    due_by = request.args.get("due-by", None)
    if not due_by is None: due_by = parse_datetime(due_by)
    assignee_id = request.args.get("assignee", None)
    if not assignee_id is None: assignee_idf = int(assignee_id)
    for_day = request.args.get("for-day", None)
    if not for_day is None: for_day = parse_datetime(for_day)

    # perform query
    event_ids = query_events(pending, author_id, due_by, skip, limit, assignee_id,
                             for_day)
    return jsonify(event_ids)

# api - read, create, update, delete events
@assign.route(f"/api/v{API_VERSION}/{assign.name}/event", methods=["POST"])
@assign.route(f"/api/v{API_VERSION}/{assign.name}/event/<event_id>",
              methods=["GET", "PATCH", "DELETE"])
@authenticate(kind="access")
def route_event(event_id=None):
    if request.method == "GET" and event_id:
        # get event for id
        event = get_event(event_id)
        # convert to iso date format
        # add "Z" to signal utc timezone
        event["startTime"] = event["startTime"].isoformat() + "Z"
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

## Assignment API
# api - query assignments
@assign.route(f"/api/v{API_VERSION}/{assign.name}/assigns")
@authenticate(kind="access")
def route_assigns():
    # parse query params
    skip = int(request.args.get("skip", 0))
    kind = request.args.get("kind", None)
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    assigner_id = request.args.get("assigner", None)
    if not assigner_id is None: assigner_id = int(assigner_id)
    assignee_id = request.args.get("assignee", None)
    if not assignee_id is None: assignee_id = int(assignee_id)
    item_id = request.args.get("item", None)
    if not item_id is None: item_id = int(item_id)
    pending = request.args.get("pending", None)
    if not pending is None: pending = parse_bool(pending)
    due_by = request.args.get("due-by", None)
    if not due_by is None: due_by = parse_datetime(due_by)
    for_day = request.args.get("for-day", None)
    if not for_day is None: for_day = parse_datetime(for_day)

    # perform query
    assign_ids = query_assigns(kind, item_id, assignee_id, assignee_id,
                               pending, due_by, skip, limit, for_day)
    return jsonify(assign_ids)

# api - read, create, update, delete assignments
@assign.route(f"/api/v{API_VERSION}/{assign.name}/assign", methods=["POST"])
@assign.route(f"/api/v{API_VERSION}/{assign.name}/assign/<assign_id>",
              methods=["GET", "PATCH", "DELETE"])
@authenticate(kind="access")
def route_assign(assign_id=None):
    if request.method == "GET" and assign_id:
        # get assign for id
        assign = get_assign(assign_id)
        return jsonify(assign)
    elif request.method == "POST" and request.is_json:
        # create assign with params in json
        params = parse_params(request, assign_mapping)
        assign_id = create_assign(**params)
        return jsonify({ "id": assign_id })
    elif request.method == "PATCH" and assign_id and request.is_json:
        # parse params in json
        params = parse_params(request, assign_mapping)
        # update assign with params in json
        update_assign(assign_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and assign_id:
        # delete assign with params in json
        delete_assign(assign_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError
