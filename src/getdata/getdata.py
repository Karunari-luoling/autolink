from email.contentmanager import ContentManager
import time
import schedule
from src.getdata.config import get_enabled_db, getlocaldb
from src.getdata.process_data import process_data
from src.utils.database.update_data import update_links_data
import src.utils.config as config

def run_getdata(db, fentch_time, restart_event):
    while True:
        if restart_event.is_set():
            # 清除重启事件并重新开始
            restart_event.clear()
        if get_enabled_db(db) == 'local':
            schedule.every(fentch_time["fentch_interval"]).minutes.do(start_getdata, getlocaldb(db[0]["url"]))
            schedule.run_all()
            while True:
                schedule.run_pending()
                time.sleep(60)
        elif get_enabled_db(db) == 'mongodb':
            print('mongodb')

def start_getdata(content):
    for item in content:
        data = process_data(item)
        if data is not None:
            partners = [data['name'], data['avatar'], data['descr'], data['link'], data['siteshot'], data['state'], data['created']]
            update_links_data(config.conn, partners, data['mail'])
