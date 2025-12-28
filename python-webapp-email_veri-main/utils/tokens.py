from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_verification_token(user_id):
    """Generate a time-sensitive, cryptographically signed token for email verification."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt='email-verification-salt')


def verify_token(token, expiration=None):
    """
    Verify and decode a verification token.
    
    Args:
        token: The token to verify
        expiration: Token expiration time in seconds (defaults to app config)
    
    Returns:
        user_id if token is valid, None otherwise
    """
    if expiration is None:
        expiration = current_app.config['TOKEN_EXPIRATION']
    
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            salt='email-verification-salt',
            max_age=expiration
        )
        return user_id
    except Exception:
        return None
