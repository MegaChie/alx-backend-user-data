#!/usr/bin/env python3
"""Flask app for the routes"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def greeting() -> str:
    """Greeats the user"""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
