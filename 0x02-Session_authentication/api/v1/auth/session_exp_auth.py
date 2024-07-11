#!/usr/bin/env python3
"""Session expiration process"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session expiration managing for the app"""
    def __init__(self):
        """Initiates the class"""
        time_to_Live = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(time_to_Live)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """Creates and returns a session ID"""
        session_ID = super().create_session(user_id)
        if not session_ID:
            return None
        self.user_id_by_session_id[session_ID] = {
                                                  "user_id": user_id,
                                                  "created_at": datetime.now()
                                                  }
        return session_ID

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns user_id from the session dictionary"""
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        user_Session = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return user_Session.get('user_id')
        created_at = user_Session.get('created_at')
        if created_at is None:
            return None
        if (created_at +
                timedelta(seconds=self.session_duration)) < datetime.now():
            return None
        return user_Session.get('user_id')
