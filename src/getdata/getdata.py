import time
import traceback
from src.getdata.config import get_enabled_db, getlocaldb
from src.getdata.process_data import process_data
from src.utils.database.insert_data import insert_links_data
import src.utils.config as config
from src.utils.database.read_data import read_data
from src.utils.notice.feishu_upload_images import upload_feishu_image
from src.utils.server_status import server_status
from src.utils.notice.mail_notice import send_mail

def run_getdata(db, fentch_time, restart_event):
    if restart_event.is_set():
        # 清除重启事件并重新开始
        restart_event.clear()
    if get_enabled_db(db) == 'local':
        while True:
            try:
                start_getdata(getlocaldb(db[0]["url"]))
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
            finally:
                time.sleep(fentch_time["fentch_interval"]*60)
    elif get_enabled_db(db) == 'mongodb':
        print('mongodb')

def start_getdata(content):
    feishu_token = read_data(config.conn, "feishu_token", "token", None)[0][0]
    for item in content:
        data = process_data(item)
        if data is not None:
            partners = [data['name'], data['avatar'], data['descr'], data['link'], data['siteshot'], data['state'], data['created']]
            partners = [str(item) if item is not None else 'NONE' for item in partners]
            read_data_result = read_data(config.conn, "links", 'created', 'mail == "'+data['mail']+'"')
            if len(read_data_result) > 0:
                first_tuple = read_data_result[0]
                if len(first_tuple) > 0:
                    first_value = first_tuple[0]
                    try:
                        if first_value < data['created']:
                            if server_status("feishu"):
                                if feishu_token:
                                    config.executor.submit(upload_feishu_image, feishu_token, data['mail'], partners)
                            if server_status("mail"):
                                config.executor.submit(send_mail, data['mail'], partners,server_status("mail"),"申请友链审核")
                            insert_links_data(config.conn, partners, data['mail'])
                    except Exception as e:
                        if server_status("feishu"):
                            if feishu_token:
                                config.executor.submit(upload_feishu_image, feishu_token, data['mail'], partners)
                        if server_status("mail"):
                            config.executor.submit(send_mail, data['mail'], partners,server_status("mail"),"申请友链审核")
                        insert_links_data(config.conn, partners, data['mail'])
            else:
                if server_status("feishu"):
                    if feishu_token:
                        config.executor.submit(upload_feishu_image, feishu_token, data['mail'], partners)
                if server_status("mail"):
                    config.executor.submit(send_mail, data['mail'], partners,server_status("mail"),"申请友链审核")
                insert_links_data(config.conn, partners, data['mail'])
