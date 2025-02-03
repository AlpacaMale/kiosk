from functools import wraps
from flask import session, redirect


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("email"):
            return redirect("/admin/login")
        return f(*args, **kwargs)

    return wrapper
