import io
import requests
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from PIL import Image
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '354f73040cdcbcd1a82bee0b45261b49e7db39f04de7f077062cbdfd11683471'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(is_admin=True).first():
            admin = User(username='admin', email='admin', is_admin=True, is_approved=True, is_unlimited=True)
            admin.set_password('admin@1234')
            db.session.add(admin)
            db.session.commit()
            print("Super Admin created: email=admin, password=admin@1234")

# --- Blueprints ---
from routes.main import main_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
from routes.api import api_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=False, threaded=True, port=5000)
