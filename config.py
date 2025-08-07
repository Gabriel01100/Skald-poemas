import os

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "ContraseñaDePoemas2025**")

    ADMIN_USER = "brokeme_w"
    ADMIN_PASSWORD_HASH = "scrypt:32768:8:1$P5Pw7UJJf1nCCNYF$b118272a3aa8585058758d97b9535ddf2aed7b8873352e824c743c67781fd2f5bd7337952c3d857993dedc3dfc6b20183bf401fa3206f9e494068c20af37c7d5"
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASEDIR, "poemas.db")

