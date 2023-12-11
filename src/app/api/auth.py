import os
import threading
from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import create_access_token
from src.app.config import get_password, block_token
import src.app.config as config
from werkzeug.security import check_password_hash

root_dir = os.path.abspath('.')
login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
def login_view():
    password = request.json.get('password', None)
    password_hash = get_password(password)
    if not check_password_hash(password_hash, password):
        abort(403)
    if config.timer is not None:
        config.timer.cancel()
        block_token(config.access_token)
    config.access_token = create_access_token(identity=password)
    config.timer = threading.Timer(24 * 60 * 60, block_token, args=[config.access_token])
    config.timer.start()
    return jsonify(code=200,access_token=config.access_token)