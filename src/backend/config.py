#
# Memento
# Backend
# App Config
#

import os
from tempfile import gettempdir

from .utils import parse_bool

## config
# database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                         "sqlite:///" + os.path.join(gettempdir(),
                                                                     "test.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = \
    parse_bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False))
SQLALCHEMY_ECHO =  parse_bool(os.environ.get("SQLALCHEMY_ECHO", False))

# api
API_VERSION = os.environ.get("API_VERSION", "0")
