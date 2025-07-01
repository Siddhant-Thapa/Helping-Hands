from flask import Flask
from flask_migrate import Migrate
import os
from app.models import db  # <-- import db from your models.py

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

    # Register routes
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.slot import slot_bp
    app.register_blueprint(slot_bp)

    from app.routes.feedback import feedback_bp
    app.register_blueprint(feedback_bp)

    # (Later: register other blueprints for profile, dashboard, admin, etc.)

    return app
