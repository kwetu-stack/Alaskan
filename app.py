from flask import Flask

from config import Config
from models import db, login_manager
from flask_migrate import Migrate

from routes.auth import auth_bp
from routes.products import products_bp
from routes.receipts import receipts_bp
from routes.api import api_bp


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
        return "<h1>ALASKAN SALES™ is Running!</h1>"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)