import json
import re
from shutil import copy

def get_enabled_db(config):
    for db in config:
        for key, value in db.items():
            if value == 'enable':
                return key
    return None

def getlocaldb(url):
    copy(url, './data/db.json')
    content = []
    for line in open("./data/db.json", 'r', encoding='utf-8', errors='ignore'):
        content.append(json.loads(line))
    return content

def get_match(pattern, string):
    match = re.search(pattern, string)
    return match.group(1) if match else None

def process_link(link):
    if link.endswith('/'):
        link = link.rstrip('/')
    protocol = 'http://' if 'http://' in link else 'https://'
    if ('https:' or 'http:') not in link:
        if '//' in link:
            link = link.replace('//', 'https://')
        else :
            link = 'https://' + link
    link = re.sub(r'(https?://)', '', link)
    link = re.sub(r'(//.*|#.*)', '', link)
    link = protocol + link
    return link

def process_data_final(name, avatar, descr, siteshot):
    extensions = ['jpg', 'png', 'gif', 'webp', 'jpeg', 'ico', 'svg', 'bmp', 'tif', 'tiff']

    if name:
        name = name.split('//')[0].split('#')[0].strip()
    if avatar:
        for ext in extensions:
            avatar = re.sub(r'(?<=' + ext + ') //.*', '', avatar)
    if descr:
        descr = descr.split('//')[0].split('#')[0].strip()
    if siteshot:
        for ext in extensions:
            siteshot = re.sub(r'(?<=' + ext + ') //.*', '', siteshot)

    return name, avatar, descr, siteshot