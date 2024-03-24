from datetime import timezone, datetime
from flask import Blueprint, jsonify, request
import src.utils.config as config
from src.utils.database.insert_data import insert_ban_data, insert_links_data
from src.utils.database.read_data import read_data
from src.utils.token_required import token_required

insert_links = Blueprint('insert_links', __name__)

@insert_links.route('/insert_links', methods=['POST'])
@token_required
def custom_view():
    json_data = request.get_json()
    partners = json_data["partners"]
    bans = json_data["ban"]
    if partners != []:
        for partner in partners:
            created = int(datetime.now(timezone.utc).timestamp() * 1000)
            try:
                data = [partner['name'], partner['avatar'], partner['descr'], partner['link'], partner['siteshot'], partner['state'], created]
            except KeyError as e:
                return jsonify({"code": "err", "message": f"Missing required partner information: {e}"})
            mail = partner['mail']
            insert_links_data(config.conn,data,mail)
        data = read_data(config.conn,"links")
        keys = ["id","mail", "name", "avatar", "descr", "link", "siteshot","state","created"]
        data = [dict(zip(keys, item)) for item in data]
        return jsonify({"partners": data})
    if bans != []:
        for ban in bans:
            insert_ban_data(config.conn,ban)
        data = read_data(config.conn,"ban")
        data = [item[0] for item in data]
        return jsonify({"ban": data})
    return jsonify({"code": "err", "message": "There is no modified data"})
