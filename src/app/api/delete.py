from flask import Blueprint, jsonify, request
import src.utils.config as config
from src.utils.database.delete_data import delete_ban_data, delete_links_data
from src.utils.database.read_data import read_data
from src.utils.token_required import token_required

delete = Blueprint('delete', __name__)

@delete.route('/delete', methods=['POST'])
@token_required
def delete_view():
    json_data = request.get_json()
    partners = json_data["partners"]
    bans = json_data["ban"]
    if partners != []:
        for partner in partners:
            delete_links_data(config.conn, partner)
        data = read_data(config.conn,"links")
        keys = ["id","mail", "name", "avatar", "descr", "link", "siteshot","state"]
        data = [dict(zip(keys, item)) for item in data]
        return jsonify({"partners": data})
    if bans != []:
        for ban in bans:
            delete_ban_data(config.conn, ban)
        data = read_data(config.conn,"ban")
        data = [item[0] for item in data]
        return jsonify({"ban": data})
    return jsonify({"code": "err", "message": "There is no modified data"})