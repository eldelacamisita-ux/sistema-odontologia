from flask import Blueprint
pacientes_bp = Blueprint('pacientes', __name__)
from . import routes