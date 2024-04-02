from src.app.app import app
from src.utils.config import load_config,run_app
from src.getdata.getdata import run_getdata
from src.utils.file_change_handler import set_should_continue
from src.utils.database.create_database import check_and_create_database
from multiprocessing import Process, Event
from src.utils.notice.feishu_refreshtoken import feishu_refresh
from multiprocessing import Process, Manager

if __name__ == '__main__':
    try:
        config = load_config('./config/config.yml')
        basic_settings = config['basic_settings']
        db = config['basic_settings']['db']
        fentch_time = config['fentch_time']
        feishu = config['feishu']

        restart_event = Event()
        check_and_create_database()

        with Manager() as manager:
            shared_dict = manager.dict()
            p1 = Process(target=run_getdata, args=(db, fentch_time, restart_event))
            p1.start()
            
            if feishu['enable']:
                p2 = Process(target=feishu_refresh, args=(feishu['app_id'],feishu['app_secret'],shared_dict))
                p2.start()

            run_app(app, basic_settings,shared_dict)
            
            p1.join()
            if feishu['enable']:
                p2.join()
    except KeyboardInterrupt:
        set_should_continue(False)