#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates a user in the database and returns it as an object"""
        new_User = User(email=email, hashed_password=hashed_password)
        self._session.add(new_User)
        self._session.commit()
        return new_User

    def find_user_by(self, **kwargs) -> User:
        """Search for a user in database and returns it if found"""
        try:
            found = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
        return found

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates the user with the given ID"""
        found_User = self.find_user_by(id=user_id)
        if not found_User:
            return
        for key in kwargs:
            if hasattr(found_User, key):
                setattr(found_User, key, kwargs[key])
            else:
                raise ValueError
        self._session.commit()
