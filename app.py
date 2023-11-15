import json
import logging
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, abort, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config['JWT_SECRET_KEY'] = 'thunder_luoling'
access_token = None
timer = None
BLACKLIST = set()
# 生成密码哈希
password_hash = generate_password_hash('thunder_luoling')
jwt = JWTManager(app)


@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(500)
def handle_server_error(e):
    return jsonify(error=str(e)), 500


@app.before_request
def before():
    if request.path not in ['/autolink', '/hexo_circle_of_friends', '/custom', '/login', '/test']:
        return jsonify({"code": "正常", "message": "{}".format("输入正确参数")})


@app.route('/login', methods=['GET', 'POST'])
def login():
    password = request.json.get('password', None)
    if not check_password_hash(password_hash, password):
        abort(403)
    global access_token, timer
    if timer is not None:
        timer.cancel()
        block_token(access_token)
    access_token = create_access_token(identity=password)
    timer = threading.Timer(24 * 60 * 60, block_token, args=[access_token])
    timer.start()
    return jsonify(access_token=access_token)


@app.route('/custom', methods=['GET', 'POST'])
def custom():
    access_token_headers = request.headers.get('Authorization', None)
    if not access_token_headers:
        return jsonify({"code": "err", "msg": "Missing authorization token"}), 401
    if access_token == None:
        return jsonify({"code": "err", "msg": "Please log in first!"}), 401
    if access_token_headers == access_token and access_token not in BLACKLIST:
        try:
            json_data = request.get_json()
        except:
            abort(400, 'Invalid JSON')
        json_data = request.get_json()
        partners = json_data["partners"]
        ban = json_data["ban"]
        dangerous = json_data["dangerous"]
        try:
            with open('./config/custom.json', encoding='utf-8') as f:
                jsons = json.load(f)
            if dangerous != '[]':
                for dangerous_item in dangerous:
                    if dangerous_item not in jsons["dangerous"]:
                        jsons["dangerous"].append(dangerous_item)
            if partners != '[]':
                for partner in partners:
                    if partner["mail"] in [partner["mail"] for partner in jsons["partners"]]:
                        for partner_item in jsons["partners"]:
                            if partner_item["mail"] == partner["mail"]:
                                for key in ('created', 'name', 'link', 'avatar', 'descr', 'siteshot'):
                                    if partner.get(key):
                                        partner_item[key] = partner.get(key)
                    else:
                        jsons["partners"].append(partner)
            if ban != '[]':
                for ban_item in ban:
                    if ban_item not in jsons["ban"]:
                        jsons["ban"].append(ban_item)
            with open('./config/custom.json', 'w', encoding='utf-8') as f:
                json.dump(jsons, f, indent=4, ensure_ascii=False)
            return jsonify(jsons)
        except Exception as e:
            return jsonify({"code": "异常", "message": "{}".format(e)})
    else:
        return jsonify({"msg": "The token is incorrect, please log in again!"}), 401


@app.route('/<json_name>', methods=['GET', 'POST'])
def read_json(json_name):
    if json_name in ["autolink", "hexo_circle_of_friends"]:
        filename = json_name + '.json'
        try:
            with open('./' + filename, encoding='utf-8') as f:
                jsons = json.load(f)
            return jsonify(jsons)
        except Exception as e:
            return jsonify({"code": "异常", "message": "{}".format(e)})


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def block_token(token):
    BLACKLIST.add(token)


if __name__ == "__main__":
    try:
        with open("./config/config.json", 'r') as f:
            config = json.load(f)
            port = config['port']
    except:
        print("获取配置出错")
    app.after_request(after_request)
    app.run(debug=False, host='0.0.0.0', port=port)
