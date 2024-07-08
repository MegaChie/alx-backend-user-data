#!/usr/bin/env python3
"""Basic Authentication"""
from flask import request
from typing import List, TypeVar, Union


class Auth():
    """Manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns a boolen Stating if authentication is needed or not"""
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path:
            return True
        for allowed in excluded_paths:
            if path in allowed:
                return False
        return True

    def authorization_header(self, request=None) -> Union[str, str]:
        """Returns the value of the header request (Authorization)"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the user of session"""
        return None
