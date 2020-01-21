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
# returns id of user if login is success otherwise throws AuthError
def perform_login(username, password):
    #TODO: add hashing
    # match find user account with given credentials
    user_ids = User.query.with_entities(User.id)
    user_ids = user_ids.filter_by(email=username, password=password)

    if user_ids.count() < 1:
        raise AuthError
    return user_ids.one()[0]

# attempts to verify the given auth token
# kind - kind of token to validate "access, "refresh" or "any"
# returns true if the token is valid, otherwise retu false
def verify_token(jwt_token, kind="access"):
    # attempt to parse JWT token
    try:
        token = Token.from_jwt(jwt_token)
    except Exception as e:
        return False

    # verify token fields
    if kind != "any" and token.kind != kind: return False
    if token.expires < datetime.utcnow(): return False
    if token.issue_on > datetime.utcnow(): return False
    # check if user exists
    user = User.query.get(token.user_id)
    return False if user is None else True

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

