from flask import Blueprint, jsonify, request
from app.models.vote import VoteModel

bp = Blueprint('vote', __name__, url_prefix='/api/vote')
vote_model = VoteModel()

@bp.route('/options')
def get_options():
    if vote_model.data['show_count']:
        return jsonify({
            'title': vote_model.data['title'],
            'options': [
                {'text': opt, 'count': vote_model.data['votes'].get(opt, 0)}
                for opt in vote_model.data['options']
            ],
            'showCount': True
        })
    else:
        return jsonify({
            'title': vote_model.data['title'],
            'options': [
                {'text': opt, 'count': -1}
                for opt in vote_model.data['options']
            ],
            'showCount': False
        })
        

@bp.route('/submit', methods=['POST'])
def submit_vote():
    option = request.json.get('option')
    if vote_model.add_vote(option):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': '无效的选项'}), 400

@bp.route('/stats')
def get_stats():
    return jsonify(vote_model.get_stats())
