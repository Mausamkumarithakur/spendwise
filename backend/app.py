"""
Application factory — creates and configures the Flask app.
Use create_app() everywhere; never import 'app' directly.
"""
from __future__ import annotations
import logging
from flask import Flask
from flask_cors import CORS
from models import db
from config import Config


def create_app(config_object: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Logging
    logging.basicConfig(level=logging.INFO)
    if not app.debug:
        app.logger.setLevel(logging.WARNING)

    # Extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

    # Blueprints
    from routes.expenses import bp as expenses_bp
    app.register_blueprint(expenses_bp)

    # Health check
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
