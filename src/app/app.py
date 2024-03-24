from src.app.api.upload import upload
from src.app.api.update_links import update_links
import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from src.utils.config import load_config
from src.app.api.auth import login
from src.app.api.insert_links import insert_links
from src.app.api.delete import delete
from src.app.api.config_change import config
from src.app.api.links_and_friends import links_and_friends
from flask_jwt_extended.exceptions import NoAuthorizationError

app = Flask(__name__)
root_dir = os.path.abspath('.')
app.config['JWT_SECRET_KEY'] = load_config(os.path.join(root_dir, 'config', 'config.yml'))["basic_settings"]["JWT_SECRET_KEY"]
jwt = JWTManager(app)

@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify(error=str(e)), 401

@app.errorhandler(500)
def handle_server_error(e):
    return jsonify(error=str(e)), 500

@app.before_request
def before():
    if request.path not in ['/autolink', '/hexo_circle_of_friends', '/insert_links', '/login', '/test','/config','/delete','/upload','/update_links'] and request.method != 'OPTIONS':
        return jsonify({"code": "正常", "message": "{}".format("输入正确参数")})

app.register_blueprint(login)
app.register_blueprint(links_and_friends)
app.register_blueprint(config)
app.register_blueprint(insert_links)
app.register_blueprint(delete)
app.register_blueprint(upload)
app.register_blueprint(update_links)