#!/usr/bin/env python3
"""0x02. Session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Taskes care of the session authentication for the app"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Resturns session ID of ussers"""
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_ID = str(uuid4())
        self.user_id_by_session_id[session_ID] = user_id
        return session_ID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_ID = self.user_id_for_session_id(cookie)
        return User.get(user_ID)

    def destroy_session(self, request=None):
        """Returns a boolen dectating seesion logout"""
        if not request:
            return False
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        session_ID = self.user_id_for_session_id(cookie)
        if not session_ID:
            return False
        del self.user_id_by_session_id[cookie]
        return True
