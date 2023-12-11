import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

should_continue = True

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('config.yml'):
            print('config.yml has been modified, reloading config...')

def set_should_continue(value):
    global should_continue
    should_continue = value

def start_observer():
    global should_continue
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./config/', recursive=False)
    observer.start()

    while should_continue:
        time.sleep(1)
    observer.stop()
    observer.join()
