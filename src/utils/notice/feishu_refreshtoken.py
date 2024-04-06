import time
import traceback
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
    while True:
        try:
            feishu_refreshtoken(app_id, app_secret, shared_dict)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        finally:
            time.sleep(3600)
