from flask import Blueprint
from app.models.status import status_model,Status
import os

bp = Blueprint('base', __name__, url_prefix='/api/')

@bp.route("/get_mode")
def get_mode():
    return status_model.get().name.lower()
