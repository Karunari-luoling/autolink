from datetime import timezone, datetime
from src.utils.database.read_data import read_data
from flask import Blueprint, g, jsonify, request
import src.utils.config as config
from src.utils.database.insert_data import insert_links_data
from src.utils.notice.feishu_notice import feishu_notice
from src.utils.notice.feishu_upload_images import feish_uploadImage, download_image
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
                data = [partner['name'], partner['avatar'], partner['descr'], partner['link'], partner['siteshot'], "-1", created]
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

def upload_feishu_image(feishu_token,mail,data):
    if data[1] != "NONE" and data[1] != "" and data[1] is not None:
        image_content = download_image(data[1])
        if image_content is not None:
            avatar = feish_uploadImage(image_content, feishu_token)
        else:
            avatar = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    if data[4] != "NONE" and data[4] != "" and data[4] is not None:
        image_content = download_image(data[4])
        if image_content is not None:
            siteshot = feish_uploadImage(image_content, feishu_token)
        else:
            siteshot = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    else:
        image_content = "https://image.thum.io/get/width/400/crop/800/allowJPG/wait/20/noanimate/"+data[3]
        image_content = download_image(image_content)
        if image_content is not None:
            siteshot = feish_uploadImage(image_content, feishu_token)
        else:
            siteshot = "img_v2_9dd98485-2900-4d65-ada9-e31d1408dcfg"
    feishu_notice("申请友链",data,mail,feishu_token,siteshot,avatar)