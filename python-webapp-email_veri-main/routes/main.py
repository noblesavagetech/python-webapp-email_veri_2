from flask import Blueprint, render_template
from flask_login import login_required, current_user
from utils.decorators import verification_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
@verification_required
def dashboard():
    """Protected dashboard - only accessible to verified users."""
    return render_template('dashboard.html', user=current_user)
