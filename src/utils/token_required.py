from functools import wraps
from flask import jsonify, request
import src.app.config as config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token_headers = request.headers.get('Authorization', None)
        if not access_token_headers:
            return jsonify({"code": "err", "msg": "Missing authorization token"}), 401
        if config.access_token == None:
            return jsonify({"code": "err", "msg": "Please log in first!"}), 401
        if access_token_headers == config.access_token and config.access_token not in config.BLACKLIST:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({"code": "err", "message": "{}".format(e)})
        else:
            return jsonify({"code":"err","msg": "The token is incorrect, please log in again!"}), 401
    return decorated_function