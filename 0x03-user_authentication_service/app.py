#!/usr/bin/env python3
"""Flask app for the routes"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def greeting() -> str:
    return jsonify({"message": "Bienvenue"}), 200
