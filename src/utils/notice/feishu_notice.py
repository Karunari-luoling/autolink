import json
import os
import requests
import src.utils.config as config
from src.utils.database.update_data import update_links_data

def feishu_notice(title, data, mail,feishu_token,siteshot,avatar):
    root_dir = os.path.abspath('.')
    feishu = config.load_config(os.path.join(root_dir, 'config', 'config.yml'))['feishu']
    data = [item if item != '' else 'NONE' for item in data]
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": "oc_3acfeb33544e58af6381ac4d3cfd5224",
        "msg_type": "interactive",
        "content": "{\"type\":\"template\",\"data\":{\"template_id\":\""+feishu["template_id"]+"\",\""+feishu['template_version_name']+"\":\"1.0.4\",\"template_variable\":{\"applyFriendLink\":\""+title+"\",\"siteshot\":\""+siteshot+"\",\"avatar\":\""+avatar+"\",\"avatar_link\":\""+data[1]+"\",\"descr\":\""+data[2]+"\",\"name\":\""+data[0]+"\",\"siteshot_link\":\""+data[4]+"\",\"state\":\""+data[5]+"\",\"mail\":\""+mail+"\",\"link\":\""+data[3]+"\"}}}"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ feishu_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    message_id = response.json()['data']['message_id']
    result = {
        "message_id": message_id,
        "mail": mail
    }
    update_links_data(config.conn, result)


