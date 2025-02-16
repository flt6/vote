from flask import Blueprint, jsonify, request, make_response,redirect
from app.models.chain import chain_model
from app.models.vote import vote_model
from app.models.status import status_model,Status
from app.utils.session_manager import SessionManager
from functools import wraps
from .base import get_mode
import os

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

session_manager = SessionManager()

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD",None)
if ADMIN_PASSWORD is None:
    ADMIN_PASSWORD = "admin"
    print("Using defalut password `admin`")
    print("Please set environment varible ADMIN_PASSWORD for safety.")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if not session_manager.validate_session(session_id):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/login', methods=['POST'])
def login():
    session_manager.clear_expired()
    password = request.json.get('password')
    if password == ADMIN_PASSWORD:
        session_id = session_manager.create_session()
        mode = "/admin/config" if get_mode()=="config" else "/admin/dashboard"
        response = make_response(jsonify({'success': True,"jump":mode}))
        response.set_cookie('session_id', session_id, httponly=True, secure=True)
        return response
    return jsonify({'success': False, 'error': '密码错误'}), 401

# @bp.route('/logout', methods=['POST'])
# def logout():
#     session_id = request.cookies.get('session_id')
#     if session_id in session_manager.sessions:
#         del session_manager.sessions[session_id]
#     response = make_response(jsonify({'success': True}))
#     response.delete_cookie('session_id')
#     return response

@bp.route('/config/chain', methods=['POST'])
@login_required
def config_chain():
    names = request.json.get('names', [])
    chain_model.set_names(names)
    status_model.set(Status.CHAIN)
    return jsonify({'success': True})

@bp.route('/config/vote', methods=['POST'])
@login_required
def config_vote():
    data:dict = request.json
    vote_model.set_config(
        data.get('title', ''),
        data.get('options', []),
        data.get('show_count', False)
    )
    status_model.set(Status.VOTE)
    return jsonify({'success': True})

@bp.route('/reset', methods=['POST'])
@login_required
def reset_system():
    vote_model.reset()
    chain_model.reset()
    status_model.set(Status.CONFIG)
    return jsonify({'success': True})