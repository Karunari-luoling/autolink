import os
from flask import Blueprint, jsonify, request
from src.utils.database.read_data import read_data
import src.utils.config as config
import src.app.config as config_token

links_and_friends = Blueprint('read_json', __name__)

def get_data(json_name, include_mail):
    if json_name == "autolink":
        keys = ["mail", "name", "avatar", "descr", "link", "siteshot", "state"] if include_mail else ["name", "avatar", "descr", "link", "siteshot", "state"]
        if include_mail:
            data = read_data(config.conn, "links", keys)
        else:
            data = read_data(config.conn, "links", keys, "state != -99 AND state != -98")
        data = [dict(zip(keys, item)) for item in data]
        state_values = list(set(item['state'] for item in data))
        return jsonify({"partners": data,"state_list":state_values})
    elif json_name == "hexo_circle_of_friends":
        keys = ["name", "link", "avatar"]
        data = read_data(config.conn, "links", keys, "state != -99 AND state != -98")
        return jsonify({"friends": data})
    else:
        return jsonify({"code": "err", "msg": "暂未开放"})

@links_and_friends.route('/<json_name>', methods=['POST', 'GET'])
def links_and_friends_view(json_name):
    access_token_headers = request.headers.get('Authorization', None)
    if not access_token_headers or config_token.access_token == None:
        return get_data(json_name, False)
    if access_token_headers == config_token.access_token and config_token.access_token not in config_token.BLACKLIST:
        try:
            return get_data(json_name, True)
        except Exception as e:
            return jsonify({"code": "异常", "message": "{}".format(e)})
    else:
        return get_data(json_name, False)
