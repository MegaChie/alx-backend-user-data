#!/usr/bin/env python3
"""Authentication for the app"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns the hashed password"""
    if not password:
        return
    salting = bcrypt.gensalt()
    hashed_paswrd = bcrypt.hashpw(password.encode('utf-8'), salting)
    return hashed_paswrd
