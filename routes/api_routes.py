from flask import Blueprint, jsonify
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/status')
def status():
    return jsonify({'status': 'API funcionando!'})
