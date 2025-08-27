from flask import Blueprint

bp = Blueprint("poemas", __name__)

from . import public, admin, auth
