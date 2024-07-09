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
        for a Basic Authentication.
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        authorization_header = authorization_header[6:]
        return authorization_header

    def decode_base64_authorization_header(self,
                                    base64_authorization_header: str) -> str:
        """
        Returns the decoded value
        of a Base64 string base64_authorization_header.
        """
        header = base64_authorization_header
        if not header:
            return None
        if not isinstance(header, str):
            return None
        try:
            header_Bytes = base64.b64decode(header, validate=True)
            UTF8_header = header_Bytes.decode("utf-8")
            return UTF8_header
        except (base64.binascii.Error, UnicodeDecodeError):
            pass
