import json

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.before_request
def before():
    if not request.path == '/autolink':
        return jsonify({"code": "正常", "message": "{}".format("输入正确参数")})


@app.route('/<json_name>', methods=['GET', 'POST'])
def read_json(json_name):
    filename = json_name + '.json'
    try:
        with open('./' + filename, encoding='utf-8') as f:
            autolink = json.load(f)
        return jsonify(autolink)
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    try:
        with open("../config/config.json", 'r') as f:
            config = json.load(f)
            port = config['port']
    except:
        print("获取配置出错")
    app.after_request(after_request)
    app.run(debug=False, host='0.0.0.0', port=port)
