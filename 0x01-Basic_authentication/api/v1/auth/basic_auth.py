#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


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

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
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

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        email, sep, paswrd = decoded_base64_authorization_header.partition(":")
        if sep == "":
            return (None, None)
        return (email, paswrd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if not user_email or not user_pwd:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        header = self.authorization_header(request)
        base64_Token = self.extract_base64_authorization_header(header)
        auth_Token = self.decode_base64_authorization_header(base64_Token)
        user_Name, user_Password = self.extract_user_credentials(auth_Token)
        return self.user_object_from_credentials(user_Name, user_Password)
