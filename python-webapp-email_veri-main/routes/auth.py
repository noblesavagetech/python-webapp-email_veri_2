from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from email_validator import validate_email, EmailNotValidError
from models import db, User
from utils.tokens import generate_verification_token, verify_token
from utils.email import send_verification_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validation
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('signup.html')
        
        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('signup.html')
        
        # Validate email format
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash(f'Invalid email address: {str(e)}', 'danger')
            return render_template('signup.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'danger')
            return render_template('signup.html')
        
        # Create new user (is_verified defaults to False)
        new_user = User(email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate verification token and send email
        token = generate_verification_token(new_user.id)
        if send_verification_email(new_user.email, token):
            flash('Account created! Please check your email to verify your account.', 'success')
            login_user(new_user)
            return redirect(url_for('auth.unverified'))
        else:
            flash('Account created, but we could not send the verification email. Please contact support.', 'warning')
            return redirect(url_for('auth.login'))
    
    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        if current_user.is_verified:
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('auth.unverified'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            # Redirect to dashboard if verified, otherwise to unverified page
            if user.is_verified:
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                return redirect(url_for('auth.unverified'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/verify/<token>')
def verify_email(token):
    """Verify user's email address using the token."""
    user_id = verify_token(token)
    
    if user_id is None:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    
    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('main.dashboard') if current_user.is_authenticated else url_for('auth.login'))
    
    # Mark user as verified
    user.verify_email()
    db.session.commit()
    
    flash('Email verified successfully! You can now access your dashboard.', 'success')
    
    if current_user.is_authenticated and current_user.id == user.id:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('auth.login'))


@auth_bp.route('/unverified')
@login_required
def unverified():
    """Page shown to users who haven't verified their email."""
    if current_user.is_verified:
        return redirect(url_for('main.dashboard'))
    
    return render_template('unverified.html')


@auth_bp.route('/resend-verification')
@login_required
def resend_verification():
    """Resend verification email to the current user."""
    if current_user.is_verified:
        flash('Your email is already verified.', 'info')
        return redirect(url_for('main.dashboard'))
    
    token = generate_verification_token(current_user.id)
    if send_verification_email(current_user.email, token):
        flash('Verification email sent! Please check your inbox.', 'success')
    else:
        flash('Failed to send verification email. Please try again later.', 'danger')
    
    return redirect(url_for('auth.unverified'))
