"""Initialize Flask app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import routes
        from . import models

        db.create_all()

        from .dashboard.dash_app import create_dashboard

        # Write the logic to create the app only if setup is complete
        # app = create_dashboard(app)

        return app
