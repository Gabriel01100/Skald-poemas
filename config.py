import os

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "ContraseñaDePoemas2025**")

    ADMIN_USER = "brokeme_w"
    ADMIN_PASSWORD_HASH = "pbkdf2:sha256:260000$e3Z7JP2h92z8TLrD$9f414a5b750ce21c519f1dbbd7c67c3e9f65c1a579f3385462929f84e7fe4cd6"
    print("=== CONFIG CARGADO ===")
    print("Usuario config:", ADMIN_USER)
    print("Hash config:", ADMIN_PASSWORD_HASH)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASEDIR, "poemas.db")

