from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def verification_required(f):
    """
    Decorator to protect routes that require email verification.
    Redirects unverified users to a "check your email" page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        
        if not current_user.is_verified:
            flash('Please verify your email address to access this page.', 'warning')
            return redirect(url_for('auth.unverified'))
        
        return f(*args, **kwargs)
    
    return decorated_function
