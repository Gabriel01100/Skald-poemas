import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_segura_123")

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASEDIR, "poemas.db")