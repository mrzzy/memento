#
# Memento
# Backend
# API Error Handling
#

from flask import abort, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

## custom exceptions
# raised when something is not found
class NotFoundError(Exception):
    pass

## error handlers
err = Blueprint("err", __name__)

# error handler for object not found error (NotFoundError)
@err.app_errorhandler(404)
@err.app_errorhandler(NotFoundError)
def route_not_found(error):
    return jsonify({
        "error": "not-found",
        "message": "Requested object not found."
    }), 404

# error handler for conflict in db errror (IntegrityError)
@err.app_errorhandler(409)
@err.app_errorhandler(IntegrityError)
def route_conflict(error):
    return jsonify({
        "error": "conflict",
        "message": "Requested operation will cause a conflict/data integrity issue."
    }), 409

# error handler for malformed request error
@err.app_errorhandler(400)
@err.app_errorhandler(TypeError)
def route_bad_request(error):
    return jsonify({
        "error": "bad-request",
        "message": "Submitted a malformed request."
    }), 400

# error handler for method not allowed/implmented (NotImplementedError)
@err.app_errorhandler(405)
@err.app_errorhandler(NotImplementedError)
def route_method_not_allowed(error):
    return jsonify({
        "error": "method-not-allowed",
        "message": "Method used is not allowed/Implemented."
    }), 405

# error handler for request failing validation
@err.app_errorhandler(422)
@err.app_errorhandler(AssertionError)
def route_validation(error):
    return jsonify({
        "error": "validation-failed",
        "message": error.message
    }), 422

# error handler for internal server errors
@err.app_errorhandler(500)
def route_validation(error):
    return jsonify({
        "error": "intenal-server-error",
        "message": "Backend server encounted an unexpected error."
    })
