import json
import requests
import src.utils.config as config

def feishu_notice(title, data, mail,feishu_token,siteshot,avatar):
    data = [item if item != '' else 'NONE' for item in data] 
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    payload = json.dumps({
        "receive_id": "oc_3acfeb33544e58af6381ac4d3cfd5224",
        "msg_type": "interactive",
        "content": "{\"type\":\"template\",\"data\":{\"template_id\":\"AAqUNPYR4miy5\",\"template_version_name\":\"1.0.4\",\"template_variable\":{\"applyFriendLink\":\""+title+"\",\"siteshot\":\""+siteshot+"\",\"avatar\":\""+avatar+"\",\"avatar_link\":\""+data[1]+"\",\"descr\":\""+data[2]+"\",\"name\":\""+data[0]+"\",\"siteshot_link\":\""+data[4]+"\",\"state\":\""+data[5]+"\",\"mail\":\""+mail+"\",\"link\":\""+data[3]+"\"}}}"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ feishu_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    message_id = response.json()['data']['message_id']
    result = {"message_id": message_id, "mail": mail,"name": data[0], "avatar": data[1], "descr": data[2], "link": data[3], "siteshot": data[4], "state": data[5], "created":data[6]}
    config.feishu_callback_list.append(result)


