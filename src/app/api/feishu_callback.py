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
        item = read_data(config.conn, "links", None, "message_id == '"+message_id+"'")
        if len(item) > 0:
            item = item[0]
            action = decrypted_dict['event']['action']['value']
            if action == 'agree':
                state = 2
            elif action == 'refuse':
                state = -99
            elif action == 'refresh':
                state = -98
            feishu_linkdata = {"mail":item[1],"state":state}
            created = int(datetime.now(timezone.utc).timestamp() * 1000)
            config.executor.submit(update_links_data,config.conn, feishu_linkdata)
            if server_status("mail"):
                partner = [item[2], item[3], item[4], item[5], item[6], item[7], created]
                config.executor.submit(send_mail, item[1], partner,server_status("mail"),"申请友链成功")
            return jsonify({
                "toast": {
                    "type": "success",
                    "content": "同意成功" if action == 'agree' else "拒绝成功" if action == 'refuse' else "重新审核"
                }
            })
        else:
            print("No data to process")
            return jsonify({"code": "err", "message": "No data to process"})