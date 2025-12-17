from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        return redirect(url_for('dashboard.index'))
    users = User.query.filter_by(is_admin=False).all()
    
    total_users = len(users)
    total_conversions = sum(u.limit_used for u in users)
    pending_count = sum(1 for u in users if not u.is_approved)
    
    return render_template('admin.html', users=users, 
                         total_users=total_users, 
                         total_conversions=total_conversions,
                         pending_count=pending_count)

@admin_bp.route('/action', methods=['POST'])
@login_required
def action():
    if not current_user.is_admin:
        return "Unauthorized", 403
        
    action = request.form.get('action')
    user_id = request.form.get('user_id')
    user = db.session.get(User, user_id)
    
    if not user:
        return "User not found", 404
        
    if action == 'approve':
        user.is_approved = True
    elif action == 'delete':
        db.session.delete(user)
    elif action == 'update_email':
        user.email = request.form.get('email')
    elif action == 'set_limit':
        limit = request.form.get('limit')
        if limit == 'unlimited':
            user.is_unlimited = True
        else:
            user.is_unlimited = False
            user.limit_total = int(limit)
            
    db.session.commit()
    return redirect(url_for('admin.index'))
