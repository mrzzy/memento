#
# Memento
# Backend
# API
#

from .error import err
from .iam import iam
from .assignment import assign
from .notification import notify
from .status import status

# register api components with given flask app
def register_api(app):
    app.register_blueprint(status)
    app.register_blueprint(err)
    app.register_blueprint(iam)
    app.register_blueprint(assign)
    app.register_blueprint(notify)
