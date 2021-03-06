#
# Memento
# Backend
# Authentication API
#

import os
import jwt
from functools import wraps
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from flask import abort, request, Blueprint, jsonify

from ..utils import map_obj, map_dict, reverse_mapping
from ..config import API_VERSION
from ..models import *
from ..ops.auth import *

auth = Blueprint("auth", __name__)

## routes
# api route to perform login with login credentials
# POST - perform login with login credentials
# responses with a refresh token 
@auth.route(f"/api/v{API_VERSION}/auth/login", methods=["POST"])
def route_login():
    # check if can parse body as json
    credentials = request.json
    if credentials is None: abort(400)

    # perform login & generate refresh token
    jwt_token = perform_login(credentials["username"], credentials["password"])

    return jsonify({"refreshToken": jwt_token })

# api route to refresh access token with refresh token
# POST - refresh access token with refresh token
# responses with a access token
@auth.route(f"/api/v{API_VERSION}/auth/refresh", methods=["GET"])
@authenticate(kind="refresh")
def route_refresh():
    refresh_token = extract_token(request)
    # generate access token
    access_jwt_token = Token("access", refresh_token.user_id).to_jwt()

    return jsonify({"accessToken": access_jwt_token })

# api route to verify if token is valid
# GET - check if the given token is valid
# responses with user id with user currently authenticated as  if valid
@auth.route(f"/api/v{API_VERSION}/auth/check", methods=["GET"])
@authenticate(kind="any")
def route_check():
    token = extract_token(request)
    return jsonify({"success": True, "userId": token.user_id})
