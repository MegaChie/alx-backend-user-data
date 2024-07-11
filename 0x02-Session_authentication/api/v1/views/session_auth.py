#!/usr/bin/env python3
"""Handles all routes for the Session authentication"""
from flask import abort, jsonify, request
from os import getenv
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"],
                 strict_slashes=False)
def login() -> str:
    """Seddion login for the app"""
    email = request.form.get("email")
    paswrd = request.form.get("password")
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not paswrd or len(paswrd) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(paswrd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_ID = auth.create_session(user.id)
    cookie = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(cookie, session_ID)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout() -> str:
    """Session logout for the app"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
