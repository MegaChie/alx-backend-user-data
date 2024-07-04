#!/usr/bin/env python3
"""Password encription"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    paswrd = password.encode()
    hashedPassword = hashpw(paswrd, bcrypt.gensalt())
    return hashedPassword
