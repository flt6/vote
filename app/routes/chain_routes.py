from flask import Blueprint, jsonify, request
from app.models.chain import ChainModel
from app.utils.pinyin import pinyinMatch

bp = Blueprint('chain', __name__, url_prefix='/api/chain')
chain_model = ChainModel()

@bp.route('/names')
def get_names():
    return jsonify(chain_model.get_stats()["unchained"])


@bp.route('/search')
def search_names():
    query = request.args.get('query', '').strip()
    names = [name for name in chain_model.data['names'] if name not in chain_model.data["chained"].keys()]
    if not query:
        return jsonify(names)
    
    filtered_names = [
        name for name in names
        if pinyinMatch(name, query)
    ]
    return jsonify(filtered_names)

@bp.route('/submit', methods=['POST'])
def submit_chain():
    name = request.json.get('name')
    if chain_model.add_chain(name):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': '无效的名字'}), 400

@bp.route('/cancel', methods=['POST'])
def cancel_chain():
    name = request.json.get('name')
    if chain_model.remove_chain(name):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': '未找到记录'}), 400

@bp.route('/stats')
def get_stats():
    return jsonify(chain_model.get_stats())

# @bp.route("/")
# def index():
#     return render_template("chain/select.html")

# @bp.route("/confirm")
# def confim_page():
#     return render_template("chain/confirm.html")