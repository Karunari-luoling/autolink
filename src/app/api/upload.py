from datetime import timezone, datetime
from src.utils.database.read_data import read_data
from flask import Blueprint, jsonify, request
import src.utils.config as config
from src.utils.database.insert_data import insert_links_data

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_view():
    banurl = read_data(config.conn, "ban", None, None)
    banurl = [item[0] for item in banurl]
    json_data = request.get_json()
    partners = json_data["partners"]
    if partners != []:
        for partner in partners:
            created = int(datetime.now(timezone.utc).timestamp() * 1000)
            banlink = partner['link'].replace('https://', '').replace('http://', '').split('/')[0]
            banlink = '.'.join(banlink.split('.')[-2:])
            if banlink in banurl:
                return jsonify({"code": "err", "message": "The link is banned"})
            try:
                data = [partner['name'], partner['avatar'], partner['descr'], partner['link'], partner['siteshot'], "-1", created]
            except KeyError as e:
                return jsonify({"code": "err", "message": f"Missing required partner information: {e}"})
            mail = partner['mail']
            insert_links_data(config.conn,data,mail)
        return jsonify({"code": "ok", "message": "Data has been modified successfully"})
    return jsonify({"code": "err", "message": "There is no modified data"})
