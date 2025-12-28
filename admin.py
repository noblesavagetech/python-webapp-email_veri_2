"""Quick admin script to delete user"""
from app import app
from models import db, User
import sys

with app.app_context():
    email = sys.argv[1] if len(sys.argv) > 1 else None
    if not email:
        print("Usage: python admin.py <email>")
        sys.exit(1)
    
    user = User.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"✓ Deleted user: {email}")
    else:
        print(f"✗ User not found: {email}")
