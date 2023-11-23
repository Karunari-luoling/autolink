import json
import threading
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, abort, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError

app = Flask(__name__)
with open("./config/config.json", 'r') as f:
    config = json.load(f)
    password_config = config['password']
    JWT_SECRET_KEY_config = config['JWT_SECRET_KEY']
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY_config
access_token = None
timer = None
BLACKLIST = set()
# 生成密码哈希
password_hash = generate_password_hash(password_config)
jwt = JWTManager(app)

@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(500)
def handle_server_error(e):
    return jsonify(error=str(e)), 500


@app.before_request
def before():
    if request.path not in ['/autolink', '/hexo_circle_of_friends', '/custom', '/login', '/test','/config']:
        return jsonify({"code": "正常", "message": "{}".format("输入正确参数")})


@app.route('/login', methods=['POST'])
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
    return jsonify(code=200,access_token=access_token)

@app.route('/config', methods=['GET', 'POST'])
def config():
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
        try:
            with open('./config/config.json','r', encoding='utf-8') as f:
                jsons = json.load(f)
            for key in ('url', 'port', 'fentch_interval', 'JWT_SECRET_KEY', 'password'):
                if json_data.get(key):
                    jsons[key] = json_data.get(key)
            with open('./config/config.json', 'w', encoding='utf-8') as f:
                json.dump(jsons, f, indent=4, ensure_ascii=False)
            return jsons
        except Exception as e:
            return jsonify({"code": "异常", "message": "{}".format(e)})
    else:
        return jsonify({"msg": "The token is incorrect, please log in again!"}), 401

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
            print(json_data)
        except:
            abort(400, 'Invalid JSON')
        partners = json_data["partners"]
        ban = json_data["ban"]
        dangerous = json_data["dangerous"]
        try:
            with open('./config/custom.json', encoding='utf-8') as f:
                jsons = json.load(f)
            if dangerous:
                jsons["dangerous"] = dangerous
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
            if ban:
                jsons["ban"] = ban
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
    # 允许跨域请求
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # 允许携带Content-Type Authorization请求头
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Access-Control-Request-Headers,Authorization'  
    return resp


def block_token(token):
    BLACKLIST.add(token)


if __name__ == "__main__":
    try:
        with open("./config/config.json", 'r') as f:
            config = json.load(f)
            port = config['port']
            password_config = config['password']
            JWT_SECRET_KEY_config = config['JWT_SECRET_KEY']
    except:
        print("获取配置出错")
    app.after_request(after_request)
    app.run(debug=True, host='0.0.0.0', port=port)
