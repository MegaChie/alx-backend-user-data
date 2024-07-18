#!/usr/bin/env python3
"""Authentication for the app"""
import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


def _hash_password(password: str) -> bytes:
    """Returns the hashed password"""
    if not password:
        return
    salting = bcrypt.gensalt()
    hashed_paswrd = bcrypt.hashpw(password.encode('utf-8'), salting)
    return hashed_paswrd


def _generate_uuid() -> str:
    """Returns the session ID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self):
        """Initializes the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Hashes the password of the new user"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            hased_Pasword = _hash_password(password)
            new_User = self._db.add_user(email, hased_Pasword)
            return new_User
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Returns True is user is logged in, False is not"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False
        paswrd = user.hashed_password
        check_Paswrd = password.encode("utf-8")
        return bcrypt.checkpw(check_Paswrd, paswrd)

    def create_session(self, email: str) -> str:
        """Returns the session ID saved to the user in the database"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return None
        ID = _generate_uuid()
        self._db.update_user(user.id, session_id=ID)
        return ID

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns the user with corresponding session ID"""
        if not session_id:
            return None
        try:
            found = self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None
        return found

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session by removings its session ID"""
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for the user and returns it"""
        try:
            found = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password of a user based on the reset token"""
        found = self._db.find_user_by(reset_token=reset_token)
        if not found:
            raise ValueError
        new_Paswrd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_Paswrd,
                             reset_token=None)
