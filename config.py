import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "alaskan-sales-2026")

    os.makedirs(INSTANCE_DIR, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(INSTANCE_DIR, "alaskan.db")
    )

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://",
            1,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
