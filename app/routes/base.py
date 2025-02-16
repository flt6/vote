from flask import Blueprint
import os

bp = Blueprint('base', __name__, url_prefix='/api/')

@bp.route("/get_mode")
def get_mode():
    if os.path.exists("data/vote.json"):
        return "vote"
    elif os.path.exists("data/chain.json"):
        return "chain"
    else:
        return "config"