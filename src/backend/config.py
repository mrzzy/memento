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
SQL_DATABASE = os.environ.get("SQL_DATABASE", "sqlite")
SQLALCHEMY_DATABASE_URI = ""
if SQL_DATABASE == "sqlite":
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                             "sqlite:///" + os.path.join(gettempdir(),
                                                                         "test.db"))
elif SQL_DATABASE == "postgresql":
    # load postgres config from env
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "user")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "user")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost:5432")

    # construct db connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}/{POSTGRES_DB}")
else:
    raise NotImplementedError(f"Database not supported: {SQL_DATABASE}")

SQLALCHEMY_TRACK_MODIFICATIONS = \
    parse_bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False))
SQLALCHEMY_ECHO =  parse_bool(os.environ.get("SQLALCHEMY_ECHO", False))

# api
API_VERSION = os.environ.get("API_VERSION", "0")
