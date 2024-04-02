import json
from datetime import timezone, datetime
import os
from flask import Blueprint, jsonify, request
import hashlib
import base64
from Crypto.Cipher import AES
import src.utils.config as config
from src.utils.database.update_data import update_links_data
from src.utils.database.read_data import read_data
from src.utils.config import load_config
from src.utils.server_status import server_status
from src.utils.notice.mail_notice import send_mail
from concurrent.futures import ThreadPoolExecutor

feishu_callback = Blueprint('feishu_callback', __name__)

@feishu_callback.route('/feishu_callback', methods=['POST'])
def webhook_event():
    data = request.get_json()
    root_dir = os.path.abspath('.')
    feishu_config = load_config(os.path.join(root_dir, 'config', 'config.yml'))["feishu"]
    encrypt_key = feishu_config['encrypt']
    class AESCipher(object):
        def __init__(self, key):
            self.bs = AES.block_size
            self.key=hashlib.sha256(AESCipher.str_to_bytes(key)).digest()
        @staticmethod
        def str_to_bytes(data):
            u_type = type(b"".decode('utf8'))
            if isinstance(data, u_type):
                return data.encode('utf8')
            return data
        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s) - 1:])]
        def decrypt(self, enc):
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return  self._unpad(cipher.decrypt(enc[AES.block_size:]))
        def decrypt_string(self, enc):
            enc = base64.b64decode(enc)
            return  self.decrypt(enc).decode('utf8')
    encrypt = data['encrypt']
    cipher = AESCipher(encrypt_key)
    decrypted_string = cipher.decrypt_string(encrypt)
    decrypted_dict = json.loads(decrypted_string)

    if 'challenge' in decrypted_dict and decrypted_dict['challenge']:
        return jsonify({"challenge": decrypted_dict['challenge']})
    else:
        message_id = decrypted_dict['event']['context']['open_message_id']
        target_mail = None
        keys = ["mail", "name", "avatar", "descr", "link", "siteshot", "state"]
        if config.feishu_callback_list is None or config.feishu_callback_list == []:
            print("No data to process")
            return jsonify({"code": "err", "message": "No data to process"})
        for item in config.feishu_callback_list:
            if item['message_id'] == message_id:
                target_mail = item['mail']
                target_name = item['name']
                target_avatar = item['avatar']
                target_descr = item['descr']
                target_link = item['link']
                target_siteshot = item['siteshot']
                break
        if target_mail is not None:
            review_links = read_data(config.conn, "links", keys, f"mail = '{target_mail}'")
            review_links = [dict(zip(keys, item)) for item in review_links]
            action = decrypted_dict['event']['action']['value']
            return process_action(action, review_links, target_mail, target_link, target_siteshot, target_name, target_avatar, target_descr)

def process_action(action, review_links, target_mail, target_link, target_siteshot, target_name, target_avatar, target_descr):
    created = int(datetime.now(timezone.utc).timestamp() * 1000)
    for item in review_links:
        item['mail'] = target_mail
        item['created'] = created

        if action == 'agree':
            item['link'] = target_link
            item['siteshot'] = target_siteshot
            item['state'] = 2
            item['name'] = target_name
            item['avatar'] = target_avatar
            item['descr'] = target_descr
        elif action == 'refuse':
            item['state'] = 0
        elif action == 'refresh':
            item['link'] = target_link
            item['siteshot'] = target_siteshot
            item['state'] = -1
            item['name'] = target_name
            item['avatar'] = target_avatar
            item['descr'] = target_descr

        config.executor.submit(update_links_data,config.conn, item)
        if server_status("mail"):
            data = [target_name, target_avatar, target_descr, target_link, target_siteshot, "2", created]
            config.executor.submit(send_mail, item['mail'], data,server_status("mail"),"申请友链成功")

    return jsonify({
        "toast": {
            "type": "success",
            "content": "同意成功" if action == 'agree' else "拒绝成功" if action == 'refuse' else "重新审核"
        }
    })
