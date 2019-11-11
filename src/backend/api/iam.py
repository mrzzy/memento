#
# Memento
# Backend
# IAM API
#

import json

from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from ..utils import map_keys, reverse_mapping
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
    def parse_body():
        # parse params in json
        params = request.get_json()
        params = map_keys(params, reverse_mapping(org_mapping))
        return params

    if request.method == "GET" and org_id:
        # get org for id
        org = get_org(org_id)
        return jsonify(org)
    elif request.method == "POST" and request.is_json:
        # create org with params in json
        params = parse_body()
        org_id = create_org(**params)
        return jsonify({ "id": org_id })
    elif request.method == "PATCH" and org_id and request.is_json:
        # parse params in json
        params = parse_body()
        # update org with params in json
        update_org(org_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and org_id:
        # delete org with params in json
        delete_org(org_id)
        return jsonify({"success": True })
    else:
        # malformed request
        raise NotImplementedError
