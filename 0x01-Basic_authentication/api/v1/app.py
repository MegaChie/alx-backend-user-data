#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
Auth_Type = os.getenv("AUTH_TYPE")
if Auth_Type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def acess_Denied(error) -> str:
    """Handels the unauthorized acess cases"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def resource_Denied(error) -> str:
    """Handels authorized user with no enough prevelages for resource"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def path_check() -> str:
    """Checks the paths the user is accessing"""
    if not auth:
        return
    excluded_paths = [
                      '/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/'
                      ]
    if auth.require_auth(request.path, excluded_paths):
        header = auth.authorization_header(request)
        user = auth.current_user(request)
        if not header:
            abort(401)
        if not user:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
