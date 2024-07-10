#!/usr/bin/env python3
"""Basic Authentication"""
from flask import request
from os import getenv
import re
from typing import List, TypeVar, Union


class Auth():
    """Manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns a boolen Stating if authentication is needed or not"""
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path:
            return True
        for allowed in map(lambda x: x.strip(), excluded_paths):
            pattern = ''
            if allowed[-1] == '*':
                pattern = '{}.*'.format(allowed[0:-1])
            elif allowed[-1] == '/':
                pattern = '{}/*'.format(allowed[0:-1])
            else:
                pattern = '{}/*'.format(allowed)
            if re.match(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> Union[str, str]:
        """Returns the value of the header request (Authorization)"""
        if not request:
            return None
        auth_Header = request.headers.get("Authorization")
        return auth_Header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the user of session"""
        return None

    def session_cookie(self, request=None):
        """Returns cookie value from a request"""
        if not request:
            return None
        cookie_Name = request.cookies.get(getenv("SESSION_NAME"))
        return cookie_Name
