from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, User
import secrets

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin.index'))
    return render_template('dashboard.html')

@dashboard_bp.route('/api', methods=['GET', 'POST'])
@login_required
def api():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'regenerate_key':
            current_user.api_key = secrets.token_hex(32)
            db.session.commit()
            flash('API Key regenerated successfully. Old key is now invalid.')
            
    return render_template('dashboard_api.html')

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        new_name = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_email != current_user.email:
             if User.query.filter_by(email=new_email).first():
                 flash('Email already in use.')
                 return redirect(url_for('dashboard.settings'))

        current_user.username = new_name
        current_user.email = new_email
        
        if new_password:
            if new_password != confirm_password:
                flash('Passwords do not match.')
                return redirect(url_for('dashboard.settings'))
            current_user.set_password(new_password)
            
        db.session.commit()
        flash('Profile updated.')
        
    return render_template('dashboard_settings.html')
