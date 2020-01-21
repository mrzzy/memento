#
# Memento
# Backend
# Authentication API
#

import os
import jwt
from functools import wraps
from utils import map_obj, map_dict, reverse_mapping
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from flask import abort, request, Blueprint, jsonify

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
    uid = perform_login(credentials["username"], credentials["password"])
    jwt_token = Token("refresh", uid).to_jwt()

    return jsonify({"refreshToken": jwt_token })

# api route to refresh access token with refresh token
# POST - refresh access token with refresh token
# responses with a access token
@auth.route(f"/api/v{API_VERSION}/auth/refresh", methods=["GET"])
@authenticate(kind="refresh")
def route_refresh():
    # extract user id from refresh token
    auth_header = request.headers.get("Authorization", "")
    _, refresh_jwt_token = auth_header.split()
    refresh_token = Token.from_jwt(refresh_jwt_token)

    # generate access token
    access_jwt_token = Token("access", refresh_token.user_id).to_jwt()

    return jsonify({"accessToken": access_jwt_token })

# api route to verify if token is valid
@auth.route(f"/api/v{API_VERSION}/auth/check", methods=["GET"])
@authenticate(kind="any")
def route_check():
    return jsonify({"success": True})

