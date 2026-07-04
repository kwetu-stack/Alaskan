import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "alaskan-sales-2026"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "instance", "alaskan.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False