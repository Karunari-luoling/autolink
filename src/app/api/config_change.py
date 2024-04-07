import os
from flask import Blueprint, jsonify, request
from src.utils.config import load_config, update_config
from src.utils.token_required import token_required

root_dir = os.path.abspath('.')
config = Blueprint('config', __name__)
@config.route('/config', methods=['POST'])
@token_required
def config_view():
    json_data = request.get_json()
    for key, value in json_data.items():
        update_config(os.path.join(root_dir, 'config', 'config.yml'), key, value)
    #return jsonify({"code": "success", "message": "Configuration updated successfully"})
    return jsonify(load_config(os.path.join(root_dir, 'config', 'config.yml')))
