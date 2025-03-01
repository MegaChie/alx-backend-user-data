#!/usr/bin/env python3
"""Flask app for the routes"""
from flask import abort, Flask, jsonify, redirect, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def greeting() -> str:
    """Greeats the user"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Register new users"""
    email = request.form.get("email")
    paswrd = request.form.get("password")
    try:
        AUTH.register_user(email, paswrd)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Impliment session login"""
    email = request.form.get("email")
    paswrd = request.form.get("password")
    if not email or not paswrd:
        abort(401)
    if not AUTH.valid_login(email, paswrd):
        abort(401)
    ID = AUTH.create_session(email)
    responce = jsonify({"email": email, "message": "logged in"})
    responce.set_cookie("session_id", ID)
    return responce


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Logs out a user from the app"""
    ID = request.cookies.get("session_id")
    if not ID:
        abort(403)
    user = AUTH.get_user_from_session_id(ID)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    response = jsonify({"message": "logout successful, session distroyed"})
    response.delete_cookie("session_id")
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """States the email of the user with the passed session ID"""
    ID = request.cookies.get("session_id")
    if not ID:
        abort(403)
    user = AUTH.get_user_from_session_id(ID)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """States the passwords reset token for a user"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Handles the password changing for the app"""
    email = request.form.get("email")
    new_Paswrd = request.form.get("new_password")
    token = request.form.get("reset_token")
    try:
        AUTH.update_password(token, new_Paswrd)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
