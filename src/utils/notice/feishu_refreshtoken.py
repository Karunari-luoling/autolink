import time
import requests
import json

def feishu_refreshtoken(app_id,app_secret,shared_dict):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
    'Content-Type': 'application/json',
    'charset': 'utf-8'
    }
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.json().get("tenant_access_token") 
    shared_dict["token"] = token

def feishu_refresh(app_id,app_secret,shared_dict):
    feishu_refreshtoken(app_id, app_secret, shared_dict)  
    time.sleep(3600)
