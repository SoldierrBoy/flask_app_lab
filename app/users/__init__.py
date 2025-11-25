from flask import Blueprint

users_bp = Blueprint(
    'users',
    __name__,
    template_folder='templates/users',
    static_folder='static'
)

from . import views
from . import models