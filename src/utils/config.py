import json
from flask import g
import yaml
from ruamel.yaml import YAML
import sqlite3
from src.utils.database.create_database import check_and_create_database
from concurrent.futures import ThreadPoolExecutor

db_path = check_and_create_database()
conn = sqlite3.connect(db_path, check_same_thread=False)
feishu_callback_list = []
executor = ThreadPoolExecutor(max_workers=5)

def load_config(file_path):
    with open(file_path, encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def yaml_to_json(file_path):
    data = load_config(file_path)
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data

def update_config(file_path, key, value):
    yaml = YAML()
    yaml.preserve_quotes = True
    # 加载配置
    config = load_config(file_path)
    # 更新配置
    keys = key.split('.')
    sub_config = config
    for k in keys[:-1]:
        sub_config = sub_config.setdefault(k, {})
    sub_config[keys[-1]] = value
    # 将配置写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f)
    return config

def run_app(app, config,shared_dict):
    if config['cors']:
        app.after_request(after_request)
    @app.before_request
    def before_request():
        g.shared_dict = shared_dict
    app.run(debug=config['debug'], host='0.0.0.0', port=config['port'], use_reloader=False)

def after_request(resp):
    # 允许跨域请求
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # 允许携带Content-Type Authorization请求头
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Access-Control-Request-Headers,Authorization'  
    return resp
