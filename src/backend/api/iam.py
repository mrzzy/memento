#
# Memento
# Backend
# IAM API
#

import json

from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from .utils import parse_params
from ..mapping.iam import *
from ..ops.iam import *
from ..config import API_VERSION

iam = Blueprint("iam", __name__)

## Organisation API
# api - query organisations 
# returns organisation ids using
@iam.route(f"/api/v{API_VERSION}/iam/orgs", methods=["GET"])
def route_orgs():
    # parse query args
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    # query orgs
    org_ids = query_orgs(skip, limit)
    return jsonify(org_ids)

# api - read, create, update, delete organisations
@iam.route(f"/api/v{API_VERSION}/iam/org", methods=["POST"])
@iam.route(f"/api/v{API_VERSION}/iam/org/<org_id>", methods=["GET", "PATCH", "DELETE"])
def route_org(org_id=None):
    if request.method == "GET" and org_id:
        # get org for id
        org = get_org(org_id)
        return jsonify(org)
    elif request.method == "POST" and request.is_json:
        # create org with params in json
        params = parse_params(request, org_mapping)
        org_id = create_org(**params)
        return jsonify({ "id": org_id })
    elif request.method == "PATCH" and org_id and request.is_json:
        # parse params in json
        params = parse_params(request, org_mapping)
        # update org with params in json
        update_org(org_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and org_id:
        # delete org with params in json
        delete_org(org_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

## Team API
# api - query teams with filters
@iam.route(f"/api/v{API_VERSION}/iam/teams", methods=["GET"])
def route_teams():
    # parse query args
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    org_id = request.args.get("org", None)

    # query teams
    team_ids = query_teams(org_id, skip, limit)
    return jsonify(team_ids)

# api - read, create, update, delete teams
@iam.route(f"/api/v{API_VERSION}/iam/team", methods=["POST"])
@iam.route(f"/api/v{API_VERSION}/iam/team/<team_id>", methods=["GET", "PATCH", "DELETE"])
def route_team(team_id=None):
    if request.method == "GET" and team_id:
        # get team for id
        team = get_team(team_id)
        return jsonify(team)
    elif request.method == "POST" and request.is_json:
        # create team with params in json
        params = parse_params(request, team_mapping)
        team_id = create_team(**params)
        return jsonify({ "id": team_id })
    elif request.method == "PATCH" and team_id and request.is_json:
        # parse params in json
        params = parse_params(request, team_mapping)
        # update team with params in json
        update_team(team_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and team_id:
        # delete team with params in json
        delete_team(team_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError
