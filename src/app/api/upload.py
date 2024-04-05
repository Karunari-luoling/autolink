from datetime import timezone, datetime
from src.utils.database.read_data import read_data
from flask import Blueprint, g, jsonify, request
import src.utils.config as config
from src.utils.database.insert_data import insert_links_data
from src.utils.notice.feishu_upload_images import upload_feishu_image
from src.utils.server_status import server_status
from src.utils.notice.mail_notice import send_mail

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_view():
    feishu_token = g.shared_dict.get('token')
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
                data = [partner['name'], partner['avatar'], partner['descr'], partner['link'], partner['siteshot'], "-98", created]
                data = [str(item) if item is not None else 'NONE' for item in data]
                mail = partner['mail']
                if server_status("feishu"):
                    config.executor.submit(upload_feishu_image, feishu_token, mail, data)
                if server_status("mail"):
                    config.executor.submit(send_mail, mail, data,server_status("mail"),"申请友链审核")
            except KeyError as e:
                return jsonify({"code": "err", "message": f"Missing required partner information: {e}"})
            insert_links_data(config.conn,data,mail)
        return jsonify({"code": "ok", "message": "Data has been modified successfully"})
    return jsonify({"code": "err", "message": "There is no modified data"})

