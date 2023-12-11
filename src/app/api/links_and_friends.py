import os
from flask import Blueprint, jsonify
from src.utils.database.read_data import read_data
import src.utils.config as config

links_and_friends = Blueprint('read_json', __name__)
root_dir = os.path.abspath('.')
db_path = os.path.join(root_dir, 'data', 'autolink.db')

@links_and_friends.route('/<json_name>', methods=['POST', 'GET'])
def links_and_friends_view(json_name):
    if json_name == "autolink":
        keys = ["mail", "name", "avatar", "descr", "link", "siteshot", "state"]
        data = read_data(config.conn, "links", keys, "state != 0")
        data = [dict(zip(keys, item)) for item in data]
        return jsonify({"partners": data})
    elif json_name == "hexo_circle_of_friends":
        keys = ["name", "link", "avatar"]
        data = read_data(config.conn, "links", keys, "state != 0")
        return jsonify(data)
    return jsonify({"code": "err", "msg": "暂未开放"})