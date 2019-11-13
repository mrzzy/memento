#
# Memento
# Backend
# API
#

from .error import err
from .iam import iam
from .assignment import assign
from .notification import notify, notify_ws
from .status import status

# register api components with given flask app/sockets
def register_api(app, sockets):
    # regular api
    app.register_blueprint(status)
    app.register_blueprint(err)
    app.register_blueprint(iam)
    app.register_blueprint(assign)
    app.register_blueprint(notify)
    # websockets api
    sockets.register_blueprint(notify_ws)
