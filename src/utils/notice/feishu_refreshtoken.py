import src.utils.config as config
import time
import traceback
import requests
import json
from src.utils.database.insert_data import insert_feishu_token
from src.utils.database.read_data import read_data

def feishu_refreshtoken(app_id,app_secret):
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
    expire = response.json().get("expire")
    insert_feishu_token(config.conn,token,expire)

def feishu_refresh(app_id,app_secret):
    while True:
        try:
            feishu_refreshtoken(app_id, app_secret)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        finally:
            expire = read_data(config.conn, "feishu_token", "expire", None)
            time.sleep(expire[0][0])
