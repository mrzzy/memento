#
# Memento
# Backend
# Authentication Model
#

import jwt

from base64 import b64encode, b64decode
from datetime import datetime, timedelta

from ..utils import *
from ..config import API_JWT_KEY


# represents a token that is use to authenticate
class Token:
    JWT_ISSUER = "k8s-cms/master"
    JWT_AUDIENCE = "k8s-cms/master"

    # mapping between jwt claims and token field
    mapping = {
        ("subject", "sub"),
        ("issue_on", "iat"),
        ("expires", "exp"),
        ("user_secret", "usersec")
    }

    # create a token of the given kind
    # kind - kind of token to create "access, "refresh" or "any"
    # user_id - unique identifier of the user that created the token
    # user_secret - user secret used to validate refresh toknes
    def __init__(self, kind=None, user_id=None, user_secret=None):
        self.issue_on = datetime.utcnow()
        self.subject = f"k8s-cms/token/{kind}/{user_id}"
        self.user_secret = user_secret

        if kind == "access":
            self.expires = self.issue_on + timedelta(minutes=5)
        elif kind == "refresh":
            self.expires = self.issue_on + timedelta(days=14)
        elif kind is None:
            self.expires = None
        else:
            raise ValueError(f"Unsupported token kind: {kind}")

    # convert this object as a JWT token
    # returns this object in JWT token representation
    def to_jwt(self):
        # build payload for jwt
        payload = map_dict(self, Token.mapping)
        jwt_bytes = jwt.encode(payload, API_JWT_KEY, algorithm="HS256")
        return b64encode(jwt_bytes).decode()

    # create token using the given JWT token
    @classmethod
    def from_jwt(cls, jwt_token):
        # extract jwt
        jwt_bytes = b64decode(jwt_token)
        payload = jwt.decode(jwt_bytes, API_JWT_KEY, algorithms='HS256')
        # map fields
        token = cls()
        map_obj(token, payload, reverse_mapping(Token.mapping))
        # convert data types
        token.issue_on = datetime.fromtimestamp(token.issue_on)
        token.expires = datetime.fromtimestamp(token.expires)

        return token

    ## properties
    @property
    def kind(self):
        _, _, kind, _ = self.subject.split("/")
        return kind

    @property
    def user_id(self):
        _, _, _, user_id = self.subject.split("/")
        return user_id
