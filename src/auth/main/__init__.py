from flask import Blueprint

bp = Blueprint('main', __name__)

from auth.main import views
