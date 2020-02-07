#
# Memento
# Backend
# Authentication Ops
#

from flask import request, abort
from functools import wraps

from ..app import db
from ..api.error import AuthError
from ..models import *

# perform login for the given credentials
# return token on success others raises auth error
def perform_login(username, password):
    #TODO: add hashing
    # match find user account with given credentials
    users = User.query.filter_by(email=username, password=password)
    # check that the user exists
    if users.count() < 1:
        raise AuthError
    user = users.one()

    # build refresh token for login
    token = Token("refresh", user.id, user.password).to_jwt()
    return token


# attempts to verify the given auth token
# kind - kind of token to validate "access, "refresh" or "any"
# returns true if the token is valid, otherwise retu false
def verify_token(jwt_token, kind="access"):
    # attempt to parse JWT token
    try:
        token = Token.from_jwt(jwt_token)
    except Exception as e:
        print(e)
        return False

    # verify token fields
    if kind != "any" and token.kind != kind: return False
    if token.expires < datetime.utcnow(): return False
    if token.issue_on > datetime.utcnow(): return False
    # verify user info if a refresh token
    if kind == "refresh":
        user = User.query.get(token.user_id)
        if user is None: return False
        if user.password != token.user_secret: return False
    return True

# decorator to verify authentication before executing the given request fn
# raise AuthError on failure to authenticate
# kind - kind of token to validate "access, "refresh" or "any"
def authenticate(kind="access"):
    def auth_decorator(request_fn):
        @wraps(request_fn)
        def auth_fn(*args, **kwargs):
            # check auth header
            auth_header = request.headers.get("Authorization", "")
            if not "Bearer" in auth_header: raise AuthError
            # extract & verify jwt token
            _, jwt_token = auth_header.split()
            if not verify_token(jwt_token, kind): raise AuthError
            # run request fn
            return request_fn(*args, **kwargs)
        return auth_fn
    return auth_decorator

# extract the bearer token from the given flask request
# request - request to extract jwt token from
# returns jwt token object
def extract_token(request):
    auth_header = request.headers.get("Authorization", "")
    _, jwt_token = auth_header.split()
    token  = Token.from_jwt(jwt_token)
    return token
