#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Handels the basic authentication process of the app"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        authorization_header = authorization_header[6:]
        return authorization_header
