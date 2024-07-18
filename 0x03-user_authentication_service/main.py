#!/usr/bin/env python3
import requests as req

base = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Tests the users endpoint"""
    with req.post(base + "/users", data={"email": email,
                                         "password": password}) as marko:
        assert marko.status_code == 200
        payload = {"email": email, "message": "user created"}
        assert marko.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests the sessions endpoint with the wrong password passed"""
    with req.post(base + "/sessions", data={"email": email,
                                            "password": password}) as marko:
        assert marko.status_code == 401
        payload = None


def log_in(email: str, password: str) -> str:
    """Tests the sessions endpoint with the correct password passed"""
    with req.post(base + "/sessions", data={"email": email,
                                            "password": password}) as marko:
        assert marko.status_code == 200
        payload = {"email": email, "message": "logged in"}
        assert marko.json() == payload
        ID = marko.cookies.get("session_id")
        return ID


def profile_unlogged() -> None:
    """Tests the profile endpoint when a session is deleted"""
    with req.get(base + "/profile") as marko:
        assert marko.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests the profile endpoint when a user is logged in"""
    header = {"cookie": "session_id={}".format(session_id)}
    with req.get(base + "/profile", headers=header) as marko:
        assert marko.status_code == 200
        payload = {"email": EMAIL}
        assert marko.json() == payload


def log_out(session_id: str) -> None:
    """Tests the sessions endpoint"""
    header = {"cookie": "session_id={}".format(session_id)}
    with req.delete(base + "/sessions", headers=header) as marko:
        assert marko.status_code == 200


def reset_password_token(email: str) -> str:
    """Tests the reset_password endpoint"""
    with req.post(base + "/reset_password", data={"email": email}) as marko:
        assert marko.status_code == 200
        ID = marko.cookies.get("reset_token")
        return ID


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests the reset_password when a new password is passed"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    with req.put(base + "/reset_password", data=data) as marko:
        assert marko.status_code == 200 or 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
