from flask import Flask
from flask_migrate import Migrate
import os
from app.models import db, User  # <- Make sure path is correct!
from flask_login import LoginManager

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"

    # PostgreSQL config
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Siddhant1@localhost/helping_hand"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # File uploads
    app.config["UPLOAD_FOLDER"] = os.path.join("app", "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB max
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

    db.init_app(app)
    migrate.init_app(app, db)

    # -------- Flask-Login Setup START ----------
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'   # endpoint for your login page

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -------- Flask-Login Setup END ------------

    # Register routes
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.slot import slot_bp
    app.register_blueprint(slot_bp)

    from app.routes.feedback import feedback_bp
    app.register_blueprint(feedback_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.manage_slots import manage_slots_bp
    app.register_blueprint(manage_slots_bp)

    from app.routes.manage_feedback import manage_feedback_bp
    app.register_blueprint(manage_feedback_bp)

    return app
