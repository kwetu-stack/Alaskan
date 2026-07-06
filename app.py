import os

from flask import Flask

from config import Config
from models import db, login_manager
from flask_migrate import Migrate

from routes.auth import auth_bp
from routes.products import products_bp
from routes.receipts import receipts_bp
from routes.api import api_bp
from flask import render_template


def initialize_database(app):
    with app.app_context():
        db.create_all()

        from models.user import User

        if not User.query.filter_by(username="admin").first():
            user = User(
                full_name="System Administrator",
                username="admin",
                role="Admin",
                active=True,
            )
            user.set_password(os.environ.get("ADMIN_PASSWORD", "admin123"))
            db.session.add(user)
            db.session.commit()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(receipts_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def home():
        return render_template("dashboard.html")

    initialize_database(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
