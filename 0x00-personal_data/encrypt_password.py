#!/usr/bin/env python3
"""Password encription"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    paswrd = password.encode()
    hashedPassword = hashpw(paswrd, bcrypt.gensalt())
    return hashedPassword


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Returns a boolian value indicating
    if the password match the saved one.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
