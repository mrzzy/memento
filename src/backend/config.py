#
# Memento
# Backend
# App Config
#

import os
from tempfile import gettempdir

## utils
# evaluates if the given environment configuration value is true or false
def parse_bool(value):
    assert(type(value) == bool or type(value) == str)

    if type(value) == bool: return value
    elif type(value) == str:
        val_lower = value.lower()

        if val_lower == "true" or val_lower == "t" or val_lower == "1": return True
        elif val_lower == "false" or val_lower == "f" or val_lower == "0": return False
        else: return False

## config
# database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                         "sqlite:///" + os.path.join(gettempdir(),
                                                                     "test.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = \
    parse_bool(os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False))
SQLALCHEMY_ECHO =  parse_bool(os.environ.get("SQLALCHEMY_ECHO", False))
