import json
from shutil import copy
from src.getdata.process_data import process_data
from src.utils.database.update_data import update_friends_data, update_links_data
import src.utils.config as config

def get_enabled_db(config):
    for db in config:
        for key, value in db.items():
            if value == 'enable':
                return key
    return None

def getlocaldb(url):
    copy(url, './data/db.json')
    for line in open("./data/db.json", 'r', encoding='utf-8', errors='ignore'):
        content = json.loads(line)
        data = process_data(content)
        partners = [data['name'], data['avatar'], data['descr'], data['link'], data['siteshot'], data['state']]
        update_links_data(config.conn, partners, data['mail'])