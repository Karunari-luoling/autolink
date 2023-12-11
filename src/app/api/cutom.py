from flask import Blueprint, jsonify, request
import src.utils.config as config
from src.utils.database.update_data import update_ban_data, update_links_data
from src.utils.database.read_data import read_data
from src.utils.token_required import token_required

custom = Blueprint('custom', __name__)

@custom.route('/custom', methods=['POST'])
@token_required
def custom_view():
    json_data = request.get_json()
    partners = json_data["partners"]
    bans = json_data["ban"]
    if partners != []:
        for partner in partners:
            data = [partner['name'], partner['avatar'], partner['descr'], partner['link'], partner['siteshot'], partner['state']]
            mail = partner['mail']
            update_links_data(config.conn,data,mail)
            data = read_data(config.conn,"links")
            keys = ["id","mail", "name", "avatar", "descr", "link", "siteshot","state"]
            data = [dict(zip(keys, item)) for item in data]
            return jsonify({"partners": data})
    if bans != []:
        for ban in bans:
            update_ban_data(config.conn,ban)
            data = read_data(config.conn,"ban")
            data = [item[0] for item in data]
            return jsonify({"ban": data})
    return jsonify({"code": "err", "message": "There is no modified data"})
