from functools import wraps
from flask import session, redirect, url_for
from app.models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_module(module_id):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = User.query.get(session.get('id'))
            if not user or module_id not in (user.role.modules if user.role else []):
                return redirect(url_for('core.unauthorized'))
            return f(*args, **kwargs)
        return wrapped
    return decorator
