#
# Memento
# Backend
# Run Server
#

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

# pathhack required to get imports to work
import sys
sys.path.append("..")

from backend import config
from backend.app import app

## start server
if __name__ == "__main__":
    port = int(config.BACKEND_PORT)
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    print("[OK] Memento Backend listening on port 5000.")
    server.serve_forever()
