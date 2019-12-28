#
# Memento
# Backend
# Run Server
#

from gevent import monkey
monkey.patch_all()
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
    print(f"[OK] Started Memento Backend: API v{config.API_VERSION}"
          f", port {config.BACKEND_PORT}")
    server.serve_forever()
