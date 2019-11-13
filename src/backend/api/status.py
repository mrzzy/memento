#
# Memento
# Backend
# Status API
#

from flask import Blueprint, jsonify

from ..config import API_VERSION

status = Blueprint("status", __name__)

# api health check status 
@status.route(f"/api/v{API_VERSION}/status")
def route_api_status():
    return jsonify({"status": "OK"}), 200
