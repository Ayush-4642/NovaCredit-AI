"""
NovaCredit AI
Main Flask application entry point.

Run with:  python app.py
"""

from flask import Flask

from config import Config
from database.database import init_db

from routes.home import home_bp
from routes.predict import predict_bp
from routes.analytics import analytics_bp
from routes.dashboard import dashboard_bp
from routes.history import history_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Auto-create banking.db + tables if they do not exist
    init_db()

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {"current_year": datetime.now().year}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
