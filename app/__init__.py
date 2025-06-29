from flask import Flask
from flask_pymongo import PyMongo
import os

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"

    # MongoDB config (use your URI from MongoDB Compass or Atlas)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/helping_hand"

    app.config["UPLOAD_FOLDER"] = os.path.join("app", "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB max
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

    mongo.init_app(app)

    # Register routes
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.slot import slot_bp
    app.register_blueprint(slot_bp)

    from app.routes.feedback import feedback_bp
    app.register_blueprint(feedback_bp)

    return app
