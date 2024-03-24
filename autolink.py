from src.app.app import app
from src.utils.config import load_config,run_app
import threading
from src.getdata.getdata import run_getdata
from src.utils.file_change_handler import set_should_continue, start_observer
from src.utils.database.create_database import check_and_create_database
from multiprocessing import Process, Event

if __name__ == '__main__':
    try:
        config = load_config('./config/config.yml')
        basic_settings = config['basic_settings']
        db = config['basic_settings']['db']
        fentch_time = config['fentch_time']

        restart_event = Event()
        check_and_create_database()

        p1 = Process(target=run_getdata, args=(db, fentch_time, restart_event))
        p1.start()
        
        run_app(app, basic_settings)
        
        p1.join()
    except KeyboardInterrupt:
        set_should_continue(False)