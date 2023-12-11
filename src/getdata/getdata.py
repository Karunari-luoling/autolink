import time
import schedule
from src.getdata.config import get_enabled_db, getlocaldb

def run_getdata(db, fentch_time, restart_event):
    while True:
        if restart_event.is_set():
            # 清除重启事件并重新开始
            restart_event.clear()
        if get_enabled_db(db) == 'local':
            schedule.every(fentch_time["fentch_interval"]).minutes.do(getlocaldb, db[0]["url"])
            schedule.run_all()
            while True:
                schedule.run_pending()
                time.sleep(60)
        elif get_enabled_db(db) == 'mongodb':
            print('mongodb')